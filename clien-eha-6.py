# This is the Twisted Clien EHA Now! client, version 5.0.

# NOTE: This should not be used as the basis for production code.
# It uses low-level Twisted APIs as a learning exercise.
import datetime
import time
import threading
from sources.ebilockorder import Ebilock_order as ord
from sources.ebilockstatus import Ebilock_status as stat
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

        self.system_data = {
            "System_Status": "PASSIVE",
            "Number_OK": 3,
            "FIRST_START": True,
            "Count_A": 1,
            "Count_B": 254,
            "Err_Count": 0,
            "Err_timer_status": False,
            "order": ""
        }

        self.start_time = time.time()
        self.receive_data = {"hdlc": "", "time_delta": ""}
        self.timer_err = threading.Timer(1.5, self.work_timer_err())

    def check_err_first_stage(self):
        if self.system_data["order"]["CODE_ALARM"] == 10 or\
        self.system_data["order"]["CODE_ALARM"] == 11 or\
        self.system_data["order"]["CODE_ALARM"] == 12 or\
        self.system_data["order"]["CODE_ALARM"] == 21 or\
        self.system_data["order"]["CODE_ALARM"] == 22 or\
        self.system_data["order"]["CODE_ALARM"] == 23 or\
        self.system_data["order"]["CODE_ALARM"] == 51 or\
        self.system_data["order"]["CODE_ALARM"] == 62 or\
        self.system_data["order"]["CODE_ALARM"] == 63 or\
        self.system_data["order"]["CODE_ALARM"] == 64 or\
        self.system_data["order"]["CODE_ALARM"] == 65 or\
        self.system_data["order"]["CODE_ALARM"] == 66 or\
        self.system_data["order"]["CODE_ALARM"] == 81:
            print("The telegram is not taken into account. code: {}, desc: {}".format(self.system_data["order"]["CODE_ALARM"], self.system_data["order"]["DESC_ALARM"]))
            return False
        else:
            return True

    def check_err_second_stage(self):
        print("into secong stage")
        if self.system_data["order"]["CODE_ALARM"] == 31 or\
            self.system_data["order"]["CODE_ALARM"] == 32 or\
            self.system_data["order"]["CODE_ALARM"] == 33 or\
            self.system_data["order"]["CODE_ALARM"] == 34 or\
            self.system_data["order"]["CODE_ALARM"] == 35 or\
            self.system_data["order"]["CODE_ALARM"] == 36 or\
            self.system_data["order"]["CODE_ALARM"] == 37 or\
            self.system_data["order"]["CODE_ALARM"] == 38 or\
                self.system_data["order"]["CODE_ALARM"] == 39:
            print("order alarm: {}".format(self.system_data["order"]["CODE_ALARM"]))
            return False
        else:
            print("True second stage")
            return True

    def work_timer_err(self):
        self.switch_to_pass()
        pass

    def timer_err_start(self):
        if not self.timer_err.is_alive():
            self.timer_err.start()
        print("timer Error START!!!")
        self.system_data["Err_timer_status"] = True

    def checking_number_ok(self):
        """ Checking the OK number """
        tlg_a = self.system_data["order"]["TLG_A"]
        if self.system_data["Number_OK"] == tlg_a["NUMBER_OK"]:
            return True
        else:
            print("Number OK {} in not equal to the received {}".format(self.system_data["Number_OK"], tlg_a["NUMBER_OK"]))
            return False

    def check_count_ok(self):
        """ check counters good Telegram """
        status = False
        print("into_check_count")
        if self.check_err_second_stage():
            print("second stage OK")
            if self.system_data["FIRST_START"]:
                self.system_data["Count_A"] = self.system_data["order"]["PACKET_COUNT_A"]
                self.system_data["Count_B"] = self.system_data["order"]["PACKET_COUNT_B"]
                self.system_data["FIRST_START"] = False
                status = True
                print("First Start!!!")
            else:
                order_a = self.system_data["order"]["PACKET_COUNT_A"]
                order_b = self.system_data["order"]["PACKET_COUNT_B"]
                global_a = self.system_data["Count_A"]
                global_b = self.system_data["Count_B"]

                if order_a - global_a <= 2 and global_b - order_b <= 2:
                    self.system_data["Count_A"] = self.system_data["order"]["PACKET_COUNT_A"]
                    self.system_data["Count_B"] = self.system_data["order"]["PACKET_COUNT_B"]
                    status = True
        return status

    def switch_to_pass(self):
        """ system to switch to the safe mode """
        self.system_data["System_Status"] = "SAFE"
        self.system_data["FIRST_START"] = True

    def switching_to_work(self):
        """system to switch to the operating mode"""
        self.system_data["Err_Count"] = 0
        #timer_error = stop
        self.system_data["System_Status"] = "WORK"

    def send_status(self):
        #status = stat(self.system_data)
        print("Send status OK")

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

        order = ord.from_hdlc(source_hdlc).check_telegramm()
        self.system_data["order"] = order
        self.work_order()

    def work_order(self):
        if self.system_data["order"]["DESC_ALARM"] == "This send status":
            print("Send status")
        else:
            if self.check_err_first_stage():
                print("first stage")
                if self.check_count_ok():
                    print("check_count_OK")
                    if self.system_data["order"]["CODE_ALARM"] == 0:
                        print(self.system_data["order"]["DESC_ALARM"])
                        if self.checking_number_ok():
                            self.switching_to_work()
                            self.send_status()
                            print "status system: {0}, order status: {1}, delta time: {2}, CountA: {3}, CountB: {4}".format(self.system_data["System_Status"],\
                                    self.system_data["order"]["DESC_ALARM"], self.receive_data["time_delta"],\
                                     self.system_data["Count_A"], self.system_data["Count_B"])
                        else:  # not self.checking_number_ok()
                            pass
                    else:  # status_order not OK
                        if self.system_data["Err_Count"] == 0:
                            self.timer_err_start()
                        else:
                            pass
                        self.system_data["Err_Count"] += 1
                else:  # not self.check_count_ok()
                    print("Lost Communication\nTransfer status with old counters and Increase the counter\n")
                    #
            else:  # not check_err_first_stage
                print("Discard a telegram")


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

