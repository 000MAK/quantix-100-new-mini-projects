import unittest
from main import process
class ToolTests(unittest.TestCase):
 def test_password_obeys_requested_length(self):
  r=process({"length":24,"symbols":False})
  self.assertEqual(r["length"],24); self.assertEqual(len(r["password"]),24); self.assertTrue(r["cryptographic_randomness"])
 def test_refuses_weak_length(self):
  with self.assertRaises(ValueError): process({"length":4})
if __name__ == "__main__": unittest.main()
