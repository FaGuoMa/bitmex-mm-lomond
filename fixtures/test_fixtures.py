from random import randint
from utilities import dtnow
import datetime as dt
# this is a set of fixtures to facilitate the testing of the agent/trader
# We need to be able to generate :
# 1) partials and subsequent updates
# 2) acks (from websocket)

def partial_order_book(n_lvls = 20, ba = 0.0278, bb = 0.0277, tick_size = 0.0001, symbol = 'BCHZ18', ):
    """
    Generates partial  Size is some sort of randint

    Partial in the format:
    {'table': 'orderBookL2_25', 'action': 'partial', 'keys': ['symbol', 'id', 'side'],
     'types': {'symbol': 'symbol', 'id': 'long', 'side': 'symbol', 'size': 'long', 'price': 'float'},
     'foreignKeys': {'symbol': 'instrument', 'side': 'side'},
     'attributes': {'symbol': 'grouped', 'id': 'sorted'}, 'filter': {'symbol': 'TRXZ18'},
     'data': [{'symbol': 'TRXZ18', 'id': 39799999406, 'side': 'Sell', 'size': 1000000, 'price': 5.94e-06},
              {'symbol': 'TRXZ18', 'id': 39799999544, 'side': 'Sell', 'size': 50000, 'price': 4.56e-06},
              {'symbol': 'TRXZ18', 'id': 39799999550, 'side': 'Sell', 'size': 2001, 'price': 4.5e-06},
              {'symbol': 'TRXZ18', 'id': 39799999556, 'side': 'Sell', 'size': 3085973, 'price': 4.44e-06},
              {'symbol': 'TRXZ18', 'id': 39799999564, 'side': 'Sell', 'size': 1000, 'price': 4.36e-06},

    deltas:
    to be implemented


    :param n_lvls: int levels *each* side
    :param ba: float best ask at instantiation
    :param bb: float best bid
    :param tick_size: float
    :return: dict message
    """
    raw_resp = {'table': 'orderBookL2_25', 'action': 'partial', 'keys': ['symbol', 'id', 'side'],
     'types': {'symbol': 'symbol', 'id': 'long', 'side': 'symbol', 'size': 'long', 'price': 'float'},
     'foreignKeys': {'symbol': 'instrument', 'side': 'side'},
     'attributes': {'symbol': 'grouped', 'id': 'sorted'}, 'filter': {'symbol': symbol},
     'data': []}

    #buy
    for i in range(0,n_lvls):
        raw_resp['data'].append({'symbol': symbol, 'id': 3900000000 + 50*i, 'side': 'Buy', 'size': randint(1,10)*10, 'price': bb - i *tick_size})
    # sell
    for i in range(0, n_lvls):
        raw_resp['data'].append(
            {'symbol': symbol, 'id': 4200000000 + 50 * i, 'side': 'Sell', 'size': randint(1, 10) * 10,
             'price': ba + i * tick_size})

    return raw_resp

#GUT
# print(partial_order_book())

def deltas_orderbook(order_book, deltas, ws_ack=None):
    """
    generates delta ladder message, possibly based on an ack for status check

    {'table': 'orderBookL2_25', 'action': 'update',
                'data': [{'symbol': 'XBTUSD', 'id': 15599609650, 'side': 'Buy', 'size': 284}]}

    :param order_book: an orderBook object properly instantiated
    :param deltas: list (if ws_ack is None) of [price,qty]. Disregared if an ack is provided
    :param ws_ack: a pseudo exchange ack
    :return: a message dict
    """
    raw_msg = {'table': 'orderBookL2_25', 'action': 'update',
                'data': []}
    if ws_ack:
        for ack in ws_ack:

            id_level = order_book.get_id(ack['price'])[0]
            if ack['orderQty'] > 0:
                side = 'Buy'
            else:
                side = 'Sell'

            raw_msg['data'].append({'symbol': ack['symbol'], 'id': id_level, 'side': side, 'size': ack['orderQty']})

    else:
        print("not implemented")

    return raw_msg

def orders_ack_gen(ordkeep):
    """
    gets "new" orders in a keep, and generate a related ack
    :param ordkeep:
    :return:
    """
    ords =  ordkeep.ord_report(['symbol', 'price', 'clOrdID', 'orderQty'])
    res = []
    cnt = 10

    for order in ords:
        #orderQty is possibly a string (red/dered for floeting point error management)
        # if isinstance(order['orderQty'], str):
        #     if float(order['orderQty']) < 0:
        #         qty = ""
        qty = order['orderQty']

        res.append({'orderID': cnt ,
                    'clOrdID': order['clOrdID'],  # order in list
                    'clOrdLinkID': '',
                    'account': 115737,
                    'symbol': 'BCHZ18',
                    'side': 'Buy',
                    'simpleOrderQty': None,
                    'orderQty': qty,
                    'price': order['price'],
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
                    'transactTime': dtnow() - dt.timedelta(seconds=2) ,
                    'timestamp': dtnow()- dt.timedelta(seconds=2)})
        cnt +=1
    return res