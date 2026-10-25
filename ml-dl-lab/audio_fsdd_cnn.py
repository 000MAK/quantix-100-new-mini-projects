"""Train a 1-D CNN on the online Free Spoken Digit Dataset (FSDD).

Downloads a version-tagged source archive at runtime. The data are cached outside
the repository. FSDD is licensed CC BY-SA 4.0; see ONLINE_DATA_SOURCES.md.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import random
import re
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import torch
from scipy.io import wavfile
from sklearn.metrics import accuracy_score, f1_score
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

DATASET_TAG = "v1.0.10"
DATASET_URL = f"https://codeload.github.com/Jakobovski/free-spoken-digit-dataset/zip/refs/tags/{DATASET_TAG}"
DATASET_REPO = "https://github.com/Jakobovski/free-spoken-digit-dataset"
DATASET_LICENSE = "CC BY-SA 4.0"
SAMPLE_RATE = 8000
CLIP_SAMPLES = 8000
FILENAME_PATTERN = re.compile(r"^(?P<label>[0-9])_(?P<speaker>[A-Za-z0-9]+)_(?P<index>[0-9]+)\.wav$", re.IGNORECASE)
MAX_ARCHIVE_BYTES = 100_000_000


def seed_everything(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)


def _cache_root() -> Path:
    override = os.environ.get("QUANTIX_DATA_CACHE")
    root = Path(override).expanduser() if override else Path.home() / ".cache" / "quantix-online-data"
    root.mkdir(parents=True, exist_ok=True)
    return root


def download_fsdd() -> Path:
    """Fetch a versioned FSDD ZIP and extract only WAVs into the user cache."""
    root = _cache_root()
    recordings = root / f"fsdd-{DATASET_TAG}" / "recordings"
    if recordings.is_dir() and len(list(recordings.glob("*.wav"))) >= 100:
        return recordings

    request = urllib.request.Request(DATASET_URL, headers={"User-Agent": "Quantix-Research-Lab/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        advertised = response.headers.get("Content-Length")
        if advertised and int(advertised) > MAX_ARCHIVE_BYTES:
            raise ValueError("FSDD archive exceeds configured size limit.")
        payload = response.read(MAX_ARCHIVE_BYTES + 1)
    if len(payload) > MAX_ARCHIVE_BYTES:
        raise ValueError("FSDD download exceeded configured size limit.")
    if not zipfile.is_zipfile(io.BytesIO(payload)):
        raise ValueError("FSDD download is not a valid ZIP archive; refusing to extract it.")

    target = recordings
    target.mkdir(parents=True, exist_ok=True)
    archive_sha256 = hashlib.sha256(payload).hexdigest()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        extracted = 0
        for info in archive.infolist():
            member = Path(info.filename)
            if member.is_absolute() or ".." in member.parts or info.is_dir():
                continue
            if "recordings" not in member.parts or member.suffix.lower() != ".wav":
                continue
            if info.file_size > 2_000_000:
                continue
            basename = member.name
            if not FILENAME_PATTERN.match(basename):
                continue
            output = target / basename
            with archive.open(info) as src, output.open("wb") as dst:
                dst.write(src.read(2_000_001))
            if output.stat().st_size > 2_000_000:
                output.unlink(missing_ok=True)
                continue
            extracted += 1

    if extracted < 100:
        raise RuntimeError(f"Only {extracted} valid WAV recordings were extracted; expected at least 100.")

    manifest = {
        "dataset": "Free Spoken Digit Dataset",
        "tag": DATASET_TAG,
        "url": DATASET_URL,
        "downloaded_at_note": "Archive fetched during this run; timestamp omitted for deterministic metadata.",
        "sha256_of_downloaded_archive": archive_sha256,
        "extracted_wav_files": extracted,
        "license": DATASET_LICENSE,
        "source": DATASET_REPO,
    }
    (target.parent / "download_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return recordings


def parse_recording_name(path: Path) -> tuple[int, str, int] | None:
    match = FILENAME_PATTERN.match(path.name)
    if not match:
        return None
    return int(match.group("label")), match.group("speaker"), int(match.group("index"))


def _read_waveform(path: Path) -> np.ndarray:
    sample_rate, audio = wavfile.read(str(path))
    if int(sample_rate) != SAMPLE_RATE:
        raise ValueError(f"{path.name}: expected {SAMPLE_RATE} Hz, got {sample_rate} Hz.")
    array = np.asarray(audio)
    if array.ndim == 2:
        array = array.astype(np.float32).mean(axis=1)
    if np.issubdtype(array.dtype, np.integer):
        maximum = float(max(abs(np.iinfo(array.dtype).min), np.iinfo(array.dtype).max))
        waveform = array.astype(np.float32) / maximum
    else:
        waveform = array.astype(np.float32)
    waveform = np.nan_to_num(waveform, nan=0.0, posinf=0.0, neginf=0.0)
    # Deterministic center crop/pad to one second. The source recordings are short 8 kHz WAVs.
    if len(waveform) > CLIP_SAMPLES:
        start = (len(waveform) - CLIP_SAMPLES) // 2
        waveform = waveform[start:start + CLIP_SAMPLES]
    elif len(waveform) < CLIP_SAMPLES:
        pad_total = CLIP_SAMPLES - len(waveform)
        waveform = np.pad(waveform, (pad_total // 2, pad_total - pad_total // 2))
    peak = float(np.max(np.abs(waveform))) if waveform.size else 0.0
    if peak > 1e-7:
        waveform = waveform / peak
    return waveform.astype(np.float32)


def load_fsdd_arrays(recordings_dir: Path, max_train: int = 1200, seed: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Use the upstream split: recording indices 0-4 are test; 5-49 are train."""
    files = sorted(Path(recordings_dir).glob("*.wav"))
    training: list[tuple[Path, int, str, int]] = []
    testing: list[tuple[Path, int, str, int]] = []
    for path in files:
        parsed = parse_recording_name(path)
        if parsed is None:
            continue
        label, speaker, index = parsed
        row = (path, label, speaker, index)
        if index <= 4:
            testing.append(row)
        else:
            training.append(row)
    if len(training) < 100 or len(testing) < 30:
        raise ValueError(f"Not enough FSDD files after applying the upstream split: train={len(training)}, test={len(testing)}")
    rng = np.random.default_rng(seed)
    if max_train > 0 and len(training) > max_train:
        # Stratify the train subset by digit label so the capped demo remains balanced.
        selected = []
        labels = np.asarray([row[1] for row in training])
        for label in range(10):
            candidates = np.flatnonzero(labels == label)
            if len(candidates) == 0:
                continue
            quota = max(1, int(round(max_train * len(candidates) / len(training))))
            selected.extend(rng.choice(candidates, size=min(quota, len(candidates)), replace=False).tolist())
        training = [training[int(i)] for i in sorted(set(selected))]
        if len(training) > max_train:
            training = training[:max_train]
    rng.shuffle(training)
    train_x = np.stack([_read_waveform(row[0]) for row in training])
    train_y = np.asarray([row[1] for row in training], dtype=np.int64)
    # Official test clips are not used for training or early stopping.
    test_x = np.stack([_read_waveform(row[0]) for row in sorted(testing)])
    test_y = np.asarray([row[1] for row in sorted(testing)], dtype=np.int64)
    if len(np.unique(train_y)) < 10 or len(np.unique(test_y)) < 10:
        raise ValueError("The downloaded subset must contain examples of all ten digits in train and test.")
    return train_x[:, None, :], train_y, test_x[:, None, :], test_y


