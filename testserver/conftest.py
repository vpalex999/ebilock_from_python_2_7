import pytest
import allure
import re

# from allure.constants import AttachmentType
from datetime import datetime

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.protocol import ServerFactory
from twisted.internet.defer import Deferred
from twisted.internet.defer import maybeDeferred
from twisted.internet.defer import succeed


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


# tearUp/tearDown
# @pytest.yield_fixture()
# def test_server():
#     endpoint = None
# 
#     @allure.step("Create_test_server() from tearUp/tearDown")
#     def server(host, port, timeout_connect):
#         allure.attach("Create_test_server", "Create_test_server {}:{}:{}sec".format(host, port, timeout_connect))
#         d = Deferred()
#         allure.attach("Defer from factory", "Create deferred for Factory: {} ".format(d))
#         factory = ServerEHAFactory(d, timeout_connect)
#         nonlocal endpoint
#         assert endpoint is None
#         from twisted.internet import reactor
#         endpoint = reactor.listenTCP(port, factory, interface=host)
#         return d
#     yield server
#     with allure.step("Stop test server"):
#         if endpoint is not None:
#             allure.attach("Stop test server", "Stop test server:{}".format(endpoint))
#             endpoint.stopListening()


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
        "timeout_connect": 5,
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


# FUXTURE 2


class service_1(object):

    def __init__(self, data, server_port):
        self.data = data
        self.server_port = server_port

    def check_timeout_connected(self, status):
        print("servicestatus1: {}".format((status)))
        allure.attach("Check connected client from test server",\
                      "Callback is return result connect for server {}:{} from: {}"\
                      .format(self.data["server_host"], self.server_port, status))

        if self.data["double"]:
            pass
            # assert re.search(self.data["client_eha_side_1"], status) or re.search(self.data["client_eha_side_2"], status),\
            #        "Detection connection to local port {} from an unexpected ip address: {}.\n\
            #        The system waits for connection from the addreses: {} or {}\n"\
            #        .format(self.server_port, status, self.data["client_eha_side_1"], self.data["client_eha_side_2"])
            
            print("End re double")

        else:
            assert re.search(self.data["client_eha_float"], status),\
                   "Detection connection to local port {} from an unexpected ip address: {}.\n\
                   The system waits for connection from the addreses: {} or {}\n"\
                   .format(self.server_port, status, self.data["client_eha_float"])
        print("End re double2")
        # return "return service"


class ServerServiceProtocol_2(Protocol):

    def prnt(self, status):
        print("prnt: {}".format(status))

    def connectionMade(self):
        print("\n{} Conn Made...{}".format(date_time(), self.transport.getPeer()))
        print("\nStatus_connect before: {}".format(self.factory.status_connect))
        self.factory.status_connect = "{}:{}:{}"\
            .format(date_time(),\
                    self.transport.getPeer().host,\
                    self.transport.getPeer().port)

        succeed(self.factory.service.check_timeout_connected(self.factory.status_connect))
        print("EEE: {}".format(self.factory.status_test))


class ServerServiceFactory_2(ServerFactory):
    protocol = ServerServiceProtocol_2

    def __init__(self, deferred, service):
        self.deferred = deferred
        self.service = service
        self.status_connect = False
        self.status_test = "dddd"
        self.timeout_connect = self.service.data["timeout_connect"]
        print("\nInitial factory service: {}, deferred: {}, time_out: {}"\
              .format(self.service, self.deferred, self.timeout_connect))
        from twisted.internet import reactor
        # reactor.callLater(self.timeout_connect, self.service.check_timeout_connected, self.status_connect, self.return_result))
        # reactor.callLater(self.timeout_connect,\
        #                   self.service.check_timeout_connected, self.status_connect, self.return_result("status"))

    def return_result(self, status):
        print("return_result_ok: {}".format("status"))
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
        # if status:
        d.callback("status")

    def print_result(self):
        print("print_result:")
        return


# ######################################################################

class ServerServiceProtocol_3(Protocol):

    def prnt(self, status):
        print("prnt: {}".format(status))

    @allure.step("connectionMade")
    def connectionMade(self):
        print("\n{} Conn Made...{}".format(date_time(), self.transport.getPeer()))
        print("\nStatus_connect before: {}".format(self.factory.status_connect))
        self.factory.status_connect = "{}:{}:{}"\
            .format(date_time(),\
                    self.transport.getPeer().host,\
                    self.transport.getPeer().port)
        allure.attach("In Connect",\
                      "source address: {}".format(self.factory.status_connect))
        print("\nStatus_connect after: {}".format(self.factory.status_connect))
        with pytest.allure.step("Start chk()"):
            self.factory.chk()
            print("start chk()")


