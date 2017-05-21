import pytest
import allure
import re

# from allure.constants import AttachmentType
from datetime import datetime

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.defer import Deferred


def date_time():
    nt = datetime.now()
    return "{}-{:02}-{:02} {:02}:{:02}:{:02}.{:3}".format(nt.year,\
                                                          nt.month,\
                                                          nt.day,\
                                                          nt.hour,\
                                                          nt.minute,\
                                                          nt.second,\
                                                          str(nt.microsecond)[:3])


class ServerProtocol(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("\n{} Conn Made...{}".format(date_time(), self.transport.getPeer()))
        print("\nStatus_connect before: {}".format(self.factory.status_connect))
        self.factory.count_connect.append(self.transport.getPeer())
        if not self.factory.status_connect:
            self.factory.status_connect = "{}:{}:{}"\
                .format(date_time(),\
                        self.transport.getPeer().host,\
                        self.transport.getPeer().port)
            print("\nStatus_connect after: {}".format(self.factory.status_connect))
        else:
            if self.factory.status_connect:
                print("\n{} Conn Close...{}".format(date_time(), self.transport.getPeer()))
                self.transport.loseConnection()

    def connectionLost(self, reason):
        print("\nConnection lost {}\n{}".format(reason, self.transport.getPeer()))
        if re.search("Connection to the other side was lost", str(reason)):
            print("\nConnection to the other side was lost {}\n{}".format(reason, self.transport.getPeer()))
            self.factory.status_connect = False


@allure.step("class ServerEHAFactory(Factory)")
class ServerEHAFactory(Factory):
    protocol = ServerProtocol

    def __init__(self, deferred, timeout_connect):
        with pytest.allure.step("Init factory"):
            self.deferred = deferred
            self.timeout_connect = timeout_connect
            self.status_connect = False
            self.connection_lost = False
            self.connection_failed = False
            self.count_connect = []
            from twisted.internet import reactor
            reactor.callLater(self.timeout_connect, self.check_connect)
            allure.attach("Start reactor.callater",\
                          "{} Start check_connect with timeout {}sec: {}"\
                          .format(date_time(), self.timeout_connect, self.check_connect))
            # print("factory defer: {}".format(self.deferred))

    def buildProtocol(self, addr):
        self.protocol = ServerProtocol(self)
        return self.protocol

    def ConnectionLost(self):
        with pytest.allure.step("Detect clientConnLost"):
            # self.connection_lost = connector
            allure.attach("Lost connect from",\
                          "clientConnectionLost: {}")

    @allure.step("Factory check_connect")
    def check_connect(self):
        allure.attach("In check_connect",\
                      "Status connect from connector EHA:\n{}"\
                      .format(self.status_connect))
        allure.attach("In count_connected",\
                      "Count connected from server:\n{}"\
                      .format(self.count_connect))
        print("\nIn Count connected from server:{}".format(self.count_connect))

        if self.deferred is not None:
            d, self.deferred = self.deferred, None
        # Connected_OK, Other_Connect, Reconnect
        if self.status_connect:
            if len(self.count_connect) > 1:
                d.errback(self.count_connect)
            # allure.attach("Close connect", "{} Status connect  from connector EHA: {}"\
            #               .format(date_time(), self.status_connect))
            else:
                d.callback(self.status_connect)
        else:  # notConnect
            #if self.connection_lost:
            #    allure.attach("Detected loss of connection between {} seconds"\
            #                  .format(self.timeout_connect),\
            #                  "Status connect from connector EHA:{}.\n\
            #                  Start errback".format(self.status_connect))
            #    d.errback(self.connection_lost)
            #else:
            d.errback(self.count_connect)
            allure.attach("Out check_connect delay after {} seconds"\
                          .format(self.timeout_connect),\
                          "Status connect from connector EHA: {}.\n\
                          Start errback".format(self.status_connect))


# FIXTURES


# tearUp/rearDown
@pytest.yield_fixture()
def test_server():
    endpoint = None

    @allure.step("Create_test_server() from tearUp/tearDown")
    def server(host, port, timeout_connect):
        allure.attach("Create_test_server", "Create_test_server {}:{}:{}sec".format(host, port, timeout_connect))
        d = Deferred()
        allure.attach("Defer from factory", "Create deferred for Factory: {} ".format(d))
        factory = ServerEHAFactory(d, timeout_connect)
        nonlocal endpoint
        assert endpoint is None
        from twisted.internet import reactor
        endpoint = reactor.listenTCP(port, factory, interface=host)
        return d
    yield server
    with allure.step("Stop test server"):
        if endpoint is not None:
            allure.attach("Stop test server", "Stop test server:{}".format(endpoint))
            endpoint.stopListening()


@pytest.fixture()
def data_maket_mea1209_1211():
    data = {
        "server_port1": 10000,
        "server_port2": 10001,
        "server_host": "192.168.10.168",
        "server_localhost": "127.0.0.1",
        "client_eha_side_1": "192.168.101.3",
        "client_eha_side_2": "192.168.101.4",
        "client_eha_float": "192.168.101.5",
        "timeout_connect": 15,
        "double": True,
        }
    return data


@pytest.fixture()
def from_port_1(test_server, data_maket_mea1209_1211):
    server = test_server(data_maket_mea1209_1211["server_host"],\
                         data_maket_mea1209_1211["server_port1"],\
                         data_maket_mea1209_1211["timeout_connect"])
    return {"defer": server, "data": data_maket_mea1209_1211}


@pytest.fixture()
def from_port_2(test_server, data_maket_mea1209_1211):
    server = test_server(data_maket_mea1209_1211["server_host"],\
                         data_maket_mea1209_1211["server_port2"],\
                         data_maket_mea1209_1211["timeout_connect"])
    return {"defer": server, "data": data_maket_mea1209_1211}



