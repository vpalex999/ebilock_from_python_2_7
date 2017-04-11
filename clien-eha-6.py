# This is the Twisted Clien EHA Now! client, version 5.0.

# NOTE: This should not be used as the basis for production code.
# It uses low-level Twisted APIs as a learning exercise.
import datetime
import time
import threading
from sources.ebilockorder import Ebilock_order as ord
from sources.ebilockstatus import Ebilock_status as stat
from sources.hdlc import read_hdlc
from sources.hdlc import create_hdlc

#from sources.work_order import work_order
#from sources.work_order import to_work_timer_err
#from sources.work_order import sys_data
from sources.work_order import WorkTimer as wtimer
from sources.work_order import WorkFlow as wf
from sources.print_status import PrintStatus as prints



from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import defer
from twisted.python import log
from twisted.application import service


class EbilockProtocol(Protocol):

    def __init__(self, factory, system_data):
        self.system_data = system_data
        self.factory = factory
        self.d = defer.Deferred()

    def delta_time(self, receive_time):
        self.system_data["time_delta"] = receive_time - self.system_data["start_time"]
        self.system_data["start_time"] = time.time()
        #self.factory.system_data["time_delta"] = receive_time - self.factory.start_time
        #self.factory.start_time = time.time()

    def dataReceived(self, data):
        self.delta_time(time.time())
        self.system_data["hdlc"] = data
        self.factory.order_received()
        from twisted.internet import reactor
        #d.addCallback(self.dataSend())
        reactor.callLater(0, self.dataSend, "send_status")


        #self.factory.d_send_status(self.system_data["HDLC_SEND_STATUS"])
        #self.transport.write(self.hello)

    def dataSend(self, status):
        
        #print(self.system_data["HDLC_SEND_STATUS"])
        self.transport.write(self.system_data["HDLC_SEND_STATUS"])
        #print("send status!!!")

    
    #def connectionMade(self):
    #    self.transport.write("Hello!")

    #def connectionLost(self, reason):
    #    print("Connection Lost!!! {}".format(reason))
    #    self.factory.clientConnectionLost(connector, reason)
        
        #self.order_finished(reason)
    

    #def order_finished(self, reason):
    #    self.factory.client_finished(reason)

