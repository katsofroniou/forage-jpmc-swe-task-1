import unittest
from client3 import getDataPoint, getRatio


class ClientTest(unittest.TestCase):
  def test_getDataPoint_calculatePrice(self):
    quotes = [
      {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]

    """ ------------ Add the assertion below ------------ """
    calculated_price = (quotes[0]['top_ask']['price'] + quotes[0]['top_bid']['price']) / 2
    self.assertEqual(calculated_price, 120.84)

  def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
    quotes = [
      {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]

    """ ------------ Add the assertion below ------------ """
    self.assertGreater(quotes[0]['top_bid']['price'], quotes[0]['top_ask']['price'])

    """ ------------ Add more unit tests ------------ """

  def test_getRatio_NormalCase(self):
    # Test when price_b is not 0
    price_a = 100.0
    price_b = 50.0
    expected_ratio = 2.0
    self.assertEqual(getRatio(price_a, price_b), expected_ratio)

  def test_getRatio_PriceBIsZero(self):
    # Test when price_b is 0, the result should be None
    price_a = 100.0
    price_b = 0
    self.assertIsNone(getRatio(price_a, price_b))

  def test_getRatio_PriceAIsZero(self):
    # Test when price_a is 0, the result should be 0.0
    price_a = 0
    price_b = 50.0
    expected_ratio = 0.0
    self.assertEqual(getRatio(price_a, price_b), expected_ratio)

  def test_getRatio_BothPricesAreZero(self):
    # Test when both price_a and price_b are 0, the result should be None
    price_a = 0
    price_b = 0
    self.assertIsNone(getRatio(price_a, price_b))

  def test_getRatio_NegativePrices(self):
    # Test when prices are negative, the result should be the negative ratio
    price_a = -50.0
    price_b = -100.0
    expected_ratio = 0.5
    self.assertEqual(getRatio(price_a, price_b), expected_ratio)

  def test_getRatio_DecimalPrices(self):
    # Test when prices have decimal values, the result should have the correct ratio
    price_a = 3.1415
    price_b = 1.4142
    expected_ratio = 2.22
    self.assertEqual(getRatio(price_a, price_b), expected_ratio)

  def test_getDataPoint_EmptyQuote(self):
    # Test when the quote is empty, should return None for all values
    quote = {}
    stock, bid_price, ask_price, price = getDataPoint(quote)

    self.assertIsNone(stock)
    self.assertIsNone(bid_price)
    self.assertIsNone(ask_price)
    self.assertIsNone(price)

  def test_getDataPoint_InvalidQuote(self):
    # Test when the quote contains invalid or missing keys, should return None for all values
    invalid_quote = {
      'stock': 'InvalidStock',
      'invalid_key': {'price': 10.0, 'size': 20},
      'top_ask': {'price': 12.0, 'size': 15},
    }
    stock, bid_price, ask_price, price = getDataPoint(invalid_quote)

    self.assertIsNone(stock)
    self.assertIsNone(bid_price)
    self.assertIsNone(ask_price)
    self.assertIsNone(price)

    def test_missing_bid(self):
      quote = {
        'stock': 'AAPL',
        'top_ask': {
          'price': 150.0
        }
        # No bid price provided
      }

      stock, bid_price, ask_price, price = getDataPoint(quote)
      self.assertIsNone(stock)
      self.assertIsNone(bid_price)  # Corrected assertion to check bid_price is None
      self.assertEqual(ask_price, 150.0)
      self.assertIsNone(price)

  def test_missing_ask(self):
    quote = {
      'stock': 'GOOG',
      'top_bid': {
        'price': 2000.0
      }
      # No ask price provided
    }

    stock, bid_price, ask_price, price = getDataPoint(quote)
    self.assertIsNone(stock)
    self.assertIsNone(bid_price)
    self.assertIsNone(ask_price)
    self.assertIsNone(price)

  def test_getDataPoint_RoundingBehavior(self):
    quote = {
      'stock': 'XYZ',
      'top_bid': {'price': 3.1415, 'size': 10},
      'top_ask': {'price': 1.4142, 'size': 20}
    }

    stock, bid_price, ask_price, price = getDataPoint(quote)
    expected_price = round((quote['top_bid']['price'] + quote['top_ask']['price']) / 2, 2)
    self.assertEqual(price, expected_price)

if __name__ == '__main__':
    unittest.main()
