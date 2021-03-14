import unittest
import subprocess


class ParserTest(unittest.TestCase):
    def setUp(self):     
        return super().setUp()

    def test_help(self):
        self.result = subprocess.check_output(["python", "-m", "hasher", "-h"], text=True, encoding="utf-8", shell=True, cwd="../")
        self.assertIn("Description:", self.result)
        self.assertIn("Required Arguments", self.result)
        self.assertIn("ptional Arguments", self.result)

    def test_no_arg(self):
        self.result = subprocess.run(["python", "-m", "hasher"], capture_output=True, text=True, encoding="utf-8", shell=True, cwd="../", check=False)
        self.assertIn("usage:", self.result.stderr)
        self.assertIn("usage example:", self.result.stderr)
        self.assertIn("error:", self.result.stderr)


if __name__ == "__main__":
    unittest.main()
