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
from testserver.server import RemoteEHAFactory


def connect1_ok(reason):
    print("{} Connected 1 OK: {}".format(reason[0], reason[1]))
    return True


def connect2_ok(reason):
    print("{} Connected 2 OK: {}".format(reason[0], reason[1]))
    return True


def lost_connection1(reason):
    print("{} Connected 1 filed: {}".format(reason.value[0], reason.value[1]))


def lost_connection2(reason):
    print("{} Connected 2 filed: {}".format(reason.value[0], reason.value[1]))


class RemoteClientTestCase(unittest.TestCase):

    def setUp(self):

        self.status1 = False
        self.status2 = False
        self.d1 = defer.Deferred()
        self.d2 = defer.Deferred()
        self.d1.addCallback(connect1_ok)
        self.d1.addCallbacks(self.d_status1, lost_connection1)
        self.d1.addBoth(self.reactor_down)
        self.d2.addCallback(connect2_ok)
        self.d2.addCallbacks(self.d_status2, lost_connection2)
        self.d2.addBoth(self.reactor_down)
        self.factory1 = RemoteEHAFactory(self.d1)
        self.factory2 = RemoteEHAFactory(self.d2)
        from twisted.internet import reactor
        self.port1 = reactor.listenTCP(10000, self.factory1, interface='localhost')
        self.port2 = reactor.listenTCP(10001, self.factory2, interface='localhost')
        reactor.run()
        self.client = None

    def reactor_down(self, _):
        from twisted.internet import reactor
        # reactor.callLater(2, self.reactor_stop)
        reactor.callLater(2, self.port1.stopListening())
        reactor.callLater(2, self.port2.stopListening())

    def reactor_stop(self):
        from twisted.internet import reactor
        reactor.callLater(0.0, self.d1.cancel)
        reactor.callLater(0.0, self.d2.cancel)
        reactor.stop()

    def d_status1(self, status):
        self.status1 = status

    def d_status2(self, status):
        self.status2 = status

    def test_connect_client_port1(self):
        """ test detecting connect from client to port1 """
        print(self.status1)
        self.assertTrue(self.status1)

    # def test_connect_client_port2(self):
    #     """ test detecting connect from client to port2 """
    #     print(self.status1)
    #     self.assertTrue(self.status2)

    # def tearDown(self):
    #     self.port1.stopListening()
    #     self.port2.stopListening()

