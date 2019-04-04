from unittest import TestCase

from orderbook import OrderBook
from orders import Order, OrderKeep, BitmexInterface
from utilities import dtnow
from agent.agent import MM
import datetime as dt
from time import sleep


class Inputs(TestCase):

    def test_partial(self):
        o = OrderBook('XBTUSD', update_callback=print)

        msg1 = {'table': 'orderBookL2_25', 'action': 'partial', 'keys': ['symbol', 'id', 'side'],
                'types': {'symbol': 'symbol', 'id': 'long', 'side': 'symbol', 'size': 'long', 'price': 'float'},
                'foreignKeys': {'symbol': 'instrument', 'side': 'side'},
                'attributes': {'symbol': 'grouped', 'id': 'sorted'},
                'filter': {'symbol': 'XBTUSD'},
                'data': [{'symbol': 'XBTUSD', 'id': 15599607950, 'side': 'Sell', 'size': 80, 'price': 3920.5},
                         {'symbol': 'XBTUSD', 'id': 15599608000, 'side': 'Sell', 'size': 341, 'price': 3920},
                         {'symbol': 'XBTUSD', 'id': 15599608050, 'side': 'Sell', 'size': 91, 'price': 3919.5},
                         {'symbol': 'XBTUSD', 'id': 15599608100, 'side': 'Sell', 'size': 41, 'price': 3919},
                         {'symbol': 'XBTUSD', 'id': 15599608150, 'side': 'Sell', 'size': 235, 'price': 3918.5},
                         {'symbol': 'XBTUSD', 'id': 15599608200, 'side': 'Sell', 'size': 460, 'price': 3918},
                         {'symbol': 'XBTUSD', 'id': 15599608250, 'side': 'Sell', 'size': 50, 'price': 3917.5},
                         {'symbol': 'XBTUSD', 'id': 15599608300, 'side': 'Sell', 'size': 287, 'price': 3917},
                         {'symbol': 'XBTUSD', 'id': 15599608350, 'side': 'Sell', 'size': 161, 'price': 3916.5},
                         {'symbol': 'XBTUSD', 'id': 15599608400, 'side': 'Sell', 'size': 360, 'price': 3916},
                         {'symbol': 'XBTUSD', 'id': 15599608500, 'side': 'Sell', 'size': 845, 'price': 3915},
                         {'symbol': 'XBTUSD', 'id': 15599608550, 'side': 'Sell', 'size': 418, 'price': 3914.5},
                         {'symbol': 'XBTUSD', 'id': 15599608600, 'side': 'Sell', 'size': 424, 'price': 3914},
                         {'symbol': 'XBTUSD', 'id': 15599608650, 'side': 'Sell', 'size': 2500, 'price': 3913.5},
                         {'symbol': 'XBTUSD', 'id': 15599608700, 'side': 'Sell', 'size': 39, 'price': 3913},
                         {'symbol': 'XBTUSD', 'id': 15599608750, 'side': 'Sell', 'size': 70, 'price': 3912.5},
                         {'symbol': 'XBTUSD', 'id': 15599608800, 'side': 'Sell', 'size': 275, 'price': 3912},
                         {'symbol': 'XBTUSD', 'id': 15599608900, 'side': 'Sell', 'size': 10, 'price': 3911},
                         {'symbol': 'XBTUSD', 'id': 15599608950, 'side': 'Sell', 'size': 161, 'price': 3910.5},
                         {'symbol': 'XBTUSD', 'id': 15599609000, 'side': 'Sell', 'size': 50212, 'price': 3910},
                         {'symbol': 'XBTUSD', 'id': 15599609100, 'side': 'Sell', 'size': 139, 'price': 3909},
                         {'symbol': 'XBTUSD', 'id': 15599609150, 'side': 'Sell', 'size': 2000, 'price': 3908.5},
                         {'symbol': 'XBTUSD', 'id': 15599609200, 'side': 'Sell', 'size': 300, 'price': 3908},
                         {'symbol': 'XBTUSD', 'id': 15599609250, 'side': 'Sell', 'size': 443, 'price': 3907.5},
                         {'symbol': 'XBTUSD', 'id': 15599609300, 'side': 'Sell', 'size': 6860, 'price': 3907},
                         {'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 259, 'price': 3903.5},
                         {'symbol': 'XBTUSD', 'id': 15599609700, 'side': 'Buy', 'size': 100, 'price': 3903},
                         {'symbol': 'XBTUSD', 'id': 15599609800, 'side': 'Buy', 'size': 382, 'price': 3902},
                         {'symbol': 'XBTUSD', 'id': 15599609850, 'side': 'Buy', 'size': 100, 'price': 3901.5},
                         {'symbol': 'XBTUSD', 'id': 15599609900, 'side': 'Buy', 'size': 100, 'price': 3901},
                         {'symbol': 'XBTUSD', 'id': 15599609950, 'side': 'Buy', 'size': 100, 'price': 3900.5},
                         {'symbol': 'XBTUSD', 'id': 15599610000, 'side': 'Buy', 'size': 100, 'price': 3900},
                         {'symbol': 'XBTUSD', 'id': 15599610050, 'side': 'Buy', 'size': 100, 'price': 3899.5},
                         {'symbol': 'XBTUSD', 'id': 15599610100, 'side': 'Buy', 'size': 100, 'price': 3899},
                         {'symbol': 'XBTUSD', 'id': 15599610200, 'side': 'Buy', 'size': 691, 'price': 3898},
                         {'symbol': 'XBTUSD', 'id': 15599610250, 'side': 'Buy', 'size': 43, 'price': 3897.5},
                         {'symbol': 'XBTUSD', 'id': 15599610300, 'side': 'Buy', 'size': 726, 'price': 3897},
                         {'symbol': 'XBTUSD', 'id': 15599610400, 'side': 'Buy', 'size': 23, 'price': 3896},
                         {'symbol': 'XBTUSD', 'id': 15599610500, 'side': 'Buy', 'size': 100, 'price': 3895},
                         {'symbol': 'XBTUSD', 'id': 15599610600, 'side': 'Buy', 'size': 400, 'price': 3894},
                         {'symbol': 'XBTUSD', 'id': 15599610650, 'side': 'Buy', 'size': 1559, 'price': 3893.5},
                         {'symbol': 'XBTUSD', 'id': 15599610700, 'side': 'Buy', 'size': 405, 'price': 3893},
                         {'symbol': 'XBTUSD', 'id': 15599610800, 'side': 'Buy', 'size': 3592, 'price': 3892},
                         {'symbol': 'XBTUSD', 'id': 15599610850, 'side': 'Buy', 'size': 69, 'price': 3891.5},
                         {'symbol': 'XBTUSD', 'id': 15599610900, 'side': 'Buy', 'size': 201, 'price': 3891},
                         {'symbol': 'XBTUSD', 'id': 15599611000, 'side': 'Buy', 'size': 598, 'price': 3890},
                         {'symbol': 'XBTUSD', 'id': 15599611050, 'side': 'Buy', 'size': 98, 'price': 3889.5},
                         {'symbol': 'XBTUSD', 'id': 15599611150, 'side': 'Buy', 'size': 10, 'price': 3888.5},
                         {'symbol': 'XBTUSD', 'id': 15599611200, 'side': 'Buy', 'size': 60, 'price': 3888},
                         {'symbol': 'XBTUSD', 'id': 15599611250, 'side': 'Buy', 'size': 130, 'price': 3887.5}]}

        msg2 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'XBTUSD', 'id': 15599608300, 'side': 'Sell', 'size': 289}]}
        msg3 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 252}]}

        msg4 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'XBTUSD', 'id': 15599609000, 'side': 'Sell', 'size': 50211}]}
        msg5 = {'table': 'orderBookL2_25', 'action': 'delete',
                'data': [{'symbol': 'XBTUSD', 'id': 15599611250, 'side': 'Buy'}]}
        msg6 = {'table': 'orderBookL2_25', 'action': 'insert',
                'data': [{'symbol': 'XBTUSD', 'id': 15599609600, 'side': 'Buy', 'size': 1761, 'price': 3904}]}

        o.getmsg(msg1)
        print(o.book)

        self.assertIsInstance(o.book, dict)
        self.assertEqual(o.book[15599607950]['side'], "Sell")
        self.assertTrue(o.partial)
        print("msg2")
        o.getmsg(msg2)
        self.assertEqual(o.book[15599608300]['size'], 289)
        o.getmsg(msg3)
        self.assertEqual(o.book[15599609650]['size'], 252)
        o.getmsg(msg4)
        self.assertEqual(o.book[15599609000]['size'], 50211)

        o.getmsg(msg5)
        with self.assertRaises(KeyError):
            o.book[15599611250]

        o.getmsg(msg6)
        self.assertEqual(o.book[15599609600]['size'], 1761)

        print(o.p_ladder)
        print(o.bbo())

        self.assertEqual(o.bbo(5),
                         {'bid': [3904, 3903.5, 3903.0, 3902.0, 3901.5], 'ask': [3907.0, 3907.5, 3908.0, 3908.5, 3909.0]})

        self.assertEqual(o.get_id(3920.5), [15599607950, 80])


        #print test with TRX/flot point
        print("TRX test")
        o = OrderBook('TRXZ18', update_callback=print)
        msg1 = {'table': 'orderBookL2_25', 'action': 'partial', 'keys': ['symbol', 'id', 'side'], 'types': {'symbol': 'symbol', 'id': 'long', 'side': 'symbol', 'size': 'long', 'price': 'float'}, 'foreignKeys': {'symbol': 'instrument', 'side': 'side'}, 'attributes': {'symbol': 'grouped', 'id': 'sorted'}, 'filter': {'symbol': 'TRXZ18'}, 'data': [{'symbol': 'TRXZ18', 'id': 39799999406, 'side': 'Sell', 'size': 1000000, 'price': 5.94e-06}, {'symbol': 'TRXZ18', 'id': 39799999544, 'side': 'Sell', 'size': 50000, 'price': 4.56e-06}, {'symbol': 'TRXZ18', 'id': 39799999550, 'side': 'Sell', 'size': 2001, 'price': 4.5e-06}, {'symbol': 'TRXZ18', 'id': 39799999556, 'side': 'Sell', 'size': 3085973, 'price': 4.44e-06}, {'symbol': 'TRXZ18', 'id': 39799999564, 'side': 'Sell', 'size': 1000, 'price': 4.36e-06}, {'symbol': 'TRXZ18', 'id': 39799999576, 'side': 'Sell', 'size': 1, 'price': 4.24e-06}, {'symbol': 'TRXZ18', 'id': 39799999580, 'side': 'Sell', 'size': 50100, 'price': 4.2e-06}, {'symbol': 'TRXZ18', 'id': 39799999582, 'side': 'Sell', 'size': 1000000, 'price': 4.18e-06}, {'symbol': 'TRXZ18', 'id': 39799999588, 'side': 'Sell', 'size': 100000, 'price': 4.12e-06}, {'symbol': 'TRXZ18', 'id': 39799999592, 'side': 'Sell', 'size': 10, 'price': 4.08e-06}, {'symbol': 'TRXZ18', 'id': 39799999595, 'side': 'Sell', 'size': 1000, 'price': 4.05e-06}, {'symbol': 'TRXZ18', 'id': 39799999599, 'side': 'Sell', 'size': 200, 'price': 4.01e-06}, {'symbol': 'TRXZ18', 'id': 39799999600, 'side': 'Sell', 'size': 104500, 'price': 4e-06}, {'symbol': 'TRXZ18', 'id': 39799999601, 'side': 'Sell', 'size': 21000, 'price': 3.99e-06}, {'symbol': 'TRXZ18', 'id': 39799999602, 'side': 'Sell', 'size': 5076142, 'price': 3.98e-06}, {'symbol': 'TRXZ18', 'id': 39799999604, 'side': 'Sell', 'size': 2538071, 'price': 3.96e-06}, {'symbol': 'TRXZ18', 'id': 39799999605, 'side': 'Sell', 'size': 2500, 'price': 3.95e-06}, {'symbol': 'TRXZ18', 'id': 39799999607, 'side': 'Sell', 'size': 1522837, 'price': 3.93e-06}, {'symbol': 'TRXZ18', 'id': 39799999608, 'side': 'Buy', 'size': 1522842, 'price': 3.92e-06}, {'symbol': 'TRXZ18', 'id': 39799999611, 'side': 'Buy', 'size': 2988071, 'price': 3.89e-06}, {'symbol': 'TRXZ18', 'id': 39799999613, 'side': 'Buy', 'size': 5226142, 'price': 3.87e-06}, {'symbol': 'TRXZ18', 'id': 39799999614, 'side': 'Buy', 'size': 20000, 'price': 3.86e-06}, {'symbol': 'TRXZ18', 'id': 39799999615, 'side': 'Buy', 'size': 15000, 'price': 3.85e-06}, {'symbol': 'TRXZ18', 'id': 39799999620, 'side': 'Buy', 'size': 32000, 'price': 3.8e-06}, {'symbol': 'TRXZ18', 'id': 39799999627, 'side': 'Buy', 'size': 1000, 'price': 3.73e-06}, {'symbol': 'TRXZ18', 'id': 39799999628, 'side': 'Buy', 'size': 1000, 'price': 3.72e-06}, {'symbol': 'TRXZ18', 'id': 39799999630, 'side': 'Buy', 'size': 11000, 'price': 3.7e-06}, {'symbol': 'TRXZ18', 'id': 39799999636, 'side': 'Buy', 'size': 400, 'price': 3.64e-06}, {'symbol': 'TRXZ18', 'id': 39799999640, 'side': 'Buy', 'size': 100, 'price': 3.6e-06}, {'symbol': 'TRXZ18', 'id': 39799999641, 'side': 'Buy', 'size': 130000, 'price': 3.59e-06}, {'symbol': 'TRXZ18', 'id': 39799999643, 'side': 'Buy', 'size': 20000, 'price': 3.57e-06}, {'symbol': 'TRXZ18', 'id': 39799999644, 'side': 'Buy', 'size': 1000000, 'price': 3.56e-06}, {'symbol': 'TRXZ18', 'id': 39799999645, 'side': 'Buy', 'size': 1, 'price': 3.55e-06}, {'symbol': 'TRXZ18', 'id': 39799999647, 'side': 'Buy', 'size': 500000, 'price': 3.53e-06}, {'symbol': 'TRXZ18', 'id': 39799999650, 'side': 'Buy', 'size': 20001, 'price': 3.5e-06}, {'symbol': 'TRXZ18', 'id': 39799999655, 'side': 'Buy', 'size': 270000, 'price': 3.45e-06}, {'symbol': 'TRXZ18', 'id': 39799999660, 'side': 'Buy', 'size': 2350, 'price': 3.4e-06}, {'symbol': 'TRXZ18', 'id': 39799999661, 'side': 'Buy', 'size': 4, 'price': 3.39e-06}, {'symbol': 'TRXZ18', 'id': 39799999670, 'side': 'Buy', 'size': 12, 'price': 3.3e-06}, {'symbol': 'TRXZ18', 'id': 39799999673, 'side': 'Buy', 'size': 1000000, 'price': 3.27e-06}, {'symbol': 'TRXZ18', 'id': 39799999680, 'side': 'Buy', 'size': 40054, 'price': 3.2e-06}, {'symbol': 'TRXZ18', 'id': 39799999686, 'side': 'Buy', 'size': 36, 'price': 3.14e-06}, {'symbol': 'TRXZ18', 'id': 39799999690, 'side': 'Buy', 'size': 21000, 'price': 3.1e-06}]}
        o.getmsg(msg1)
        print(o.book)
        print(o.p_ladder)
        print(o.bbo())


