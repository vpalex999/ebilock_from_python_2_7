from twisted.trial.unittest import TestCase
import unittest
import pytest
from allure.constants import AttachmentType
import allure
import sys
import os
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.defer import Deferred
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ' ')))
from data_server import server_port2


class ServerProtocol(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        # print("Conn Made...{}".format(self.transport.getPeer()))
        self.factory.status_connect = "{}:{}".format(self.transport.getPeer().host, self.transport.getPeer().port)

    def close_connect(self):
        self.transport.loseConnection()


class ServerEHAFactory(Factory):
    protocol = ServerProtocol

    def __init__(self, deferred):
        self.deferred = deferred
        # print("defer: {}".format(self.deferred))
        self.status_connect = False

    def buildProtocol(self, addr):
        self.protocol = ServerProtocol(self)
        return self.protocol

    def start_check(self):
        from twisted.internet import reactor
        reactor.callLater(1.5, self.check_connect)

    def check_connect(self):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None

        d.callback(self.status_connect)
        if self.status_connect:
            self.protocol.close_connect()


skipped = False


class EhaTestCaseClient1(TestCase):

    def setUp(self):
        self.d = Deferred()
        self.factory = ServerEHAFactory(self.d)
        from twisted.internet import reactor
        self.endpoint = reactor.listenTCP(server_port2, self.factory, interface="192.168.10.168")

    def tearDown(self):
        return self.endpoint.stopListening()

    @unittest.skipIf(skipped, "")
    def test_trial_connect_for_client_port2(self):
        """Test connect client to server from port2"""
        
        def check_connect(status):
            if self.assertTrue(status, "Delay 1.5 seconds connection to local port {} from EHA".format(server_port2)):
                # print("Connect to local port:{} from EHA: {}".format(server_port1, status))
                allure.attach("check_connect", "Connect to local port:{} from EHA: {}".format(server_port2, status))
        self.d.addCallback(check_connect)
        self.factory.start_check()
        return self.d


if __name__ == "__main__":
    unittest.main()
