"""Offline tests for model plumbing and CNN shapes; no online dataset downloads."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from scipy.io import wavfile
from audio_fsdd_cnn import AudioDigitCNN, load_fsdd_arrays
from run_20_models import run_all_online_models
from vision_beans_cnn import BeansCNN

def make_wine_frame(n: int = 160, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "fixed_acidity": rng.normal(7.0, 1.0, n),
        "volatile_acidity": rng.normal(0.3, 0.1, n),
        "citric_acid": rng.uniform(0.0, 0.7, n),
        "residual_sugar": rng.lognormal(1.0, 0.4, n),
        "chlorides": rng.uniform(0.02, 0.12, n),
        "free_sulfur_dioxide": rng.uniform(1, 70, n),
        "total_sulfur_dioxide": rng.uniform(5, 250, n),
        "density": rng.normal(0.995, 0.003, n),
        "ph": rng.normal(3.2, 0.2, n),
        "sulphates": rng.uniform(0.2, 1.5, n),
        "alcohol": rng.uniform(8, 14, n),
        "wine_color": np.where(np.arange(n) % 2 == 0, "red", "white"),
        "quality": np.where(np.arange(n) % 4 == 0, rng.integers(7, 9, n), rng.integers(3, 7, n)),
    })

def make_bike_frames(n_hour: int = 400, n_day: int = 300, seed: int = 42):
    rng = np.random.default_rng(seed)
    dates_hour = pd.date_range("2012-01-01", periods=n_hour, freq="h")
    def frame(dates):
        n = len(dates)
        return pd.DataFrame({
            "dteday": dates,
            "temp": rng.uniform(0.0, 1.0, n),
            "atemp": rng.uniform(0.0, 1.0, n),
            "hum": rng.uniform(0.0, 1.0, n),
            "windspeed": rng.uniform(0.0, 1.0, n),
            "season": rng.integers(1, 5, n),
            "yr": rng.integers(0, 2, n),
            "mnth": pd.DatetimeIndex(dates).month,
            "holiday": rng.integers(0, 2, n),
            "weekday": pd.DatetimeIndex(dates).weekday,
            "workingday": rng.integers(0, 2, n),
            "weathersit": rng.integers(1, 4, n),
            "hr": pd.DatetimeIndex(dates).hour,
            "cnt": rng.poisson(120, n).astype(float),
        })
    return frame(dates_hour), frame(pd.date_range("2011-01-01", periods=n_day, freq="D"))

class OnlineModelTests(unittest.TestCase):
    def test_twenty_online_model_functions_accept_dataframes_without_network(self):
        wine = make_wine_frame()
        hourly, daily = make_bike_frames()
        report = run_all_online_models(wine=wine, bike_hour=hourly, bike_day=daily, seed=11)
        combined = report["results"]
        self.assertEqual(report["model_count"], 20)
        self.assertEqual(len(combined), 20)
        self.assertEqual(len({item["model"] for item in combined}), 20)
        self.assertEqual(len(report["sources"]), 2)
        for item in combined:
            self.assertTrue(item["metrics"])
            for key, value in item["metrics"].items():
                if isinstance(value, (int, float)):
                    self.assertTrue(np.isfinite(value), f"{item['model']}:{key}")

    def test_beans_cnn_output_shape(self):
        model = BeansCNN(num_classes=3)
        with torch.no_grad():
            logits = model(torch.zeros((2, 3, 96, 96)))
        self.assertEqual(tuple(logits.shape), (2, 3))

    def test_audio_cnn_output_shape(self):
        model = AudioDigitCNN(num_classes=10)
        with torch.no_grad():
            logits = model(torch.zeros((2, 1, 8000)))
        self.assertEqual(tuple(logits.shape), (2, 10))

    def test_audio_loader_respects_upstream_index_split(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            rate = 8000
            t = np.arange(512) / rate
            waveform = (np.sin(2 * np.pi * 440 * t) * 16000).astype(np.int16)
            for digit in range(10):
                for speaker in ("jackson", "theo", "nicolas", "george", "lucas", "yweweler"):
                    for idx in range(7):
                        wavfile.write(root / f"{digit}_{speaker}_{idx}.wav", rate, waveform)
            train_x, train_y, test_x, test_y = load_fsdd_arrays(root, max_train=300, seed=7)
            self.assertEqual(train_x.shape[1:], (1, 8000))
            self.assertEqual(test_x.shape[1:], (1, 8000))
            self.assertTrue(set(train_y.tolist()).issuperset(set(range(10))))
            self.assertEqual(set(test_y.tolist()), set(range(10)))

if __name__ == "__main__":
    unittest.main()
