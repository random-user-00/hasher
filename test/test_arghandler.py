import unittest
import subprocess

class ParserTest(unittest.TestCase):
    def setUp(self):     
        return super().setUp()

    def test_help(self):
        self.result = subprocess.run(["python", "-m", "hasher", "-h"], text=True, encoding="utf-8", cwd="../", capture_output=True)
        self.assertIn("usage:", self.result.stdout)
        self.assertIn("usage example:", self.result.stdout)
        self.assertIn("Description:", self.result.stdout)
        self.assertIn("Required Arguments", self.result.stdout)
        self.assertIn("ptional Arguments", self.result.stdout)

    def test_no_arg(self):
        self.result = subprocess.run(["python", "-m", "hasher"], capture_output=True, text=True, encoding="utf-8", cwd="../", check=False)
        self.assertIn("usage:", self.result.stderr)
        self.assertIn("usage example:", self.result.stderr)
        self.assertIn("error:", self.result.stderr)

if __name__ == "__main__":
    unittest.main()
