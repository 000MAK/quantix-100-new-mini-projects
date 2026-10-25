"""Train a small PyTorch MLP on scikit-learn's built-in Digits dataset.

This is a compact educational baseline, not a production image classifier.
It runs on CPU and does not download data or pretrained model weights.
"""
from __future__ import annotations

import copy
import random

import numpy as np
import torch
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def set_seeds(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def make_loader(features: np.ndarray, labels: np.ndarray, *, shuffle: bool) -> DataLoader:
    x_tensor = torch.tensor(features, dtype=torch.float32)
    y_tensor = torch.tensor(labels, dtype=torch.long)
    return DataLoader(
        TensorDataset(x_tensor, y_tensor),
        batch_size=64,
        shuffle=shuffle,
        num_workers=0,
    )


def main() -> None:
    set_seeds()
    torch.set_num_threads(1)

    dataset = load_digits()
    features = dataset.data.astype(np.float32) / 16.0
    labels = dataset.target.astype(np.int64)

    x_train_all, x_test, y_train_all, y_test = train_test_split(
        features,
        labels,
        test_size=0.20,
        random_state=42,
        stratify=labels,
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_all,
        y_train_all,
        test_size=0.15,
        random_state=42,
        stratify=y_train_all,
    )

    train_loader = make_loader(x_train, y_train, shuffle=True)
    val_loader = make_loader(x_val, y_val, shuffle=False)
    test_loader = make_loader(x_test, y_test, shuffle=False)

    model = nn.Sequential(
        nn.Linear(64, 128),
        nn.ReLU(),
        nn.Dropout(p=0.10),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 10),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_function = nn.CrossEntropyLoss()

    best_validation_loss = float("inf")
    best_state = copy.deepcopy(model.state_dict())
    best_epoch = 0
    epochs_without_improvement = 0
    max_epochs = 40
    patience = 6

    for epoch in range(1, max_epochs + 1):
        model.train()
        for batch_features, batch_labels in train_loader:
            optimizer.zero_grad(set_to_none=True)
            logits = model(batch_features)
            loss = loss_function(logits, batch_labels)
            loss.backward()
            optimizer.step()

        model.eval()
        validation_loss_total = 0.0
        validation_count = 0
        with torch.no_grad():
            for batch_features, batch_labels in val_loader:
                logits = model(batch_features)
                loss = loss_function(logits, batch_labels)
                validation_loss_total += loss.item() * len(batch_labels)
                validation_count += len(batch_labels)

        validation_loss = validation_loss_total / validation_count
        if validation_loss < best_validation_loss - 1e-4:
            best_validation_loss = validation_loss
            best_state = copy.deepcopy(model.state_dict())
            best_epoch = epoch
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        print(
            f"Epoch {epoch:02d} | validation loss: {validation_loss:.4f}"
        )
        if epochs_without_improvement >= patience:
            print("Early stopping: validation loss did not improve.")
            break

    model.load_state_dict(best_state)
    model.eval()
    predictions: list[int] = []
    targets: list[int] = []
    with torch.no_grad():
        for batch_features, batch_labels in test_loader:
            logits = model(batch_features)
            predictions.extend(logits.argmax(dim=1).cpu().tolist())
            targets.extend(batch_labels.cpu().tolist())

    print("\nDigits dataset: PyTorch MLP")
    print(f"Train samples: {len(y_train)} | Validation samples: {len(y_val)}")
    print(f"Test samples: {len(y_test)} | Best epoch: {best_epoch}")
    print(f"Test accuracy: {accuracy_score(targets, predictions):.3f}")
    print(
        classification_report(
            targets,
            predictions,
            labels=list(range(10)),
            zero_division=0,
        )
    )


if __name__ == "__main__":
    main()
