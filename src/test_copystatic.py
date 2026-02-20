import unittest

from copystatic import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_valid_title(self):
        result = extract_title("# Hello")
        self.assertEqual(result, "Hello")

    def test_no_title(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_multiple_headers(self):
        result = extract_title("# First\n# Second")
        self.assertEqual(result, "First")

    def test_spacing(self):
        result = extract_title("#     Hello World    ")
        self.assertEqual(result, "Hello World")

if __name__ == '__main__':
    unittest.main()
