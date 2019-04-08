from lomond.websocket import WebSocket
from lomond.persist import persist
from lomond import events
import json
import logging
import traceback
from abc import ABC, abstractmethod

from utilities import generate_nonce, generate_signature_bitmex, build_requests, findItemByKeys, avg_price_inv

from time import sleep
from config import connect
from orderbook import OrderBook
from orders import Order, OrderKeep, BitmexInterface
from agent.agent import MM

# suppress useless warnings
logging.getLogger("lomond").setLevel(logging.WARNING)

"""
This module will encompass a clear api for creating and generating Trader under the following principles
1) init will only be used create storage variables, and not make function calls (better for overrides/inheritance)
2) each instance or subclass of a trader connects to 1 specific end point or service
3) Abstract base class will encapsulate any boiler plate required to have a common API / boiler plate
4) for end user use of multiple connections requires a higher level facade API to provide access to multiple instances
5) functionality or external calls will be passed as classes to be mounted on the instantiated class as required
"""


class Trader(ABC):
    """
    Trader is an ABC providing a clear cut interface for all subsequent inherited trader handlers for any given
    exchange.

    The goal of the derived trader object is to provide a single connection interface which similar API calls to any
    given function and provide easy overloading. Any specific parsing, mapping, or modification to messages can be
    handled internally before being passed out to any facade
    """

    @abstractmethod
    def boot(self):
        """
        will encompass running any type of function methods to boot the class
        """
        raise NotImplementedError("Should implement boot()")

    @abstractmethod
    def run(self):
        """
        Provides the event loop for lomond
        """
        raise NotImplementedError("Should implement run()")

    @abstractmethod
    def message_data_updater(self, message, received_time):
        """
        takes messages from the run loop dealing with them in a per connection specific way
        """
        raise NotImplementedError("Should implement message_data_updater()")

    @abstractmethod
    def _prep_connection(self):
        """
        preparing connection to given WS
        :return:
        """
        raise NotImplementedError("Should implement _prep_connection()")

    @abstractmethod
    def _subscribe(self, ws):
        """
        subscribe to channels for given WS
        :param ws websocket
        :return:
        """
        raise NotImplementedError("Should implement _subscribe()")

    @abstractmethod
    def recent_trades(self, n=10):
        """
        retrieves the last N recent trades
        :param n: int
        :return: list
        """

        raise NotImplementedError("Should implement recent_trades()")

    @abstractmethod
    def get_inventory(self):
        """
        basic inventory calculation
        :return:
        """
        raise NotImplementedError("Should implement get_inventory()")

    @abstractmethod
    def inv_avg_price(self):
        """
        get the average price (utility function)
        :return:
        """
        raise NotImplementedError("Should implement inv_avg_price()")

    @abstractmethod
    def margin_report(self):
        """
        retrieves initial margin balance and current margin balance
        :return: float, float
        """

        raise NotImplementedError("Should implement margin_report()")