class EbilockClientFactory(ClientFactory):

    task_num = 1
    result = ""
    protocol = EbilockProtocol
    
    _SAFE = "SAFE"
    _WORK = "WORK"
    
    def __init__(self, defered):
        self.defered = defered
        self.start_time = time.time()
        self.system_data = {
            "start_time": time.time(),
            "hdlc": "",
            "time_delta": "",
            "System_Status": "SAFE",
            "Lost_Connect": False,
            "LOOP_OK": 3,
            "AREA_OK": 1,
            "HUB_OK": 5,
            "NUMBER_OK": 3,
            "FIRST_START": True,
            "Count_A": 1,
            "Count_B": 254,
            "Err_Count": 0,
            "Timer_status": False,
            "Start_timer": False,
            "order": "",
            "order_work": None,
            "ORDER_STATUS": None,
            "HDLC_SEND_STATUS": None,
            "ZONE_CNS":
            {
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0,
                7: 0,
                8: 0,
            }
        }
        
        self.wf = wf(self.system_data)
        self.prints = prints(self.system_data)

        self.system_data["Start_timer"] = True
        self.system_data["Timer_status"] = True

        self.d = defer.Deferred()
        self.d.addCallbacks(self.switch_to_pass, self.errorback_timer)
        self.d.addBoth(self.errorback_timer)
        from twisted.internet import reactor
        reactor.callLater(1.5, self.d.callback, stat)
        print("First start system. Activate CallLater 1.5c!!!")



        print("Check timer status: {}".format(self.system_data["Timer_status"]))
        print("Check timer start: {}".format(self.system_data["Start_timer"]))
        print("Check system status: {}".format(format(self.system_data["System_Status"])))

    def buildProtocol(self, addr):
        return EbilockProtocol(self, self.system_data)

    def switch_to_pass(self, *args):
        """ system to switch to the safe mode """
        print("{} Time out worked!!!!!!!!!".format(time.ctime()))
        self.system_data["Start_timer"] = False
        #if self.system_data["System_Status"] == "WORK" and self.system_data["Timer_status"]:
        self.system_data["System_Status"] = "SAFE"
        self.system_data["Timer_status"] = False
        print("{}  System switch to SAFE: {}".format(time.ctime(), self.system_data["System_Status"]))

    def errorback_timer(self, *args):
        return
        #print("Timer stop")
    
    

    def timer_restart(self):
        from twisted.internet import reactor
        reactor.callLater(0.0, self.d.cancel)
        self.d = None
        self.d = defer.Deferred()
        self.d.addCallbacks(self.switch_to_pass, self.errorback_timer)
        self.d.addBoth(self.errorback_timer)
        reactor.callLater(1.5, self.d.callback, stat)
        print("Timer Restart!!!")

    def d_send_status(self, status_order):
        from twisted.internet import reactor
        d = None
        d = defer.Deferred()
        d.addCallback(self.protocol(self, self.system_data).dataSend())
        reactor.callLater(0, d.callback, send_status)
        print("callback send status started")
        

    def check_timer(self, *args):
        print("Check timer status: {}".format(self.system_data["Timer_status"]))
        print("Check timer start: {}".format(self.system_data["Start_timer"]))
        print("Check system status: {}".format(format(self.system_data["System_Status"])))
        print("Err_Count: {}".format(self.system_data["Err_Count"]))

        if self.system_data["Timer_status"] and not self.system_data["Start_timer"] and self.system_data["System_Status"] == "WORK":
            from twisted.internet import reactor
            reactor.callLater(1.5, self.switch_to_pass, "SAFE")
            self.system_data["Err_Count"] = 0
            self.system_data["Start_timer"] = True
            print("Activate CallLater 1.5c - 1!!!")

        else:
            if not self.system_data["Timer_status"] and not self.system_data["Start_timer"] and self.system_data["System_Status"] == "WORK" or\
             not self.system_data["Timer_status"] and self.system_data["Start_timer"] and self.system_data["System_Status"] == "WORK":
                self.timer_restart()
                self.system_data["Timer_status"] = False
                self.system_data["Start_timer"] = True

            else:
                if not self.system_data["Timer_status"] and self.system_data["System_Status"] == self._SAFE and self.system_data["order"]["DESC_ALARM"] == "OK" :
                    self.system_data["System_Status"] = self._WORK
                    self.timer_restart()
                else:
                    pass

        print("\nAfter check_timer")
        print("Check timer status: {}".format(self.system_data["Timer_status"]))
        print("Check timer start: {}".format(self.system_data["Start_timer"]))
        print("Check system status: {}\n".format(format(self.system_data["System_Status"])))

    def clientConnectionFailed(self, connector, reason):
        print("Failed to connect to: {}".format(connector.getDestination()))
        time.sleep(1)
        connector.connect()

    def clientConnectionLost(self, connector, reason):
        print("Client connection Lost: {}".format(reason))
        time.sleep(1)
        connector.connect()

    def order_received(self):
        source_hdlc = read_hdlc(self.system_data["hdlc"])
        # print("hdlc {}".format(source_hdlc))
        if source_hdlc:
            self.system_data["order"] = None
            self.system_data["order"] = ord.from_hdlc(source_hdlc).check_telegramm()
            status = self.wf.work_order()
            #print("return status work_order {}".format(status))
            if status == 80:
                print("Send Status!!!")
                if stat.from_send_status(self.system_data).code_telegramm():
                    self.system_data["HDLC_SEND_STATUS"] = None
                    self.system_data["HDLC_SEND_STATUS"] = create_hdlc(self.system_data["ORDER_STATUS"])

            elif status == 110:
                print("Lost Communication\nTransfer status with old counters and Increase the counter")
                if stat.from_loss_connect(self.system_data).code_telegramm():
                    self.system_data["HDLC_SEND_STATUS"] = None
                    self.system_data["HDLC_SEND_STATUS"] = create_hdlc(self.system_data["ORDER_STATUS"])
                    # Increase by 1
                    #self.wf.increase_count()
                    print("Increase count A/B: {}, {}\n".format(hex(self.system_data["Count_A"]), hex(self.system_data["Count_B"])))

            elif status == 0:
                order_work = {}
                order_work = self.system_data["order"]
                self.system_data["order_work"] = None
                self.system_data["order_work"] = order_work.copy()
                if stat.from_ok(self.system_data).code_telegramm():
                    self.system_data["HDLC_SEND_STATUS"] = None
                    self.system_data["HDLC_SEND_STATUS"] = create_hdlc(self.system_data["ORDER_STATUS"])
                    #self.d_send_status(self.system_data["HDLC_SEND_STATUS"])
                    #print("hdlc_send: {}".format(hdlc_send))

            elif status == 50:
                print("Discard a telegram")
                self.system_data["Timer_status"] = True
            else:
                    self.system_data["HDLC_SEND_STATUS"] = None
                    self.system_data["ORDER_STATUS"] = None
                    print("Don't send status!!!")
            self.prints.show_admin_address_ok()
            self.prints.show_receive_address_ok()
            self.prints.show_zone_cns()
            self.prints.show_status_telegramm()

            self.check_timer()

            print "{} receive order: status system: {}, order status: {}, err_code: {}, delta time: {}, CountA: {}, CountB: {}, Zone: {}\n".format(time.ctime(), self.system_data["System_Status"],\
                    self.system_data["order"]["DESC_ALARM"], self.system_data["order"]["CODE_ALARM"], self.system_data["time_delta"],\
                     hex(self.system_data["Count_A"]), hex(self.system_data["Count_B"]), self.system_data["order"]["STATUS_ZONE"])

            if not self.system_data["order_work"] is None:
                print "{} order_work: status system: {}, order status: {}, delta time: {}, CountA: {}, CountB: {}, Zone: {}\n".format(time.ctime(), self.system_data["System_Status"],\
                        self.system_data["order_work"]["DESC_ALARM"], self.system_data["time_delta"],\
                            hex(self.system_data["Count_A"]), hex(self.system_data["Count_B"]), self.system_data["order_work"]["STATUS_ZONE"])
            print("#"*10)
                
        


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