class ServerServiceFactory_3(Factory):
    protocol = ServerServiceProtocol_3

    def __init__(self, server, deferred, timeout):
        self.server = server
        self.deferred = deferred
        # self.service = service
        self.status_connect = False
        self.timeout_connect = timeout
        print("\nInitial factory deferred: {}, time_out: {}"\
              .format(self.deferred, self.timeout_connect))
        from twisted.internet import reactor
        reactor.callLater(self.timeout_connect, self.chk)

    def chk(self):
        print("In chk()")
        succeed(self.server.check_timeout_connected(self.status_connect))

    def return_result(self, status):
        print("return_result_ok: {}".format(status))
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
        # if status:
        d.callback(status)

    def print_result(self):
        print("print_result!!!:")
        return

# tearUp/tearDown
# @pytest.yield_fixture()
# def test_server_2():
#     endpoint = None
# 
#     @allure.step("Create test_server2() from tearUp/tearDown")
#     def server(host, port, timeout_connect, data):
#         allure.attach("Create_test_server", "Create_test_server {}:{}:{}sec".format(host, port, timeout_connect))
#         d = Deferred()
#         allure.attach("Defer from factory", "Create deferred for Factory: {} ".format(d))
#         service1 = service_1(data, port)
#         factory = ServerServiceFactory_2(d, service1)
#         nonlocal endpoint
#         assert endpoint is None
#         from twisted.internet import reactor
#         endpoint = reactor.listenTCP(port, factory, interface=host)
#         return d
#     yield server
#     with allure.step("Stop test server"):
#         if endpoint is not None:
#             allure.attach("Stop test server", "Stop test server:{}".format(endpoint))
#             endpoint.stopListening()


@pytest.fixture()
def maket_test1_port1(test_server_2, data_maket_mea1209_1211):
    server = test_server_2(data_maket_mea1209_1211["server_host"],\
                           data_maket_mea1209_1211["server_port1"],\
                           data_maket_mea1209_1211["timeout_connect"],\
                           data_maket_mea1209_1211)
    return server





# tearUp/tearDown
@pytest.yield_fixture()
def test_server_3():
    endpoint = None

    @allure.step("Create test_server3() from tearUp/tearDown")
    # def server(host, port, timeout_connect, data):
    def server(data, port):
        d = Deferred()
        host = data["server_host"]
        timeout_connect = data["timeout_connect"]
        # allure.attach("Defer from factory", "Create deferred for Factory: {} ".format(d))
        # service = service_1(data, port)
        allure.attach("Create_test_server", "Create_test_server {}:{}:{}sec".format(host, port, timeout_connect))
        nonlocal endpoint
        assert endpoint is None
        ss = Server_Test3(host, port, timeout_connect, data, d)
        from twisted.internet import reactor
        endpoint = reactor.listenTCP(port, ss.factory, interface=host)
        return d
    yield server
    with allure.step("Stop test server"):
        if endpoint is not None:
            allure.attach("Stop test server", "Stop test server:{}".format(endpoint))
            endpoint.stopListening()


@pytest.fixture()
def maket3_test1_port1(test_server_3, data_maket_mea1209_1211):
    ss = test_server_3(data_maket_mea1209_1211, data_maket_mea1209_1211["server_port1"])
    return  ss


@pytest.fixture()
def maket3_test1_port2(test_server_3, data_maket_mea1209_1211):
    ss = test_server_3(data_maket_mea1209_1211, data_maket_mea1209_1211["server_port2"])
    return ss 


class Server_Test3(object):

    def __init__(self, host, port, timeout_connect, data, d):
        self.d = d
        self.host = host
        self.port = port
        self.timeout_connect = timeout_connect
        self.data = data
        self.factory = ServerServiceFactory_3(self, self.d, self.timeout_connect)
        # from twisted.internet import reactor
        # self.endpoint = reactor.listenTCP(self.port, self.factory1, interface=self.host)

    @allure.step("Call check_timeout_connected()")
    def check_timeout_connected(self, status):
        print("check_timeout_connected: {}".format((status)))
        allure.attach("Check connected client from test server",\
                      "Callback is return result connect for server {}:{} from: {}"\
                      .format(self.data["server_host"], self.port, status))

        if self.data["double"]:
            if not status:
                self.factory.return_result((status, "Delay {} seconds connection to local port {} from EHA"\
                                           .format(self.timeout_connect, self.port)))
            else:
                return self.factory.return_result((status, "Connect OK"))
