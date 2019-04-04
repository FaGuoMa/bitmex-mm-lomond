from uuid import uuid4
import datetime as dt
import bitmex
import json
from bravado import exception
import logging
from operator import itemgetter
import traceback

from time import process_time, time
import asyncio
from threading import Thread, Lock, Event


from utilities import dtnow, sec_now, red, dered
from exceptions import IncompleteOrder, InconsistentOrderData, Http400, Http429, Http403, WrongInput, NoExchangeMethod


class Order:
    """
    an order class to keep track of all information and encapsulate important methods

    status is critical:
    - new order was triggered by internal logic or read from queue, but not posted. id level is tentative
    - processed order was posted with a resp 200. I have time on market then
    - on_ladder order was confirmed either by finding its ladder from orderbook, or by time
    - to_ammend : order will be replaced (and back to processed step)
    - canceled : order needs to be removed, tracking of ladder is now unimportart
    - cancel_acked : transient status to allow OrderKeep to remove the orders
    - filled : order needs to be removed (and possibly booked)

    update: becase of floating poitn errors, 'price' may be a string. Thread carefully
    not implemented yet:
    - strat: repeg, limit after, limit if ticks
    """

    def __init__(self, symbol, orderQty, price, id_level=None, ordType="Limit", execInst="ParticipateDoNotInitiate",
                 strat=None):

        self.clOrdID = str(uuid4())
        self.logger = logging.getLogger("Order {}".format(self.clOrdID[:4]))
        self.logger.setLevel(logging.DEBUG)
        self.orderID = None
        self.ts = None
        self.ts_exec = None  # this is for fills
        self.symbol = symbol
        self.ordType = ordType
        if self.ordType == "Market":
            self.price = None
            self.debug("discarding price for market order")
        else:
            # hook for float
            self.price = red(price)

        self.execInst = execInst
        self.orderQty = orderQty
        if self.orderQty > 0:
            self.side = 'Buy'
        elif self.orderQty < 0:
            self.side = 'Sell'
        else:
            raise InconsistentOrderData("Qty is wrong: {}".format(orderQty))

        self.status = 'new'  # 'processed' 'on_ladder' 'canceled'
        if id_level:
            self.id_level = id_level
        else:
            self.id_level = None

        self.size_before = None
        self.size_after = None
        # wait for my update how long
        self.saw_myself = False  # this is mostly for debugging purposes
        self.wait = 0.5  # seconds

        # trader action tracking
        self.ws_ack = False
        self.ws_working = False
        self.debug("alive with ordQty {}, price {}, status {}, lvl {}, orderID {}".format(self.orderQty,
                                                                                          self.price, self.status,
                                                                                          self.id_level, self.orderID))

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def pr_if_no_lvl(self):
        """
        this should help with list comperehence
        :return: price or None if id_level is set
        """
        if not self.id_level:
            return self.price

    def upd_level(self, id_lst):
        """
        :param id_list list with 0: level and 1: size. output of get_id with_size = True
        :return:
        """
        if id_lst:
            self.id_level = id_lst[0]
            self.size_before = id_lst[1] - abs(self.orderQty)
            self.size_after = 0
            self.status = 'on_ladder'
            self.debug("status updated to on_ladder at recover")

    def process_diff_msg(self, d_m_lst):
        """
        integrates a message (for now of 'id' and 'size') in the size_before and after
        1. I have nothing yet
        2. I have myself
        :param d_m:
        :return: Nothing
        """
        for d_m in d_m_lst:
            # print(d_m)
            if not self.id_level:
                self.warn("I dont have a level on the book yet")
            elif d_m['id'] == self.id_level:
                incSize = d_m['size']
                oldSize = d_m['size_old']

                if self.status == 'on_ladder':
                    # size before and after should not be zero
                    if self.size_after is None or self.size_before is None:
                        raise InconsistentOrderData("order is on_ladder, but with no size. Logic issue somewhere")

                    if incSize > 0:
                        # it goes after us
                        self.size_after += incSize
                    elif incSize < 0:
                        # conservatively, I assume size is removed from behind
                        if abs(incSize) <= self.size_after:
                            self.size_after += incSize
                        else:
                            self.size_before = self.size_before + incSize + self.size_after
                            self.size_after = 0
                    else:
                        raise InconsistentOrderData("size is weird: {}".format(str(incSize)))

                    # a quick check (and possibly correct after testing) TODO
                    if oldSize + incSize != abs(self.orderQty) + self.size_before + self.size_after:
                        # oldSize + incSize = new level size  vs. our total level calc is !=
                        self.warn(
                            "sizes update mismatch: {}. Old {}, Increm {}. before {}, me {}, after {}. saw myself {}".format(
                                str(abs(self.orderQty) + self.size_before + self.size_after - oldSize + incSize),
                                str(oldSize),
                                str(incSize),
                                str(self.size_before),
                                str(self.orderQty),
                                str(self.size_after),
                                str(self.saw_myself)))
                    else:
                        self.debug("L2 msg: {}. Old {}, Increm {}. before {}, me {}, after {}. saw myself {}".format(
                                str(abs(self.orderQty) + self.size_before + self.size_after - oldSize + incSize),
                                str(oldSize),
                                str(incSize),
                                str(self.size_before),
                                str(self.orderQty),
                                str(self.size_after),
                                str(self.saw_myself)))

                elif self.status == 'processed':
                    # I probably don't have size before and after. I can try to see myself, but if I don't I'll cehck time
                    # testing on my size is pretty much all I can do otherwise, I might get updates before, but not for very long
                    if incSize == abs(self.orderQty):
                        self.size_before = oldSize
                        self.size_after = 0
                        self.status = "on_ladder"
                        self.saw_myself = True

                    elif self.secs_on_mkt() and self.secs_on_mkt() > self.wait:
                        self.size_before = oldSize + incSize - abs(self.orderQty)
                        self.size_after = 0
                        self.status = "on_ladder"
                        self.debug("on_ladder now because I waited too long. Difference {}. Old {}, Increm {}. before {}, me {}, after {}. saw myself {}".format(
                                str(abs(self.orderQty) + self.size_before + self.size_after - oldSize + incSize),
                                str(oldSize),
                                str(incSize),
                                str(self.size_before),
                                str(self.orderQty),
                                str(self.size_after),
                                str(self.saw_myself)))

    def secs_on_mkt(self):
        """
        returns difference between time at markt and now
        :return: float (seconds)
        """
        if not self.ts:
            return None
        return sec_now(self.ts)

    def post_format(self):
        """

        :return: dict with the right format for posting

        """
        ord = dict(symbol=self.symbol,
                   price=self.price,
                   orderQty=self.orderQty,
                   clOrdID=self.clOrdID)
        if self.ordType == "Market":
            ord['ordType'] = "Market"
        elif self.ordType == "Limit":
            ord['execInst'] = self.execInst
        else:
            raise InconsistentOrderData("order type not Market or Limit")
        return ord

    def q_and_time(self):
        """
        a function to be called form orderKeep to provide details relevant to exectuion
        :return: dict with
        """
        ord = dict(symbol=self.symbol,
                   price=self.price,
                   orderQty=self.orderQty,
                   clOrdID=self.clOrdID)
        if self.ordType == "Market":
            ord['ordType'] = "Market"
        elif self.ordType == "Limit":
            ord['execInst'] = self.execInst
        else:
            raise InconsistentOrderData("order type not Market or Limit")

        # this can be none
        ord['t_market'] = self.secs_on_mkt()

        if self.size_before is not None and self.size_after is not None: # can be validly zero to I need to test the Nonetype
            ord['q_pos'] = round(self.size_before/(self.size_before + self.size_after + abs(self.orderQty)), 3)
        else:
            ord['q_pos'] = 1.
        return ord

    def process_ack(self, ack):
        """

        validates presence in ack and enrich with orderID and ts
        also resets size_before and size_after along with status to processed for amended orders
        :param ack list of dicts returned by the request
        :return: orderID, timestamp added if clOrdID matches
        """
        res = [dict(orderID=x['orderID'], ts=x['timestamp'], ordStatus=x['ordStatus']) for x in ack if
               x['clOrdID'] == self.clOrdID]
        if res != []:
            self.debug("this is for me {}".format(res))

        if len(res) == 1:
            if 'error' in res[0].keys():
                self.warn("execution error: {}".format(res[0]['error']))
            else:
                if res[0]['ordStatus'] == 'Filled':
                    self.status = 'filled'
                elif res[0]['ordStatus'] == 'Canceled':
                    self.status = 'cancel_ack'
                elif self.status == "amend":
                    self.ts = res[0].get('ts')
                    self.status = 'processed'
                    self.size_after = None
                    self.size_before = None
                else:
                    # neither should be none, but
                    self.orderID = res[0].get('orderID')
                    self.status = 'processed'
                self.ts = res[0].get('ts')

                self.debug("I'm processed from ack, status now {}".format(self.status))
        elif len(res) > 1:
            raise Exception("wtf more than one result in ack. doing nothing")  # TODO WTF exception

    def process_ws_messages(self, msg):
        """
        msg formats are similar to the API's. After submission, two messages will come first:
        - an ack message with the main characteristics of the order with workingIndicator == False
        - an update message with the workingIndicator set to True
        Then, either a fill message (including partials) or
        a cancel message

        Since all are ex-post, they should be processed immediately:
        1. compare/confirm the orderID with the 1st
        2. note that it's working in the second

        3. adjust quantity in the case of partial, or book the whole order at avgPx for fills (return)

        4. remove the order in case of cancel

        :param msg: the ws message format (dict with list at 'data' key
        :return: a dict subset of the final ack with clOrdID, symbol, timestamp, ordQty, avgPx (needs to be parsed to datetime)
        """
        if msg['table'] != 'order':
            raise WrongInput("The message is not about orders, table is : {}".format(msg['table']))
        elif msg['action'] == 'partial':
            raise WrongInput("partials are not handled at the order level")
        elif self.clOrdID in [x['clOrdID'] for x in msg['data']]:
            rel_dat = [x for x in msg['data'] if x['clOrdID'] == self.clOrdID][0]
            if msg['action'] == "insert":
                # check orderID
                if not self.orderID:
                    self.orderID = rel_dat['orderID']
                self.status = 'processed'  # this might race with the API :-( TODO check if it does
            # this part is about the second message coming in
            elif msg[
                'action'] == "update" and not self.ws_working and not rel_dat.get('ordStatus'):
                try:
                    self.ws_working = rel_dat['workingIndicator']
                except KeyError:
                    self.warn("couldn't change working indicator with {}".format(rel_dat))
                except Exception as e:
                    self.warn("error at 2 message type {} with msg {}".format(str(e), msg))
            # this should be tested more in unit tests.
            elif msg['action'] == "update" and rel_dat.get('ordStatus') == 'Canceled':
                # this is and ack of cancel
                self.status = 'cancel_ack'
            elif msg['action'] == "update" and rel_dat.get('ordStatus') == 'Filled':
                # we update the price with avgPx for simpler processing (upd we probably don't care about it being a clot now (au contraire, even)
                try:
                    self.status = 'filled'
                    self.price = rel_dat['avgPx']
                    self.ts_exec = dt.datetime.strptime(rel_dat['timestamp'][:-1],
                                                        "%Y-%m-%dT%H:%M:%S.%f")  # for some reason the time zone doesnt parse
                    self.ts_exec.replace(tzinfo=dt.timezone.utc)
                except Exception as e:
                    self.warn("error processing fill {} for {}".format(str(e), rel_dat))
                    self.warn(traceback.format_exc(5))
            self.debug("processed a ws order message. status now {} | orderID {}".format(self.status, self.orderID))

        else:

            pass #since the message is not for that order



