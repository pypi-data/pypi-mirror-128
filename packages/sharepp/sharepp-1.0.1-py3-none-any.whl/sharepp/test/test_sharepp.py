import unittest
import sharepp


class TestSharePP(unittest.TestCase):

    def test_valid_input(self):
        try:
            price = sharepp.parse_price("IE00BHZPJ569")
            self.assertTrue(float, type(price))
        except Exception:
            self.fail("Unexpected exception!")

    def test_invalid_input(self):
        try:
            sharepp.parse_price(0)
            self.fail("Expected exception not thrown!")
        except ValueError as e:
            self.assertEqual("You must provide a string object representing a valid ISIN!", str(e))


if __name__ == '__main__':
    unittest.main()
