from twisted.trial.unittest import TestCase
import pytest
import allure
import sys
import os
print("OS")
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.defer import Deferred
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ' ')))
from data_server import server_port1
import time


class ServerProtocol(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("Conn Made...{}".format(self.transport.getPeer()))
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
        print("start check!!!")
        print("status conn: {}".format(self.status_connect))
        from twisted.internet import reactor
        # self.check_connect()
        reactor.callLater(1.5, self.check_connect)

    def check_connect(self):
        print("check_connect!!!")
        if self.deferred is not None:
            d, self.deferred = self.deferred, None

        d.callback(self.status_connect)
        if self.status_connect:
            self.protocol.close_connect()


# skipped = True

@pytest.fixture()
def Server():
    class Dummy:
        host = '192.168.10.168'
        port1 = 10000
        port2 = 10001
    return Dummy


@pytest.yield_fixture
def Endpoint():
    d = Deferred()
    factory = ServerEHAFactory(d)
    # print(factory)
    from twisted.internet import reactor
    endpoint = reactor.listenTCP(server_port1, factory, interface="192.168.10.168")
    # print(d, factory)
    yield d, factory
    # time.sleep(3)
    return endpoint.stopListening()


def test_trial_connect_for_client_port1(Endpoint):
    """Test connect client to server from port1"""
    print("Endpoint: {}".format(Endpoint))

    def callback(status):
        print("status: {}".format(status))
        assert status, "Delay 1.5 seconds connection to local port {} from EHA".format(server_port1)
        print("Connect to local port:{} from EHA: {}".format(server_port1, status))

    d = Endpoint[0]
    factory = Endpoint[1]
    print("d: {}, f: {}".format(d, factory))
    d.addCallback(callback)
    print("add callback")
    factory.start_check()
    print("factory start")
    return d

