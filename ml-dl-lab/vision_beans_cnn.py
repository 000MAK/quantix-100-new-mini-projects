"""Train a small CNN using the online Beans image dataset from Hugging Face.

The dataset is downloaded at runtime and cached by the Hugging Face Datasets library.
No dataset images or model weights are committed to this repository.
"""
from __future__ import annotations

import argparse
import json
import random
from typing import Any

import numpy as np
import torch
from datasets import load_dataset
from huggingface_hub import HfApi
from PIL import Image
from sklearn.metrics import accuracy_score, f1_score
from torch import nn
from torch.utils.data import DataLoader, Dataset


DATASET_ID = "AI-Lab-Makerere/beans"
DATASET_REVISION = "main"
DATASET_CARD_URL = "https://huggingface.co/datasets/AI-Lab-Makerere/beans"
LABEL_KEYS = ("labels", "label")


def seed_everything(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)


def _label_key(dataset_split: Any) -> str:
    for candidate in LABEL_KEYS:
        if candidate in dataset_split.features:
            return candidate
    raise ValueError("Beans dataset does not expose a recognized 'labels' or 'label' column.")


class BeansImageDataset(Dataset):
    def __init__(self, hf_split: Any, label_key: str, image_size: int = 96) -> None:
        self.hf_split = hf_split
        self.label_key = label_key
        self.image_size = image_size

    def __len__(self) -> int:
        return len(self.hf_split)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        row = self.hf_split[index]
        image = row["image"]
        if not isinstance(image, Image.Image):
            raise TypeError(f"Expected decoded PIL image, received {type(image).__name__}.")
        image = image.convert("RGB").resize((self.image_size, self.image_size), Image.Resampling.BILINEAR)
        pixels = np.asarray(image, dtype=np.float32) / 255.0
        # Simple fixed normalization, avoiding fitting image statistics on the test split.
        pixels = (pixels - 0.5) / 0.5
        tensor = torch.from_numpy(pixels.copy()).permute(2, 0, 1).contiguous()
        target = torch.tensor(int(row[self.label_key]), dtype=torch.long)
        return tensor, target


class BeansCNN(nn.Module):
    def __init__(self, num_classes: int = 3) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((4, 4)), nn.Flatten(),
        )
        self.classifier = nn.Sequential(nn.Linear(64 * 4 * 4, 64), nn.ReLU(inplace=True), nn.Dropout(0.25), nn.Linear(64, num_classes))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))


def _limit_split(split: Any, max_samples: int | None, seed: int) -> Any:
    if max_samples is None or max_samples <= 0 or len(split) <= max_samples:
        return split
    return split.shuffle(seed=seed).select(range(max_samples))


def train_beans_demo(
    max_train: int = 800,
    max_validation: int = 133,
    max_test: int = 128,
    epochs: int = 3,
    batch_size: int = 24,
    image_size: int = 96,
    seed: int = 42,
) -> dict[str, Any]:
    if epochs < 1 or epochs > 20:
        raise ValueError("epochs must be between 1 and 20")
    if batch_size < 1 or image_size < 32 or image_size > 256:
        raise ValueError("batch_size must be positive and image_size must be between 32 and 256")
    seed_everything(seed)

    # Resolve and record an immutable dataset commit before downloading.
    # The upstream images are downloaded online and are not bundled in this repository.
    dataset_info = HfApi().dataset_info(DATASET_ID, revision=DATASET_REVISION)
    resolved_revision = dataset_info.sha
    if not resolved_revision:
        raise RuntimeError("Could not resolve an immutable Hugging Face dataset revision.")
    raw = load_dataset(DATASET_ID, revision=resolved_revision)
    required_splits = {"train", "validation", "test"}
    if not required_splits.issubset(set(raw.keys())):
        raise ValueError(f"Expected train/validation/test splits, received {list(raw.keys())}")
    label_key = _label_key(raw["train"])
    label_names = list(raw["train"].features[label_key].names)
    if len(label_names) < 2:
        raise ValueError("Expected at least two image classes.")

    train_split = _limit_split(raw["train"], max_train, seed)
    val_split = _limit_split(raw["validation"], max_validation, seed)
    test_split = _limit_split(raw["test"], max_test, seed)
    train_ds = BeansImageDataset(train_split, label_key, image_size)
    val_ds = BeansImageDataset(val_split, label_key, image_size)
    test_ds = BeansImageDataset(test_split, label_key, image_size)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=0)

    model = BeansCNN(num_classes=len(label_names))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()
    best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    best_val_loss = float("inf")
    best_epoch = 0
    for epoch in range(1, epochs + 1):
        model.train()
        train_loss_total = 0.0
        train_count = 0
        for features, labels in train_loader:
            optimizer.zero_grad(set_to_none=True)
            logits = model(features)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()
            train_loss_total += loss.item() * len(labels)
            train_count += len(labels)

        model.eval()
        val_loss_total = 0.0
        val_count = 0
        with torch.no_grad():
            for features, labels in val_loader:
                loss = loss_fn(model(features), labels)
                val_loss_total += loss.item() * len(labels)
                val_count += len(labels)
        val_loss = val_loss_total / max(val_count, 1)
        print(f"Epoch {epoch}/{epochs} | train_loss={train_loss_total / max(train_count, 1):.4f} | validation_loss={val_loss:.4f}")
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_epoch = epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}

    model.load_state_dict(best_state)
    model.eval()
    y_true: list[int] = []
    y_pred: list[int] = []
    with torch.no_grad():
        for features, labels in test_loader:
            pred = model(features).argmax(dim=1).cpu().tolist()
            y_pred.extend(int(v) for v in pred)
            y_true.extend(int(v) for v in labels.cpu().tolist())

    return {
        "project": "Online Bean Leaf Image Classification — CNN",
        "dataset_id": DATASET_ID,
        "dataset_revision": resolved_revision,
        "dataset_card": DATASET_CARD_URL,
        "dataset_license_metadata": "MIT shown in the Hugging Face dataset card; upstream card notes about original source/licensing are incomplete—review before commercial reuse.",
        "source_data_downloaded_online": True,
        "image_size": image_size,
        "train_samples_used": len(train_ds),
        "validation_samples_used": len(val_ds),
        "test_samples_used": len(test_ds),
        "best_epoch_by_validation_loss": best_epoch,
        "test_accuracy": float(accuracy_score(y_true, y_pred)),
        "test_macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "labels": label_names,
        "limitations": "Small demonstrator on bean leaf disease images; not a plant-health diagnosis service. Scores are not evidence of field performance.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-train", type=int, default=800)
    parser.add_argument("--max-validation", type=int, default=133)
    parser.add_argument("--max-test", type=int, default=128)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=24)
    parser.add_argument("--image-size", type=int, default=96)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    result = train_beans_demo(args.max_train, args.max_validation, args.max_test, args.epochs, args.batch_size, args.image_size, args.seed)
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        from pathlib import Path
        target = Path(args.output).expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
