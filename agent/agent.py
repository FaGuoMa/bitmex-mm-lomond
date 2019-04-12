import logging
import math
import traceback

from utilities import red, dered


class MM:

    def __init__(self, symbol_list, bbo, execute, get_inventory, get_inv_avg_price, order_report, request_trades, margin_report):

        # logger
        self.logger = logging.getLogger("Agent MM")
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d|%(levelname)-8s|%(name)-10s|  %(message)s',
            level=logging.INFO,
            datefmt='%M:%S')

        # call backs
        self.symbol_list = symbol_list
        self.bbo = bbo
        self.execute = execute
        self.get_inventory = get_inventory
        self.get_inv_avg_px = get_inv_avg_price
        self.order_report = order_report
        self.request_trades = request_trades
        self.margin_report = margin_report

        # class variables
        self.agent_state = None
        self.PnL = 0

        # MM strategy params
        self.trade_ratio_lookback = 10
        self.layer_depth = 10  # how many orders to layer on each side
        self.layer_depth_inc = 1  # increment size of gap between layers in ticks
        self.max_loss_pct = .15
        self.max_inventory = 10
        self.min_tick_size = 0.0001  # BTCUSD 0.5
        self.skew_levels = [0, 3, None]  # inside, 2 deep, don't post opposing. This parameter is used to limit posting on one side, depending on inventory e.g.
        self.q_ratio_threshold = .25
        self.trade_dir_ratio_thresh = .25  # symmetric for bid/ask
        self.quote_size = 1
        self.grace_time_q = 1 #second
        #store (and reset) the BBO
        self.last_bbo = None

    ###########
    # Utilities#
    ###########

    def debug(self, msg):
        """
        simple wrapper to debug
        :param msg:
        :return:
        """
        self.logger.debug(str(msg))

    def warn(self, msg):
        """
        simple wrapper to warning
        :param msg:
        :return:
        """
        self.logger.warning(str(msg))

    def info(self, msg):
        """
        simple wrapper to warning
        :param msg:
        :return:
        """
        self.logger.info(str(msg))

    def critical(self, msg):
        """
        simple wrapper to warning
        :param msg:
        :return:
        """
        self.logger.critical(str(msg))


    def calc_indicators(self):
        """

        :return: dict of indi values
        """
        try:
            depth_i_want = self.layer_depth + self.layer_depth*self.layer_depth_inc
            current_ob = self.bbo(lvl=depth_i_want)

        except Exception as e:
            self.critical('could get bbo for depth {}, error {}'.format(depth_i_want, str(e)))
            current_ob = None

        try:
            trade_ratio = self.trade_directional_ratio(n=self.trade_ratio_lookback)
        except Exception as e:
            self.critical('calc_indicators trade ratio {} \n {}'.format(str(e), traceback.format_exc(5)))
            trade_ratio = None #TODO defautl to 0.5 for testing is NOT suitable for prod

        try:
            init_margin_bal, cur_margin_bal = self.margin_report()
            # above can return none, none if we didnt get the partials yet. In that case we set to 0 (TODO TBC)
            if init_margin_bal and cur_margin_bal:
                max_loss_bal = init_margin_bal * (1 - self.max_loss_pct)
            else:
                max_loss_bal = 0
        except Exception as e:
            self.critical('margin current/balance error {}\n {}'.format(str(e), traceback.format_exc(5)))
            init_margin_bal = None
            cur_margin_bal = None


        indi_dict = {'current_ob': current_ob,
                     'order_stats': self.order_report,
                     'trade_ratio': trade_ratio,
                     'init_margin_bal': init_margin_bal,
                     'cur_margin_bal': cur_margin_bal,
                     'max_loss_bal': max_loss_bal,
                     }

        return indi_dict



    def determine_state(self):

        """
        aggregate logic into finite states

        The point is clear transition between each possible states with no gaps where it will not have a state,
        also a swift reboot time in which it can resume itself in a single call to the order book / trade partials,
        and a query to inventory

        1) init -> dual
        2) bid skew post (long inv, bid farther ask closer)-> dual, ask, kill
        3) ask skew post (short inv, ask farther bid closer)-> dual, bid, kill
        4) dual post -> dual, ready, kill
        5) kill
        :return:
        """
        curr_inventory = self.get_inventory()
        indi_dict = self.calc_indicators()

        if self.agent_state is None:
            self.logger.debug(' indi_dict {}'.format(indi_dict))
        if self.agent_state in [None, 'KILL'] and None not in [v for k,v in indi_dict.items() if k != 'order_stats']:
            """
            Do we have no outstanding orders, then we need dont check q status
            if we have orders we need q status
            """
            self.agent_state = 'INIT'
            self.logger.debug('initial indi_dict {}'.format(indi_dict))
            # at boot will have cur_maring_bal is None
        elif indi_dict.get('cur_margin_bal') and indi_dict['cur_margin_bal'] <= indi_dict['max_loss_bal']:
            """
            in any situation when we have lost more than are max balance using Upnl +Rpnl
            """
            self.agent_state = 'KILL' # TODO what do we do in this state ?

        elif self.agent_state in ['INIT', 'BID', 'ASK'] and curr_inventory == 0:
            """
            we have all data, and we are flat. Post both sides equally
            """
            self.agent_state = 'DUAL'

        elif self.agent_state in ['INIT', 'DUAL', 'ASK'] and curr_inventory > 0:
            """
            we have all data, but are long inventory. post asks closer and skew the bid farther
            """
            self.agent_state = 'BID'
        elif self.agent_state in ['INIT', 'BID', 'DUAL'] and curr_inventory < 0:
            """
            we have all data, but are long inventory. post bid closer and skew the ask farther
            """
            self.agent_state = 'ASK'
        else:
            # no change of state
            pass

        self.agent_perform(indi_dict=indi_dict, curr_inventory=curr_inventory)

    def agent_perform(self, indi_dict, curr_inventory):
        """
        :param indi_dict: dict of indi values
        :param curr_inventory : int of inventory level
        :return:
        """
        self.debug('in agent perform with state: {}'.format(self.agent_state))


        if not indi_dict['current_ob'] or indi_dict['current_ob']['bid'] == [] or indi_dict['current_ob']['ask'] == []:
            bid_px = ask_px = None
        else:
            bid_px = indi_dict['current_ob']['bid'][0]
            ask_px = indi_dict['current_ob']['ask'][0]

        if self.agent_state == 'INIT':
            pass
        elif self.agent_state == 'KILL':
            self.logger.critical('KILL STATE - LOST MAX STOP LINE!')
            # todo need panic close

        # get the basic skew
        bid_skew, ask_skew = self.skew_ticks()
        # update desired lists of bids and asks
        bid_post_pxs, ask_post_pxs = self.calculate_quotes(bid_skew=bid_skew,
                                                           ask_skew=ask_skew,
                                                           bid_px=bid_px,
                                                           ask_px=ask_px)

        # we sort the prices for convenience:
        bid_post_pxs = sorted(bid_post_pxs, reverse=True)
        ask_post_pxs =sorted(ask_post_pxs)

        # now we remove the closest inside bid if trade ratio is not our way
        if self.agent_state in ['DUAL', 'BID']:
            if indi_dict['trade_ratio'] < self.trade_dir_ratio_thresh:
                if bid_post_pxs:
                    # remove the closest ask
                    bid_post_pxs.pop(0)

        if self.agent_state in ['DUAL', 'ASK']:
            # 1 way trades incoming
            if indi_dict['trade_ratio'] > 1 - self.trade_dir_ratio_thresh:
                if ask_post_pxs:
                    # remove the closest ask
                    ask_post_pxs.pop(0)

        bid_post_pxs, ask_post_pxs = self.evaluate_outstanding_orders(ask_post_pxs=ask_post_pxs,
                                                                      bid_post_pxs=bid_post_pxs)

        # we truncate both sides to the number of orders we want
        bid_post_pxs = bid_post_pxs[:self.layer_depth]
        # we hook the red function here
        bid_post_pxs = red(bid_post_pxs)
        ask_post_pxs = ask_post_pxs[:self.layer_depth]
        ask_post_pxs = red(ask_post_pxs)
        bid = [dict(symbol=self.symbol_list[0],
                    orderQty = self.quote_size,
                    price=x) for x in bid_post_pxs if x is not None]
        ask = [dict(symbol=self.symbol_list[0],
                    orderQty = - self.quote_size,
                    price=x) for x in ask_post_pxs if x is not None]

        # Inventory checks
        if curr_inventory >= self.max_inventory:
            bid = [None]

        if curr_inventory <= -self.max_inventory:
            ask = [None]

        to_exec = bid + ask
        to_exec = [x for x in to_exec if x is not None]

        # bonus, if our inventory is over 50% of mx inventory, scratch it
        cur_inv = self.get_inventory()
        avg_px = self.get_inv_avg_px()
        last_trades = self.request_trades(n=1)
        if last_trades:
            last_price = last_trades[0]['price']

        if last_trades and abs(cur_inv) > 0.5 * self.max_inventory and abs(last_price/avg_px - 1) > 0.01:# TODO harcoded ratios are not nice

            to_exec.append(dict(symbol=self.symbol_list[0],orderQty = -cur_inv,ordType= 'Market'))


        self.execute(to_exec)

    def evaluate_outstanding_orders(self, bid_post_pxs, ask_post_pxs):
        """

        compare are naive skewed quote against outstanding orders and our current best bid/ask

        update: we want to burn the BBO and only the BBO if we don't get the queue, but only opposite side if we carry an invetory
        :param order_stats: list dict
        :param bid_px= float
        :param ask_px = float
        :param bid_post_pxs = list
        :param ask_post_pxs = list
        :return: tuple of lists
        """

        # we get the order report with q times and time on market. The time on market should not be a problem for Q size
        # since orderKeep pushes a ladder value after some time if we miss some messages (Order.saw_myself = False)
        # the order report (OrderKeep.exec_report) returns a dict of bids and ask keys with lists in descending order of
        # closeness to the mid-price
        # update, at this point the bid_ps /ask_ px should be floats

        # so now we check if we have a previously burnt BBO

        if self.last_bbo:
            # if we do, has it moved
            cur_bbo = {k: v[0] for k, v in self.bbo(lvl=5).items()}
            self.debug("last bbo {} | cur bbo {}".format(self.last_bbo, cur_bbo))
            # TODO this is a bit ugly but since I have an inconsistent API for OrderBOOK.get_bbo for lvl=1 and lvl >1 that's that for now

            if red(self.last_bbo) != red(cur_bbo):
                # if so, we reset
                self.last_bbo = None
            # esle it means we have canceled an order at the ask or bid already so we'll match that price to remove it later

        cur_orders = self.order_report()

        # we get ack to float
        cur_orders = { k : dered(v) for k, v in cur_orders.items()}
        self.debug("q & prices : bids {} \n asks {}".format([{k : v for k, v in x.items() if k in ['price', 'q_pos', 't_market']} for x in cur_orders['bids']],
                                               [{k: v for k, v in x.items() if k in ['price', 'q_pos', 't_market']} for
                                                x in cur_orders['asks']]))
        # we check that we are not holding the bag (after a grace period of self.grace_time_q) for the
        # first (n) levels and remove if so
        if (cur_orders['bids'] != [] or cur_orders['asks'] != []) and self.bbo(lvl=5) and self.bbo(lvl=5).get('bid') and self.bbo(lvl=5).get('ask'):
            # we check if we have inventory
            #
            # we id our best bid and best ask orders
            #print("in flicker loop")
            self.debug("cur orders {}".format(cur_orders))
            flt_fun = lambda x: float(x['price'])
            try:
                bb = sorted(cur_orders['bids'], key= flt_fun, reverse=True)[0]
            except IndexError:
                bb= None
            try:
                ba = sorted(cur_orders['asks'], key= flt_fun)[0]
            except IndexError:
                ba = None
            self.debug("ba {} | bb {}".format(str(bb), str(ba)))


            if self.get_inventory() >= 0:
                #if ivnentory is positive, we only concern ourselves with maybe removing some ask
                self.debug("ba price {} | bbo {} | equal {}".format(ba['price'],red(self.bbo(lvl=5)['ask'][0]), ba['price'] == red(self.bbo(lvl=5)['ask'][0])))
                if ba['price'] == red(self.bbo(lvl=5)['ask'][0]):
                    #print("in flicker ask remove")
                    self.debug("ba t mkt {} | ba q pos {}".format(ba['t_market'] > self.grace_time_q ,ba['q_pos'] > self.q_ratio_threshold))
                    print('last bbo'.format(self.last_bbo))

                    if ba['q_pos'] and ba['t_market'] and\
                                    ba['q_pos'] > self.q_ratio_threshold \
                                    and ba['t_market'] > self.grace_time_q:
                        self.debug("removing inside ask (and burning value)")
                        ask_post_pxs.pop(0)
                        if not self.last_bbo:
                            self.last_bbo = dict()
                        if not self.last_bbo.get('ask'):
                            self.last_bbo['ask']=dered(self.bbo(lvl=5)['ask'][0])

                if self.last_bbo and self.last_bbo.get('ask'):
                    self.debug("We had a burned ask value")
                    ask_post_pxs.pop(0)


            if self.get_inventory() <= 0:
                #if ivnentory is negative, we only concern ourselves with maybe removing some bid
                self.debug("bb price {} | bbo {} | equal {}".format(bb['price'],red(self.bbo(lvl=5)['bid'][0]), bb['price'] == red(self.bbo(lvl=5)['bid'][0])))
                if bb['price'] == red(self.bbo(lvl=5)['bid'][0]):
                    #print("in flicker bid remove")
                    self.debug("bb t mkt {} | bb q pos {}".format(bb['t_market'] > self.grace_time_q ,bb['q_pos'] > self.q_ratio_threshold))

                    if bb['q_pos'] and bb['t_market'] and\
                                    bb['q_pos'] > self.q_ratio_threshold \
                                    and bb['t_market'] > self.grace_time_q:
                        self.debug("removing inside bid (and burning value)")
                        bid_post_pxs.pop(0)
                        if not self.last_bbo:
                            self.last_bbo = dict()
                        if not self.last_bbo.get('bid'):
                            self.last_bbo['bid']=dered(self.bbo(lvl=5)['bid'][0])

                if self.last_bbo and self.last_bbo.get('bid'):
                    self.debug("We had a burned bid value")
                    bid_post_pxs.pop(0)

        return bid_post_pxs, ask_post_pxs


    def trade_directional_ratio(self, n=10):
        """
        return the ratio of buys to all trades in the last period and  pass to the MM core logic.
        :param n int - look back
        :return: float
        """

        recent_trades = self.request_trades(n)
        if recent_trades and len(recent_trades) >= n:
            side_buy = [order for order in recent_trades if order['side'] == 'Buy']
            side_sell = [order for order in recent_trades if order['side'] == 'Sell']
            ratio = len(side_buy) / (len(side_buy) + len(side_sell))
        else:
            ratio = None #None TODO not safe for prod!

        return ratio

    def skew_ticks(self):
        """
        find the levels based on quartiles
        skew levels is a list of 'skews', gaps we want to leave between us and an the best bid or ask
        :param bid_lvl: dict
        :param ask_lvl: dict
        :return:
        """
        skew_level = None

        if self.agent_state == 'BID' or self.agent_state == 'ASK':
            # determine the severity of the skew. We put inventory levels as thresholds of max inventory (evenly spaced)
            if abs(self.get_inventory()) < self.max_inventory / len(self.skew_levels):
                skew_level = self.skew_levels[0]
            elif self.max_inventory / len(self.skew_levels) <= abs(self.get_inventory()) \
                    < 2 * self.max_inventory / len(self.skew_levels):
                skew_level = self.skew_levels[1]
            else:
                skew_level = self.skew_levels[-1]

        if self.agent_state == 'ASK':
            bid_skew = 0
            ask_skew = skew_level
        elif self.agent_state == 'BID':
            bid_skew = skew_level
            ask_skew = 0
        elif self.agent_state == 'DUAL':
            bid_skew = 0
            ask_skew = 0
        else:
            #  Don't know what happened, get wide
            self.logger.critical('Skew weird state - Quoting Wide')
            bid_skew = 8
            ask_skew = 8

        return bid_skew, ask_skew

    def calculate_quotes(self, bid_skew, ask_skew, bid_px, ask_px):
        """
        uses ceiling and floor division on the number of ticks in the price
        We use twise the layer since we might skew prices and whatnots, and we'll trim them down later
        :param bid_skew: int
        :param ask_skew: int
        :param bid_px: float - best bid (ie highest of self.bbo['bid'] /current_on)
        :param ask_px: float - best ask (ie lowest of self.bbo['ask'] /current_on)
        :return: tuple of lists of len self.depth_levels
        """
        bid_post_pxs = list()
        ask_post_pxs = list()

        if bid_skew is not None and bid_px is not None:
            for lvl in range(2 * self.layer_depth):

                bid_post_pxs.append((bid_px / self.min_tick_size # I dont think we need the rounding here, BTC
                                     - bid_skew
                                     - lvl * self.layer_depth_inc)
                                    * self.min_tick_size)
            # self.logger.debug('bid_post_pxs {}'.format(bid_post_pxs))

        if ask_skew is not None and ask_px is not None:
            for lvl in range(2 * self.layer_depth):
                ask_post_pxs.append((ask_px / self.min_tick_size
                                     + ask_skew
                                     + lvl*self.layer_depth_inc)
                                    * self.min_tick_size)
            # self.logger.debug('ask_post_pxs {}'.format(ask_post_pxs))

        self.debug("bids: {} \n asks: {}".format( bid_post_pxs, ask_post_pxs))
        return bid_post_pxs, ask_post_pxs

    def on_l2(self):
        """
        functional wrapper to trigger calculations in case of L2 udpates
        :return:
        """
        self.determine_state()

    def on_trade(self):
        """
        functional wrapper to trigger calculations in case of new trade as ratios might change udpates

        :return:
        """
        self.determine_state()