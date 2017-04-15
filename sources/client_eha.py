# This is the Twisted Clien EHA Now! client, version 5.0.

# NOTE: This should not be used as the basis for production code.
# It uses low-level Twisted APIs as a learning exercise.
import datetime
import time
import threading
import optparse
import sys

from sources.ebilockorder import Ebilock_order as ord
from sources.ebilockstatus import Ebilock_status as stat
from sources.hdlc import read_hdlc
from sources.hdlc import create_hdlc

#from sources.work_order import work_order
#from sources.work_order import to_work_timer_err
#from sources.work_order import sys_data
from sources.work_order import WorkFlow as wf
from sources.print_status import PrintStatus as prints
from sources.ebilock_decode_status import Ebilock_decode_status as decode_stat





from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import defer
from twisted.python import log
from twisted.application import service


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...

Run it like this:

  python client-eha-7.py [hostname]:port1 port2 config.json

"""

    parser = optparse.OptionParser(usage)

    _, addresses = parser.parse_args()

    if not addresses:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return host, int(port)

    return map(parse_address, addresses)



class EbilockProtocol(Protocol):

    def __init__(self, factory, system_data):
        self.system_data = system_data
        # self.system_data_old = system_data_old
        self.factory = factory
        self.d = defer.Deferred()

    def delta_time(self, receive_time):
        self.system_data["time_delta"] = receive_time - self.system_data["start_time"]
        self.system_data["start_time"] = time.time()
        # self.system_data_old["time_delta"] = receive_time - self.system_data_old["start_time"]
        # self.system_data_old["start_time"] = time.time()

    def dataReceived(self, data):
        self.delta_time(time.time())
        self.system_data["hdlc"] = data
        #self.system_data_old["hdlc"] = data
        self.factory.order_received()

        from twisted.internet import reactor
        if self.system_data["HDLC_SEND_STATUS"]:
                reactor.callLater(0, self.dataSend, "send status")
                #self.system_data["HDLC_SEND_STATUS"] = None
                #self.system_data["ORDER_STATUS"] = None

        #if self.system_data_old["HDLC_SEND_STATUS"] is None:
        #    return
        #else:
        #    reactor.callLater(0, self.dataSend, "send_status?")

    def dataSend(self, status):
        # print(self.system_data_old["HDLC_SEND_STATUS"])
        #self.transport.write(self.system_data["HDLC_SEND_STATUS"])
        # print(status)
        hdlc = self.system_data["HDLC_SEND_STATUS"]
        self.transport.write(hdlc)
        # decode_stat(self.system_data_old["HDLC_SEND_STATUS"])
        # self.system_data_old["HDLC_SEND_STATUS"] = None
        print("send status!!!")

    # def connectionLost(self, reason):
    #    print("Connection Lost!!! {}".format(reason))
    #    self.factory.clientConnectionLost(connector, reason)


class EbilockClientFactory(ClientFactory):

    task_num = 1
    result = ""
    protocol = EbilockProtocol
    
    _SAFE = "SAFE"
    _WORK = "WORK"
    
    def __init__(self, defered, system_data_ok):
        self.defered = defered
        self.start_time = time.time()

        self.system_data = {
            "start_time": time.time(),
            "hdlc": "",
            "time_delta": "",
            "System_Status": "SAFE",
            "Lost_Connect": False,
            "FIRST_START": True,
            "Count_A": 1,
            "Count_B": 254,
            "Err_Count": 0,
            "Timer_status": False,
            "Start_timer": False,
            "ORDER": False,
            "ORDER_STATUS": None,
            "HDLC_SEND_STATUS": None,
            "OK": False,
            
        }
        self.system_data["OK"] = system_data_ok
        #print("New sysytem data: {}".format(self.system_data))

        self.system_data_old = {
            "start_time": time.time(),
            "hdlc": "",
            "time_delta": "",
            "System_Status": "SAFE",
            "Lost_Connect": False,
            "LOOP_OK": 3,
            "AREA_OK": 1,
            "HUB_OK": 5,
            "NUMBER_OK": 3,
            "ADDRESS_OK": None,
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
            "ZONE_CNS": {1: 1, 2: 1, 3: 1, 4: 1, 5: 3, 6: 2, 7: 2, 8: 2, },
        }

        self.wf = wf(self.system_data)
        self.system_data["Start_timer"] = True
        self.system_data["Timer_status"] = True
        self.prints = prints(self.system_data)
# -----------------------------------------------------------------------------------------
        

        #self.system_data_old["Start_timer"] = True
        #self.system_data_old["Timer_status"] = True

        #if self.wf.checking_address_ok():
        #    print("Adress_OK: {}".format(self.system_data_old["ADDRESS_OK"]))

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
        self.system_data["System_Status"] = "SAFE"
        self.system_data["Timer_status"] = False
        print("{}  System switch to SAFE: {}".format(time.ctime(), self.system_data["System_Status"]))

        self.system_data["Start_timer"] = False
        # if self.system_data_old["System_Status"] == "WORK" and self.system_data_old["Timer_status"]:
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
                if not self.system_data["Timer_status"] and self.system_data["System_Status"] == self._SAFE and self.system_data["ORDER"]["DESC_ALARM"] == "OK" :
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
        #print("hdlc {}".format(source_hdlc))
        if source_hdlc:
            self.system_data["ORDER"] = None
            self.system_data["ORDER"] = ord.from_hdlc(source_hdlc).check_telegramm()
            #print("New ORDER: {}".format(self.system_data["ORDER"]))
            status = self.wf.work_order()

        #source_hdlc_old = read_hdlc(self.system_data_old["hdlc"])
        # print("hdlc {}".format(source_hdlc))
        #if source_hdlc_old:
        #    self.system_data_old["order"] = None
        #    self.system_data_old["order"] = ord.from_hdlc(source_hdlc_old).check_telegramm()
        #    status = self.wf.work_order()
            #print("return status work_order {}".format(status))
            if status == 80:
                print("Send Status!!!")
                #if stat.from_send_status(self.system_data_old).code_telegramm():
                #    self.system_data_old["HDLC_SEND_STATUS"] = None
                #    self.system_data_old["HDLC_SEND_STATUS"] = create_hdlc(self.system_data_old["ORDER_STATUS"])

            elif status == 110:
                print("Lost Communication\nTransfer status with old counters and Increase the counter")
                #if stat.from_loss_connect(self.system_data).code_telegramm():
                #    self.system_data_old["HDLC_SEND_STATUS"] = None
                #    self.system_data_old["HDLC_SEND_STATUS"] = create_hdlc(self.system_data_old["ORDER_STATUS"])
                    # Increase by 1
                    #self.wf.increase_count()
                #    print("Increase count A/B: {}, {}\n".format(hex(self.system_data_old["Count_A"]), hex(self.system_data_old["Count_B"])))

            elif status == 0:
                self.prints.show_receive_packet()
                order_work = {}
                order_work = self.system_data["ORDER"]
                #print(("telegramm_order: {}".format(order_work)))
                for ok in self.system_data["OK"]:
                    _ok = self.system_data["OK"][ok]
                    # print("_OK: {}".format(order_work["ADDRESS_OK"]))
                    if _ok["ADDRESS_OK"] == order_work["ADDRESS_OK"]:
                        _ok["ORDER_WORK"] = order_work.copy()
                        _ok["STATUS_OK"] = self._WORK
                        self.system_data["ORDER"] = None
                        # print(("system_data_order: {}".format(_ok["ORDER_WORK"])))
                        # self.prints.show_all_data()
                if stat.from_ok(self.system_data).create_status():
                    self.system_data["HDLC_SEND_STATUS"] = None
                    self.system_data["HDLC_SEND_STATUS"] = create_hdlc(self.system_data["ORDER_STATUS"])
                    #self.d_send_status(self.system_data_old["HDLC_SEND_STATUS"])
                    #print("hdlc_send: {}".format(hdlc_send))

            elif status == 50:
                print("Discard a telegram")
                self.system_data["Timer_status"] = True
            else:
                    self.system_data["HDLC_SEND_STATUS"] = None
                    self.system_data["ORDER_STATUS"] = None
                    print("Don't send status!!!")
            #self.prints.show_all_data()
            #self.prints.show_admin_address_ok()
            #self.prints.show_receive_address_ok()
            #self.prints.show_zone_cns()
            #self.prints.show_status_telegramm()

            self.check_timer()

            

            #if not self.system_data["order_work"] is None:
            #    print "{} order_work: status system: {}, order status: {}, delta time: {}, CountA: {}, CountB: {}, Zone: {}\n".format(time.ctime(), self.system_data_old["System_Status"],\
            #            self.system_data_old["order_work"]["DESC_ALARM"], self.system_data_old["time_delta"],\
            #                hex(self.system_data_old["Count_A"]), hex(self.system_data_old["Count_B"]), self.system_data_old["order_work"]["STATUS_ZONE"])
            print("#"*10)
                
        
