from unittest import TestCase
from time import sleep
from mm import NewTrader

class TestThreading(TestCase):


    def setUp(self):
        self.mm = NewTrader("unit test", boot_client=True)#can test only loops this way

    def test_thread_put(self):

        self.mm.thread_print("zboub")
        print(type(self.test_thread_put))


        self.mm.ord_keep.execute_target([dict(symbol='XBTUSD', price=2000, orderQty=27)])
        sleep(2)