import logging

from exceptions import NoIdLevel, NoPartial, WrongInput, WTF
from utilities import compare_and_update, red


####this is the actual class
class OrderBook:
    """
    a class that keeps track of order and order levels
    For convenience, we keep ids and ladder in two different stores
    :param symbol str
    :param depth int
    :param trk_level int for update reverse dict
    :param update_callback fun to call orders update or whatever after update
    """
    def __init__(self, symbol, update_callback = None):

        self.logger = logging.getLogger("Order Book")
        self.logger.setLevel(logging.DEBUG)

        self.symbol = symbol
        self.book = dict()
        #self.len = 2 *depth
        self.k_name = "orderBookL2_25"
        self.partial = False
        self.p_ladder = dict()
        self.callback = update_callback

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def _partial(self, msg):
        """
        fucntion to initialize the book at partial
        :param msg: list of dict
        :return: nothing
        """
        for item in msg:
            self.book[item['id']] = dict(side=item['side'],
                                            price=red(item['price']),
                                            size=item['size'])
        self.partial = True

    def _update(self,msg):
        """
        updates the relevant level, found by price (dict.update)
        :param msg: list of dict(s)
        :return: if there's a callback returns stuff. Otherwise returns nothing
        """
        if not self.partial:
            raise NoPartial("Cant init the book, not partials in")
        #unpack list
        diffs = []
        for item in msg:
            # hook the float point conv
            item = red(item)
            k = item.pop('id')
            d = compare_and_update(self.book[k], item)
            d['id'] = k

            diffs.append(d)

        if self.callback:

            return self.callback(diffs)



    def _insert(self, msg):
        if not self.partial:
            raise NoPartial("Cant init the book, no partials in")
            # unpack list
        for item in msg:
            # flt point change
            item = red(item)
            self.book[item.pop('id')] = item

    def _delete(self, msg):
        if not self.partial:
            raise NoPartial("Cant init the book, not partials in")
        for item in msg:
            #flt pt red
            item = red(item)
            del self.book[item['id']]

    def getmsg(self, msg):
        """
        gets the full message and decides
        :param msg:
        :return:
        """
        if msg['table'] != self.k_name:
            raise WrongInput("Not getting the right message in")

        if msg['action'] == 'partial':
            self._partial(msg['data'])
        elif msg['action'] == 'update':
            self._update(msg['data'])
        elif msg['action'] == 'delete':
            self._delete(msg['data'])
        elif msg['action'] == 'insert':
            self._insert(msg['data'])
        else:
            raise WrongInput("Action Type not recognized")
        #now we update the ladder
        self._ladder()

    def _ladder(self):
        self.p_ladder =  {v['price'] : dict(id=k,side=v['side']) for k, v in self.book.items()}


    def bbo(self, lvl=1):
        """
        read the keys and returns a dict of value or dict of list of values
        :return:
        """
        bb = sorted([float(k) for k,v in self.p_ladder.items() if v['side'] == 'Buy'], reverse=True)

        ba = sorted([float(k) for k,v in self.p_ladder.items() if v['side'] == 'Sell'])

        if lvl == 1:
            return {'bid' : bb[0], 'ask' : ba[0]}
        else:
            return {'bid': bb[:lvl], 'ask': ba[:lvl]}


    def get_id(self, price, side=None, with_size = True):
        """
        returns order id for a given price
        :param price:
        :param side: str Buy or Sell, optional
        :return: id int
        """
        if side:
            intm = [{ k : v} for k, v in self.book.items() if v['side'] == side]
        else:
            intm = self.book
        res = [[k, v['size']] for k,v in intm.items() if v['price'] == price]
        if len(res) == 1:
            if with_size:
                return res[0]#list
            else:
                return res[0][0]

        if res == []:
            self.warn("cant find id at this price: {}. I have \n{}".format(price, [x['price'] for x in self.book.values()]))
        else:
            raise WTF("I have more than one id level for the price. this is indicating a big screwup")