class OrderKeep:
    """
    a simple order manager that contains orders and aggregates inputs and output.  Abstracts outcome from execution
    ie. not "cancel that order" "orders I want is different now from it was"

    as much as possible, we'll pass functions as list comps
    methods:

    - outputs statistics and status about orders
    - input of orders (side, qty, type and execution mode)
    - optionally, register methods for bbo and get_id from an OrderBook object

    """

    def __init__(self, bulk_put=None, bulk_amend=None, bulk_cancel=None, bulk_query=None):

        """

        #:param get_id_level: fun should be implemented TODO MED raise if not implemented post dev
        :param bulkput: fun returns ack, code , message. ack is none if error, and message can be none
        :param bulkamend: fun
        :param bulkcancel: fun
        :param exec_flag: Threading Lock from the exchange interface

        """
        self.logger = logging.getLogger('Order Keep')
        self.logger.setLevel(logging.DEBUG)

        self.keep = dict()
        self.transactions = []
        self.bbo_fun = None  # this and the next are very poor design because at implementation in the NewTrader I need assignment AFTER instanciation
        self.get_id_lvl = None

        self.bulk_put = bulk_put
        self.bulk_amend = bulk_amend
        self.bulk_cancel = bulk_cancel
        self.bulk_query = bulk_query



        # async stuff
        self.exec_flag = False #this will eventually probably be another class, like Event or something
        self.exec_stack = []
        # async stuff
        self.worker_loop = asyncio.new_event_loop()
        self.worker = Thread(target=self.start_loop, args=(self.worker_loop,))
        # start loop after daemonization
        self.worker.daemon = True
        self.worker.start()

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def start_loop(self, loop):
        """Switch to new event loop and run forever"""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def add_order(self, data):
        """

        :param data: list of dicts with parameters: required: symbol,  orderQty,
         optional : price, id_level, type (default to "Limit"), execInst ( "ParticipateDoNotInitiate" or None), strat, status (for partials)

        checks for inconsistent orders TODO implement fat fingers and whatnots
        :return: nothing. Warnings and logs maybe
        """
        if not isinstance(data, list):
            raise InconsistentOrderData("Input is list of dict")
        for ord_i in data:
            if all(k in ord_i.keys() for k in ['symbol', 'orderQty']) and (
                    'price' in ord_i.keys() or ord_i.get('ordType') == 'Market'):
                # default to limit
                ordType = ord_i.get('ordType')
                price = ord_i.get('price')

                if ordType is None:
                    ordType = "Limit"
                if ordType == "Market" and price:
                    price = None
                    self.warn("disregarding price for market order")

                ord_d = Order(symbol=ord_i.get('symbol'),
                              orderQty=ord_i.get('orderQty'),
                              ordType=ordType,
                              price=ord_i.get('price')) # should be taken care of by red at order level

                # this is not relevant for market orders
                if ord_d.ordType != 'Market':
                    if ord_i.get("execInst"):
                        ord_d.execInst = ord_i.get("execInst")
                    if ord_i.get('strat'):
                        ord_d.strat = ord_i.get('strat')
                    if ord_i.get('id_level'):
                        ord_d.id_level = ord_i.get('id_level')

                    status = ord_i.get('status')

                    if status:
                        ord_d.status = 'processed'
                    # this is usefull for sync orders
                    if ord_i.get('clOrdID'):
                        ord_d.clOrdID = ord_i.get('clOrdID')
                    if ord_i.get('orderID'):
                        ord_d.orderID = ord_i.get('orderID')

                    elif self.get_id_lvl:
                        try:
                            ord_d.id_level = self.get_id_lvl(ord_i['price'], with_size=False)
                        except:
                            self.warn("no id level for that price")
                        # try to fetch it if a method was registered to do so from order book

                else:
                    ord_d.execInst = ord_d.strat = ord_d.id_level = None
                # appending now to a dict
                self.keep[ord_d.clOrdID] = ord_d

            else:
                raise IncompleteOrder(
                    "missing keys for order. Needs 'symbol', 'orderQty' and 'ordType' market OR 'price ")

            difSet = set(ord_i.keys()).difference(
                ['symbol', 'price', 'orderQty', 'clOrdID', 'id_level', 'execInst', 'strat', 'ordType', 'status',
                 'orderID'])

            if difSet > set():
                raise Warning("extra parameters I dont know how to interpret".format(str(difSet)))
        # basic wash check TODO implement
        if data != []:
            self.debug("book keep is now {} long".format(len(self.keep.keys())))

    def ord_report(self, ks=['symbol', 'status', 'orderQty', 'price', 'side', 'ordType', 't_market']):
        """
        returns order list and status
        :return: list of dicts
        """
        intm = [x for x in self.keep.values() if isinstance(x, Order)]  # remove Nones and stuff
        return [{k: v for k, v in x.__dict__.items() if k in ks} for x in intm]

    def exec_report(self, values = ['on_ladder', 'processed']):
        """
        returns list of dict pertaining to orders that are on_ladder
        :return: dict of lists for bid and ask, sorted by distance to mid price
        """
        intm = [x for x in self.keep.values() if isinstance(x, Order)]
        intm = [x for x in intm if x.status in values ]
        intm = [x.q_and_time() for x in intm]
        # we hook for flt order point / red
        bid = sorted([x for x in intm if x['orderQty'] > 0], key=dered(itemgetter("price")), reverse= True)
        #bid = [x for x in bid]
        ask = sorted([x for x in intm if x['orderQty'] < 0], key=dered(itemgetter("price")))
        #ask = [red(x) for x in ask]

        return {'bids' : bid, 'asks' : ask}

    def ord_idx_by_id(self, clOrdID):
        """

        :param clOrdID: string
        :return: index position of the order in self.keep for changes in place (to avoid if at all possible)
        """
        try:
            return [x.clOrdID for x in self.keep].index(clOrdID)

        except ValueError:
            return None

    def size_update(self, size_msg_list):
        """
        function to be passed to the orderbook manager as a callback. iterates over list to enrich "processed" orders
        tries to set id level
        :param size_msg_list list of dicts, hopefully with size only/mostly
        :return:
        """
        # first we check if an update is required
        clOrdID_no_id = [x.clOrdID for x in self.keep.values() if x.id_level is None]
        if clOrdID_no_id != []:
            self.id_level_update()
        for x in self.keep.values():
            x.process_diff_msg(size_msg_list)

    def id_level_update(self):
        """
        gets the order book get_id method as argument, and iterate over Orders with no id level
        :param upd_fun: fun
        :return:
        """
        if self.get_id_lvl is None:
            raise Exception("no registered method")
        for order in self.keep.values():
            if order.id_level is None and order.status == 'processed':
                order.upd_level(self.get_id_lvl(order.price))

    def ack_update(self, ack):
        """
        passes Order.process_ack to the list of orders
        :param ack: list of acks
        :return:
        """
        for x in self.keep.values():
            x.process_ack(ack)
        self.debug("len of keep now {}".format(len(self.keep.keys())))

    def orders_sync(self, data, force=True):
        """
        in case of issue, we might want to re-sync the book. A typical case would be a trader reconnection, but we can also force an API call

        the assumption is that the data is right, but we:
        00. if we have an empty data, we do nothing
        0. in case of force=True, we need to filter by workingIndicator as we will get all orders. We also might need a Lock  as we're trading and stuff happens TODO think about it
        1. keep whatever matches for clOrdID, orderQty, symbol, price (market orders are gone in case of update anyway), but update qty if the three match
        2. if something remains, create orders accordingly
        2. if some orders are still there, they can be removed although we should query if they were in fact filled (for book consistency)
        :param data:
        :param force:
        :return:
        """

        if data != []:
            # do nothing otherwise
            if force:
                data = [x for x in data if x['workingIndicator'] == True]
            # we will compare subsets
            # flt pt issue conversion
            data = [red(x) for x in data]
            data = [{k: v for k, v in x.items() if k in ['clOrdID', 'orderQty', 'symbol', 'price', 'orderID']} for x in
                    data]
            # copy, not move in place (TODO is deepcopy required ?)
            keep = dict()
            # remaining orders from the ack

            remain = []
            for order in self.keep.values():  # TODO with dicts instead this is prob unencessarily convoluted
                intm_comp = {k: v for k, v in order.__dict__.items() if k in ['clOrdID', 'orderQty', 'symbol', 'price']}
                for ack_o in data:
                    if {k: v for k, v in ack_o.items() if k in ['clOrdID', 'symbol', 'price']} == {j: f for j, f in
                                                                                                   intm_comp.items() if
                                                                                                   ['clOrdID', 'symbol',
                                                                                                    'price']}:
                        # we compare ordQty, possibly adjust (and inform) and we copy for keep (order) and remain (ack element)
                        if ack_o['ordQty'] != order.orderQty:
                            self.debug("adjusting quantity from market for clOrdID {}".format(order.clOrdID))
                        keep[order.clOrdID] = order
            # now we should have a list of orders that matched/are adjusted
            self.keep = keep
            remain = [x for x in data if x['clOrdID'] not in [y.clOrdID for y in keep]]
            # if we have orders to add we add them as "processed"
            if remain != []:
                for x in remain:
                    x['status'] = 'processed'
                self.add_order(remain)

    def rem_cancel_acks(self):
        """
        wrapper to remove orderss that were canceled
        :return: nothing
        """
        cncled_clOrdIDs = [x.clOrdID for x in self.keep.values() if x.status == 'cancel_ack']
        if cncled_clOrdIDs != []:
            self.debug("canceling for {}".format(cncled_clOrdIDs))
            self.debug("self keep was {}".format(len(self.keep.keys())))
            for clOrdID in cncled_clOrdIDs:
                del self.keep[clOrdID]
            self.debug("self keep is now {}".format(len(self.keep.keys())))


    def fill_account(self):
        """
        simply record the transaction to a buffer, that can be processed and emptied as needed
        :return:
        """
        filled_clOrdIDs = [x.clOrdID for x in self.keep.values() if x.status == 'filled']
        for clOrdID in filled_clOrdIDs:
            self.transactions.append({k: v for k, v in self.keep[clOrdID].__dict__.items() if
                                      k in ['ts', 'ts_exec', 'symbol', 'orderQty', 'price']}) # may or may not work :-(
            del self.keep[clOrdID]


    def ws_update(self, ws_msg):
        """
        this will pass the message data to the individual orders. In case of partial, we need to compare if we have all orders
        At reboot, we'll have a keep of 0, but in case of socket reboot that wont be the case
        :param ws_msg:
        :return:
        """
        if ws_msg['action'] == 'partial':
            self.debug("partial: {} ".format(ws_msg['data']))
            self.orders_sync(ws_msg['data'])

        else:
            # we let the orders do what they must
            for order in self.keep.values():
                order.process_ws_messages(ws_msg)
                # now we account and remove orders
            self.rem_cancel_acks()
            self.fill_account()

    def execute_target(self, pos_list):
        """
        gets a list of dicts with symbol, orderQty, price or ordType to be executed. of the lenght of orders is different, the methow will add, amend or cancel
        1. we remove orders that match since nothing has to be done
        2. we cancel orders if no target remains
        3. we amend orders (smartly or not) if target is logner
        4. we put the rest

        relevant keys for sorting will be status (new,
        :param pos_list:
        :return:
        """
        # we process cancels and fills, just in case
        self.rem_cancel_acks()
        self.fill_account()
        # we don't want to execute while we're executing in the thread
        # we want to stack pos_lists and pop the last one when all cancel and whatnots return

        if self.exec_flag:
            self.debug("stack new pos_lists because flag is{}".format(self.exec_flag))
            self.exec_stack.append(pos_list)
            # not self.exec_lock or self.exec_lock.is_set(): # we get through is the lock is set
        elif self.exec_stack != []:
            self.debug("retrieving last pos")
            pos_list = self.exec_stack.pop(-1)
            self.exec_stack = []
        else:
            cur_orders = self.ord_report(['symbol', 'status', 'orderQty', 'ordType', 'price', 'ordType'])
            # if we dont have an ordType we assume limit
            for pos in pos_list:
                pos.setdefault('ordType', 'Limit')
            # market orders first. Only new orders are relevant, if any
            try:
                o_mkt_inp = list(filter(lambda a: a['ordType'] == 'Market', pos_list))
            except KeyError:
                o_mkt_inp = []
            # we need to filter out (and inform) market orders with a price input
            for order in o_mkt_inp:
                if not order.pop('price', None):
                    self.debug("disregarding price input")

            # we keep the rest for next steps note that if ordType is not explicit we assume a limit order
            try:
                remain_input = list(filter(lambda a: a['ordType'] != 'Market', pos_list))
            except KeyError:
                remain_input = []

            if o_mkt_inp != []:
                # which orders match
                rel_mkt_orders = [x for x in self.keep.values() if
                                  x.status in ['new', 'processed', 'on_ladder'] and x.ordType == 'Market']
                matched_mkt_orders = [x for x in rel_mkt_orders if dict(symbol=x.symbol,
                                                                        # price=x.price,
                                                                        orderQty=x.orderQty,
                                                                        ordType="Market") in o_mkt_inp]
                # conversely, the remaining orders can be filtered accordingly if need be
                if len(matched_mkt_orders) > 0:
                    # we need to multistep the matching to make it more palatable
                    fmt_matched_mkt_orders = [x for x in matched_mkt_orders if
                                              x.status in ['new', 'processed', 'on_ladder']]

                    # then we filter by formating in list of dict
                    fmt_matched_mkt_orders = [
                        {k: v for k, v in x.__dict__.items() if k in ['symbol', 'orderQty', 'ordType']} for x in
                        fmt_matched_mkt_orders
                    ]
                    # now it's easy'
                    o_mkt_inp = [x for x in o_mkt_inp if x not in
                                 fmt_matched_mkt_orders
                                 ]

                # we keep track or clOrdIDs for further filtering
                matched_mkt_orders = [x.clOrdID for x in matched_mkt_orders]

                # now we should have only incremental orders, but we might have had a case where a new market order did not go through exec(503 and whatnots)
                rel_mkt_orders = [x for x in rel_mkt_orders if x.clOrdID not in matched_mkt_orders]
                if len(o_mkt_inp) >= len(rel_mkt_orders):
                    # simple
                    self.add_order(o_mkt_inp)
                if len(o_mkt_inp) <= len(rel_mkt_orders):
                    for clOrdID in o_mkt_inp:
                        # self.keep as lis version
                        # idx = self.ord_idx_by_id(clOrdID)
                        self.keep[clOrdID].status = 'canceled'

            # Now for limit orders let find which orders match. Compared to market, "amend" orders are to be considered
            rel_orders = [x for x in self.keep.values() if
                          x.status in ['new', 'processed', 'on_ladder', 'amend'] and x.ordType == 'Limit']

            matched_orders = [x for x in rel_orders if dict(symbol=x.symbol,
                                                            price=x.price,
                                                            orderQty=x.orderQty,
                                                            ordType=x.ordType) in remain_input]
            # conversely, the remaining orders can be filtered accordingly if need be
            if len(matched_orders) > 0:
                remain_input = [x for x in remain_input
                                if x not in
                                [{k: v for k, v in y.__dict__.items() if
                                  k in ['symbol', 'price', 'orderQty', 'ordType']}
                                 for y in matched_orders]]

            # we keep track or clOrdIDs for further filtering
            matched_orders = [x.clOrdID for x in matched_orders]

            # now if we have the same number of orders remaining or more, we amend orders if we find some on the same side
            rel_orders = [x for x in rel_orders if x.clOrdID not in matched_orders]
            if len(rel_orders) >= len(remain_input):
                # it doesnt matter which order I change them (I think)
                for item in remain_input:
                    clOrdID = rel_orders.pop(0).clOrdID
                    # yikes, I need to acces by index
                    # idx = self.ord_idx_by_id(clOrdID)
                    self.keep[clOrdID].status = 'amend'
                    self.keep[clOrdID].price = item['price']
                    self.keep[clOrdID].orderQty = item['orderQty']

                # now we can cancel the rest (we popped values so we should be good)
                if len(rel_orders) > 0:
                    o_canc_in = [x.clOrdID for x in rel_orders]
                    for clOrdID in o_canc_in:
                        # idx = self.ord_idx_by_id(clOrdID)
                        self.keep[clOrdID].status = 'canceled'
            # we add orders missing (iindent is with the ln(rel_orders line)
            else:
                self.add_order(remain_input)

            # not_in = [x for x in pos_list if ]

            # order of operations :cancel, amend (can do in one shot ?) then put
            self.debug("setting exec flag")
            self.exec_flag = True

            self.debug("execute cancel")
            self.worker_loop.call_soon_threadsafe(self.cancels, )
            self.rem_cancel_acks()

            self.debug("execute amend")
            self.worker_loop.call_soon_threadsafe(self.amends, )
            self.debug("execute put")

            self.worker_loop.call_soon_threadsafe(self.put, )
            # I clean the book after


            self.fill_account()
            self.debug("clearing exec flag")
            self.exec_flag = False

            # release the fla

    def put(self):
        """
        passes the post function to registered post function
        :param ord_lst: lst of dict (Order.post_format)
        :return:
        """

        orders = [x.post_format() for x in self.keep.values() if x.status == 'new']

        if orders != []:
            if any(['clOrdID' not in x.keys() for x in orders]):
                self.warn("There is zero reason I don't have a clOrdID. list: {}".format(orders))
            self.debug("sending to market: {}".format(orders))
            if self.bulk_put:
                ack = self.bulk_put(orders)
            else:
                self.debug("put method is None")
                ack = None
            if ack:
                self.debug("processing ack")
                self.ack_update(ack)


    def cancels(self):
        """
        takes a list and passes it to the registered method
        :param clOrID_lst: lst
        :return:
        """
        cncl = [order.orderID for order in self.keep.values() if order.status == "canceled"]
        if cncl != []:
            if self.bulk_cancel:
                try:
                    ack = self.bulk_cancel(cncl)  # see signature
                except Http400 as e:
                    if str(e) == 'Invalid ordStatus':  # TODO using str(error) is probably not the nicest way to go about that
                        self.warn(
                            "Order Status error")  # TODO I need more direct order access method OrderKeep.keep as dict instead of list
                        # normally, the trader update would have udpated status (if execute strat is threaded though)
                        # i need to retrieve the clOrdIDs
                        clOrderID_list = [k for k, v in self.keep.items() if v.orderID in [x['orderID'] for x in cncl]]
                        for clOrdID in clOrderID_list:
                            if self.keep[clOrdID] in ['filled', 'cancel_ack']:
                                self.warn("Tried to cancel an order that was already gone, cleaning")
                                self.rem_cancel_acks()
                                self.fill_account()
                            else:
                                self.warn("something is wrong, forcing a sync from exchange")
                                self.query_status(clOrderID_list)
            else:
                self.debug("cancel method is None")
                ack = None
            if ack:
                self.ack_update(ack)


    def amends(self):
        """
        takes a list and passes it to the registered method

        ack processing should set the orders back to processed for position on the ladder tracking purposes
        :param clOrID_lst: lst
        :return:
        """

        amn = [{k: v for k, v in order.__dict__.items() if k in ['symbol', 'orderID', 'price', 'orderQty']} for order in
               self.keep.values() if order.status == "amend"]
        if amn != []:
            # it's possible I'm filled (or canceled even) at the time request reaches the exchange
            # I try, and catch the Http400 for 'Invalid ordStatus' to check what the keep has in memory

            if self.bulk_amend:
                try:
                    ack = self.bulk_amend(amn)  # see signature
                except Http400 as e:
                    if str(
                            e) == 'Invalid ordStatus':  # TODO using str(error) is probably not the nicest way to go about that
                        self.warn(
                            "Order Status error")  # TODO I need more direct order access method OrderKeep.keep as dict instead of list
                        # normally, the trader update would have udpated status (if execute strat is threaded though)
                        # i need to retrieve the clOrdIDs
                        clOrderID_list = [k for k, v in self.keep.items() if v.orderID in [x['orderID'] for x in amn]]
                        for clOrdID in clOrderID_list:
                            if self.keep[clOrdID] in ['filled', 'cancel_ack']:
                                self.warn("Tried to move an order that was already gone, cleaning")
                                self.rem_cancel_acks()
                                self.fill_account()
                            else:
                                self.warn("something is wrong, forcing a sync from exchange")
                                self.query_status(clOrderID_list)
                    else:
                        self.warn("other http400: {}".format(str(e)))
                    ack = None
                except Exception as e:
                    self.warn("issue: {}".format(str(e)))
                    ack = None

            else:
                self.debug('amend method is None')
                ack = None
            if ack:
                self.ack_update(ack)


    def query_status(self, clOrdID_list):
        """
        another function that needs to be registered.
        :param clOrdID_list list of IDs
        :return: nothing bu passes ack (if any not empty to self.process_ack
        """
        if clOrdID_list != []:
            # it's possible I'm filled (or canceled even) at the time request reaches the exchange
            # I try, and catch the Http400 for 'Invalid ordStatus' to check what the keep has in memory

            if self.bulk_query:
                try:
                    ack = self.bulk_query(clOrdID_list)  # see signature
                except Http400 as e:
                    self.warn("other http400: {}".format(str(e)))
                    ack = None
                except Exception as e:
                    self.warn("issue: {}".format(str(e)))

            else:
                self.debug('query method is None')
                ack = None
            if ack:
                self.ack_update(ack)

        else:
            self.warn("Trying to query an empty list")


