import json, unittest
from pathlib import Path
from main import process
BASE = Path(__file__).parent
class ToolTests(unittest.TestCase):
    def test_sample_case(self):
        source = json.loads((BASE / "sample_input.json").read_text(encoding="utf-8"))
        expected = json.loads((BASE / "sample_output.json").read_text(encoding="utf-8"))
        self.assertEqual(process(source), expected)
    def test_rejects_non_object_input(self):
        with self.assertRaises(ValueError):
            process([])
if __name__ == "__main__": unittest.main()