class Bitmex(Trader):
    def __init__(self, myname):

        self.whatsmyname = myname
        self.logger = logging.getLogger(self.whatsmyname)
        self.logger.setLevel(logging.DEBUG)

        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d|%(levelname)-8s|%(name)-10s|  %(message)s',
            level=logging.INFO,
            datefmt='%M:%S')

        # class vars
        self.data = {}
        self.keys = {}
        self.partials = []
        self.ord_keep = None
        self.book = None
        self.max_len = None
        self.agent = None
        self.init_margin_balance = None
        self.deadman_renew = None
        self.client = None
        self.rem_limit = None
        # ws specific
        self.subs = None
        self.symbol_list = None
        self.endpoint = None
        self.api_key = None
        self.secret = None

    def boot(self, conf=0, boot_client=True,
             deadman_renew=6,
             subs=None,
             symbol_list=None):

        """
        boot sequence and any specific params
        :param conf: config value
        :param boot_client: bool
        :param deadman_renew: int
        :param subs: list
        :param symbol_list: list
        """

        # using sentinels for defaults instead of mutables (these create memory errors that spawn deep copy issues)
        if subs is None:
            subs = ['orderBookL2_25', 'order', 'trade', 'margin']

        if symbol_list is None:
            symbol_list = ['BCHZ18']

        # testnet
        if conf == "test":
            # max
            self.endpoint = connect['test']['endpoint']
            self.api_key = connect['test']['apiKey']
            self.secret = connect['test']['apiSecret']
            test = True

        elif conf == 'prod':
            # trade@test
            self.endpoint = connect['prod']['endpoint']
            self.api_key = connect['prod']['apiKey']
            self.secret = connect['prod']['apiSecret']
            test = False
            self.warn("!!!!!!! YOU ARE RUNNING IN PROD !!!!!!!")

        else:
            raise Exception("conf must be of test or prod (str)")

        self.deadman_renew = deadman_renew  # every {} * 5 (poll intervalls) seconds
        # subs
        self.subs = subs
        self.symbol_list = symbol_list

        # data repo
        if boot_client:
            self.client = BitmexInterface(apiKey=self.api_key, apiSecret=self.secret, endpoint=self.endpoint,
                                          min_remain=30, test=test)
        else:
            self.client = None

            # TODO MED mount these externally, either via passing to boot or via object assignment
        self.ord_keep = OrderKeep(bulk_put=self.client.put_orders,
                                  bulk_amend=self.client.amend_orders,
                                  bulk_cancel=self.client.cancel_orders,
                                  bulk_query=self.client.query_orders)
        self.book = OrderBook(self.symbol_list[0],
                              update_callback=self.ord_keep.size_update)  # TODO MED: this only gets one symbol. For actual trading, we need more
        # I need to patch the method after instantiation :-/
        self.ord_keep.get_id_lvl = self.book.get_id
        self.max_len = 5000

        # trading stuff
        self.agent = MM(symbol_list=self.symbol_list,
                        bbo=self.book.bbo,
                        get_inventory=self.get_inventory,
                        get_inv_avg_price=self.inv_avg_price,
                        execute=self.ord_keep.execute_target,
                        margin_report=self.margin_report,
                        request_trades=self.recent_trades,
                        order_report=self.ord_keep.exec_report)

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

    def _prep_connection(self):
        ws = WebSocket(self.endpoint, compress=True)
        apikey = self.api_key
        secret = self.secret
        nonce = generate_nonce()
        ws.add_header(str.encode("api-nonce"), str.encode(str(nonce)))
        ws.add_header(str.encode("api-signature"),
                      str.encode(str(generate_signature_bitmex(secret, 'GET', '/realtime', nonce, ''))))
        ws.add_header(str.encode("api-key"), str.encode(str(apikey)))
        return ws

    def message_data_updater(self, message, received_time):
        '''Handler for parsing WS messages.
        message is json parsed
        data and ks are dicts (to be onboarded in the class
        I need a different dict to make sure I don
        '''
        # message = json.loads(message)
        # self.logger.debug(json.dumps(message))

        table = message['table'] if 'table' in message.keys() else None
        action = message['action'] if 'action' in message.keys() else None
        try:
            # if 'subscribe' in message:
            #     self.logger.debug("Subscribed to %s." % message['subscribe'])
            if action:
                if table not in self.data:
                    self.data[table] = []

                # There are four possible actions from the WS:
                # 'partial' - full table image
                # 'insert'  - new row
                # 'update'  - update row
                # 'delete'  - delete row
                if action == 'partial':
                    # print(message)
                    # self.logger.debug('\n %s: partial %s \n' % (table, message['data']))
                    self.data[table] += message['data']
                    self.keys[table] = message['keys']
                    self.partials.append(table)

                    if table == 'margin' and 'marginBalance' in message['data'][0].keys():
                        if not self.init_margin_balance:
                            self.init_margin_balance = message['data'][0]['marginBalance']

                elif action == 'insert' and table in self.partials:
                    # print(message)
                    # self.logger.debug('\n %s: inserting %s \n' % (table, message['data']))
                    self.data[table] += message['data']
                    # Limit the max length of the table to avoid excessive memory usage.
                    # Don't trim orders because we'll lose valuable state if we do.
                    if table not in ['order', 'orderBookL2'] and len(self.data[table]) > self.max_len:
                        self.data[table] = self.data[table][int(self.max_len / 2):]

                elif action == 'update' and table in self.partials:
                    # print(message)
                    # self.logger.debug('\n %s: updating %s \n' % (table, message['data']))
                    # Locate the item in the collection and update it.
                    for updateData in message['data']:
                        item = findItemByKeys(self.keys[table], self.data[table], updateData)
                        item.update(updateData)

                elif action == 'delete' and table in self.partials:  # TODO this should no necessarily be a problem as we would remain if everybody else cancels
                    # self.logger.debug('%s: deleting %s' % (table, message['data']))
                    # Locate the item in the collection and remove it.
                    for deleteData in message['data']:
                        item = findItemByKeys(self.keys[table], self.data[table], deleteData)
                        self.data[table].remove(item)

                elif table not in self.partials:
                    self.debug("discarding incomplete data")

                elif action not in ['delete', 'update', 'insert', 'partial']:

                    raise Exception("Unknown action: %s" % action)
        except:
            self.logger.warning(traceback.format_exc())

    def recent_trades(self, n=10):
        """
        retrieves the last N recent trades
        :param n: int
        :return: list
        """
        if 'margin' in self.partials:
            print(self.data['trade'])
            return self.data['trade'][-n:]

        else:
            return None

    def get_inventory(self):
        """
        basic inventory calculation
        :return:
        """
        if self.ord_keep.transactions != []:
            return sum([x['orderQty'] for x in self.ord_keep.transactions])
        else:
            return 0

    def inv_avg_price(self):
        """
        get the average price (utility function)
        :return:
        """
        if self.ord_keep.transactions != []:
            return avg_price_inv(self.symbol_list[0], self.ord_keep.transactions)
        else:
            return None

    def margin_report(self):
        """
        retrieves initial margin balance and current margin balance
        :return: float, float
        """

        if 'margin' in self.partials:
            return self.init_margin_balance, self.data['margin'][0]['marginBalance']
            #print("m bal: {}\n{}".format(self.init_margin_balance,self.data['margin'][0]['marginBalance']))
        else:
            return None, None

    def _subscribe(self, ws):
        subs_args = build_requests(self.subs, self.symbol_list)

        if len(subs_args) > 10:
            for i in range(0, len(subs_args), 10):
                # Create an index range for l of n items:
                ws.send_json({"op": "subscribe", "args": subs_args[i:i + 10]})
        else:
            ws.send_json({"op": "subscribe", "args": subs_args})
        # margin
        ws.send_json({"op": "subscribe", "args": "margin"})

    def run(self):
        cnt_deadman = 0  # recommended is 15 seconds, but 30 should do for dev
        cnt2 = 0  # ghetto reducing spamm

        subs_args = build_requests(self.subs, self.symbol_list)
        ws = self._prep_connection()

        for event in persist(ws):

            if isinstance(event, events.Rejected):
                self.logger.warning(str(event.response))
                self.warn(event.response)

            if isinstance(event, events.BackOff):
                self.warn("backing off for {} s".format(str(event.delay)))
                sleep(event.delay)
                ws.close()
                self.run()  # regen nonce and stuff

            if event.name == "ready":
                # send deadman switch
                ws.send_json({"op": "cancelAllAfter", "args": 60000})
                self._subscribe(ws=ws)

            if isinstance(event, events.Text):
                msg = (json.loads(event.text))
                # print(msg)
                # now we get the limit value from welcome message (or rate limit, later)#TODO MED test it rough!!!
                if 'info' in msg.keys() and 'limit' in msg.keys():
                    self.rem_limit = msg['limit']
                # we check and ack subscriptions
                if 'success' in msg.keys() and 'subscribe' in msg.keys():
                    try:
                        subs_args.remove(msg['subscribe'])
                    except:
                        self.warn("that's weird : {} was not to be sub'd".format(msg['subscribe']))
                    if len(subs_args) == 0:
                        self.debug("all subs good to go")

                # # now we deal with L2
                if 'table' in msg.keys() and msg['table'] == 'orderBookL2_25':

                    self.book.getmsg(msg)
                    if self.book.partial:  # waiting for the order book
                        # self.toy_mm()
                        self.agent.on_l2()

                # # orders
                if 'table' in msg.keys() and msg['table'] == 'order':
                    # print(msg)
                    self.ord_keep.ws_update(msg)  # TODO this needs to be threadsafe

                if 'table' in msg.keys() and msg['table'] in ['trade', 'margin']:
                    self.message_data_updater(msg, event.received_time)
                    if msg['table'] == 'trade':
                        # we calculate state (trade ratio might change as a result)
                        self.agent.on_trade()

            if isinstance(event, events.Poll):
                cnt_deadman += 1
                print(self.ord_keep.exec_report())
                if cnt_deadman == self.deadman_renew:
                    # send deadman switch
                    self.debug("deadman re-activate")
                    ws.send_json({"op": "cancelAllAfter", "args": 60000})
                    cnt_deadman = 0

                try:
                    self.debug(self.book.bbo(lvl=5))
                except:
                    pass
                self.debug(self.ord_keep.ord_report())

                print("current inventory: {}".format(sum([x['orderQty'] for x in self.ord_keep.transactions])))
                avg_price = avg_price_inv(self.symbol_list[0], self.ord_keep.transactions)
                if avg_price:
                    print("holding at avg price {}".format(str(avg_price)))


# class Bitfinex(Trader):


if __name__ == "__main__":
    c = Bitmex(myname="devmm")
    c.boot(conf="test", symbol_list=['BCHM19'])
    c.run()
