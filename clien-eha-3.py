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
    receive_count = 0
    start_time = datetime.datetime.now().microsecond

    def dataReceived(self, data):
        #self.order = data
        time_now = datetime.datetime.now().microsecond
        delta_time = time_now - self.start_time
        self.start_time = time_now
        self.factory.order_received(data, self.receive_count, delta_time)
        self.receive_count += 1

    def connectionLost(self, reason):
        self.order_finished()
        

    def order_finished(self):
        self.factory.client_finished()

class EbilockClientFactory(ClientFactory):
    
    task_num = 1

    protocol = EbilockProtocol

    def __init__(self, callback, order_count):
        #self.order = order
        self.order_count = order_count
        self.callback = callback

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

    def order_received(self, data, receive_count, delta_time):
        self.callback(data, receive_count, delta_time)

        

        

def get_order(host, port, callback, count_orders):

    from twisted.internet import reactor
    factory = EbilockClientFactory(callback, count_orders)
    reactor.connectTCP(host, port, factory)


def client_main():
    from twisted.internet import reactor
    start = datetime.datetime.now()
    count_orders = 50
    host = '192.168.101.100'
    port = 4016

    def got_order(order, receive_count, delta_time):
        result = eb.from_hdlc(read_hdlc(order)).check_telegramm()
        print "status order: {0}, delta time: {1}".format(result, delta_time)
        if count_orders == receive_count:
            reactor.stop()

    get_order(host, port, got_order, count_orders)
    reactor.run()
    elasped = datetime.datetime.now() - start
    print 'Got {} orders in {}'.format(count_orders, elasped)

if __name__ == '__main__':
    client_main()

