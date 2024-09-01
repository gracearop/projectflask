import unittest

if __name__ == "__main__":
    # Discover and run all test files in the 'tests' directory
    unittest.TextTestRunner().run(unittest.defaultTestLoader.discover('tests'))