class TestOrder(TestCase):

    def test_ladder(self):
        ord = Order(symbol="XBTUSD", price=3903.5, id_level=15599609650, orderQty=25)
        # I am assuming we have the ack processed
        ord.status = "processed"

        ob = OrderBook('XBTUSD', update_callback=ord.process_diff_msg)

        msg1 = {'table': 'orderBookL2_25', 'action': 'partial', 'keys': ['symbol', 'id', 'side'],
                'types': {'symbol': 'symbol', 'id': 'long', 'side': 'symbol', 'size': 'long', 'price': 'float'},
                'foreignKeys': {'symbol': 'instrument', 'side': 'side'},
                'attributes': {'symbol': 'grouped', 'id': 'sorted'},
                'filter': {'symbol': 'XBTUSD'},
                'data': [{'symbol': 'XBTUSD', 'id': 15599607950, 'side': 'Sell', 'size': 80, 'price': 3920.5},
                         {'symbol': 'XBTUSD', 'id': 15599608000, 'side': 'Sell', 'size': 341, 'price': 3920},
                         {'symbol': 'XBTUSD', 'id': 15599608050, 'side': 'Sell', 'size': 91, 'price': 3919.5},
                         {'symbol': 'XBTUSD', 'id': 15599608100, 'side': 'Sell', 'size': 41, 'price': 3919},
                         {'symbol': 'XBTUSD', 'id': 15599608150, 'side': 'Sell', 'size': 235, 'price': 3918.5},
                         {'symbol': 'XBTUSD', 'id': 15599608200, 'side': 'Sell', 'size': 460, 'price': 3918},
                         {'symbol': 'XBTUSD', 'id': 15599608250, 'side': 'Sell', 'size': 50, 'price': 3917.5},
                         {'symbol': 'XBTUSD', 'id': 15599608300, 'side': 'Sell', 'size': 287, 'price': 3917},
                         {'symbol': 'XBTUSD', 'id': 15599608350, 'side': 'Sell', 'size': 161, 'price': 3916.5},
                         {'symbol': 'XBTUSD', 'id': 15599608400, 'side': 'Sell', 'size': 360, 'price': 3916},
                         {'symbol': 'XBTUSD', 'id': 15599608500, 'side': 'Sell', 'size': 845, 'price': 3915},
                         {'symbol': 'XBTUSD', 'id': 15599608550, 'side': 'Sell', 'size': 418, 'price': 3914.5},
                         {'symbol': 'XBTUSD', 'id': 15599608600, 'side': 'Sell', 'size': 424, 'price': 3914},
                         {'symbol': 'XBTUSD', 'id': 15599608650, 'side': 'Sell', 'size': 2500, 'price': 3913.5},
                         {'symbol': 'XBTUSD', 'id': 15599608700, 'side': 'Sell', 'size': 39, 'price': 3913},
                         {'symbol': 'XBTUSD', 'id': 15599608750, 'side': 'Sell', 'size': 70, 'price': 3912.5},
                         {'symbol': 'XBTUSD', 'id': 15599608800, 'side': 'Sell', 'size': 275, 'price': 3912},
                         {'symbol': 'XBTUSD', 'id': 15599608900, 'side': 'Sell', 'size': 10, 'price': 3911},
                         {'symbol': 'XBTUSD', 'id': 15599608950, 'side': 'Sell', 'size': 161, 'price': 3910.5},
                         {'symbol': 'XBTUSD', 'id': 15599609000, 'side': 'Sell', 'size': 50212, 'price': 3910},
                         {'symbol': 'XBTUSD', 'id': 15599609100, 'side': 'Sell', 'size': 139, 'price': 3909},
                         {'symbol': 'XBTUSD', 'id': 15599609150, 'side': 'Sell', 'size': 2000, 'price': 3908.5},
                         {'symbol': 'XBTUSD', 'id': 15599609200, 'side': 'Sell', 'size': 300, 'price': 3908},
                         {'symbol': 'XBTUSD', 'id': 15599609250, 'side': 'Sell', 'size': 443, 'price': 3907.5},
                         {'symbol': 'XBTUSD', 'id': 15599609300, 'side': 'Sell', 'size': 6860, 'price': 3907},
                         {'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 259, 'price': 3903.5},
                         # level of order
                         {'symbol': 'XBTUSD', 'id': 15599609700, 'side': 'Buy', 'size': 100, 'price': 3903},
                         {'symbol': 'XBTUSD', 'id': 15599609800, 'side': 'Buy', 'size': 382, 'price': 3902},
                         {'symbol': 'XBTUSD', 'id': 15599609850, 'side': 'Buy', 'size': 100, 'price': 3901.5},
                         {'symbol': 'XBTUSD', 'id': 15599609900, 'side': 'Buy', 'size': 100, 'price': 3901},
                         {'symbol': 'XBTUSD', 'id': 15599609950, 'side': 'Buy', 'size': 100, 'price': 3900.5},
                         {'symbol': 'XBTUSD', 'id': 15599610000, 'side': 'Buy', 'size': 100, 'price': 3900},
                         {'symbol': 'XBTUSD', 'id': 15599610050, 'side': 'Buy', 'size': 100, 'price': 3899.5},
                         {'symbol': 'XBTUSD', 'id': 15599610100, 'side': 'Buy', 'size': 100, 'price': 3899},
                         {'symbol': 'XBTUSD', 'id': 15599610200, 'side': 'Buy', 'size': 691, 'price': 3898},
                         {'symbol': 'XBTUSD', 'id': 15599610250, 'side': 'Buy', 'size': 43, 'price': 3897.5},
                         {'symbol': 'XBTUSD', 'id': 15599610300, 'side': 'Buy', 'size': 726, 'price': 3897},
                         {'symbol': 'XBTUSD', 'id': 15599610400, 'side': 'Buy', 'size': 23, 'price': 3896},
                         {'symbol': 'XBTUSD', 'id': 15599610500, 'side': 'Buy', 'size': 100, 'price': 3895},
                         {'symbol': 'XBTUSD', 'id': 15599610600, 'side': 'Buy', 'size': 400, 'price': 3894},
                         {'symbol': 'XBTUSD', 'id': 15599610650, 'side': 'Buy', 'size': 1559, 'price': 3893.5},
                         {'symbol': 'XBTUSD', 'id': 15599610700, 'side': 'Buy', 'size': 405, 'price': 3893},
                         {'symbol': 'XBTUSD', 'id': 15599610800, 'side': 'Buy', 'size': 3592, 'price': 3892},
                         {'symbol': 'XBTUSD', 'id': 15599610850, 'side': 'Buy', 'size': 69, 'price': 3891.5},
                         {'symbol': 'XBTUSD', 'id': 15599610900, 'side': 'Buy', 'size': 201, 'price': 3891},
                         {'symbol': 'XBTUSD', 'id': 15599611000, 'side': 'Buy', 'size': 598, 'price': 3890},
                         {'symbol': 'XBTUSD', 'id': 15599611050, 'side': 'Buy', 'size': 98, 'price': 3889.5},
                         {'symbol': 'XBTUSD', 'id': 15599611150, 'side': 'Buy', 'size': 10, 'price': 3888.5},
                         {'symbol': 'XBTUSD', 'id': 15599611200, 'side': 'Buy', 'size': 60, 'price': 3888},
                         {'symbol': 'XBTUSD', 'id': 15599611250, 'side': 'Buy', 'size': 130, 'price': 3887.5}]}

        ob.getmsg(msg1)
        # we get bbo and relevant id level
        pr = ob.bbo()['bid']
        idl = ob.get_id(pr)
        print(pr)
        print(idl)

        msg2 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 284}]}

        # process message
        ob.getmsg(msg2)

        self.assertEqual(ord.status, "on_ladder")
        self.assertEqual(ord.size_before, 259)
        self.assertEqual(ord.size_after, 0)

        msg3 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 300}]}

        # process message
        ob.getmsg(msg3)

        self.assertEqual(ord.size_after, 16)
        self.assertEqual(ord.size_before, 259)

        msg4 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 250}]}

        ob.getmsg(msg4)
        self.assertEqual(ord.size_after, 0)
        self.assertEqual(ord.size_before, 259 - 34)

        # adding directly to the queue after when ord.size_after = 0
        msg5 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 350}]}

        ob.getmsg(msg5)
        self.assertEqual(ord.size_before, 259 - 34)
        self.assertEqual(ord.size_after, 100)

        # adding directly to the queue after when ord.size_after = 100 + 50
        msg6 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 400}]}

        ob.getmsg(msg6)
        self.assertEqual(ord.size_before, 259 - 34)
        self.assertEqual(ord.size_after, 150)

        # TRX version
        print("TRX testing")

        ord = Order(symbol="TRXZ18", price=3.92e-06, id_level=39799999608, orderQty=1000)
        # I am assuming we have the ack processed
        ord.status = "processed"

        ob = OrderBook('XBTUSD', update_callback=ord.process_diff_msg)

        msg1 = {'table': 'orderBookL2_25', 'action': 'partial', 'keys': ['symbol', 'id', 'side'],
                'types': {'symbol': 'symbol', 'id': 'long', 'side': 'symbol', 'size': 'long', 'price': 'float'},
                'foreignKeys': {'symbol': 'instrument', 'side': 'side'},
                'attributes': {'symbol': 'grouped', 'id': 'sorted'}, 'filter': {'symbol': 'TRXZ18'},
                'data': [{'symbol': 'TRXZ18', 'id': 39799999406, 'side': 'Sell', 'size': 1000000, 'price': 5.94e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999544, 'side': 'Sell', 'size': 50000, 'price': 4.56e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999550, 'side': 'Sell', 'size': 2001, 'price': 4.5e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999556, 'side': 'Sell', 'size': 3085973, 'price': 4.44e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999564, 'side': 'Sell', 'size': 1000, 'price': 4.36e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999576, 'side': 'Sell', 'size': 1, 'price': 4.24e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999580, 'side': 'Sell', 'size': 50100, 'price': 4.2e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999582, 'side': 'Sell', 'size': 1000000, 'price': 4.18e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999588, 'side': 'Sell', 'size': 100000, 'price': 4.12e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999592, 'side': 'Sell', 'size': 10, 'price': 4.08e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999595, 'side': 'Sell', 'size': 1000, 'price': 4.05e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999599, 'side': 'Sell', 'size': 200, 'price': 4.01e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999600, 'side': 'Sell', 'size': 104500, 'price': 4e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999601, 'side': 'Sell', 'size': 21000, 'price': 3.99e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999602, 'side': 'Sell', 'size': 5076142, 'price': 3.98e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999604, 'side': 'Sell', 'size': 2538071, 'price': 3.96e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999605, 'side': 'Sell', 'size': 2500, 'price': 3.95e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999607, 'side': 'Sell', 'size': 1522837, 'price': 3.93e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999608, 'side': 'Buy', 'size': 1522842, 'price': 3.92e-06},#here
                         {'symbol': 'TRXZ18', 'id': 39799999611, 'side': 'Buy', 'size': 2988071, 'price': 3.89e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999613, 'side': 'Buy', 'size': 5226142, 'price': 3.87e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999614, 'side': 'Buy', 'size': 20000, 'price': 3.86e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999615, 'side': 'Buy', 'size': 15000, 'price': 3.85e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999620, 'side': 'Buy', 'size': 32000, 'price': 3.8e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999627, 'side': 'Buy', 'size': 1000, 'price': 3.73e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999628, 'side': 'Buy', 'size': 1000, 'price': 3.72e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999630, 'side': 'Buy', 'size': 11000, 'price': 3.7e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999636, 'side': 'Buy', 'size': 400, 'price': 3.64e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999640, 'side': 'Buy', 'size': 100, 'price': 3.6e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999641, 'side': 'Buy', 'size': 130000, 'price': 3.59e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999643, 'side': 'Buy', 'size': 20000, 'price': 3.57e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999644, 'side': 'Buy', 'size': 1000000, 'price': 3.56e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999645, 'side': 'Buy', 'size': 1, 'price': 3.55e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999647, 'side': 'Buy', 'size': 500000, 'price': 3.53e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999650, 'side': 'Buy', 'size': 20001, 'price': 3.5e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999655, 'side': 'Buy', 'size': 270000, 'price': 3.45e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999660, 'side': 'Buy', 'size': 2350, 'price': 3.4e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999661, 'side': 'Buy', 'size': 4, 'price': 3.39e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999670, 'side': 'Buy', 'size': 12, 'price': 3.3e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999673, 'side': 'Buy', 'size': 1000000, 'price': 3.27e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999680, 'side': 'Buy', 'size': 40054, 'price': 3.2e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999686, 'side': 'Buy', 'size': 36, 'price': 3.14e-06},
                         {'symbol': 'TRXZ18', 'id': 39799999690, 'side': 'Buy', 'size': 21000, 'price': 3.1e-06}]}


        ob.getmsg(msg1)
        # we get bbo and relevant id level
        pr = ob.bbo()['bid']
        idl = ob.get_id(pr)
        print(pr)
        print(idl)

        msg2 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'TRXZ18', 'id': 39799999608, 'side': 'Buy', 'size': 1522842 + 1000}]}

        # process message
        ob.getmsg(msg2)

        self.assertEqual(ord.status, "on_ladder")
        self.assertEqual(ord.size_before, 1522842)
        self.assertEqual(ord.size_after, 0)
        print("msg3")
        msg3 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'TRXZ18', 'id': 39799999608, 'side': 'Buy', 'size': 1522842 + 1000  +100}]}

        # process message
        ob.getmsg(msg3)
        self.assertEqual(ord.size_before, 1522842)
        self.assertEqual(ord.size_after, 100)

        print('msg4')
        msg4 = {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'TRXZ18', 'id': 39799999608, 'side': 'Buy', 'size': 1522842 + 1000  +100 - 200}]}

        ob.getmsg(msg4)
        self.assertEqual(ord.size_after, 0)
        self.assertEqual(ord.size_before, 1522842 - 100)


