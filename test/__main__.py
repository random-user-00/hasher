# __main__.py to run tests directly as `python -m test`
# Command line tests are sensitive to the working directory.
import unittest

# import all required test classes here to run them
from .test_arghandler import ParserTest

if __name__ == "__main__":
    unittest.main()
