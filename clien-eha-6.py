# This is the Twisted Clien EHA Now! client, version 5.0.

# NOTE: This should not be used as the basis for production code.
# It uses low-level Twisted APIs as a learning exercise.
import datetime
import time
from sources.ebilockorder import Ebilock_order as eb
from sources.hdlc import read_hdlc

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import defer
from twisted.python import log
from twisted.application import service


class EbilockProtocol(Protocol):
    

    def delta_time(self, receive_time):
        self.factory.receive_data["time_delta"] = receive_time - self.factory.start_time
        self.factory.start_time = time.time()

    def dataReceived(self, data):
        self.delta_time(time.time())
        self.factory.receive_data["hdlc"] = data
        self.factory.order_received()


    def dataSend(self, data):
        self.transport.write(data)

    
    #def connectionMade(self):
    #    self.transport.write("Hello!")

    def connectionLost(self, reason):
        print("Connection Lost!!!")
        #self.order_finished(reason)
    

    #def order_finished(self, reason):
    #    self.factory.client_finished(reason)

class EbilockClientFactory(ClientFactory):

    task_num = 1
    result = ""
    protocol = EbilockProtocol

    def __init__(self, defered):
        self.defered = defered
        self.clientprotocol = EbilockProtocol()
        self.order = ""
        self.start_time = time.time()
        self.receive_data = {"hdlc": "", "time_delta": "",}
        self.work_data = {
            "System_Status": "PASSIVE",
            "status_order": "",
            "Count_A": 1,
            "Count_B": 254,
            "Err_Count": 0,
            "order": "",
        }
    
    def check_count_ok(self):
        """ check counters good Telegram """
        status = False
        order_a = self.work_data["order"]["PACKET_COUNT_A"]
        order_b = self.work_data["order"]["PACKET_COUNT_B"]
        global_a = self.work_data["Count_A"]
        global_b = self.work_data["Count_B"]
        if order_a - global_a <= 2 and order_b - global_b <= 2:
            status = True
        else:
            pass
            #send status from old counts
        self.work_data["Count_A"] = self.work_data["order"]["PACKET_COUNT_A"]
        self.work_data["Count_B"] = self.work_data["order"]["PACKET_COUNT_B"]
        return status
        
        

    def switching_to_work(self):
        """ system to switch to the operating mode """

        self.work_data["Err_Count"] = 0
        #timer_error = stop
        self.work_data["System_Status"] = "WORK"
        #print("System status: Work!!!")
        


    #def buildProtocol(self, address):
    #    proto = EbilockClientFactory.buildProtocol(self, address)
    #    return proto
    #def buildProtocol(self, address):
    #    return EbilockProtocol(EbilockClientFactory)

    def client_finished(self,reason):
        if self.defered is not None:
            d = self.defered
            self.defered = None
            d.errback(reason)
        #self.errorback(reason)

    #def clientConnectionFailed(self, connector, reason):
    #    print("Failed to connect to: {}".format(connector.getDestination()))
    #    if self.defered is not None:
    #        d = self.defered
    #        self.defered = None
    #       d.errback(reason)


    def order_received(self):
        if self.defered is not None:
            d = self.defered
            self.defered = None
        #    d.callback(data)
        #self.callback(data, receive_count, delta_time)

        source_hdlc = read_hdlc(self.receive_data["hdlc"])

        order = eb.from_hdlc(source_hdlc).check_telegramm()
        self.work_data["status_order"] = order["status"]
        self.work_data["order"] = order["order"]
        self.work_order()

    def work_order(self):
        if self.work_data["status_order"] == "This send status":
            print("Send status")
        elif self.work_data["status_order"] == "OK":
            if self.check_count_ok():
                self.switching_to_work()
                
        else:
            #wrong telegram
            self.work_data["Err_Count"] += 1
            #print("order: {}, CountA: {}, CountB: {}, Err_count: {}".format(self.work_data["status_order"],\
             #self.work_data["Count_A"], self.work_data["Count_B"], self.work_data["Err_Count"]))

        print "status system: {0}, order: {1}, delta time: {2}, CountA: {3}, CountB: {4}".format(self.work_data["System_Status"],\
                 self.work_data["status_order"], self.receive_data["time_delta"], self.work_data["Count_A"], self.work_data["Count_B"])
        

    #def sendResult(self, data):
    #    print("Factory send over")
    #    self.protocol.dataSend(data)



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
    #port = 10000
    #host = "localhost"

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
        #order_done()

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

