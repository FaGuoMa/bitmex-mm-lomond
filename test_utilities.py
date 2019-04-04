from unittest import TestCase
from utilities import red, dered

class RedTest(TestCase):

    def test_red(self):

        a = 1
        b = 3.7800000000000002e-06
        c = 0.1
        d = {'symbol': 'XBTUSD', 'id': 15599607950, 'side': 'Sell', 'size': 80, 'price': 3.7800000000000002e-06}
        e = (3.7800000000000002e-06, "b")
        f = [3.7800000000000002e-06, 3 , 4]

        bch_p = 0.030100000000000002
        self.assertEqual(red(bch_p), '0.0301')
        self.assertEqual(red(a), a)
        self.assertEqual(red(b), '3.78e-06')
        self.assertEqual(red(c), c)
        self.assertEqual(red(d), {'symbol': 'XBTUSD', 'id': 15599607950, 'side': 'Sell', 'size': 80, 'price': '3.78e-06'})
        self.assertEqual(red(e), ('3.78e-06', "b"))
        self.assertEqual(red(f), ['3.78e-06', 3, 4])

        self.assertEqual(dered(red(b)), 3.78e-06)
        self.assertEqual(dered(red(d)),
                         {'symbol': 'XBTUSD', 'id': 15599607950, 'side': 'Sell', 'size': 80, 'price': 3.78e-06})
        self.assertEqual(dered('871528a8-7d67-45d9-a9de-112e0da22ff4'), '871528a8-7d67-45d9-a9de-112e0da22ff4')