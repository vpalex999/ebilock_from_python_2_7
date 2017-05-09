import sys
import os
from twisted.trial import unittest
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet import defer
from twisted.test import proto_helpers
import binascii
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from testserver.server import ServerEHAFactory





class RemoteClientTestCase(unittest.TestCase):

    def setUp(self):

        self.port1 = 10000
        self.port2 = 10001
        self.host = "localhost"
        self.factory1 = ServerEHAFactory()
        # self.factory2 = ServerEHAFactory()
        from twisted.internet import reactor
        self.port1 = reactor.listenTCP(self.port1, self.factory1, interface=self.host)
        # self.port2 = reactor.listenTCP(self.port2, self.factory2, interface=self.host)
        # reactor.run()
        # self.client = None

    def tearDown(self):
        self.port1.stopListening()
        # self.port2.stopListening()

    def test_1(self):
        def check_connect():
            print("activate check connect after 2c!")
            self.assertTrue(self.factory1.check_connect())
            
        print(self.factory1.check_connect())
        self.assertTrue(self.factory1.check_connect())


        # from twisted.internet import reactor
        # reactor.callLater(2, check_connect)


    # def reactor_down(self, _):
    #     from twisted.internet import reactor
    #     # reactor.callLater(2, self.reactor_stop)
    #     reactor.callLater(2, self.port1.stopListening())
    #     reactor.callLater(2, self.port2.stopListening())
# 
    # def reactor_stop(self):
    #     from twisted.internet import reactor
    #     reactor.callLater(0.0, self.d1.cancel)
    #     reactor.callLater(0.0, self.d2.cancel)
    #     reactor.stop()
# 
    # def d_status1(self, status):
    #     self.status1 = status
# 
    # def d_status2(self, status):
    #     self.status2 = status
# 
    # def test_connect_client_port1(self):
    #     """ test detecting connect from client to port1 """
    #     print(self.status1)
    #     self.assertTrue(self.status1)

    # def test_connect_client_port2(self):
    #     """ test detecting connect from client to port2 """
    #     print(self.status1)
    #     self.assertTrue(self.status2)

    

