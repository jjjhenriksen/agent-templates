import unittest
from counts import parse_count

class CountTests(unittest.TestCase):
    def test_integer_and_whitespace(self):
        self.assertEqual(parse_count(' 12 '), 12)
        self.assertEqual(parse_count('0'), 0)
    def test_invalid(self):
        for value in ('', '-1', '1.5', '1e2', '１２', None, 4, True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_count(value)
