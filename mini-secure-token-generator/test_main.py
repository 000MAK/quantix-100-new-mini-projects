import unittest
from main import process
class ToolTests(unittest.TestCase):
 def test_token_has_expected_metadata(self):
  r=process({"bytes":24})
  self.assertEqual(r["requested_random_bytes"],24); self.assertGreaterEqual(len(r["token"]),30)
 def test_refuses_too_small_entropy_setting(self):
  with self.assertRaises(ValueError): process({"bytes":1})
if __name__ == "__main__": unittest.main()