class TestKeep(TestCase):

    def test_add_order(self):
        k = OrderKeep()
        # basic order
        ord1 = dict(symbol='XBTUSD', price=4200, orderQty=-10)
        ord2 = dict(symbol='XBTUSD', price=3600, orderQty=11, execInst="ParticipateDoNotInitiate")
        ord3 = dict(symbol='XBTUSD', price=3500, orderQty=12, ordType="Limit")
        # complete order (mkt)
        ord4 = dict(symbol='XBTUSD', orderQty=13, ordType="Market")
        ord5 = dict(symbol='XBTUSD', orderQty=14, ordType="Market", price=3600)

        # ord with bogus parameter
        ord6 = dict(symbol='XBTUSD', price=4200., orderQty=-15, foo=42)

        ords = [ord1, ord2, ord3, ord4]
        # init test
        self.assertEqual(k.keep, dict())
        k.add_order(ords)
        ords_warn1 = [ord5]
        ords_warn2 = [ord6]

        # with self.assertRaises(Warning):
        #     k.add_order(ords_warn1)
        # with self.assertRaises(Warning):
        #     k.add_order(ords_warn2)

        print(len(k.keep))
        print(k.ord_report())

    def test_enrich_order(self):
        """
        we put a basic book, then add an order with id level, one without and run for 'processed' and 'on_ladder'
        :return:
        """

        k = OrderKeep()
        ob = OrderBook('XBTUSD', update_callback=k.size_update)

        msg1 = {'table': 'orderBookL2_25', 'action': 'partial', 'keys': ['symbol', 'id', 'side'],
                'types': {'symbol': 'symbol', 'id': 'long', 'side': 'symbol', 'size': 'long', 'price': 'float'},
                'foreignKeys': {'symbol': 'instrument', 'side': 'side'},
                'attributes': {'symbol': 'grouped', 'id': 'sorted'},
                'filter': {'symbol': 'XBTUSD'},
                'data': [{'symbol': 'XBTUSD', 'id': 15599607950, 'side': 'Sell', 'size': 80, 'price': 3920.5},
                         {'symbol': 'XBTUSD', 'id': 15599608000, 'side': 'Sell', 'size': 341, 'price': 3920},
                         {'symbol': 'XBTUSD', 'id': 15599608050, 'side': 'Sell', 'size': 91, 'price': 3919.5},
                         {'symbol': 'XBTUSD', 'id': 15599608100, 'side': 'Sell', 'size': 41, 'price': 3919},
                         {'symbol': 'XBTUSD', 'id': 15599608150, 'side': 'Sell', 'size': 235, 'price': 3918.5},
                         {'symbol': 'XBTUSD', 'id': 15599608200, 'side': 'Sell', 'size': 460, 'price': 3918},
                         {'symbol': 'XBTUSD', 'id': 15599608250, 'side': 'Sell', 'size': 50, 'price': 3917.5},
                         {'symbol': 'XBTUSD', 'id': 15599608300, 'side': 'Sell', 'size': 287, 'price': 3917},
                         {'symbol': 'XBTUSD', 'id': 15599608350, 'side': 'Sell', 'size': 161, 'price': 3916.5},
                         {'symbol': 'XBTUSD', 'id': 15599608400, 'side': 'Sell', 'size': 360, 'price': 3916},
                         {'symbol': 'XBTUSD', 'id': 15599608500, 'side': 'Sell', 'size': 845, 'price': 3915},
                         {'symbol': 'XBTUSD', 'id': 15599608550, 'side': 'Sell', 'size': 418, 'price': 3914.5},
                         {'symbol': 'XBTUSD', 'id': 15599608600, 'side': 'Sell', 'size': 424, 'price': 3914},
                         {'symbol': 'XBTUSD', 'id': 15599608650, 'side': 'Sell', 'size': 2500, 'price': 3913.5},
                         {'symbol': 'XBTUSD', 'id': 15599608700, 'side': 'Sell', 'size': 39, 'price': 3913},
                         {'symbol': 'XBTUSD', 'id': 15599608750, 'side': 'Sell', 'size': 70, 'price': 3912.5},
                         {'symbol': 'XBTUSD', 'id': 15599608800, 'side': 'Sell', 'size': 275, 'price': 3912},
                         {'symbol': 'XBTUSD', 'id': 15599608900, 'side': 'Sell', 'size': 10, 'price': 3911},
                         {'symbol': 'XBTUSD', 'id': 15599608950, 'side': 'Sell', 'size': 161, 'price': 3910.5},
                         {'symbol': 'XBTUSD', 'id': 15599609000, 'side': 'Sell', 'size': 50212, 'price': 3910},
                         {'symbol': 'XBTUSD', 'id': 15599609100, 'side': 'Sell', 'size': 139, 'price': 3909},
                         {'symbol': 'XBTUSD', 'id': 15599609150, 'side': 'Sell', 'size': 2000, 'price': 3908.5},
                         {'symbol': 'XBTUSD', 'id': 15599609200, 'side': 'Sell', 'size': 300, 'price': 3908},
                         {'symbol': 'XBTUSD', 'id': 15599609250, 'side': 'Sell', 'size': 443, 'price': 3907.5},
                         {'symbol': 'XBTUSD', 'id': 15599609300, 'side': 'Sell', 'size': 6860, 'price': 3907},
                         {'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 259, 'price': 3903.5},
                         # level of order
                         {'symbol': 'XBTUSD', 'id': 15599609700, 'side': 'Buy', 'size': 100, 'price': 3903},
                         {'symbol': 'XBTUSD', 'id': 15599609800, 'side': 'Buy', 'size': 382, 'price': 3902},
                         {'symbol': 'XBTUSD', 'id': 15599609850, 'side': 'Buy', 'size': 100, 'price': 3901.5},
                         {'symbol': 'XBTUSD', 'id': 15599609900, 'side': 'Buy', 'size': 100, 'price': 3901},
                         {'symbol': 'XBTUSD', 'id': 15599609950, 'side': 'Buy', 'size': 100, 'price': 3900.5},
                         {'symbol': 'XBTUSD', 'id': 15599610000, 'side': 'Buy', 'size': 100, 'price': 3900},
                         {'symbol': 'XBTUSD', 'id': 15599610050, 'side': 'Buy', 'size': 100, 'price': 3899.5},
                         {'symbol': 'XBTUSD', 'id': 15599610100, 'side': 'Buy', 'size': 100, 'price': 3899},
                         {'symbol': 'XBTUSD', 'id': 15599610200, 'side': 'Buy', 'size': 691, 'price': 3898},
                         {'symbol': 'XBTUSD', 'id': 15599610250, 'side': 'Buy', 'size': 43, 'price': 3897.5},
                         {'symbol': 'XBTUSD', 'id': 15599610300, 'side': 'Buy', 'size': 726, 'price': 3897},
                         {'symbol': 'XBTUSD', 'id': 15599610400, 'side': 'Buy', 'size': 23, 'price': 3896},
                         {'symbol': 'XBTUSD', 'id': 15599610500, 'side': 'Buy', 'size': 100, 'price': 3895},
                         {'symbol': 'XBTUSD', 'id': 15599610600, 'side': 'Buy', 'size': 400, 'price': 3894},
                         {'symbol': 'XBTUSD', 'id': 15599610650, 'side': 'Buy', 'size': 1559, 'price': 3893.5},
                         {'symbol': 'XBTUSD', 'id': 15599610700, 'side': 'Buy', 'size': 405, 'price': 3893},
                         {'symbol': 'XBTUSD', 'id': 15599610800, 'side': 'Buy', 'size': 3592, 'price': 3892},
                         {'symbol': 'XBTUSD', 'id': 15599610850, 'side': 'Buy', 'size': 69, 'price': 3891.5},
                         {'symbol': 'XBTUSD', 'id': 15599610900, 'side': 'Buy', 'size': 201, 'price': 3891},
                         {'symbol': 'XBTUSD', 'id': 15599611000, 'side': 'Buy', 'size': 598, 'price': 3890},
                         {'symbol': 'XBTUSD', 'id': 15599611050, 'side': 'Buy', 'size': 98, 'price': 3889.5},
                         {'symbol': 'XBTUSD', 'id': 15599611150, 'side': 'Buy', 'size': 10, 'price': 3888.5},
                         {'symbol': 'XBTUSD', 'id': 15599611200, 'side': 'Buy', 'size': 60, 'price': 3888},
                         {'symbol': 'XBTUSD', 'id': 15599611250, 'side': 'Buy', 'size': 130, 'price': 3887.5}]}

        ob.getmsg(msg1)
        # we get bbo and relevant id level
        pr = ob.bbo()['bid']
        idl = ob.get_id(pr, with_size=False)
        self.assertEqual(pr, 3903.5)
        self.assertEqual(idl, 15599609650)
        k.add_order([dict(symbol='XBTUSD', price=pr, orderQty=20, id_level=idl)])
        # print(k.keep)
        # simlulate process ack
        # now we use dict, not list so I need to retrieve the key
        cl_k1 = list(k.keep.keys())[0]
        ack1 = [{'orderID': '12345',
                 'clOrdID': cl_k1,  # order in list
                 'clOrdLinkID': '',
                 'account': 115737,
                 'symbol': 'XBTUSD',
                 'side': 'Buy',
                 'simpleOrderQty': None,
                 'orderQty': 20,
                 'price': 3903.5,
                 'displayQty': None,
                 'stopPx': None,
                 'pegOffsetValue': None,
                 'pegPriceType': '',
                 'currency': 'USD',
                 'settlCurrency': 'XBt',
                 'ordType': 'Limit',
                 'timeInForce': 'GoodTillCancel',
                 'execInst': '',
                 'contingencyType': '',
                 'exDestination': 'XBME',
                 'ordStatus': 'New',
                 'triggered': '',
                 'workingIndicator': True,
                 'ordRejReason': '',
                 'simpleLeavesQty': None,
                 'leavesQty': 10,
                 'simpleCumQty': None,
                 'cumQty': 0,
                 'avgPx': None,
                 'multiLegReportingType': 'SingleSecurity',
                 'text': 'Submitted via API.',
                 'transactTime': dtnow(),
                 'timestamp': dtnow()}]

        k.ack_update(ack1)
        # assert status orderID and ts
        # print(k.ord_report(['orderID', 'status', 'ts']))
        # print(k.keep[0])
        self.assertEqual(k.keep[cl_k1].status, 'processed')
        self.assertIsNotNone(k.keep[cl_k1].ts)
        self.assertIsNotNone(k.keep[cl_k1].orderID)
        print('timestamp')
        print(k.keep[cl_k1].orderID)
        self.assertIsNotNone(k.keep[cl_k1].orderID)

        # size updates
        sz1 = {'table': 'orderBookL2_25', 'action': 'update',
               'data': [{'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 279, 'price': 3903.5}]}
        ob.getmsg(sz1)
        print(k.ord_report(['status', 'size_before', 'size_after', 'saw_myself', 'id_level']))
        self.assertEqual(k.keep[cl_k1].status, 'on_ladder')
        sz2 = {'table': 'orderBookL2_25', 'action': 'update',
               'data': [{'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 299, 'price': 3903.5}]}
        ob.getmsg(sz2)
        self.assertEqual(k.keep[cl_k1].size_after, 20)

        # now we put and order with no id level

        k.add_order([dict(symbol='XBTUSD', price=3903, orderQty=30)])
        # ok now I need to retrieve the order key
        cl_k2 = [x for x in k.keep.keys() if x != cl_k1][0]
        self.assertEqual(k.keep[cl_k2].status, 'new')
        # faking ack
        k.keep[cl_k2].status = 'processed'
        k.get_id_lvl = ob.get_id
        k.id_level_update()
        self.assertEqual(k.keep[cl_k2].status, 'on_ladder')

        # now we put and order with no id level but we registed the proper method for keep
        k.get_id_lvl = ob.get_id
        print(k.get_id_lvl(3898, with_size=False))
        k.add_order([dict(symbol='XBTUSD', price=3898, orderQty=27)])
        print(k.ord_report(['orderQty', 'status', 'id_level']))
        cl_k3 = [x for x in k.keep.keys() if x not in [cl_k2, cl_k1]][0]
        self.assertEqual(k.keep[cl_k3].status, 'new')
        self.assertEqual(k.keep[cl_k3].id_level, 15599610200)

    def test_process_ws_ack(self):
        k = OrderKeep()

        part_ws_order2 = {'table': 'order', 'action': 'partial', 'keys': ['orderID'],
                          'types': {'orderID': 'guid', 'clOrdID': 'symbol', 'clOrdLinkID': 'symbol', 'account': 'long',
                                    'symbol': 'symbol', 'side': 'symbol', 'simpleOrderQty': 'float', 'orderQty': 'long',
                                    'price': 'float', 'displayQty': 'long', 'stopPx': 'float',
                                    'pegOffsetValue': 'float', 'pegPriceType': 'symbol', 'currency': 'symbol',
                                    'settlCurrency': 'symbol', 'ordType': 'symbol', 'timeInForce': 'symbol',
                                    'execInst': 'symbol', 'contingencyType': 'symbol', 'exDestination': 'symbol',
                                    'ordStatus': 'symbol', 'triggered': 'symbol', 'workingIndicator': 'boolean',
                                    'ordRejReason': 'symbol', 'simpleLeavesQty': 'float', 'leavesQty': 'long',
                                    'simpleCumQty': 'float', 'cumQty': 'long', 'avgPx': 'float',
                                    'multiLegReportingType': 'symbol', 'text': 'symbol', 'transactTime': 'timestamp',
                                    'timestamp': 'timestamp'},
                          'foreignKeys': {'symbol': 'instrument', 'side': 'side', 'ordStatus': 'ordStatus'},
                          'attributes': {'orderID': 'grouped', 'account': 'grouped', 'ordStatus': 'grouped',
                                         'workingIndicator': 'grouped'},
                          'filter': {'account': 159999, 'symbol': 'XBTUSD'}, 'data': [
                {'orderID': '53d19e5f-2626-eb6a-5e89-5340daab5b4e', 'clOrdID': 'xxx', 'clOrdLinkID': '',
                 'account': 159999,
                 'symbol': 'XBTUSD', 'side': 'Sell', 'simpleOrderQty': None, 'orderQty': 60, 'price': 3317,
                 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None, 'pegPriceType': '', 'currency': 'USD',
                 'settlCurrency': 'XBt', 'ordType': 'Limit', 'timeInForce': 'GoodTillCancel', 'execInst': '',
                 'contingencyType': '', 'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '',
                 'workingIndicator': True, 'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60,
                 'simpleCumQty': None, 'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                 'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-07T07:41:36.752Z',
                 'timestamp': '2018-12-07T07:41:36.752Z'},
                {'orderID': '0ed240ac-ea94-512c-d1be-641e36f004d0', 'clOrdID': 'yyy', 'clOrdLinkID': '',
                 'account': 159999,
                 'symbol': 'XBTUSD', 'side': 'Buy', 'simpleOrderQty': None, 'orderQty': 60, 'price': 3306,
                 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None, 'pegPriceType': '', 'currency': 'USD',
                 'settlCurrency': 'XBt', 'ordType': 'Limit', 'timeInForce': 'GoodTillCancel', 'execInst': '',
                 'contingencyType': '', 'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '',
                 'workingIndicator': True, 'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60,
                 'simpleCumQty': None, 'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                 'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-07T07:41:41.667Z',
                 'timestamp': '2018-12-07T07:41:41.667Z'}]}

        print("partial with 2 orders in already")
        k.ws_update(part_ws_order2)
        k.ws_update(part_ws_order2)
        self.assertEqual(len(k.keep), 2)
        self.assertEqual(k.keep['xxx'].price, 3317)
        self.assertEqual(k.keep['xxx'].status, 'processed')
        self.assertEqual(k.keep['xxx'].orderQty, 60)
        self.assertEqual(k.keep['xxx'].clOrdID, 'xxx')
        self.assertEqual(k.keep['xxx'].orderID, '53d19e5f-2626-eb6a-5e89-5340daab5b4e')
        self.assertEqual(k.keep['yyy'].price, 3306)
        self.assertEqual(k.keep['yyy'].status, 'processed')
        self.assertEqual(k.keep['yyy'].orderQty, 60)
        self.assertEqual(k.keep['yyy'].clOrdID, 'yyy')
        self.assertEqual(k.keep['yyy'].orderID, '0ed240ac-ea94-512c-d1be-641e36f004d0')
        # reset
        k.keep = dict()

        part_w_orders = {'table': 'order', 'action': 'partial', 'keys': ['orderID'],
                         'types': {'orderID': 'guid', 'clOrdID': 'symbol', 'clOrdLinkID': 'symbol', 'account': 'long',
                                   'symbol': 'symbol', 'side': 'symbol', 'simpleOrderQty': 'float', 'orderQty': 'long',
                                   'price': 'float', 'displayQty': 'long', 'stopPx': 'float', 'pegOffsetValue': 'float',
                                   'pegPriceType': 'symbol', 'currency': 'symbol', 'settlCurrency': 'symbol',
                                   'ordType': 'symbol', 'timeInForce': 'symbol', 'execInst': 'symbol',
                                   'contingencyType': 'symbol', 'exDestination': 'symbol', 'ordStatus': 'symbol',
                                   'triggered': 'symbol', 'workingIndicator': 'boolean', 'ordRejReason': 'symbol',
                                   'simpleLeavesQty': 'float', 'leavesQty': 'long', 'simpleCumQty': 'float',
                                   'cumQty': 'long', 'avgPx': 'float', 'multiLegReportingType': 'symbol',
                                   'text': 'symbol', 'transactTime': 'timestamp', 'timestamp': 'timestamp'},
                         'foreignKeys': {'symbol': 'instrument', 'side': 'side', 'ordStatus': 'ordStatus'},
                         'attributes': {'orderID': 'grouped', 'account': 'grouped', 'ordStatus': 'grouped',
                                        'workingIndicator': 'grouped'},
                         'filter': {'account': 159999, 'symbol': 'XBTUSD'},
                         'data': []}
        print("partial")
        k.ws_update(part_w_orders)
        k.add_order([dict(symbol='XBTUSD', price=3725, orderQty=60)])
        # now we use dict, not list so I need to retrieve the key
        cl_k1 = list(k.keep.keys())[0]
        # force clOrdID and status
        k.keep[cl_k1].status = 'processed'
        # k.keep[cl_k1].clOrdID = 'xxx'

        part_ws_order2 = {'table': 'order', 'action': 'partial', 'keys': ['orderID'],
                          'types': {'orderID': 'guid', 'clOrdID': 'symbol', 'clOrdLinkID': 'symbol', 'account': 'long',
                                    'symbol': 'symbol', 'side': 'symbol', 'simpleOrderQty': 'float', 'orderQty': 'long',
                                    'price': 'float', 'displayQty': 'long', 'stopPx': 'float',
                                    'pegOffsetValue': 'float', 'pegPriceType': 'symbol', 'currency': 'symbol',
                                    'settlCurrency': 'symbol', 'ordType': 'symbol', 'timeInForce': 'symbol',
                                    'execInst': 'symbol', 'contingencyType': 'symbol', 'exDestination': 'symbol',
                                    'ordStatus': 'symbol', 'triggered': 'symbol', 'workingIndicator': 'boolean',
                                    'ordRejReason': 'symbol', 'simpleLeavesQty': 'float', 'leavesQty': 'long',
                                    'simpleCumQty': 'float', 'cumQty': 'long', 'avgPx': 'float',
                                    'multiLegReportingType': 'symbol', 'text': 'symbol', 'transactTime': 'timestamp',
                                    'timestamp': 'timestamp'},
                          'foreignKeys': {'symbol': 'instrument', 'side': 'side', 'ordStatus': 'ordStatus'},
                          'attributes': {'orderID': 'grouped', 'account': 'grouped', 'ordStatus': 'grouped',
                                         'workingIndicator': 'grouped'},
                          'filter': {'account': 159999, 'symbol': 'XBTUSD'}, 'data': [
                {'orderID': '53d19e5f-2626-eb6a-5e89-5340daab5b4e', 'clOrdID': '', 'clOrdLinkID': '', 'account': 159999,
                 'symbol': 'XBTUSD', 'side': 'Sell', 'simpleOrderQty': None, 'orderQty': 60, 'price': 3317,
                 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None, 'pegPriceType': '', 'currency': 'USD',
                 'settlCurrency': 'XBt', 'ordType': 'Limit', 'timeInForce': 'GoodTillCancel', 'execInst': '',
                 'contingencyType': '', 'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '',
                 'workingIndicator': True, 'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60,
                 'simpleCumQty': None, 'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                 'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-07T07:41:36.752Z',
                 'timestamp': '2018-12-07T07:41:36.752Z'},
                {'orderID': '0ed240ac-ea94-512c-d1be-641e36f004d0', 'clOrdID': '', 'clOrdLinkID': '', 'account': 159999,
                 'symbol': 'XBTUSD', 'side': 'Buy', 'simpleOrderQty': None, 'orderQty': 60, 'price': 3306,
                 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None, 'pegPriceType': '', 'currency': 'USD',
                 'settlCurrency': 'XBt', 'ordType': 'Limit', 'timeInForce': 'GoodTillCancel', 'execInst': '',
                 'contingencyType': '', 'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '',
                 'workingIndicator': True, 'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60,
                 'simpleCumQty': None, 'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                 'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-07T07:41:41.667Z',
                 'timestamp': '2018-12-07T07:41:41.667Z'}]}

        ws1 = {'table': 'order', 'action': 'insert', 'data': [
            {'orderID': '8f05b332-7ae8-8097-a603-1940bac7b7af', 'clOrdID': cl_k1, 'clOrdLinkID': '',
             'account': 159999, 'symbol': 'XBTUSD', 'side': 'Sell', 'simpleOrderQty': None, 'orderQty': 60,
             'price': 3725, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None, 'pegPriceType': '',
             'currency': 'USD', 'settlCurrency': 'XBt', 'ordType': 'Limit', 'timeInForce': 'GoodTillCancel',
             'execInst': '', 'contingencyType': '', 'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '',
             'workingIndicator': False, 'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 10,
             'simpleCumQty': None, 'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
             'text': 'Submitted via API.', 'transactTime': '2018-12-06T07:56:00.689Z',
             'timestamp': '2018-12-06T07:56:00.689Z'}]}

        k.ws_update(ws1)
        print("first message")
        ws2 = {'table': 'order', 'action': 'update', 'data': [
            {'orderID': '8f05b332-7ae8-8097-a603-1940bac7b7af', 'workingIndicator': True, 'clOrdID': cl_k1,
             'account': 159999, 'symbol': 'XBTUSD', 'timestamp': '2018-12-06T07:56:00.689Z'}]}
        k.ws_update(ws2)
        self.assertEqual(k.keep[cl_k1].ws_working, True)
        print("fill message")
        ws_fil = {'table': 'order', 'action': 'update', 'data': [
            {'orderID': '8f05b332-7ae8-8097-a603-1940bac7b7af', 'ordStatus': 'Filled', 'workingIndicator': False,
             'leavesQty': 0, 'cumQty': 60, 'avgPx': 3720, 'clOrdID': cl_k1, 'account': 159999, 'symbol': 'XBTUSD',
             'timestamp': '2018-12-06T07:53:42.945Z'}]}

        k.ws_update(ws_fil)
        self.assertNotEqual(k.transactions, [])
        self.assertEqual(len(k.keep), 0)

        # now the same with a cancel at the end
        k.transactions = []
        k.add_order([dict(symbol='XBTUSD', price=3725, orderQty=60)])
        # now we use dict, not list so I need to retrieve the key
        cl_k2 = list(k.keep.keys())[0]
        # force clOrdID and status

        k.keep[cl_k2].status = 'processed'
        k.keep[cl_k2].clOrdID = cl_k2

        ws1 = {'table': 'order', 'action': 'insert', 'data': [
            {'orderID': '8f05b332-7ae8-8097-a603-1940bac7b7af', 'clOrdID': cl_k2, 'clOrdLinkID': '',
             'account': 159999, 'symbol': 'XBTUSD', 'side': 'Sell', 'simpleOrderQty': None, 'orderQty': 60,
             'price': 3725, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None, 'pegPriceType': '',
             'currency': 'USD', 'settlCurrency': 'XBt', 'ordType': 'Limit', 'timeInForce': 'GoodTillCancel',
             'execInst': '', 'contingencyType': '', 'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '',
             'workingIndicator': False, 'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 10,
             'simpleCumQty': None, 'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
             'text': 'Submitted via API.', 'transactTime': '2018-12-06T07:56:00.689Z',
             'timestamp': '2018-12-06T07:56:00.689Z'}]}

        k.ws_update(ws1)

        ws2 = {'table': 'order', 'action': 'update', 'data': [
            {'orderID': '8f05b332-7ae8-8097-a603-1940bac7b7af', 'workingIndicator': True, 'clOrdID': cl_k2,
             'account': 159999, 'symbol': 'XBTUSD', 'timestamp': '2018-12-06T07:56:00.689Z'}]}
        k.ws_update(ws2)
        self.assertEqual(k.keep[cl_k2].ws_working, True)
        print(k.ord_report())
        print("cancel message")
        ws_cnc = {'table': 'order', 'action': 'update', 'data': [
            {'orderID': '8f05b332-7ae8-8097-a603-1940bac7b7af', 'ordStatus': 'Canceled', 'workingIndicator': False,
             'leavesQty': 0, 'text': 'Canceled: Canceled via API.\nSubmitted via API.',
             'timestamp': '2018-12-06T07:56:21.455Z', 'clOrdID': cl_k2, 'account': 159999,
             'symbol': 'XBTUSD'}]}
        k.ws_update(ws_cnc)
        self.assertEqual(k.transactions, [])
        print(k.ord_report())
        self.assertEqual(len(k.keep), 0)

    def test_sync_orders(self):
        k = OrderKeep()
        k.add_order([dict(symbol='XBTUSD', price=3725, orderQty=60)])
        # force clOrdID
        k.keep['xxx'] = list(k.keep.values())[0]
        k.keep['xxx'].clOrdID = "xxx"
        partial = {'table': 'order', 'action': 'partial', 'keys': ['orderID'],
                   'types': {'orderID': 'guid', 'clOrdID': 'symbol', 'clOrdLinkID': 'symbol', 'account': 'long',
                             'symbol': 'symbol', 'side': 'symbol', 'simpleOrderQty': 'float', 'orderQty': 'long',
                             'price': 'float', 'displayQty': 'long', 'stopPx': 'float', 'pegOffsetValue': 'float',
                             'pegPriceType': 'symbol', 'currency': 'symbol', 'settlCurrency': 'symbol',
                             'ordType': 'symbol', 'timeInForce': 'symbol', 'execInst': 'symbol',
                             'contingencyType': 'symbol', 'exDestination': 'symbol', 'ordStatus': 'symbol',
                             'triggered': 'symbol', 'workingIndicator': 'boolean', 'ordRejReason': 'symbol',
                             'simpleLeavesQty': 'float', 'leavesQty': 'long', 'simpleCumQty': 'float', 'cumQty': 'long',
                             'avgPx': 'float', 'multiLegReportingType': 'symbol', 'text': 'symbol',
                             'transactTime': 'timestamp', 'timestamp': 'timestamp'},
                   'foreignKeys': {'symbol': 'instrument', 'side': 'side', 'ordStatus': 'ordStatus'},
                   'attributes': {'orderID': 'grouped', 'account': 'grouped', 'ordStatus': 'grouped',
                                  'workingIndicator': 'grouped'},
                   'filter': {'account': 159999, 'symbol': 'XBTUSD'},
                   'data': [{'orderID': '258fd85c-6eee-19e6-b0bd-a0a47ca86c07', 'clOrdID': 'xxx', 'clOrdLinkID': '',
                             'account': 159999, 'symbol': 'XBTUSD', 'side': 'Buy', 'simpleOrderQty': None,
                             'orderQty': 60, 'price': 3725, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None,
                             'pegPriceType': '', 'currency': 'USD', 'settlCurrency': 'XBt', 'ordType': 'Limit',
                             'timeInForce': 'GoodTillCancel', 'execInst': '', 'contingencyType': '',
                             'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '', 'workingIndicator': True,
                             'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60, 'simpleCumQty': None,
                             'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                             'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-06T09:22:07.709Z',
                             'timestamp': '2018-12-06T09:22:07.709Z'},
                            {'orderID': 'e2c154c8-a96f-67c0-1050-404bab83c949', 'clOrdID': 'yyy', 'clOrdLinkID': '',
                             'account': 159999, 'symbol': 'XBTUSD', 'side': 'Sell', 'simpleOrderQty': None,
                             'orderQty': 60, 'price': 3784, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None,
                             'pegPriceType': '', 'currency': 'USD', 'settlCurrency': 'XBt', 'ordType': 'Limit',
                             'timeInForce': 'GoodTillCancel', 'execInst': '', 'contingencyType': '',
                             'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '', 'workingIndicator': True,
                             'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60, 'simpleCumQty': None,
                             'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                             'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-06T10:00:56.419Z',
                             'timestamp': '2018-12-06T10:00:56.419Z'}]}

        print("process partial")
        k.ws_update(partial)
        print(k.ord_report(['price', 'clOrdID', 'orderQty']))
        self.assertEqual(len(k.keep), 2)
        # self.assertEqual([x.price for x in k.keep], [3725, 3784])
        # self.assertEqual([x.orderQty for x in k.keep], [60, 60])
        self.assertEqual(k.keep['xxx'].status, 'processed')
        self.assertEqual(k.keep['xxx'].price, 3725)
        self.assertEqual(k.keep['xxx'].orderQty, 60)
        self.assertEqual(k.keep['yyy'].status, 'processed')
        self.assertEqual(k.keep['yyy'].price, 3784)
        self.assertEqual(k.keep['yyy'].orderQty, 60)
        # now we test change of qty
        # we need to change the clOrdID of order 2 in the partial

        partial2 = {'table': 'order', 'action': 'partial', 'keys': ['orderID'],
                    'types': {'orderID': 'guid', 'clOrdID': 'symbol', 'clOrdLinkID': 'symbol', 'account': 'long',
                              'symbol': 'symbol', 'side': 'symbol', 'simpleOrderQty': 'float', 'orderQty': 'long',
                              'price': 'float', 'displayQty': 'long', 'stopPx': 'float', 'pegOffsetValue': 'float',
                              'pegPriceType': 'symbol', 'currency': 'symbol', 'settlCurrency': 'symbol',
                              'ordType': 'symbol', 'timeInForce': 'symbol', 'execInst': 'symbol',
                              'contingencyType': 'symbol', 'exDestination': 'symbol', 'ordStatus': 'symbol',
                              'triggered': 'symbol', 'workingIndicator': 'boolean', 'ordRejReason': 'symbol',
                              'simpleLeavesQty': 'float', 'leavesQty': 'long', 'simpleCumQty': 'float',
                              'cumQty': 'long',
                              'avgPx': 'float', 'multiLegReportingType': 'symbol', 'text': 'symbol',
                              'transactTime': 'timestamp', 'timestamp': 'timestamp'},
                    'foreignKeys': {'symbol': 'instrument', 'side': 'side', 'ordStatus': 'ordStatus'},
                    'attributes': {'orderID': 'grouped', 'account': 'grouped', 'ordStatus': 'grouped',
                                   'workingIndicator': 'grouped'},
                    'filter': {'account': 159999, 'symbol': 'XBTUSD'},
                    'data': [{'orderID': '258fd85c-6eee-19e6-b0bd-a0a47ca86c07', 'clOrdID': 'xxx', 'clOrdLinkID': '',
                              'account': 159999, 'symbol': 'XBTUSD', 'side': 'Buy', 'simpleOrderQty': None,
                              'orderQty': 60, 'price': 3725, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None,
                              'pegPriceType': '', 'currency': 'USD', 'settlCurrency': 'XBt', 'ordType': 'Limit',
                              'timeInForce': 'GoodTillCancel', 'execInst': '', 'contingencyType': '',
                              'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '', 'workingIndicator': True,
                              'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60, 'simpleCumQty': None,
                              'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                              'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-06T09:22:07.709Z',
                              'timestamp': '2018-12-06T09:22:07.709Z'},
                             {'orderID': 'e2c154c8-a96f-67c0-1050-404bab83c949', 'clOrdID': 'yyy', 'clOrdLinkID': '',
                              # <- thats where the magic happens
                              'account': 159999, 'symbol': 'XBTUSD', 'side': 'Sell', 'simpleOrderQty': None,
                              'orderQty': 60, 'price': 3784, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None,
                              'pegPriceType': '', 'currency': 'USD', 'settlCurrency': 'XBt', 'ordType': 'Limit',
                              'timeInForce': 'GoodTillCancel', 'execInst': '', 'contingencyType': '',
                              'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '', 'workingIndicator': True,
                              'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60, 'simpleCumQty': None,
                              'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                              'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-06T10:00:56.419Z',
                              'timestamp': '2018-12-06T10:00:56.419Z'}]}

        print("process partial")
        k.ws_update(partial)
        print(k.ord_report(['price', 'clOrdID', 'orderQty']))
        self.assertEqual(len(k.keep), 2)
        self.assertEqual([x.price for x in k.keep], [3725, 3784])
        self.assertEqual([x.orderQty for x in k.keep], [60, 60])
        self.assertEqual(k.keep[0].status, 'processed')
        self.assertEqual(k.keep[1].status, 'processed')
        # now we test change of qty
        # we need to change the clOrdID of order 2 in the partial

        partial2 = {'table': 'order', 'action': 'partial', 'keys': ['orderID'],
                    'types': {'orderID': 'guid', 'clOrdID': 'symbol', 'clOrdLinkID': 'symbol', 'account': 'long',
                              'symbol': 'symbol', 'side': 'symbol', 'simpleOrderQty': 'float', 'orderQty': 'long',
                              'price': 'float', 'displayQty': 'long', 'stopPx': 'float', 'pegOffsetValue': 'float',
                              'pegPriceType': 'symbol', 'currency': 'symbol', 'settlCurrency': 'symbol',
                              'ordType': 'symbol', 'timeInForce': 'symbol', 'execInst': 'symbol',
                              'contingencyType': 'symbol', 'exDestination': 'symbol', 'ordStatus': 'symbol',
                              'triggered': 'symbol', 'workingIndicator': 'boolean', 'ordRejReason': 'symbol',
                              'simpleLeavesQty': 'float', 'leavesQty': 'long', 'simpleCumQty': 'float',
                              'cumQty': 'long',
                              'avgPx': 'float', 'multiLegReportingType': 'symbol', 'text': 'symbol',
                              'transactTime': 'timestamp', 'timestamp': 'timestamp'},
                    'foreignKeys': {'symbol': 'instrument', 'side': 'side', 'ordStatus': 'ordStatus'},
                    'attributes': {'orderID': 'grouped', 'account': 'grouped', 'ordStatus': 'grouped',
                                   'workingIndicator': 'grouped'},
                    'filter': {'account': 159999, 'symbol': 'XBTUSD'},
                    'data': [{'orderID': '258fd85c-6eee-19e6-b0bd-a0a47ca86c07', 'clOrdID': 'xxx', 'clOrdLinkID': '',
                              'account': 159999, 'symbol': 'XBTUSD', 'side': 'Buy', 'simpleOrderQty': None,
                              'orderQty': 50, 'price': 3725, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None,
                              'pegPriceType': '', 'currency': 'USD', 'settlCurrency': 'XBt', 'ordType': 'Limit',
                              'timeInForce': 'GoodTillCancel', 'execInst': '', 'contingencyType': '',
                              'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '', 'workingIndicator': True,
                              'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60, 'simpleCumQty': None,
                              'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                              'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-06T09:22:07.709Z',
                              'timestamp': '2018-12-06T09:22:07.709Z'},
                             {'orderID': 'e2c154c8-a96f-67c0-1050-404bab83c949', 'clOrdID': k.keep[1].clOrdID,
                              'clOrdLinkID': '',
                              # <- thats where the magic happens
                              'account': 159999, 'symbol': 'XBTUSD', 'side': 'Sell', 'simpleOrderQty': None,
                              'orderQty': 60, 'price': 3784, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None,
                              'pegPriceType': '', 'currency': 'USD', 'settlCurrency': 'XBt', 'ordType': 'Limit',
                              'timeInForce': 'GoodTillCancel', 'execInst': '', 'contingencyType': '',
                              'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '', 'workingIndicator': True,
                              'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60, 'simpleCumQty': None,
                              'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                              'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-06T10:00:56.419Z',
                              'timestamp': '2018-12-06T10:00:56.419Z'}]}

        print("process ack 2 (change of size/partial fills")
        k.ws_update(partial2)
        print(k.ord_report(['price', 'clOrdID', 'orderQty']))
        self.assertEqual(len(k.keep), 2)
        self.assertEqual(k.keep['xxx'].status, 'processed')
        self.assertEqual(k.keep['xxx'].price, 3725)
        self.assertEqual(k.keep['xxx'].orderQty, 50)
        self.assertEqual(k.keep['yyy'].status, 'processed')
        self.assertEqual(k.keep['yyy'].price, 3784)
        self.assertEqual(k.keep['yyy'].orderQty, 60)

        partial3 = {'table': 'order', 'action': 'partial', 'keys': ['orderID'],
                    'types': {'orderID': 'guid', 'clOrdID': 'symbol', 'clOrdLinkID': 'symbol', 'account': 'long',
                              'symbol': 'symbol', 'side': 'symbol', 'simpleOrderQty': 'float', 'orderQty': 'long',
                              'price': 'float', 'displayQty': 'long', 'stopPx': 'float', 'pegOffsetValue': 'float',
                              'pegPriceType': 'symbol', 'currency': 'symbol', 'settlCurrency': 'symbol',
                              'ordType': 'symbol', 'timeInForce': 'symbol', 'execInst': 'symbol',
                              'contingencyType': 'symbol', 'exDestination': 'symbol', 'ordStatus': 'symbol',
                              'triggered': 'symbol', 'workingIndicator': 'boolean', 'ordRejReason': 'symbol',
                              'simpleLeavesQty': 'float', 'leavesQty': 'long', 'simpleCumQty': 'float',
                              'cumQty': 'long',
                              'avgPx': 'float', 'multiLegReportingType': 'symbol', 'text': 'symbol',
                              'transactTime': 'timestamp', 'timestamp': 'timestamp'},
                    'foreignKeys': {'symbol': 'instrument', 'side': 'side', 'ordStatus': 'ordStatus'},
                    'attributes': {'orderID': 'grouped', 'account': 'grouped', 'ordStatus': 'grouped',
                                   'workingIndicator': 'grouped'},
                    'filter': {'account': 159999, 'symbol': 'XBTUSD'},
                    'data': [{'orderID': '258fd85c-6eee-19e6-b0bd-a0a47ca86c07', 'clOrdID': 'xxx', 'clOrdLinkID': '',
                              'account': 159999, 'symbol': 'XBTUSD', 'side': 'Buy', 'simpleOrderQty': None,
                              'orderQty': 50, 'price': 3725, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None,
                              'pegPriceType': '', 'currency': 'USD', 'settlCurrency': 'XBt', 'ordType': 'Limit',
                              'timeInForce': 'GoodTillCancel', 'execInst': '', 'contingencyType': '',
                              'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '', 'workingIndicator': True,
                              'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 60, 'simpleCumQty': None,
                              'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity',
                              'text': 'Submission from testnet.bitmex.com', 'transactTime': '2018-12-06T09:22:07.709Z',
                              'timestamp': '2018-12-06T09:22:07.709Z'}]}

        print("process ack 3 (remove one order")
        k.ws_update(partial3)
        print(k.ord_report(['price', 'clOrdID', 'orderQty']))
        self.assertEqual(len(k.keep), 1)

    def test_agent_fun(self):

        k = OrderKeep()
        ord1 = dict(symbol='XBTUSD', price=4200, orderQty=-10)
        ord2 = dict(symbol='XBTUSD', price=3600, orderQty=11, execInst="ParticipateDoNotInitiate")
        ord3 = dict(symbol='XBTUSD', price=3500, orderQty=13)

        ords = [ord1, ord2, ord3]
        # init test
        print("init test")
        self.assertEqual(k.keep, dict())
        k.add_order(ords)
        # get the clOrdIDs
        cl_k1 = [k for k, v in k.keep.items() if v.price == 4200][0]
        cl_k2 = [k for k, v in k.keep.items() if v.price == 3600][0]
        cl_k3 = [k for k, v in k.keep.items() if v.price == 3500][0]

        # put size_before, after and time
        k.keep[cl_k1].ts = dtnow()
        k.keep[cl_k1].size_before = 1000
        k.keep[cl_k1].size_after = 500
        k.keep[cl_k1].status = 'on_ladder'
        k.keep[cl_k2].ts = dtnow()
        k.keep[cl_k2].size_before = None
        k.keep[cl_k2].size_after = None
        k.keep[cl_k2].status = 'on_ladder'
        sleep(0.1)
        k.keep[cl_k3].ts = dtnow()
        k.keep[cl_k3].size_before = 500
        k.keep[cl_k3].size_after = 300
        k.keep[cl_k3].status = 'on_ladder'
        print(k.exec_report())






class TestBitmexInterface(TestCase):

    def test_execute(self):
        """
        this will focus on inputs adjustments from a target input, not on execution or enrichment
        :return:
        """
        k = OrderKeep()

        mk1 = [dict(symbol='XBTUSD',
                    price=2000,
                    orderQty=27,
                    ordType="Market"),
               dict(symbol='XBTUSD',
                    ordType="Limit",
                    orderQty=-29,
                    price=5000)]

        k.execute_target(mk1)
        print(k.ord_report())
        k.execute_target(mk1)
        print("are we idempotent ?")
        # assume orders have been processed by first pass
        # we get clOrdID from dict keys now
        clOrdID1 = [k for k, v in k.keep.items() if v.orderQty == 27][0]
        clOrdID2 = [k for k, v in k.keep.items() if v.orderQty == -29][0]

        k.keep[clOrdID1].status = 'processed'
        k.keep[clOrdID2].status = 'processed'
        print(k.ord_report())
        self.assertEqual(len(k.keep), 2)
        self.assertEqual(k.keep[clOrdID1].status, 'processed')
        self.assertEqual(k.keep[clOrdID2].status, 'processed')

        print("another limit order in")
        # we repeat the same market order the limit order, and add another limit order
        mk2 = [dict(symbol='XBTUSD',
                    price=2000,
                    orderQty=27,
                    ordType="Market"),
               dict(symbol='XBTUSD',
                    ordType="Limit",
                    orderQty=-29,
                    price=5000),
               dict(symbol='XBTUSD',
                    ordType="Limit",
                    orderQty=-32,
                    price=5500)
               ]
        k.execute_target(mk2)
        print(k.ord_report())
        # find the third key
        clOrdID3 = [x for x in k.keep.keys() if x not in [clOrdID1, clOrdID2]][0]
        self.assertEqual(len(k.keep), 3)
        self.assertEqual(k.keep[clOrdID1].status, 'processed')
        self.assertEqual(k.keep[clOrdID2].status, 'processed')
        self.assertEqual(k.keep[clOrdID3].status, 'new')

        # we change status of orders to processed or on_ladder for  the limit orders and we update the price of one

        k.keep[clOrdID2].status = "on_ladder"
        mk3 = [dict(symbol='XBTUSD',
                    price=2000,
                    orderQty=27,
                    ordType="Market"),
               dict(symbol='XBTUSD',
                    ordType="Limit",
                    orderQty=-29,
                    price=5000),
               dict(symbol='XBTUSD',
                    ordType="Limit",
                    orderQty=-32,
                    price=6000)]
        print("we change one limit order")
        k.execute_target(mk3)
        print(k.ord_report())
        self.assertEqual(len(k.keep), 3)

        self.assertEqual(k.keep[clOrdID3].price, 6000)
        self.assertEqual(k.keep[clOrdID3].status, 'amend')

        # we remove a limit order
        mk4 = [dict(symbol='XBTUSD',
                    price=2000,
                    orderQty=27,
                    ordType="Market"),

               dict(symbol='XBTUSD',
                    ordType="Limit",
                    orderQty=-32,
                    price=6000)]
        print("we remove one limit order")
        k.execute_target(mk4)
        print(k.ord_report())
        self.assertEqual(len(k.keep), 3)
        self.assertEqual(k.keep[clOrdID3].status, 'amend')
        self.assertEqual(k.keep[clOrdID2].status, 'canceled')

    def test_put_amend_cancel(self):
        ex = BitmexInterface(apiKey='va6avtLnBcgkGu4ZRwYyADpj',
                             apiSecret='Mm5oZNpfbHnrxbNk6OCDJdw4whk-cOmkjcf_GL9CXPr3YmPO',
                             endpoint='wss://testnet.bitmex.com/realtime',
                             test=True,
                             min_remain=30)
        k = OrderKeep(bulk_put=ex.put_orders, bulk_amend=ex.amend_orders, bulk_cancel=ex.cancel_orders)

        k.execute_target([dict(symbol='XBTUSD', price=2000, orderQty=27),
                          dict(symbol='XBTUSD', price=6000, orderQty=-29)])  # wide and easy
        # k.put()
        self.assertEqual(k.ord_report(['status']), [{'status': 'processed'}, {'status': 'processed'}])
        print(k.ord_report(['symbol', 'status', 'orderQty', 'ordType', 'price', 'clOrdID', 'orderID']))
        print("we change one order")
        k.execute_target(
            [dict(symbol='XBTUSD', price=1500, orderQty=27), dict(symbol='XBTUSD', price=6000, orderQty=-29)])
        print(k.ord_report(['symbol', 'status', 'orderQty', 'ordType', 'price', 'clOrdID', 'orderID']))


### this needs to be tested
# from utilities import avg_price_inv
# import datetime
# from dateutil.tz import tzutc
#
# transactions = [{'ts': datetime.datetime(2018, 12, 11, 6, 50, 30, 681000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 52, 25, 146000), 'symbol': 'XBTUSD', 'price': 3377.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 50, 30, 681000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 54, 21, 246000), 'symbol': 'XBTUSD', 'price': 3376, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 54, 22, 647000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 54, 33, 585000), 'symbol': 'XBTUSD', 'price': 3376, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 54, 24, 892000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 54, 42, 340000), 'symbol': 'XBTUSD', 'price': 3376.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 54, 34, 10000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 54, 42, 340000), 'symbol': 'XBTUSD', 'price': 3376, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 54, 43, 543000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 54, 44, 442000), 'symbol': 'XBTUSD', 'price': 3376.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 54, 54, 6000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 55, 5, 72000), 'symbol': 'XBTUSD', 'price': 3376, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 54, 42, 810000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 55, 5, 72000), 'symbol': 'XBTUSD', 'price': 3375.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 55, 15, 600000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 55, 50, 605000), 'symbol': 'XBTUSD', 'price': 3375.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 55, 6, 431000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 55, 50, 605000), 'symbol': 'XBTUSD', 'price': 3376, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 52, 26, 593000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 56, 6, 542000), 'symbol': 'XBTUSD', 'price': 3377.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 55, 9, 628000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 56, 6, 542000), 'symbol': 'XBTUSD', 'price': 3376.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 54, 44, 964000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 56, 6, 542000), 'symbol': 'XBTUSD', 'price': 3377, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 55, 51, 110000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 56, 6, 542000), 'symbol': 'XBTUSD', 'price': 3376, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 56, 8, 21000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 56, 35, 209000), 'symbol': 'XBTUSD', 'price': 3376, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 56, 8, 21000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 56, 35, 209000), 'symbol': 'XBTUSD', 'price': 3377, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 56, 20, 580000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 56, 35, 209000), 'symbol': 'XBTUSD', 'price': 3376.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 55, 51, 840000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 56, 58, 775000), 'symbol': 'XBTUSD', 'price': 3375.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 56, 59, 209000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 58, 13, 68000), 'symbol': 'XBTUSD', 'price': 3375.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 55, 51, 110000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 59, 25, 656000), 'symbol': 'XBTUSD', 'price': 3375, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 56, 35, 614000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 59, 25, 656000), 'symbol': 'XBTUSD', 'price': 3374.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 6, 59, 27, 114000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 6, 59, 45, 532000), 'symbol': 'XBTUSD', 'price': 3374.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 56, 42, 715000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 0, 17, 9000), 'symbol': 'XBTUSD', 'price': 3376.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 59, 27, 114000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 0, 17, 9000), 'symbol': 'XBTUSD', 'price': 3375, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 56, 43, 117000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 0, 17, 9000), 'symbol': 'XBTUSD', 'price': 3377, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 56, 59, 209000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 0, 17, 9000), 'symbol': 'XBTUSD', 'price': 3376, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 6, 59, 45, 985000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 0, 17, 9000), 'symbol': 'XBTUSD', 'price': 3374.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 0, 18, 414000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 0, 46, 795000), 'symbol': 'XBTUSD', 'price': 3374.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 7, 0, 18, 414000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 0, 46, 795000), 'symbol': 'XBTUSD', 'price': 3376.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 7, 0, 18, 787000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 0, 46, 795000), 'symbol': 'XBTUSD', 'price': 3376, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 7, 0, 28, 906000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 0, 46, 795000), 'symbol': 'XBTUSD', 'price': 3375, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 7, 0, 28, 547000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 0, 46, 795000), 'symbol': 'XBTUSD', 'price': 3375.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 7, 0, 48, 399000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 1, 45, 536000), 'symbol': 'XBTUSD', 'price': 3371, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 1, 46, 26000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 2, 52, 752000), 'symbol': 'XBTUSD', 'price': 3371, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 0, 48, 399000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 3, 9, 719000), 'symbol': 'XBTUSD', 'price': 3371.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 2, 53, 250000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 3, 9, 719000), 'symbol': 'XBTUSD', 'price': 3371, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 3, 12, 21000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 3, 37, 744000), 'symbol': 'XBTUSD', 'price': 3371, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 7, 3, 10, 869000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 3, 37, 744000), 'symbol': 'XBTUSD', 'price': 3371.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 7, 0, 52, 812000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 3, 55, 931000), 'symbol': 'XBTUSD', 'price': 3373, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 3, 41, 811000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 3, 55, 931000), 'symbol': 'XBTUSD', 'price': 3371.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 3, 39, 130000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 3, 55, 931000), 'symbol': 'XBTUSD', 'price': 3371, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 3, 38, 218000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 3, 55, 931000), 'symbol': 'XBTUSD', 'price': 3372, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 3, 38, 218000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 3, 55, 931000), 'symbol': 'XBTUSD', 'price': 3372.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 3, 56, 772000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 3, 57, 703000), 'symbol': 'XBTUSD', 'price': 3376.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 7, 3, 58, 393000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 4, 7, 951000), 'symbol': 'XBTUSD', 'price': 3376.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 7, 4, 8, 502000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 4, 20, 907000), 'symbol': 'XBTUSD', 'price': 3378.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 4, 21, 409000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 4, 25, 657000), 'symbol': 'XBTUSD', 'price': 3381, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 4, 21, 409000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 4, 25, 657000), 'symbol': 'XBTUSD', 'price': 3381.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 4, 21, 409000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 4, 25, 657000), 'symbol': 'XBTUSD', 'price': 3382, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 4, 21, 409000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 4, 25, 657000), 'symbol': 'XBTUSD', 'price': 3382.5, 'orderQty': -10}, {'ts': datetime.datetime(2018, 12, 11, 7, 4, 22, 361000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 6, 52, 825000), 'symbol': 'XBTUSD', 'price': 3378.5, 'orderQty': 10}, {'ts': datetime.datetime(2018, 12, 11, 7, 8, 25, 15000, tzinfo=tzutc()), 'ts_exec': datetime.datetime(2018, 12, 11, 7, 8, 26, 731000), 'symbol': 'XBTUSD', 'price': 3379, 'orderQty': 10}]
#
# print(avg_price_inv('XBTUSD', transactions))