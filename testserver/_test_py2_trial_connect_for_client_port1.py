from twisted.trial.unittest import TestCase
import unittest
import pytest
import allure
from allure.constants import AttachmentType
import sys
import os
import re
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.defer import Deferred
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ' ')))
from config_mea1209_1211 import server_host
from config_mea1209_1211 import server_port1
from config_mea1209_1211 import server_port2
from config_mea1209_1211 import client_mea1209_1211
from config_mea1209_1211 import timeout_connect


class ServerProtocol(Protocol):

    def __init__(self, factory):
        self.factory = factory
        self.count_connect = []

    def connectionMade(self):
        # print("Conn Made...{}".format(self.transport.getPeer()))
        if not self.factory.status_connect:
            self.factory.status_connect = "{}:{}".format(self.transport.getPeer().host, self.transport.getPeer().port)
        else:
            self.transport.loseConnection()
            self.count_connect.append(self.transport.getPeer())

    def close_connect(self):
        self.transport.loseConnection()


class ServerEHAFactory(Factory):
    protocol = ServerProtocol

    def __init__(self, deferred):
        with pytest.allure.step("Init factory"):
            self.deferred = deferred
            # print("defer: {}".format(self.deferred))
            self.status_connect = False
            self.connection_lost = False
            from twisted.internet import reactor
            reactor.callLater(timeout_connect, self.check_connect)
            allure.attach("start reactor.callater",\
                          "statr check_connect with timeout {}sec: {}".format(timeout_connect, self.check_connect))

    def buildProtocol(self, addr):
        self.protocol = ServerProtocol(self)
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        with pytest.allure.step("Detect clientConnLost"):
            self.connection_lost = connector
            allure.attach("Lost connect from", "clientConnectionLost: {}".format(connector))

    def check_connect(self):
        with pytest.allure.step("Second step"):
            allure.attach("In check_connect",\
                          "status connect from connector EHA: {}".format(self.status_connect))
            if self.deferred is not None:
                d, self.deferred = self.deferred, None
            if self.status_connect and not self.connection_lost:  # Connected_OK, Other_Connect, Reconnect
                allure.attach("close connect", "status connect  from connector \
                              EHA: {}".format(self.status_connect))
                if self.protocol.count_connect:
                    allure.attach("Count connected client from test server",\
                                  "{}".format(self.protocol.count_connect))
                self.protocol.close_connect()
                d.callback(self.status_connect)
            else:  # notConnect, lostConnect
                if self.connection_lost:
                    allure.attach("Detected loss of connection between {} seconds".format(timeout_connect),\
                                  "status connect from connector EHA: {}.\nStart errback".format(self.status_connect))
                    d.errback(self.connection_lost)
                else:
                    d.errback(self.status_connect)
                    allure.attach("Out check_connect delay after {} seconds".format(timeout_connect),\
                                  "status connect from connector EHA: {}.\nStart errback".format(self.status_connect))


skipped = False


class EhaTestCaseClient1(TestCase):

    def setUp(self):
        self.d = Deferred()
        self.factory = ServerEHAFactory(self.d)
        from twisted.internet import reactor
        self.endpoint = reactor.listenTCP(server_port1, self.factory, interface=server_host)

    def tearDown(self):
        # allure.attach("Tear Down", "{}".format(self.endpoint))
        return self.endpoint.stopListening()

    @unittest.skipIf(skipped, "")
    def test_trial_connect_for_client_port1(self):
        """Test connect client to server from port1"""

        def connected(status):
            with pytest.allure.step("Connected step"):
                allure.attach("Check connected client from test server",\
                              "Callback is return result connect for server\
                               {}:{} from: {}".format(server_host, server_port1, status))
                self.assertTrue(status, "Delay {} seconds connection to local port \{} from EHA".format(timeout_connect, server_port1))
                self.assertTrue(re.match(client_mea1209_1211, status),\
                                "Detection connection to local port {} from an unexpected ip address: {}.\
                                \nThe system waits for connection from the address: {}\n".format(server_port1, status, client_mea1209_1211))

        def connected_err(reason):
            with pytest.allure.step("Connected Error step"):
                allure.attach("Return Error from test server",\
                              "Callback is return Error result connect for server\
                               {}:{} from: {}".format(server_host, server_port1, reason))
                self.assertTrue(reason.value, "Delay {} seconds connection to local port \{} from EHA".format(timeout_connect, server_port1))

        with pytest.allure.step("First step"):
            allure.attach("Add callbacks function connected()", "{}".format(connected))
            self.d.addCallbacks(connected, connected_err)

        return self.d


if __name__ == "__main__":
    unittest.main()