class AudioDigitCNN(nn.Module):
    def __init__(self, num_classes: int = 10) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=15, stride=4, padding=7), nn.BatchNorm1d(16), nn.ReLU(inplace=True),
            nn.MaxPool1d(2),
            nn.Conv1d(16, 32, kernel_size=9, stride=2, padding=4), nn.BatchNorm1d(32), nn.ReLU(inplace=True),
            nn.MaxPool1d(2),
            nn.Conv1d(32, 48, kernel_size=7, stride=2, padding=3), nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool1d(16), nn.Flatten(),
        )
        self.classifier = nn.Sequential(nn.Linear(48 * 16, 64), nn.ReLU(inplace=True), nn.Dropout(0.2), nn.Linear(64, num_classes))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))


def train_fsdd_demo(max_train: int = 1200, epochs: int = 5, batch_size: int = 64, seed: int = 42) -> dict[str, Any]:
    if epochs < 1 or epochs > 30:
        raise ValueError("epochs must be between 1 and 30")
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    seed_everything(seed)
    recordings_dir = download_fsdd()
    train_x, train_y, test_x, test_y = load_fsdd_arrays(recordings_dir, max_train=max_train, seed=seed)
    train_dataset = TensorDataset(torch.from_numpy(train_x), torch.from_numpy(train_y))
    test_dataset = TensorDataset(torch.from_numpy(test_x), torch.from_numpy(test_y))
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    model = AudioDigitCNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()
    for epoch in range(1, epochs + 1):
        model.train()
        loss_sum = 0.0
        seen = 0
        for features, labels in train_loader:
            optimizer.zero_grad(set_to_none=True)
            logits = model(features)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()
            loss_sum += loss.item() * len(labels)
            seen += len(labels)
        print(f"Epoch {epoch}/{epochs} | train_loss={loss_sum / max(seen, 1):.4f}")

    model.eval()
    y_true: list[int] = []
    y_pred: list[int] = []
    with torch.no_grad():
        for features, labels in test_loader:
            y_pred.extend(model(features).argmax(dim=1).cpu().tolist())
            y_true.extend(labels.cpu().tolist())

    return {
        "project": "Online Spoken Digit Recognition — 1-D CNN",
        "dataset": "Free Spoken Digit Dataset (FSDD)",
        "dataset_version": DATASET_TAG,
        "dataset_repository": DATASET_REPO,
        "dataset_license": DATASET_LICENSE,
        "source_data_downloaded_online": True,
        "sample_rate_hz": SAMPLE_RATE,
        "train_samples_used": len(train_dataset),
        "official_test_samples": len(test_dataset),
        "speaker-independent_generalization_not_claimed": True,
        "test_accuracy": float(accuracy_score(y_true, y_pred)),
        "test_macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "limitations": "Small English spoken-digit dataset; the official index split may contain the same speakers in train/test. Do not interpret as speaker-independent recognition.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-train", type=int, default=1200)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    result = train_fsdd_demo(args.max_train, args.epochs, args.batch_size, args.seed)
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        from pathlib import Path
        target = Path(args.output).expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
