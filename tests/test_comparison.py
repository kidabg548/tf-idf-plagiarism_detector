import unittest
from src import comparison

class TestComparison(unittest.TestCase):

    def test_compare_identical_texts(self):
        text = "This is the same text"
        self.assertEqual(comparison.compare_texts(text, text), 100.0)

    def test_compare_completely_different_texts(self):
        text1 = "This is one text."
        text2 = "This is another text."
        self.assertAlmostEqual(comparison.compare_texts(text1, text2), 50.0, places=2)  # Allow for slight variations in calculation

    def test_compare_empty_text(self):
        self.assertEqual(comparison.compare_texts("", "Some text"), 0.0)
        self.assertEqual(comparison.compare_texts("Some text", ""), 0.0)
        self.assertEqual(comparison.compare_texts("", ""), 0.0)


if __name__ == '__main__':
    unittest.main()