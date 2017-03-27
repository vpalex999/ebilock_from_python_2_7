""" This is the Twisted Clien for Ebilock """

import optparse
import random
import sys
from twisted.internet import defer
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory


# Протокол
class EblClientProtocol(Protocol):
    order = ""

    # Принимаем данные
    def dataReceived(self, data):
        self.order = data
        print("Reseive order: {}".format(self.order))

    # обрыв соединения
    def connectionLost(self, reason):
        # При обрыве соединения передаём телеграмму на обработку
        self.orderReceived(self.order)

    # При завершении, передаем телеграмму на обработку
    def orderReceived(self, order):
        self.factory.order_finished(order)


# Фабрика
class EblClientFactory(ClientFactory):
    protocol = EblClientProtocol

    def __init__(self, deferred):
        self.deferred = deferred

    def order_finished(self, order):
        if self.deferred is None:
            d, self.deferred = self.deferred, None
            d.callback(order)

    def clientConnectionFailed(self, connector, reason):
        if self.deferred is None:
            d, self.deferred = self.deferred, None
            d.errback(reason)


def get_order(host, port):
    """ Забираем телеграмму с указанного host и port """
    d = defer.Deferred()
    from twisted.internet import reactor
    factory = EblClientFactory(d)
    reactor.connectTCP(host, port, factory)
    return d


def order_main():
    from twisted.internet import reactor
    print("start")
    orders = []
    errors = []
    host = '192.168.101.100'
    port = 4016

    def ok_order(order):
        orders.append(order)
        print("order: {}".format(order))
    
    def err_order(err):
        errors.append(err)
        print("error order : {}".format(err))

    def order_done(_):
        reactor.stop()

    d = get_order(host, port)
    d.addCallbacks(ok_order, err_order)
    d.addBoth(order_done)
    print("stop")


if __name__ == '__main__':
    order_main()
