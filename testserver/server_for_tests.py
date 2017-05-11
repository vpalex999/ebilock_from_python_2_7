""" Module for test client EHA """
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.defer import Deferred
from twisted.internet import reactor


class ServerProtocol(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("Conn Made...")
        self.factory.status_connect = self.transport.getPeer().host


class ServerEHAFactory(Factory):
    protocol = ServerProtocol

    def __init__(self, deferred):
        self.deferred = deferred
        self.status_connect = False
        reactor.callLater(1.5, self.check_connect)


    def buildProtocol(self, addr):
        return ServerProtocol(self)

    def check_connect(self):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None

        if self.status_connect:
            d.callback(self.status_connect)
            # print("Connect to F... {}".format(self.status_connect))
        else:
            # print("No Connect to port... ")
            d.errback(self.status_connect)


def mainTest(port1=9090, port2=9091):

    status1 = [None]
    status2 = [False]

    def stop_reactor1(stop):
        # print("reactor stop")
        # from twisted.internet import reactor
        if status2 is not None:
            endpoint1.stopListening()
            # reactor.stop()

    def connection_ok1(host):
        status1.clear()
        status1.append("Connect from... {}".format(host))

    def connection_err1(reason):
        status1.clear()
        status1.append(False)

    def stop_reactor2(stop):
        # print("reactor stop")
        # from twisted.internet import reactor
        if status1 is not None:
            endpoint2.stopListening()
            # reactor.stop()

    def connection_ok2(host):
        status1.clear()
        status1.append("Connect from... {}".format(host))

    def connection_err2(reason):
        status1.clear()
        status1.append(False)

    if port1 is not None:
        d1 = Deferred()
        d1.addCallback(connection_ok1)
        d1.addErrback(connection_err1)
        d1.addBoth(stop_reactor1)
        print("d1 start: {}".format(d1))
        # endpoint1 = TCP4ServerEndpoint(reactor, port1)
        # endpoint1.listen(ServerEHAFactory(d1))
        endpoint1 = reactor.listenTCP(port1, ServerEHAFactory(d1))

    if port2 is not None:
        d2 = Deferred()
        d2.addCallback(connection_ok2)
        d2.addErrback(connection_err2)
        d2.addBoth(stop_reactor2)
        print("d2 start: {}".format(d2))
        # endpoint2 = TCP4ServerEndpoint(reactor, port2)
        # endpoint2.listen(ServerEHAFactory(d2))
        endpoint2 = reactor.listenTCP(port2, ServerEHAFactory(d2))

    reactor.run()
    if port1 is not None:
        if d1.result is None:
            print("d1: {}".format(d1))

    if port2 is not None:
        print("d2: {}".format(d2))

    return status1[0]


# status = main(10000)
# print(status)

