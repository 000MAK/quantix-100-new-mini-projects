"""Train a tiny 1-D CNN to classify synthetic low/mid/high-pitch signal mixtures.

No microphone access, external recordings, or downloaded assets are used.
"""
from __future__ import annotations
import argparse
import random
from typing import Any
import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from torch import nn

LABEL_NAMES = ["low_frequency", "mid_frequency", "high_frequency"]
SAMPLE_RATE = 256


def seed_everything(seed: int = 42) -> None:
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed); torch.set_num_threads(1)


def make_signal_dataset(n_samples: int = 420, signal_length: int = 256, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    """Create noisy tone mixtures as single-channel waveforms with 3 frequency labels."""
    if n_samples < 12 or signal_length < 64:
        raise ValueError("n_samples must be >= 12 and signal_length must be >= 64")
    rng = np.random.default_rng(seed)
    labels = np.arange(n_samples, dtype=np.int64) % 3
    rng.shuffle(labels)
    t = np.arange(signal_length, dtype=np.float32) / SAMPLE_RATE
    freqs = np.array([4.0, 15.0, 36.0], dtype=float)
    signals = np.empty((n_samples, 1, signal_length), dtype=np.float32)
    for i, label in enumerate(labels):
        phase = float(rng.uniform(0.0, 2.0 * np.pi))
        fundamental = freqs[label] * float(rng.uniform(0.94, 1.06))
        wave = np.sin(2 * np.pi * fundamental * t + phase)
        wave += 0.25 * np.sin(2 * np.pi * fundamental * 2.0 * t + phase / 2.0)
        wave += rng.normal(0.0, 0.18, size=signal_length)
        peak = max(float(np.max(np.abs(wave))), 1e-6)
        signals[i, 0] = (wave / peak).astype(np.float32)
    return signals, labels


class TinyAudioCNN(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv1d(1, 8, kernel_size=9, padding=4), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(8, 16, kernel_size=7, padding=3), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(16, 24, kernel_size=5, padding=2), nn.ReLU(),
            nn.AdaptiveAvgPool1d(16), nn.Flatten(), nn.Linear(24 * 16, 32), nn.ReLU(), nn.Linear(32, 3),
        )
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


def train_demo(n_samples: int = 420, epochs: int = 8, seed: int = 42) -> dict[str, Any]:
    if epochs < 1 or epochs > 30:
        raise ValueError("epochs must be between 1 and 30")
    seed_everything(seed)
    x, y = make_signal_dataset(n_samples=n_samples, seed=seed)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed, stratify=y)
    train_x, train_y = torch.from_numpy(x_train), torch.from_numpy(y_train)
    test_x, test_y = torch.from_numpy(x_test), torch.from_numpy(y_test)
    model = TinyAudioCNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)
    loss_fn = nn.CrossEntropyLoss()
    model.train()
    batch_size = 48
    for _ in range(epochs):
        order = torch.randperm(len(train_x))
        for idx in order.split(batch_size):
            optimizer.zero_grad(set_to_none=True)
            logits = model(train_x[idx])
            loss = loss_fn(logits, train_y[idx])
            loss.backward(); optimizer.step()
    model.eval()
    with torch.no_grad():
        pred = model(test_x).argmax(dim=1).cpu().numpy()
    return {"project": "Synthetic Audio Signal Classification — 1-D CNN", "dataset": "procedurally generated noisy tone mixtures; no audio recordings", "sample_rate_hz": SAMPLE_RATE, "samples": int(n_samples), "epochs": int(epochs), "accuracy": float(accuracy_score(y_test, pred)), "macro_f1": float(f1_score(y_test, pred, average="macro")), "labels": LABEL_NAMES}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=420)
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    import json
    print(json.dumps(train_demo(args.samples, args.epochs, args.seed), indent=2))

if __name__ == "__main__":
    main()
