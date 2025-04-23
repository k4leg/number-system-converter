import unittest
from converter import convert_base

class TestConverter(unittest.TestCase):

    def test_binary_to_decimal(self):
        self.assertEqual(convert_base("1010", 2, 10), "10")

    def test_decimal_to_binary(self):
        self.assertEqual(convert_base("10", 10, 2), "1010")

    def test_hexadecimal_to_decimal(self):
        self.assertEqual(convert_base("A5", 16, 10), "165")

    def test_decimal_to_hexadecimal(self):
        self.assertEqual(convert_base("165", 10, 16), "A5")

    def test_negative_number(self):
        self.assertEqual(convert_base("-1010", 2, 10), "-10")

    def test_fractional_number(self):
        self.assertEqual(convert_base("10.1", 2, 10), "2.5")

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            convert_base("1" * 65, 2, 10)

if __name__ == '__main__':
    unittest.main()
