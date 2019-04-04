from unittest import TestCase
from unittest.mock import MagicMock, patch

from .agent import MM
from utilities import findItemByKeys



class MMTest(TestCase):

    def setUp(self):
        self.mm = MM(symbol_list=['TEST'],
                     bbo=MagicMock(),
                     execute=MagicMock(),
                     get_inventory=MagicMock(),
                     get_inv_avg_price=MagicMock(),
                     order_report=MagicMock(),
                     request_trades=MagicMock(),
                     margin_report=MagicMock())

        self.mm.order_report.return_value = [
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3370, 'orderQty': 10, 'side': 'Buy',
             'status': 'on_ladder',
             'size_before': 42718, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3369.5, 'orderQty': 10, 'side': 'Buy',
             'status': 'on_ladder',
             'size_before': 1500, 'size_after': 150},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3369, 'orderQty': 10, 'side': 'Buy',
             'status': 'on_ladder',
             'size_before': 110, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3370.5, 'orderQty': -10, 'side': 'Sell',
             'status': 'on_ladder', 'size_before': 2045, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3371, 'orderQty': -10, 'side': 'Sell',
             'status': 'on_ladder',
             'size_before': 0, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3371.5, 'orderQty': -10, 'side': 'Sell',
             'status': 'on_ladder', 'size_before': 0, 'size_after': 9763280},
            # filter out below
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3390.5, 'orderQty': -10, 'side': 'Sell',
             'status': 'processing', 'size_before': 9763280, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3300.5, 'orderQty': 10, 'side': 'Buy',
             'status': 'new', 'size_before': 0, 'size_after': 0}
        ]

        self.mm.request_trades.return_value = [
            {'timestamp': '2018-12-11T02:42:20.558Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 56, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'a9cab1b4-5d94-a431-b902-320290988322',
             'grossValue': 1661464,
             'homeNotional': 0.01661464, 'foreignNotional': 56},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 50, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '1627361a-387b-9c66-3cdc-c5e4975caede',
             'grossValue': 1483450,
             'homeNotional': 0.0148345, 'foreignNotional': 50},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 100, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'ad756ab6-7e2d-17ef-b2cb-55671e60bcb8',
             'grossValue': 2966900,
             'homeNotional': 0.029669, 'foreignNotional': 100},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 1000, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '527566bf-0630-0b49-19c6-7b9100cba704',
             'grossValue': 29669000, 'homeNotional': 0.29669, 'foreignNotional': 1000},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 10, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '68a6902a-41a8-b077-0488-322f76c706bf',
             'grossValue': 296690,
             'homeNotional': 0.0029669, 'foreignNotional': 10},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 270, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '3bbe15d4-38cb-5e38-bf05-3176813de529',
             'grossValue': 8010630,
             'homeNotional': 0.0801063, 'foreignNotional': 270},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 1346, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'e47f9941-2460-630f-6006-9c246858aacc',
             'grossValue': 39934474, 'homeNotional': 0.39934474, 'foreignNotional': 1346},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 323, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '401260a6-484c-d3b0-838b-6594e37f2c11',
             'grossValue': 9583087,
             'homeNotional': 0.09583087, 'foreignNotional': 323},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 1401, 'price': 3370,
             'tickDirection': 'MinusTick', 'trdMatchID': '412fc21e-70ad-42c7-fadf-6bebc289492f', 'grossValue': 41573274,
             'homeNotional': 0.41573274, 'foreignNotional': 1401},
            {'timestamp': '2018-12-11T02:42:41.670Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 201, 'price': 3371,
             'tickDirection': 'PlusTick', 'trdMatchID': '6fc382cb-518c-dfe9-fd34-43cf9ae36836', 'grossValue': 5962665,
             'homeNotional': 0.05962665, 'foreignNotional': 201}]

    def test_skew_ticks(self):
        # params
        self.mm.skew_levels = [0, 2, None]
        self.min_tick_size = 0.00000001
        self.mm.agent_state = "BID"
        self.max_inventory = 100

        self.mm.get_inventory = 0
        bid_skew, ask_skew = self.mm.skew_ticks()
        self.assertEqual(bid_skew, 0)
        self.assertEqual(ask_skew, 0)

        self.mm.get_inventory = 50
        bid_skew, ask_skew = self.mm.skew_ticks()
        self.assertEqual(bid_skew, 2)
        self.assertEqual(ask_skew, 0)

        self.mm.get_inventory = 90
        bid_skew, ask_skew = self.mm.skew_ticks()
        self.assertEqual(bid_skew, None)
        self.assertEqual(ask_skew, 0)

        self.mm.agent_state = "ASK"

        self.mm.get_inventory = 0
        bid_skew, ask_skew = self.mm.skew_ticks()
        self.assertEqual(bid_skew, 0)
        self.assertEqual(ask_skew, 0)

        self.mm.get_inventory = -50
        bid_skew, ask_skew = self.mm.skew_ticks()
        self.assertEqual(bid_skew, 0)
        self.assertEqual(ask_skew, 2)

        self.mm.get_inventory = -90
        bid_skew, ask_skew = self.mm.skew_ticks()
        self.assertEqual(bid_skew, 0)
        self.assertEqual(ask_skew, None)

    def test_trade_directional_ratio(self):
        ratio = self.mm.trade_directional_ratio(n=10)
        self.assertEqual(ratio, .1)

        self.mm.request_trades.return_value = [
            {'timestamp': '2018-12-11T02:42:20.558Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 56, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'a9cab1b4-5d94-a431-b902-320290988322',
             'grossValue': 1661464,
             'homeNotional': 0.01661464, 'foreignNotional': 56},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 50, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '1627361a-387b-9c66-3cdc-c5e4975caede',
             'grossValue': 1483450,
             'homeNotional': 0.0148345, 'foreignNotional': 50},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 100, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'ad756ab6-7e2d-17ef-b2cb-55671e60bcb8',
             'grossValue': 2966900,
             'homeNotional': 0.029669, 'foreignNotional': 100},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 1000, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '527566bf-0630-0b49-19c6-7b9100cba704',
             'grossValue': 29669000, 'homeNotional': 0.29669, 'foreignNotional': 1000},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 10, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '68a6902a-41a8-b077-0488-322f76c706bf',
             'grossValue': 296690,
             'homeNotional': 0.0029669, 'foreignNotional': 10},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 270, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '3bbe15d4-38cb-5e38-bf05-3176813de529',
             'grossValue': 8010630,
             'homeNotional': 0.0801063, 'foreignNotional': 270},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 1346, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'e47f9941-2460-630f-6006-9c246858aacc',
             'grossValue': 39934474, 'homeNotional': 0.39934474, 'foreignNotional': 1346},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 323, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '401260a6-484c-d3b0-838b-6594e37f2c11',
             'grossValue': 9583087,
             'homeNotional': 0.09583087, 'foreignNotional': 323},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 1401, 'price': 3370,
             'tickDirection': 'MinusTick', 'trdMatchID': '412fc21e-70ad-42c7-fadf-6bebc289492f', 'grossValue': 41573274,
             'homeNotional': 0.41573274, 'foreignNotional': 1401},
            {'timestamp': '2018-12-11T02:42:41.670Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 201, 'price': 3371,
             'tickDirection': 'PlusTick', 'trdMatchID': '6fc382cb-518c-dfe9-fd34-43cf9ae36836', 'grossValue': 5962665,
             'homeNotional': 0.05962665, 'foreignNotional': 201}]

        ratio = self.mm.trade_directional_ratio(n=10)
        self.assertEqual(ratio, .5)

        self.mm.request_trades.return_value = [
            {'timestamp': '2018-12-11T02:42:20.558Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 56, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'a9cab1b4-5d94-a431-b902-320290988322',
             'grossValue': 1661464,
             'homeNotional': 0.01661464, 'foreignNotional': 56},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 50, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '1627361a-387b-9c66-3cdc-c5e4975caede',
             'grossValue': 1483450,
             'homeNotional': 0.0148345, 'foreignNotional': 50},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 100, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'ad756ab6-7e2d-17ef-b2cb-55671e60bcb8',
             'grossValue': 2966900,
             'homeNotional': 0.029669, 'foreignNotional': 100},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 1000, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '527566bf-0630-0b49-19c6-7b9100cba704',
             'grossValue': 29669000, 'homeNotional': 0.29669, 'foreignNotional': 1000},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 10, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '68a6902a-41a8-b077-0488-322f76c706bf',
             'grossValue': 296690,
             'homeNotional': 0.0029669, 'foreignNotional': 10},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 270, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '3bbe15d4-38cb-5e38-bf05-3176813de529',
             'grossValue': 8010630,
             'homeNotional': 0.0801063, 'foreignNotional': 270},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 1346, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'e47f9941-2460-630f-6006-9c246858aacc',
             'grossValue': 39934474, 'homeNotional': 0.39934474, 'foreignNotional': 1346},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Sell', 'size': 323, 'price': 3370.5,
             'tickDirection': 'ZeroMinusTick', 'trdMatchID': '401260a6-484c-d3b0-838b-6594e37f2c11',
             'grossValue': 9583087,
             'homeNotional': 0.09583087, 'foreignNotional': 323},
            {'timestamp': '2018-12-11T02:42:26.183Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 1401, 'price': 3370,
             'tickDirection': 'MinusTick', 'trdMatchID': '412fc21e-70ad-42c7-fadf-6bebc289492f', 'grossValue': 41573274,
             'homeNotional': 0.41573274, 'foreignNotional': 1401},
            {'timestamp': '2018-12-11T02:42:41.670Z', 'symbol': 'XBTUSD', 'side': 'Buy', 'size': 201, 'price': 3371,
             'tickDirection': 'PlusTick', 'trdMatchID': '6fc382cb-518c-dfe9-fd34-43cf9ae36836', 'grossValue': 5962665,
             'homeNotional': 0.05962665, 'foreignNotional': 201}]

        ratio = self.mm.trade_directional_ratio(n=10)
        self.assertEqual(ratio, .7)

    def test_order_statistics(self):
        order_report = self.mm.order_statistics()

        item = findItemByKeys(['price'], order_report, {'price': 3370})
        self.assertEqual(item['q_ratio'], 1)
        self.assertEqual(item['total_size'], 42718 + 10)
        self.assertEqual(item['status'], 'on_ladder')

        item = findItemByKeys(['price'], order_report, {'price': 3369.5})
        self.assertEqual(item['q_ratio'], round(1500 / (1500 + 150 + 10), 3))
        self.assertEqual(item['total_size'], 1500 + 150 + 10)
        self.assertEqual(item['status'], 'on_ladder')

        item = findItemByKeys(['price'], order_report, {'price': 3371.5})
        self.assertEqual(item['q_ratio'], round(0 / (9763280 + 10), 3))
        self.assertEqual(item['total_size'], 9763280 + 10)
        self.assertEqual(item['status'], 'on_ladder')

        item = findItemByKeys(['price'], order_report, {'price': 3371})
        self.assertEqual(item['q_ratio'], round(0 / 10, 3))
        self.assertEqual(item['total_size'], 10)
        self.assertEqual(item['status'], 'on_ladder')

    def test_calculate_quotes(self):
        # order_stats = self.mm.order_statistics()

        # standard 1 level layer 3 deep balanced
        self.mm.layer_depth = 3
        self.mm.layer_depth_inc = 1
        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(bid_skew=0, ask_skew=0,
                                                              bid_px=0.00000389, ask_px=0.00000390)

        self.assertEqual(ask_post_pxs, [0.00000390, 0.00000391, 0.00000392])
        self.assertEqual(bid_post_pxs, [0.00000389, 0.00000388, 0.00000387])

        # inc 2 balanced skew
        self.mm.layer_depth_inc = 2
        self.mm.bbo.return_value = {'bid': 0.00000389, 'ask': 0.00000390}
        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(bid_skew=0, ask_skew=0,
                                                              bid_px=0.00000389, ask_px=0.00000390)

        self.assertEqual(ask_post_pxs, [0.00000390, 0.00000392, 0.00000394])
        self.assertEqual(bid_post_pxs, [0.00000389, 0.00000387, 0.00000385])

        # inc 2 bid skew 2
        self.mm.layer_depth_inc = 2
        self.mm.bbo.return_value = {'bid': 0.00000389, 'ask': 0.00000390}
        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(bid_skew=2, ask_skew=0,
                                                              bid_px=0.00000389, ask_px=0.00000390)

        self.assertEqual(ask_post_pxs, [0.00000390, 0.00000392, 0.00000394])
        self.assertEqual(bid_post_pxs, [0.00000387, 0.00000385, 0.00000383])

        # inc 2 ask skew 2
        self.mm.layer_depth_inc = 2
        self.mm.bbo.return_value = {'bid': 0.00000389, 'ask': 0.00000390}
        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(bid_skew=0, ask_skew=2,
                                                              bid_px=0.00000389, ask_px=0.00000390)

        self.assertEqual(ask_post_pxs, [0.00000392, 0.00000394, 0.00000396])
        self.assertEqual(bid_post_pxs, [0.00000389, 0.00000387, 0.00000385])

    def test_evaluate_outstanding_orders(self):
        order_report = self.mm.order_statistics()
        bid_px = 3370
        ask_px = 3370.5
        bid_post_pxs = [3370, 3369.5, 3369]
        ask_post_pxs = [3370.5, 3371, 3371.5]
        new_bid_post_pxs, new_ask_post_pxs = self.mm.evaluate_outstanding_orders(order_stats=order_report,
                                                                                 bid_px=bid_px,
                                                                                 ask_px=ask_px,
                                                                                 ask_post_pxs=ask_post_pxs,
                                                                                 bid_post_pxs=bid_post_pxs)
        self.assertEqual(new_bid_post_pxs, [3369.5, 3369])
        self.assertEqual(new_ask_post_pxs, [3371, 3371.5])

        # test if we do not have a inside offer
        bid_px = 3370
        ask_px = 3370.5
        bid_post_pxs = [3370, 3369.5, 3369]
        ask_post_pxs = [3370.5, 3371, 3371.5]

        self.mm.order_report.return_value = [
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3370, 'orderQty': 10, 'side': 'Buy',
             'status': 'on_ladder',
             'size_before': 42718, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3369.5, 'orderQty': 10, 'side': 'Buy',
             'status': 'on_ladder',
             'size_before': 1500, 'size_after': 150},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3369, 'orderQty': 10, 'side': 'Buy',
             'status': 'on_ladder',
             'size_before': 110, 'size_after': 0},
            # {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3370.5, 'orderQty': -10, 'side': 'Sell',
            #  'status': 'on_ladder', 'size_before': 2045, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3371, 'orderQty': -10, 'side': 'Sell',
             'status': 'on_ladder',
             'size_before': 0, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3371.5, 'orderQty': -10, 'side': 'Sell',
             'status': 'on_ladder', 'size_before': 0, 'size_after': 9763280}]
        order_report = self.mm.order_statistics()

        new_bid_post_pxs, new_ask_post_pxs = self.mm.evaluate_outstanding_orders(order_stats=order_report,
                                                                                 bid_px=bid_px,
                                                                                 ask_px=ask_px,
                                                                                 ask_post_pxs=ask_post_pxs,
                                                                                 bid_post_pxs=bid_post_pxs)
        self.assertEqual(new_bid_post_pxs, [3369.5, 3369])
        self.assertEqual(new_ask_post_pxs, [3370.5, 3371, 3371.5])

        # test if we do not have a inside bid
        bid_px = 3370
        ask_px = 3370.5
        bid_post_pxs = [3370, 3369.5, 3369]
        ask_post_pxs = [3370.5, 3371, 3371.5]

        self.mm.order_report.return_value = [
            # {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3370, 'orderQty': 10, 'side': 'Buy',
            #  'status': 'on_ladder',
            #  'size_before': 42718, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3369.5, 'orderQty': 10, 'side': 'Buy',
             'status': 'on_ladder',
             'size_before': 1500, 'size_after': 150},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3369, 'orderQty': 10, 'side': 'Buy',
             'status': 'on_ladder',
             'size_before': 110, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3370.5, 'orderQty': -10, 'side': 'Sell',
             'status': 'on_ladder', 'size_before': 2045, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3371, 'orderQty': -10, 'side': 'Sell',
             'status': 'on_ladder',
             'size_before': 0, 'size_after': 0},
            {'symbol': 'XBTUSD', 'ordType': 'Limit', 'price': 3371.5, 'orderQty': -10, 'side': 'Sell',
             'status': 'on_ladder', 'size_before': 0, 'size_after': 9763280}]
        order_report = self.mm.order_statistics()

        new_bid_post_pxs, new_ask_post_pxs = self.mm.evaluate_outstanding_orders(order_stats=order_report,
                                                                                 bid_px=bid_px,
                                                                                 ask_px=ask_px,
                                                                                 ask_post_pxs=ask_post_pxs,
                                                                                 bid_post_pxs=bid_post_pxs)
        self.assertEqual(new_bid_post_pxs, [3370, 3369.5, 3369])
        self.assertEqual(new_ask_post_pxs, [3371, 3371.5])
