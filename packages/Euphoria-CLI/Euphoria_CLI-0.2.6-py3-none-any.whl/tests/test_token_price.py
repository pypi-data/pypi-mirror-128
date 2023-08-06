import unittest

from src.helpers.token_price import loadTokenPrices


class TestTokenPrice(unittest.TestCase):
    def test_wagmi_price(self):
        data = "WAGMI"
        res = loadTokenPrices(data)
        self.assertIs(type(res), float)

    def test_harmony_price(self):
        data = "ONE"
        res = loadTokenPrices(data)
        self.assertIs(type(res), float)

    @unittest.expectedFailure
    def test_rand_value(self):
        data = "BSC"
        self.assertRaises(KeyError, loadTokenPrices(data))


if __name__ == "__main__":
    unittest.main()
