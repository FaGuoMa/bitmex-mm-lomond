from unittest import TestCase
from unittest.mock import MagicMock, patch
from mm import NewTrader
from .agent import MM
from utilities import findItemByKeys, red
from fixtures.test_fixtures import partial_order_book, deltas_orderbook, orders_ack_gen
from time import sleep
import datetime as dt
#this test suite focuses on Bitmex and BCH


class MMTest(TestCase):

    def setUp(self):
        self.mm = MM(symbol_list=['BCHZ18'],
                     bbo=MagicMock(),
                     execute=MagicMock(),
                     get_inventory=MagicMock(),
                     get_inv_avg_price=MagicMock(),
                     order_report=MagicMock(),
                     request_trades=MagicMock(),
                     margin_report=MagicMock())

        self.mm.bbo.return_value = {'bid': [0.0281, 0.028, 0.0279, 0.0275, 0.0273, 0.0272, 0.0271, 0.027, 0.0269, 0.0268, 0.0267, 0.0266, 0.0265, 0.0264, 0.026, 0.0255, 0.025, 0.0249, 0.0233, 0.02], 'ask': [0.0286, 0.0287, 0.0288, 0.029, 0.0294, 0.0295, 0.0296, 0.0297, 0.0298, 0.0299, 0.03, 0.0301, 0.0302, 0.0303, 0.0324, 0.0371, 0.0383, 0.0417, 0.0433, 0.0442]}
        self.mm.margin_report.return_value = 100, 100 # not ideal but not core for test
        self.mm.request_trades.return_value = [{'timestamp': '2018-12-13T01:26:44.035Z', 'symbol': 'BCHZ18', 'side': 'Sell', 'size': 2, 'price': 0.0281, 'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9', 'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:27:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Buy', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:26:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Sell', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:27:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Buy', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:26:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Sell', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:27:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Buy', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:26:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Sell', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:27:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Buy', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:26:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Sell', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:27:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Buy', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562}
                                               ]# should give a trade ratio of 0.5
        self.mm.get_inventory.return_value = 0

        self.mm.order_report.return_value = {'bids': [
            {'symbol': 'BCHZ18', 'price': '0.0272', 'orderQty': 1, 'clOrdID': 'ffbf6395-5ee4-445d-aa2c-6d34054dfd89',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937583, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0271', 'orderQty': 1, 'clOrdID': '9b44512f-089a-4567-81d2-f3491625a5b5',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937621, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.027', 'orderQty': 1, 'clOrdID': 'cdba985c-5052-4dee-94f6-7922f175df41',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937633, 'q_pos': 0.981},
            {'symbol': 'BCHZ18', 'price': '0.0269', 'orderQty': 1, 'clOrdID': '61217f5a-c6d7-4c01-a09b-06b21489696c',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937664, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0268', 'orderQty': 1, 'clOrdID': 'f1d9f281-3062-44a8-bb26-aaf1ef8fe91b',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937674, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0267', 'orderQty': 1, 'clOrdID': '1c03a008-88dc-49fe-82e8-5c8598a70e66',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937684, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0266', 'orderQty': 1, 'clOrdID': 'bf941e11-d50f-4779-86a7-be05e993c3f7',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937694, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0265', 'orderQty': 1, 'clOrdID': '3711db86-6d22-43ae-9080-94b01a744422',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937703, 'q_pos': 0.98},
            {'symbol': 'BCHZ18', 'price': '0.0264', 'orderQty': 1, 'clOrdID': 'b92a646a-4457-423c-9ee8-b39c61a75758',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937718, 'q_pos': 0.98},
            {'symbol': 'BCHZ18', 'price': '0.0263', 'orderQty': 1, 'clOrdID': '7dbfdad0-20c5-48b9-a7cd-21527b767171',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937732, 'q_pos': 1.0}], 'asks': [
            {'symbol': 'BCHZ18', 'price': '0.0293', 'orderQty': -1, 'clOrdID': '1c2490e2-0961-4c2d-b3e8-5987dfe534f4',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937742, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0294', 'orderQty': -1, 'clOrdID': 'c6c6fa34-ac91-4664-8e40-79ed6a60a3c1',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937751, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0295', 'orderQty': -1, 'clOrdID': 'bf15ce89-5c21-4941-91fd-3a04b1822b3f',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.93776, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0296', 'orderQty': -1, 'clOrdID': '83031a0f-b00e-4fe4-82a0-e566a4c34d5d',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.93777, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0297', 'orderQty': -1, 'clOrdID': 'b62c6ce6-8c7a-4d5c-a994-a5bde5b4268d',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937778, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0298', 'orderQty': -1, 'clOrdID': '01b54d74-b8ae-4d79-8f10-6c411e254f0b',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937787, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0299', 'orderQty': -1, 'clOrdID': 'd9c36ae5-3691-4c1b-bfca-bcaa41b77354',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937796, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.03', 'orderQty': -1, 'clOrdID': 'd25a2689-cd88-4484-9ec3-6dbd772691ed',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937805, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0301', 'orderQty': -1, 'clOrdID': 'f6cafbf2-fb8f-4d06-844b-425ab5076781',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937813, 'q_pos': 1.0},
            {'symbol': 'BCHZ18', 'price': '0.0302', 'orderQty': -1, 'clOrdID': '57da272a-c3f0-4df0-a05d-c089783b6223',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937822, 'q_pos': 1.0}]}



    def test_calc_indicators(self):
        """
        test of a few cases of calc indicators
        :return:
        """
        ind = self.mm.calc_indicators()
        self.assertEqual(ind['trade_ratio'], 0.5)

    def test_determine_state(self):
        """

        :return:
        """
        self.mm.determine_state()
        self.assertEqual(self.mm.agent_state, 'INIT')
        print(self.mm.calc_indicators())
        print("we re-reun determine state")
        self.mm.determine_state()
        self.assertEqual(self.mm.agent_state, 'DUAL')


    def test_calculate_quotes(self):

        cur_ob = self.mm.bbo()
        print(cur_ob)
        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(0,0, cur_ob['bid'][0], cur_ob['ask'][0])
        self.assertEqual(bid_post_pxs[0], cur_ob['bid'][0])
        self.assertEqual(ask_post_pxs[0], cur_ob['ask'][0])
        print(len(ask_post_pxs))
        self.assertEqual(len(ask_post_pxs), 2*self.mm.layer_depth)
        self.assertEqual(len(bid_post_pxs), 2*self.mm.layer_depth)


    def test_skew_ticks(self):
        """
        we mostly want to test the BID or ASK states function
        :return:
        """
        self.mm.agent_state = 'BID'
        self.mm.max_inventory = 12
        self.mm.get_inventory.return_value = 3
        sk = self.mm.skew_ticks()
        self.assertEqual(sk, (self.mm.skew_levels[0], 0 ))
        self.mm.get_inventory.return_value = 5
        sk = self.mm.skew_ticks()
        self.assertEqual(sk, (self.mm.skew_levels[1], 0))
        self.mm.get_inventory.return_value = 9
        sk = self.mm.skew_ticks()
        self.assertEqual(sk, (self.mm.skew_levels[2], 0))

        print("ASK state")
        self.mm.agent_state = 'ASK'
        self.mm.max_inventory = 12
        self.mm.get_inventory.return_value = 3
        sk = self.mm.skew_ticks()
        self.assertEqual(sk, (self.mm.skew_levels[0], 0)[::-1])
        self.mm.get_inventory.return_value = 5
        sk = self.mm.skew_ticks()
        self.assertEqual(sk, (self.mm.skew_levels[1], 0)[::-1])
        self.mm.get_inventory.return_value = 9
        sk = self.mm.skew_ticks()
        self.assertEqual(sk, (self.mm.skew_levels[2], 0)[::-1])


    def test_agent_perform(self):
        """
        tests of cases from indicatos and agent state
        :return:
        """
        # we run determine twice to be in DUAL
        self.mm.determine_state()
        self.mm.determine_state()
        self.mm.agent_perform(self.mm.calc_indicators(),0)
        self.assertEqual(self.mm.agent_state, 'DUAL')


    def test_evaluate_outstanding_orders(self):
        """
        this is a tricky part. We want to test
        1. case with no removal
        2. case with removal of inside bid (or aks, or both) in case of q_pos with or without t_market
        2a. case of partial removal if we have inventory on the other side
        3. storage of said removal and automatic subsequent removal
        4. reset of removal on change of bbo
        :return:
        """
        # we only nneed one level and the return is the value straigh up # TODO API consistency would probably be better if OrderBOOK.bbo returned a list always but I dont want ot break stuff right now
        #self.mm.bbo.return_value = {'bid': '0.0281', 'ask' : '0.0286'} # TODO because of float point error (red / dered in utilities we can either have a float (XBTUSD eg or string) Not good
        cur_ob = self.mm.bbo()

        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(0, 0, cur_ob['bid'][0], cur_ob['ask'][0])

        # sub case 1
        print("case 1:  no removal")
        # we fix the q_ratios at 281 and 286
        self.mm.order_report.return_value = {'bids': [
            {'symbol': 'BCHZ18', 'price': str(0.0281 + i*0.0001), 'orderQty': 1, 'clOrdID': 'ffbf6395-5ee4-445d-aa2c-6d34054dfd89',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937583, 'q_pos': self.mm.q_ratio_threshold -0.1} for i in range(0,10)],
            'asks': [
            {'symbol': 'BCHZ18', 'price': str(0.0286 - i*0.0001), 'orderQty': -1, 'clOrdID': '1c2490e2-0961-4c2d-b3e8-5987dfe534f4',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 11.937742, 'q_pos': self.mm.q_ratio_threshold -0.1} for i in range(0,10)]}


        bid_post_pxs, ask_post_pxs = self.mm.evaluate_outstanding_orders(bid_post_pxs, ask_post_pxs)

        self.assertEqual(bid_post_pxs[0], 0.0281)
        self.assertEqual(ask_post_pxs[0], 0.0286)
        self.assertEqual(len(bid_post_pxs), 2 *self.mm.layer_depth)
        self.assertEqual(len(ask_post_pxs), 2 * self.mm.layer_depth)

        #sub case 2
        print("case 2:  no removal for grace period while q is bad")
        self.mm.order_report.return_value = {'bids': [
            {'symbol': 'BCHZ18', 'price': str(0.0281 + i * 0.0001), 'orderQty': 1,
             'clOrdID': 'ffbf6395-5ee4-445d-aa2c-6d34054dfd89',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 0.5, 'q_pos': self.mm.q_ratio_threshold + 0.1} #t_market under grace time and q ratio bad
            for i in range(0, 10)],
            'asks': [
                {'symbol': 'BCHZ18', 'price': str(0.0286 - i * 0.0001), 'orderQty': -1,
                 'clOrdID': '1c2490e2-0961-4c2d-b3e8-5987dfe534f4',
                 'execInst': 'ParticipateDoNotInitiate', 't_market': 0.5,
                 'q_pos': self.mm.q_ratio_threshold + 0.1} for i in range(0, 10)]}
        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(0, 0, cur_ob['bid'][0], cur_ob['ask'][0])

        bid_post_pxs, ask_post_pxs = self.mm.evaluate_outstanding_orders(bid_post_pxs, ask_post_pxs)

        self.assertEqual(bid_post_pxs[0], 0.0281)
        self.assertEqual(ask_post_pxs[0], 0.0286)
        self.assertEqual(len(bid_post_pxs), 2 * self.mm.layer_depth)
        self.assertEqual(len(ask_post_pxs), 2 * self.mm.layer_depth)

        print("case 2:  removal  while q is bad, both side")
        self.mm.last_bbo = None
        self.mm.order_report.return_value = {'bids': [
            {'symbol': 'BCHZ18', 'price': str(0.0281 + i * 0.0001), 'orderQty': 1,
             'clOrdID': 'ffbf6395-5ee4-445d-aa2c-6d34054dfd89',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 10, 'q_pos': self.mm.q_ratio_threshold + 0.1}
            # t_market under grace time and q ratio bad
            for i in range(0, 10)],
            'asks': [
                {'symbol': 'BCHZ18', 'price': str(0.0286 - i * 0.0001), 'orderQty': -1,
                 'clOrdID': '1c2490e2-0961-4c2d-b3e8-5987dfe534f4',
                 'execInst': 'ParticipateDoNotInitiate', 't_market': 10,
                 'q_pos': self.mm.q_ratio_threshold + 0.1} for i in range(0, 10)]}
        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(0, 0, cur_ob['bid'][0], cur_ob['ask'][0])
        # print(cur_ob)
        bid_post_pxs, ask_post_pxs = self.mm.evaluate_outstanding_orders(bid_post_pxs, ask_post_pxs)
        # print("bids: {} \n asks: {}".format(bid_post_pxs, ask_post_pxs))
        print("new inside")
        self.assertEqual(bid_post_pxs[0], 0.028)
        self.assertEqual(ask_post_pxs[0], 0.0287)
        print(self.mm.last_bbo)
        self.assertEqual({'bid' : '0.0281', 'ask' : '0.0286'}, red(self.mm.last_bbo)) # TODO is it wise ?
        self.assertNotEqual(ask_post_pxs[0], 0.0286)
        self.assertNotEqual(bid_post_pxs[0], 0.0281)
        self.assertEqual(len(bid_post_pxs), 2 * self.mm.layer_depth-1)
        self.assertEqual(len(ask_post_pxs), 2 * self.mm.layer_depth-1)

        print("case 2:  removal  while q is good but last_bbo exists, both side")
        self.mm.order_report.return_value = {'bids': [
            {'symbol': 'BCHZ18', 'price': str(0.0281 + i * 0.0001), 'orderQty': 1,
             'clOrdID': 'ffbf6395-5ee4-445d-aa2c-6d34054dfd89',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 10, 'q_pos': self.mm.q_ratio_threshold - 0.1}
            # t_market under grace time and q ratio bad
            for i in range(0, 10)],
            'asks': [
                {'symbol': 'BCHZ18', 'price': str(0.0286 - i * 0.0001), 'orderQty': -1,
                 'clOrdID': '1c2490e2-0961-4c2d-b3e8-5987dfe534f4',
                 'execInst': 'ParticipateDoNotInitiate', 't_market': 10,
                 'q_pos': self.mm.q_ratio_threshold - 0.1} for i in range(0, 10)]}
        #settign up last bbo here
        print("set last_bbo")
        self.mm.last_bbo = {'bid': 0.0281, 'ask': 0.0286}
        self.mm.get_inventory.return_value = 0
        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(0, 0, cur_ob['bid'][0], cur_ob['ask'][0])

        bid_post_pxs, ask_post_pxs = self.mm.evaluate_outstanding_orders(bid_post_pxs, ask_post_pxs)
        # print("bids: {} \n asks: {}".format(bid_post_pxs, ask_post_pxs))
        self.assertEqual(bid_post_pxs[0], 0.028)
        self.assertEqual(ask_post_pxs[0], 0.0287)
        self.assertEqual({'bid': '0.0281', 'ask': '0.0286'}, red(self.mm.last_bbo))  # TODO is it wise ?
        self.assertNotEqual(ask_post_pxs[0], 0.0286)
        self.assertNotEqual(bid_post_pxs[0], 0.0281)
        self.assertEqual(len(bid_post_pxs), 2 * self.mm.layer_depth - 1)
        self.assertEqual(len(ask_post_pxs), 2 * self.mm.layer_depth - 1)


        print("case 2a:  removal  while q is good but last_bbo exists, both side but I have pos inventory")
        self.mm.order_report.return_value = {'bids': [
            {'symbol': 'BCHZ18', 'price': str(0.0281 + i * 0.0001), 'orderQty': 1,
             'clOrdID': 'ffbf6395-5ee4-445d-aa2c-6d34054dfd89',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 10, 'q_pos': self.mm.q_ratio_threshold - 0.1}
            # t_market under grace time and q ratio bad
            for i in range(0, 10)],
            'asks': [
                {'symbol': 'BCHZ18', 'price': str(0.0286 - i * 0.0001), 'orderQty': -1,
                 'clOrdID': '1c2490e2-0961-4c2d-b3e8-5987dfe534f4',
                 'execInst': 'ParticipateDoNotInitiate', 't_market': 10,
                 'q_pos': self.mm.q_ratio_threshold - 0.1} for i in range(0, 10)]}
        # positive inv so, I only want to deal with inside bid
        self.mm.get_inventory.return_value = 10
        # settign up last bbo here
        print("set last_bbo")
        self.mm.last_bbo = {'bid': 0.0281, 'ask': 0.0286}
        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(0, 0, cur_ob['bid'][0], cur_ob['ask'][0])
        print(bid_post_pxs)
        print(ask_post_pxs)
        bid_post_pxs, ask_post_pxs = self.mm.evaluate_outstanding_orders(bid_post_pxs, ask_post_pxs)
        print("bids: {} \n asks: {}".format(bid_post_pxs, ask_post_pxs))
        self.assertEqual(bid_post_pxs[0], 0.028)
        self.assertEqual(ask_post_pxs[0], 0.0286)
        self.assertEqual({'bid': '0.0281', 'ask': '0.0286'}, red(self.mm.last_bbo))  # TODO is it wise ?
        self.assertNotEqual(ask_post_pxs[0], 0.0287)
        self.assertNotEqual(bid_post_pxs[0], 0.0281)
        self.assertEqual(len(bid_post_pxs), 2 * self.mm.layer_depth - 1)
        self.assertEqual(len(ask_post_pxs), 2 * self.mm.layer_depth )

        print("case 3:  change of BBO unsets last_bbo")
        self.mm.order_report.return_value = {'bids': [
            {'symbol': 'BCHZ18', 'price': str(0.0281 + i * 0.0001), 'orderQty': 1,
             'clOrdID': 'ffbf6395-5ee4-445d-aa2c-6d34054dfd89',
             'execInst': 'ParticipateDoNotInitiate', 't_market': 0.5, 'q_pos': self.mm.q_ratio_threshold - 0.1}
            # t_market under grace time and q ratio bad
            for i in range(0, 10)],
            'asks': [
                {'symbol': 'BCHZ18', 'price': str(0.0286 - i * 0.0001), 'orderQty': -1,
                 'clOrdID': '1c2490e2-0961-4c2d-b3e8-5987dfe534f4',
                 'execInst': 'ParticipateDoNotInitiate', 't_market': 0.5,
                 'q_pos': self.mm.q_ratio_threshold - 0.1} for i in range(0, 10)]}
        # settign up last bbo here
        print("set last_bbo")
        self.mm.last_bbo = {'bid': '0.0281', 'ask': '0.0286'}
        self.mm.bbo.return_value = {
            'bid': [ 0.028, 0.0279, 0.0275, 0.0273, 0.0272, 0.0271, 0.027, 0.0269, 0.0268, 0.0267, 0.0266,
                    0.0265, 0.0264, 0.026, 0.0255, 0.025, 0.0249, 0.0233, 0.02],
            'ask': [ 0.0287, 0.0288, 0.029, 0.0294, 0.0295, 0.0296, 0.0297, 0.0298, 0.0299, 0.03, 0.0301, 0.0302,
                    0.0303, 0.0324, 0.0371, 0.0383, 0.0417, 0.0433, 0.0442]}




        self.mm.get_inventory.return_value = 0
        bid_post_pxs, ask_post_pxs = self.mm.calculate_quotes(0, 0, self.mm.bbo()['bid'][0], self.mm.bbo()['ask'][0])# NOTE the call is a bit different here
        print(bid_post_pxs)
        bid_post_pxs, ask_post_pxs = self.mm.evaluate_outstanding_orders(bid_post_pxs, ask_post_pxs)
        # print("bids: {} \n asks: {}".format(bid_post_pxs, ask_post_pxs))
        self.assertEqual( 0.028, bid_post_pxs[0])
        self.assertEqual(0.0287, ask_post_pxs[0])
        self.assertIsNone(self.mm.last_bbo)


    def test_flicker_lvl1(self):
        """
        this test cases intends to replicate the case where:
        1. we initiate orderbook
        2. we execute a target
        3. we ack all positions
        4. BBO situation is unfavorable (possibly with no grace period)

        outcome should be that BBO orders are gone and not coming back
        :return:
        """

        # 1
        print("instantiate trade with order book and agent")
        partial = partial_order_book()
        print(partial)

        mm = NewTrader(conf=0, myname="unittest", boot_client=False)

        #initiate the book
        mm.book.getmsg(partial)
        self.assertEqual({'bid': 0.0277, 'ask': 0.0278}, mm.book.bbo())
        print(mm.book.bbo())
        self.assertEqual(40, len(mm.book.book))

        # we need to overid request trades and margin reports
        mm.agent.trade_directional_ratio = MagicMock()
        mm.agent.trade_directional_ratio.return_value = 0.5
        mm.agent.margin_report = MagicMock()
        mm.agent.margin_report.return_value = 100, 100
        mm.agent.request_trades = MagicMock()
        mm.agent.request_trades.return_value = [{'timestamp': '2018-12-13T01:26:44.035Z', 'symbol': 'BCHZ18', 'side': 'Sell', 'size': 2, 'price': 0.0281, 'tickDirection': 'ZeroMinusTick', 'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9', 'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:27:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Buy', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:26:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Sell', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:27:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Buy', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:26:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Sell', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:27:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Buy', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:26:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Sell', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:27:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Buy', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:26:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Sell', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562},
                                               {'timestamp': '2018-12-13T01:27:44.035Z', 'symbol': 'BCHZ18',
                                                'side': 'Buy', 'size': 2, 'price': 0.0281,
                                                'tickDirection': 'ZeroMinusTick',
                                                'trdMatchID': 'e280d082-8129-f4fb-b661-dee046582ea9',
                                                'grossValue': 5620000, 'homeNotional': 2, 'foreignNotional': 0.0562}
                                               ]# should give a trade ratio of 0.5
        mm.agent.get_inventory=MagicMock()
        mm.agent.get_inventory.return_value = 0
        # start with one order each side
        mm.agent.layer_depth = 3

        # we overide state
        mm.agent.agent_state = 'INIT'
        print('first determine state')
        mm.agent.determine_state()


        for order in mm.ord_keep.keep.values():
            order.status = 'on_ladder'
            order.size_before =100
            order.size_after = 0
            order.ts = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=3)
        print('ghetto update is done')
        mm.agent.determine_state()
        print("order report after re-running determine state")

        print(mm.ord_keep.ord_report())
        print("b bid : {}".format(max([float(x['price']) for x in mm.ord_keep.ord_report() if x['orderQty'] > 0])))
        print("b ask : {}".format(min([float(x['price']) for x in mm.ord_keep.ord_report() if x['orderQty'] < 0])))

        print("len of keep : {}".format(len(mm.ord_keep.ord_report())))
        for order in mm.ord_keep.keep.values():
            order.status = 'on_ladder'
            order.size_before =100
            order.size_after = 0

        # 4 bid and ask are "burnt" re-running should not change state
        mm.agent.determine_state()
        print("order report after re-re-running determine state")
        print([x['status'] for x in mm.ord_keep.ord_report()])
        print("b bid : {}".format(max([float(x['price']) for x in mm.ord_keep.ord_report() if x['orderQty'] > 0])))
        print("b ask : {}".format(min([float(x['price']) for x in mm.ord_keep.ord_report() if x['orderQty'] < 0])))
        print("len of keep : {}".format(len(mm.ord_keep.ord_report())))
