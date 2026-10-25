"""Unit and smoke tests for the Quantix research/ML lab; no network access required."""
from __future__ import annotations
import unittest
import numpy as np

from research_models import run_all_models
from vision_shapes_cnn import make_shape_dataset, train_demo as train_vision_demo
from audio_signal_cnn import make_signal_dataset, train_demo as train_audio_demo


class ResearchModelsTests(unittest.TestCase):
    def test_ten_model_results_have_numeric_metrics(self):
        results = run_all_models(seed=17)
        self.assertEqual(len(results), 10)
        self.assertEqual(len({item["model"] for item in results}), 10)
        for item in results:
            self.assertTrue(item["metrics"])
            for key, value in item["metrics"].items():
                if isinstance(value, list):
                    self.assertTrue(all(np.isfinite(v) for v in value))
                elif isinstance(value, (int, float)):
                    self.assertTrue(np.isfinite(value), f"{item['model']}:{key}")

    def test_portfolio_weights_respect_constraints(self):
        item = next(x for x in run_all_models(seed=21) if x["model"].startswith("Minimum-variance"))
        weights = np.asarray(item["metrics"]["weights"])
        self.assertAlmostEqual(float(weights.sum()), 1.0, places=6)
        self.assertTrue(np.all(weights >= -1e-8))
        self.assertTrue(np.all(weights <= 1.0 + 1e-8))


class DeepLearningSmokeTests(unittest.TestCase):
    def test_shape_data_are_local_and_shapes_are_valid(self):
        x, y = make_shape_dataset(30, 16, seed=5)
        self.assertEqual(x.shape, (30, 1, 16, 16))
        self.assertEqual(set(y.tolist()), {0, 1, 2})
        self.assertTrue(np.isfinite(x).all())

    def test_audio_data_are_local_and_shapes_are_valid(self):
        x, y = make_signal_dataset(30, 128, seed=5)
        self.assertEqual(x.shape, (30, 1, 128))
        self.assertEqual(set(y.tolist()), {0, 1, 2})
        self.assertTrue(np.isfinite(x).all())

    def test_vision_training_smoke(self):
        result = train_vision_demo(n_samples=72, epochs=1, seed=4)
        self.assertGreaterEqual(result["accuracy"], 0.0)
        self.assertLessEqual(result["accuracy"], 1.0)

    def test_audio_training_smoke(self):
        result = train_audio_demo(n_samples=72, epochs=1, seed=4)
        self.assertGreaterEqual(result["accuracy"], 0.0)
        self.assertLessEqual(result["accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()
