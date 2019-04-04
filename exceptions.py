
### to exceptions
class InconsistentOrderData(Exception):
    pass

class IncompleteOrder(Exception):
    pass

class Http400(Exception):
    pass

class Http429(Exception):
    pass

class Http403(Exception):
    pass

class NoExchangeMethod(Exception):
    pass
#for orderbook

##this will move to exceptions
class WrongInput(Exception):
    pass

class NoPartial(Exception):
    pass

class WTF(Exception):
    pass

class NoIdLevel(Exception):
    pass