# This is the Twisted Clien EHA Now! client, version 5.0.

# NOTE: This should not be used as the basis for production code.
# It uses low-level Twisted APIs as a learning exercise.
import datetime
from sources.ebilockcmain import Edilock as eb
from sources.hdlc import read_hdlc

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import defer
from twisted.python import log
from twisted.application import service


class EbilockProtocol(Protocol):
    order = ""
    task_num = 0
    #receive_count = 0
    start_time = datetime.datetime.now().microsecond
    send_data = {
        "order": "",
        "count": 0,
        "time_delta": "",
    }

    def dataReceived(self, data):

        log.msg("sending {:d} bytes of poetry to {:s}".format(len(data), self.transport.getPeer()))

        self.send_data["order"] = data
        time_now = datetime.datetime.now().microsecond
        self.send_data["time_delta"] = time_now - self.start_time
        self.start_time = time_now

        self.factory.order_received(self.send_data)
        self.send_data["count"] += 1

    def connectionLost(self, reason):
        self.order_finished(reason)
        

    def order_finished(self, reason):
        self.factory.client_finished(reason)

class EbilockClientFactory(ClientFactory):
    
    task_num = 1

    protocol = EbilockProtocol

    def __init__(self, defered):
        self.defered = defered
        #self.order = order
        #self.order_count = order_count
        #self.callback = callback
        #self.errorback = errorback

    # Create exemplar
    #def buildProtocol(self, address):
    #    proto = ClientFactory.buildProtocol(self, address)
    #    proto.task_num = self.task_num
    #    self.task_num += 1
    #    return proto

    def client_finished(self,reason):
        if self.defered is not None:
            d = self.defered
            self.defered = None
            d.errback(reason)
        #self.errorback(reason)

    def clientConnectionFailed(self, connector, reason):
        print"Failed to connect to: {}".format(connector.getDestination())
        if self.defered is not None:
            d = self.defered
            self.defered = None
            d.errback(reason)
        #self.errorback(reason)

    def order_received(self, data):
        if self.defered is not None:
            d = self.defered
            self.defered = None
            d.callback(data)
        #self.callback(data, receive_count, delta_time)


def get_order(host, port):

    d = defer.Deferred()
    from twisted.internet import reactor
    factory = EbilockClientFactory(d)
    reactor.connectTCP(host, port, factory)
    return d



def client_main():
    """
    EHM_STATUS: 'PASS' - silence mode, 'WORK' - work mode
    """

    from twisted.internet import reactor
    start = datetime.datetime.now()
    port = 4016
    host = '192.168.101.100'

    main_dict = {
        "count_orders": 5,
        "EHM_STATUS": "PASS",
        "CountA": 0,
        "CountB": 0,
        "Dog_timer": 0,
    }


    def got_order(data):
        
        result = eb.from_hdlc(read_hdlc(data["order"])).check_telegramm()
        print "status order: {0}, delta time: {1}".format(result, data["time_delta"])
        
        if main_dict["count_orders"] == data["count"]:
            main_dict["count_orders"] = data["count"]
            order_done()
        else:
            print("return")
            order_done()

    def order_filed(err):
        main_dict["count_orders"] = 0
        print("Order filed: {}".format(err))
        order_done()

    def order_done():
        print("Reactor stop!!!")
        reactor.stop()
    
    
    def first_init():
        """ start initialization """
        main_dict["CountA"] = 0
        main_dict["CountB"] = 0
        main_dict["Dog_timer"] = 0
        main_dict["EHM_STATUS"] = "PASS"


    first_init()
    d = get_order(host, port)
    d.addCallbacks(got_order, order_filed)
    reactor.run()
    elasped = datetime.datetime.now() - start
    print 'Got {} orders in {}'.format(main_dict["count_orders"], elasped)

if __name__ == '__main__':
    client_main()

