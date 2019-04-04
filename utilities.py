import datetime as dt
import time, urllib, hmac, hashlib
from itertools import product
import re

####to utilities
def dtnow():
    return dt.datetime.now(dt.timezone.utc)

def sec_now(ts):
    return (dtnow() - ts).total_seconds()


# general utility for decimal/floating point issue with small prices. Not ideal AT ALL
def red(flt, n_dec = 4):
    """
    alternative to round and display string
    :param flt: anything but only floats are affected, including in dicts and lists and tuples
    :return: string at the right decimal
    """
    if type(flt) is float:
        if flt.__float__() <0.1:

            for i in range(n_dec, 10):

                if abs(flt.__float__()-flt.__round__(i)) < abs(flt.__float__())/10000.:
                    break
            return str(flt.__round__(i))

        else:
            return flt
    elif type(flt) is dict:
        return {red(k) : red(v) for k, v in flt.items()}
    elif type(flt) is tuple:
        return tuple((red(x) for x in flt))
    elif type(flt) is list:
        return [red(x) for x in flt]

    else:
        return flt


def dered(stuff):
    """
    reverses the operation, that is seeks string that are in e-XX format and parses them to float
    :param stuff: str, dict, list or tuple
    :return:
    """

    if isinstance(stuff, str):
        # I need to make sure UUIDs are not processed ($ sign for EO string should be nough)
        regex = re.compile(r".*[e][-]\d{2}$")
        if regex.search(stuff):
            return float(stuff)
        else:
            return stuff
    elif isinstance(stuff, dict):
        return {dered(k) : dered(v) for k, v in stuff.items()}
    elif isinstance(stuff, list):
        return [dered(x) for x in stuff]
    elif isinstance(stuff, tuple):
        return tuple((dered(x) for x in stuff))
    else:
        return stuff


#for order book

##this will move to utilities
def compare_and_update(dict1, dict2):
    """
    this is used to identify differences at update of order book
    :param dict1:
    :param dict2:
    :return:
    """
    ks = dict1.keys() & dict2.keys()
    dif_d = dict()
    # print(ks)
    for k in ks:
        if dict1[k] != dict2[k]:
            dif_d[k] = dict2[k] - dict1[k]
            dif_d[k+"_old"] = dict1[k]
    dict1.update(dict2)
    return dif_d

#bitmex authentication and nonce gen

#authentication functions
def generate_nonce():
    return int(round(time.time() * 1000))

def generate_signature_bitmex(secret, verb, url, nonce, data):
    """Generate a request signature compatible with BitMEX."""
    # Parse the url so we can remove the base and extract just the path.
    parsedURL = urllib.parse.urlparse(url)
    path = parsedURL.path
    if parsedURL.query:
        path = path + '?' + parsedURL.query

    # print "Computing HMAC: %s" % verb + path + str(nonce) + data
    message = (verb + path + str(nonce) + data).encode('utf-8')

    signature = hmac.new(secret.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest()
    return signature


def generate_signature_bitfinex(secret, nonce):
        auth_payload = 'AUTH{}'.format(nonce)
        signature = hmac.new(
        secret.encode(),
        msg=auth_payload.encode(),
        digestmod=hashlib.sha384
        ).hexdigest()


        return signature


def build_requests(subs, symbol_list):
    """
    takes subscriptions, symbols and builds bitmex compliant requests

    :param subs: str
    :param symbol_list: str
    :return: str
    """
    res = list(product(subs,symbol_list))
    return [":".join(x) for x in res]


def findItemByKeys(keys, table, matchData):
    """
    This is lifted from the bitmex mm original code in order to look for specific data in nested dicts
    :param keys: list
    :param table: list of dicts
    :param matchData: dict with key value
    :return:
    """
    for item in table:
        matched = True
        for key in keys:
            if item[key] != matchData[key]:
                matched = False
        if matched:
            return item


def avg_price_inv(symbol, transactions):
    """
    a simple function, probably to be ported to an indicator management class at one point, that calculates the avg
    price of held inventory from transactions
    :return: an avg price or None if there is no inventory
    """
    cur_inv = sum([x['orderQty'] for x in transactions if x['symbol'] == symbol])
    if cur_inv != 0:
        transactions.reverse()
        qty = 0
        expenditure = 0
        for l in transactions:
            cur_inv = cur_inv - l['orderQty']
            qty = qty + l['orderQty']
            expenditure = expenditure + l['orderQty']*l['price']
            if cur_inv == 0:
                break
        return expenditure/qty
    else:
        return None