class ExchangeInterface:
    """
    the mechanics of authenticating, putting, amending or canceling orders along with keeping track of call limits
    """

    def __init__(self, endpoint, apiKey, apiSecret, min_remain):
        """

        :param endpoint: str
        :param apiKey: str
        :param apiSecret: str
        :param max_remain: int
        """

        self.endpoint = endpoint
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.min_remain = min_remain
        self.act_remain = None

    def _auth(self):
        pass

    def put_orders(self, ords):
        pass

    def amend_orders(self, ords):
        pass

    def query_orders(self, ords_nmbrs):
        pass

    def cancel_orders(self, ords_nmbr):
        pass

    def _process_response(self, resp):
        pass

    def _process_error(self, e):
        pass


class BitmexInterface(ExchangeInterface):

    def __init__(self, test=True, **kwargs):
        """
        added parameted for the client in bitmex
        :param test:
        """
        super().__init__(**kwargs)
        self.client = bitmex.bitmex(test=test, api_key=self.apiKey, api_secret=self.apiSecret)
        self.logger = logging.getLogger("Bitmex If")
        self.logger.setLevel(logging.DEBUG)



    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)



    def put_orders(self, ords):
        """
        takes an order list, presumably from the order manager
        :param ords: list of dicts
        :return:
        """
        if not self.act_remain or self.act_remain > self.min_remain:
            self.debug("{} calls remaining".format(self.act_remain))



            try:
                # self.debug("stack, n-1 {}, | n-2 {}".format(inspect.stack()[1][3], inspect.stack()[2][3]))
                self.debug("put pushing to bitmex : {}".format(ords))
                st = time()
                # so I'm switing back to float if need be
                resp = self.client.Order.Order_newBulk(orders=json.dumps(dered(ords))).result()
                # self.debug("{} ms put wire time".format(1000 * (process_time() - st)))
                ack, code, message = self._process_response(resp)
                if code == 200:
                    self.debug("put success, ack is {}".format(ack))
                    self.debug("{} ms put ack wire time".format(1000 * (time() - st)))
                    # no other case for now
                    return ack

            except exception.HTTPServiceUnavailable as e:
                self.warn("failed to process out ack for {}".format(dered(ords)))
                self.debug("{} ms put ack wire time".format(1000 * (time() - st)))
                return None

            except exception.HTTPBadRequest as e:
                ack, code, message = self._process_error(e)
                self.debug("{} ms put ack wire time".format(1000 * (time() - st)))
                if code == 400:
                    raise Http400("bad formatting. Msg : {}".format(message))  # TODO maybe log ?
                if code == 429:
                    raise Http429("Rate limited!!!. Msg : {}".format(message))
                if code == 403:
                    raise Http403("we're banned. Whip the VPN out. Msg : {}".format(message))


    def amend_orders(self, ords):
        """
        lower level function that simply bothers with amends as they're sent. Drive by a higher function "difference" or something in OrderKeep
        :param self:
        :param ords: list of dict with orderID and price and/or size
        :return:
        """

        if not self.act_remain or self.act_remain > self.min_remain:
            self.debug("{} calls remaining".format(self.act_remain))


            try:

                self.debug("amend pushing to bitmex : {}".format(dered(ords)))
                st  =time()
                resp = self.client.Order.Order_amendBulk(orders=json.dumps(dered(ords))).result()

                ack, code, message = self._process_response(resp)
                if code == 200:
                    # no other case for now
                    self.debug("amend success, ack is {}".format(ack))
                    self.debug("{} ms amend wire time".format(1000 * (time() - st)))
                    return ack

            except exception.HTTPServiceUnavailable as e:
                self.warn("503!")
                self.debug("{} ms amend wire time".format(1000 * (time() - st)))
                return None

            except exception.HTTPBadRequest as e:
                ack, code, message = self._process_error(e)
                self.debug("{} ms amend wire time".format(1000 * (time() - st)))
                if code == 400:
                    raise Http400(message)  # TODO maybe log ?
                if code == 429:
                    raise Http429("Rate limited!!!. Msg : {}".format(message))
                if code == 403:
                    raise Http403("we're banned. Whip the VPN out. Msg : {}".format(message))


    def cancel_orders(self, ords):
        """
        lower level function that simply bothers with amends as they're sent. Drive by a higher function "difference" or something in OrderKeep
        :param self:
        :param ords: list of dict with orderID and price and/or size
        :return:
        """

        if not self.act_remain or self.act_remain > self.min_remain:
            self.debug("{} calls remaining".format(self.act_remain))



            try:

                self.debug("cancel pushing to bitmex : {}".format(ords))
                st = time()
                resp = self.client.Order.Order_cancel(orderID=json.dumps(ords)).result()

                ack, code, message = self._process_response(resp)
                if code == 200:
                    self.debug("cancel success, ack is {}".format(ack))
                    # no other case for now
                    self.debug("{} ms cancel wire time".format(1000 * (time() - st)))
                    return ack

            except exception.HTTPServiceUnavailable as e:
                self.debug("{} ms cancel wire time".format(1000 * (time() - st)))
                return None

            except exception.HTTPBadRequest as e:
                ack, code, message = self._process_error(e)
                self.debug("{} ms cancel wire time".format(1000 * (time() - st)))
                if code == 400:
                    raise Http400("bad formatting. Msg : {}".format(message))  # TODO maybe log ?
                if code == 429:
                    raise Http429("Rate limited!!!. Msg : {}".format(message))
                if code == 403:
                    raise Http403("we're banned. Whip the VPN out. Msg : {}".format(message))

    def query_orders(self, ords):
        """
        request information on orders, filtering by ClOrdId
        :param self:
        :param ords: list of clORdID
        :return: an ack, or None which would pretty much inevitably be an issue
        """

        if not self.act_remain or self.act_remain > self.min_remain:
            self.debug("{} calls remaining".format(self.act_remain))



            try:

                self.debug("query pushing to bitmex : {}".format(ords))
                st = time()
                resp = self.client.Order.Order_getOrders(filter=json.dumps({'clOrdID': ords})).result()
                self.debug("{} ms query wire time".format(1000*(time() - st)))
                ack, code, message = self._process_response(resp)
                if code == 200:
                    self.debug("cancel success, ack is {}".format(ack))
                    # no other case for now
                    return ack
                else:
                    self.warn("I received no ack back despite code 200!")

            except exception.HTTPServiceUnavailable as e:
                return None

            except exception.HTTPBadRequest as e:
                ack, code, message = self._process_error(e)

                if code == 400:
                    raise Http400("bad formatting. Msg : {}".format(message))  # TODO maybe log ?
                if code == 429:
                    raise Http429("Rate limited!!!. Msg : {}".format(message))
                if code == 403:
                    raise Http403("we're banned. Whip the VPN out. Msg : {}".format(message))

    def _process_response(self, resp):
        ack = resp[0]
        code = resp[1].status_code
        self.act_remain = int(resp[1].headers['X-RateLimit-Remaining'])
        return ack, code, None

    def _process_error(self, e):
        error_code = e.status_code  # int
        message = e.swagger_result['error']['message']
        return None, error_code, message
