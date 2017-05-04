from twisted.protocols import basic
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import Factory
from base_3 import Calculation
import binascii
import struct
import time


class RemoteProtocol(Protocol):
    def __init__(self):
        self.start_time = time.time()

    def connectionMade(self):
        self.factory._count_connection()
        #self.transport.loseConnection()

    def connectionLost(self, reason):
        # print("Conn Lost")
        self.factory._connectionLost(reason)


class RemoteEHAFactory(Factory):
    protocol = RemoteProtocol

    def __init__(self, deferred):
        self.deferred = deferred
        self.counts = 0
        self.start_time = time.time()
        self.count_connections = 0

    def _count_connection(self):
        print("Connect: {}, delta time: {}".format(self.count_connections, time.time() - self.start_time))
        self.count_connections += 1
        self.start_time = time.time()
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback([self.count_connections, time.ctime()])

    def _connectionLost(self, reason):
        # print(reason)
        if self.deferred is not None:
            d, self.deferred = self.deferred1, None
            d.errback([self.count_connections, time.ctime()])


def main():
    from twisted.internet import reactor
    from twisted.python import log
    import sys
    log.startLogging(sys.stdout)
    reactor.listenTCP(0, RemoteCalculationFactory())
    reactor.run()


if __name__ == "__main__":
    main()

