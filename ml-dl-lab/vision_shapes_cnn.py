"""Train a tiny CNN on procedurally generated geometric images (no downloads)."""
from __future__ import annotations
import argparse
import random
from typing import Any
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from torch import nn

LABEL_NAMES = ["horizontal_bar", "vertical_bar", "diagonal"]


def seed_everything(seed: int = 42) -> None:
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed); torch.set_num_threads(1)


def make_shape_dataset(n_samples: int = 360, image_size: int = 24, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    """Return noisy grayscale bars/diagonals and integer labels. Data are synthetic."""
    if n_samples < 12 or image_size < 12:
        raise ValueError("n_samples must be >= 12 and image_size must be >= 12")
    rng = np.random.default_rng(seed)
    x = rng.normal(0.0, 0.08, size=(n_samples, 1, image_size, image_size)).astype(np.float32)
    y = np.arange(n_samples, dtype=np.int64) % 3
    rng.shuffle(y)
    for i, label in enumerate(y):
        thickness = int(rng.integers(1, 3))
        if label == 0:
            row = int(rng.integers(4, image_size - 4))
            x[i, 0, row:row + thickness + 1, 2:image_size - 2] += 0.9
        elif label == 1:
            col = int(rng.integers(4, image_size - 4))
            x[i, 0, 2:image_size - 2, col:col + thickness + 1] += 0.9
        else:
            offset = int(rng.integers(-4, 5))
            for row in range(2, image_size - 2):
                col = row + offset
                if 2 <= col < image_size - 2:
                    x[i, 0, row, max(1, col - thickness):min(image_size - 1, col + thickness + 1)] += 0.9
        x[i] = np.clip(x[i], 0.0, 1.0)
    return x, y


class TinyShapeCNN(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(8, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.AdaptiveAvgPool2d((4, 4)), nn.Flatten(),
        )
        self.classifier = nn.Sequential(nn.Linear(16 * 4 * 4, 32), nn.ReLU(), nn.Linear(32, 3))
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))


def train_demo(n_samples: int = 360, epochs: int = 8, seed: int = 42) -> dict[str, Any]:
    if epochs < 1 or epochs > 30:
        raise ValueError("epochs must be between 1 and 30")
    seed_everything(seed)
    x, y = make_shape_dataset(n_samples=n_samples, seed=seed)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed, stratify=y)
    train_x = torch.from_numpy(x_train); train_y = torch.from_numpy(y_train)
    test_x = torch.from_numpy(x_test); test_y = torch.from_numpy(y_test)
    model = TinyShapeCNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
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
    return {"project": "Synthetic Shape Recognition — CNN", "dataset": "procedurally generated grayscale images; no external dataset", "samples": int(n_samples), "epochs": int(epochs), "accuracy": float(accuracy_score(y_test, pred)), "macro_f1": float(f1_score(y_test, pred, average="macro")), "labels": LABEL_NAMES}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=360)
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    import json
    print(json.dumps(train_demo(args.samples, args.epochs, args.seed), indent=2))

if __name__ == "__main__":
    main()
