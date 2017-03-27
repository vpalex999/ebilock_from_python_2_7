# This is the Twisted Get Poetry Now! client, version 1.0.

# NOTE: This should not be used as the basis for production code.
# It uses low-level Twisted APIs as a learning exercise.
import datetime
from sources.ebilockcmain import Edilock as eb
from sources.hdlc import read_hdlc

from twisted.internet import main
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory


class EbilockProtocol(Protocol):
    order = ""
    task_num = 0
    start_time = None

    def dataReceived(self, data):
        order = data
        now_data = datetime.datetime.now()
        time_delta = None
        if self.start_time is None:
            self.start_time = now_data
        else:
            time_delta = now_data - self.start_time
            self.start_time = now_data

        self.order = eb.from_hdlc(read_hdlc(order)).check_telegramm()
        print "status order: {}, delta time: {}".format(self.order, time_delta)
        self.factory.order_count -= 1
        if self.factory.order_count == 0:
            self.orderReceived(self.order)

    def connectionLost(self, reason):
        self.orderReceived(self.order)

    def orderReceived(self, order):
        self.factory.client_finished()

class EbilockClientFactory(ClientFactory):
    
    task_num = 1

    protocol = EbilockProtocol

    def __init__(self, order_count):
        #self.order = order
        self.order_count = order_count

    # Create exemplar
    def buildProtocol(self, address):
        proto = ClientFactory.buildProtocol(self, address)
        proto.task_num = self.task_num
        self.task_num += 1
        return proto

    def client_finished(self,):
        from twisted.internet import reactor
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print"Failed to connect to: {}".format(connector.getDestination())
        self.client_finished()


def client_main():

    start = datetime.datetime.now()
    count_orders = 50
    factory = EbilockClientFactory(count_orders)

    host = '192.168.101.100'
    port = 4016
    from twisted.internet import reactor
    reactor.connectTCP(host, port, factory)
    reactor.run()
    elasped = datetime.datetime.now() - start
    print 'Got {} orders in {}'.format(count_orders, elasped)

if __name__ == '__main__':
    client_main()

