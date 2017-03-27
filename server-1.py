# This is the Twisted Fast Poetry Server, version 1.0

import optparse, os

from twisted.internet.protocol import ServerFactory, Protocol


class PoetryProtocol(Protocol):

    #def connectionMade(self):
    #   self.transport.write(self.factory.poem)
    #   self.transport.loseConnection()

    def dataReceived(self, data):
        print("Data: {}".format(data))

class PoetryFactory(ServerFactory):

    protocol = PoetryProtocol

    def __init__(self):
        self.poem = ""


def main():

    factory = PoetryFactory()

    from twisted.internet import reactor

    port = reactor.listenTCP(10000, factory, interface='127.0.0.1')

    reactor.run()


if __name__ == '__main__':
    main()
