# This is the Twisted Clien EHA Now! client, version 5.0.

# NOTE: This should not be used as the basis for production code.
# It uses low-level Twisted APIs as a learning exercise.
import datetime
import time
import threading
from sources.ebilockorder import Ebilock_order as ord
from sources.ebilockstatus import Ebilock_status as stat
from sources.hdlc import read_hdlc
#from sources.work_order import work_order
#from sources.work_order import to_work_timer_err
#from sources.work_order import sys_data
from sources.work_order import WorkTimer as wtimer
from sources.work_order import WorkFlow as wf


from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import defer
from twisted.python import log
from twisted.application import service


class EbilockProtocol(Protocol):

    def delta_time(self, receive_time):
        self.factory.system_data["time_delta"] = receive_time - self.factory.start_time
        self.factory.start_time = time.time()

    def dataReceived(self, data):
        self.delta_time(time.time())
        self.factory.system_data["hdlc"] = data
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
        self.start_time = time.time()
        #self.receive_data = {"hdlc": "", "time_delta": ""}
        # self.system_data = sys_data
        self.work_order = work_order
        self.system_data = {
            "hdlc": "",
            "time_delta": "",
            "System_Status": "PASSIVE",
            "Number_OK": 3,
            "FIRST_START": True,
            "Count_A": 1,
            "Count_B": 254,
            "Err_Count": 0,
            "Err_timer_status": False,
            "order": ""
        }

        self.wtimer = wtimer(self.system_data)

    def switch_to_pass(self):
        """ system to switch to the safe mode """
        self.system_data["System_Status"] = "SAFE"
        self.system_data["FIRST_START"] = True
        print("switch to pass. time out!!!")


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
        source_hdlc = read_hdlc(self.system_data["hdlc"])
        order = ord.from_hdlc(source_hdlc).check_telegramm()
        self.system_data["order"] = ""
        self.system_data["order"] = order
        wf(self.system_data, self.wtimer)
        #print(self.system_data)
 
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

