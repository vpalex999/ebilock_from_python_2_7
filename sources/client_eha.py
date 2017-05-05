# This is the Twisted Clien EHA Now! client, version 5.0.

# NOTE: This should not be used as the basis for production code.
# It uses low-level Twisted APIs as a learning exercise.

import time
from pprint import pprint

from sources.ebilockorder_new import Ebilock_order as ord_ok
from sources.ebilockstatus import Ebilock_status as stat
from sources.hdlc import create_hdlc
from sources.hdlc import hdlc_work

from sources.work_order import WorkFlow as wf
from sources.print_status import PrintStatus as prints
from sources.ebilock_decode_status import Ebilock_decode_status as decode_stat

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import defer
from twisted.python import log
from twisted.application import service

import logging
logger_client_eha = logging.getLogger("client_main.client_eha")


class EbilockProtocol(Protocol):

    def __init__(self, factory, system_data):
        self.system_data = system_data
        self.factory = factory
        self.buffer = bytearray()
        logger_client_eha.debug("initialization 'EbilockProtocol'")
        

    def delta_time(self, receive_time):
        self.system_data["time_delta"] = receive_time - self.system_data["start_time"]
        self.system_data["start_time"] = time.time()

    def connectionMade(self):
        print("{} Connect to... {}".format(time.ctime(), self.transport.connector.getDestination()))

    def dataReceived(self, data):
        host = self.transport.getPeer().host
        port = self.transport.getPeer().port
        logger_client_eha.debug("- Client[{}] {}, received HDLC DATA".format(port, host))
        work_data = hdlc_work(data, self.buffer)
        if work_data:
            logger_client_eha.info("{}Receive hdlc data [{}:{}]{}".format("="*30, host, port, "="*30))
            logger_client_eha.info("- Client[{}] received HDLC DATA".format(self.transport.getPeer().port))
            self.delta_time(time.time())
            self.system_data["hdlc"] = work_data
            self.factory.order_received()
            self.buffer.clear()

            from twisted.internet import reactor
            if self.system_data["HDLC_SEND_STATUS"]:
                    status = self.system_data["HDLC_SEND_STATUS"]
                    reactor.callLater(0, self.dataSend, status[:])
                    self.system_data["HDLC_SEND_STATUS"] = None

    def dataSend(self, status):
        self.transport.write(status)

    def get_port_host(self, st):
        host = self.transport.getPeer().host
        port = self.transport.getPeer().port
        return port, host
<<<<<<< HEAD
=======

>>>>>>> client_eha_for_python_3_6

<<<<<<< HEAD

=======
>>>>>>> 1dd4af5585806de725b942e4b47761b309663a0a
class EbilockClientFactory(ClientFactory):
    task_num = 1
    result = ""
    protocol = EbilockProtocol

    _SAFE = "SAFE"
    _WORK = "WORK"

    def __init__(self, defered, system_data):
        self.defered = defered
        self.start_time = time.time()
        self.system_data = system_data

        self.wf = wf(self.system_data)
        self.system_data["Start_timer"] = True
        self.system_data["Timer_status"] = True
        self.prints = prints(self.system_data)
# -----------------------------------------------------------------------------------------

        self.d = defer.Deferred()
        self.d.addCallbacks(self.switch_to_pass, self.errorback_timer)
        self.d.addBoth(self.errorback_timer)
        from twisted.internet import reactor
        reactor.callLater(1.5, self.d.callback, stat)
        logger_client_eha.info("First start system. Activate Timer 1.5c!!!")
        logger_client_eha.info("First System Status => {}".format(self.system_data["System_Status"]))

        self.create_timer_ok()

        logger_client_eha.debug(self.prints.show_status_timer_system())
        logger_client_eha.debug("initialization 'EbilockClientFactory'")

    def create_timer_ok(self):
        for ok in self.system_data["OK"]:
            d_ = defer.Deferred()
            d_.addCallbacks(self.switch_to_pass_ok, self.errorback_timer)
            d_.addBoth(self.errorback_timer)
            self.system_data["Timer_OK"][ok] = d_
        from twisted.internet import reactor
        for d_ok in self.system_data["Timer_OK"]:
            dd = self.system_data["Timer_OK"][d_ok]
            reactor.callLater(1.5, dd.callback, d_ok)
            self.system_data["OK"][ok]["Start_timer"] = True
            self.system_data["OK"][ok]["Timer_status"] = True
            logger_client_eha.info("First start OK: {}. Activate Timer 1.5c!!!".format(d_ok))
            logger_client_eha.info("First Status OK: {} => {}".format(d_ok, self.system_data["OK"][ok]["STATUS_OK"]))

    def buildProtocol(self, addr):
        return EbilockProtocol(self, self.system_data)


    def switch_to_pass(self, *args):
        """ system to switch to the safe mode """
        logger_client_eha.debug("The delay time of 1.5.sec has worked. To go into System in 'SAFE' mode!!!")
        self.system_data["Start_timer"] = False
        self.system_data["System_Status"] = self._SAFE
        self.system_data["Timer_status"] = False
        logger_client_eha.debug("System switch to SAFE mode => {}".format(self.system_data["System_Status"]))

    def errorback_timer(self, *args):
        return

    def switch_to_pass_ok(self, ok):
        """ system to switch to the safe mode for OK's"""
        logger_client_eha.debug("The delay time of 1.5.sec has worked. To go into OK in 'SAFE' mode!!!: {}".format(ok))
        _ok = self.system_data["WORK_OK"][ok]
        _ok["Start_timer"] = False
        _ok["STATUS_OK"] = self._SAFE
        _ok["Timer_status"] = False
        _ok["ZONE_FOR_CNS"] = dict.fromkeys(range(36), 0)
        logger_client_eha.debug("{} OK's switch to SAFE mode => {}".format(ok, _ok["STATUS_OK"]))
        logger_client_eha.debug(self.prints.show_status_cns_zone())

    def timer_restart_ok(self, ok):
        from twisted.internet import reactor

        # d_+str(ok) = self.system_data["Timer_OK"][ok]
        dd = self.system_data["Timer_OK"][ok]
        reactor.callLater(0.0, dd.cancel)
        self.system_data["Timer_OK"][ok] = None
        d_ = defer.Deferred()
        d_.addCallbacks(self.switch_to_pass_ok, self.errorback_timer)
        d_.addBoth(self.errorback_timer)
        self.system_data["Timer_OK"][ok] = d_
        from twisted.internet import reactor
        reactor.callLater(1.5, d_.callback, ok)
        logger_client_eha.debug("Timer OK: {} Restart!!!".format(ok))

    def timer_restart(self):
        from twisted.internet import reactor
        reactor.callLater(0.0, self.d.cancel)
        self.d = None
        self.d = defer.Deferred()
        self.d.addCallbacks(self.switch_to_pass, self.errorback_timer)
        self.d.addBoth(self.errorback_timer)
        reactor.callLater(1.5, self.d.callback, stat)
        logger_client_eha.debug("System Timer Restart!!!")

    def d_send_status(self, status_order):
        from twisted.internet import reactor
        d = None
        d = defer.Deferred()
        d.addCallback(self.protocol(self, self.system_data).dataSend())
        reactor.callLater(0, d.callback, 'send_status')
        logger_client_eha.debug("Callback send status started")

    def check_timer(self, *args):
        logger_client_eha.debug(self.prints.show_status_timer_system())

        if self.system_data["Timer_status"] and not self.system_data["Start_timer"] and self.system_data["System_Status"] == "WORK":
            from twisted.internet import reactor
            reactor.callLater(1.5, self.switch_to_pass, self._SAFE)
            self.system_data["Err_Count"] = 0
            self.system_data["Start_timer"] = True
            logger_client_eha.debug("Activate CallLater 1.5c - 1!!!")

        else:
            if not self.system_data["Timer_status"] and not self.system_data["Start_timer"] and self.system_data["System_Status"] == "WORK" or\
             not self.system_data["Timer_status"] and self.system_data["Start_timer"] and self.system_data["System_Status"] == "WORK":
                self.timer_restart()
                self.system_data["Timer_status"] = False
                self.system_data["Start_timer"] = True

            else:
                if not self.system_data["Timer_status"] and\
                 self.system_data["System_Status"] == self._SAFE and self.system_data["ORDER_DESC_ALARM"] is None:
                    self.system_data["System_Status"] = self._WORK
                    self.timer_restart()
                else:
                    pass

        logger_client_eha.info(self.prints.show_status_timer_system())

    def check_timer_ok(self):
        logger_client_eha.debug(self.prints.show_status_ok())

        for ok in self.system_data["WORK_OK"]:
            _ok = self.system_data["WORK_OK"][ok]
            if _ok["Timer_status"] and not _ok["Start_timer"] and _ok["STATUS_OK"] == "WORK":
                from twisted.internet import reactor
                reactor.callLater(1.5, self.switch_to_pass_ok, ok)
                _ok["Err_Count"] = 0
                _ok["Start_timer"] = True
                logger_client_eha.debug("Activate CallLater OK: {}, 1.5c!!!".format(ok))

            else:
                if not _ok["Timer_status"] and not _ok["Start_timer"] and _ok["STATUS_OK"] == "WORK" or\
                 not _ok["Timer_status"] and _ok["Start_timer"] and _ok["STATUS_OK"] == "WORK":
                    self.timer_restart_ok(ok)
                    _ok["Timer_status"] = False
                    _ok["Start_timer"] = True
                else:
                    if not _ok["Timer_status"] and\
                     _ok["STATUS_OK"] == self._SAFE and _oka["DESC_ALARM"] is None:
                        _ok["STATUS_OK"] = self._WORK
                        self.timer_restart_ok(ok)
                    else:
                        pass
        logger_client_eha.info(self.prints.show_status_ok())

    def clientConnectionFailed(self, connector, reason):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        print("{} Failed to connect to: {}".format(time.ctime(), connector.getDestination()))
=======
        logger_client_eha.warning("Failed to connect to: {}".format(connector.getDestination()))
>>>>>>> client_eha_for_python_3_6
=======
        print("{} Failed to connect to: {}".format(time.ctime(), connector.getDestination()))
>>>>>>> 1dd4af5585806de725b942e4b47761b309663a0a
=======
        logger_client_eha.warning("Failed to connect to: {}".format(connector.getDestination()))
>>>>>>> client_eha_for_python_3_6
        time.sleep(1)
        connector.connect()

    def clientConnectionLost(self, connector, reason):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        print("{} Client connection Lost: {}".format(time.ctime(), connector.getDestination()))
=======
        logger_client_eha.warning("Client connection Lost: {}".format(connector.getDestination()))
>>>>>>> client_eha_for_python_3_6
=======
        print("{} Client connection Lost: {}".format(time.ctime(), connector.getDestination()))
>>>>>>> 1dd4af5585806de725b942e4b47761b309663a0a
=======
        logger_client_eha.warning("Client connection Lost: {}".format(connector.getDestination()))
>>>>>>> client_eha_for_python_3_6
        time.sleep(1)
        connector.connect()

    def order_received(self):
        if ord_ok.from_hdlc(self.system_data).check_telegramm():
            logger_client_eha.info(self.prints.show_receive_packet())

        logger_client_eha.info(self.prints.show_work_packet())
        status = self.wf.work_order()

        if status == 80:
            logger_client_eha.debug("Send Status!!!")
            # if stat.from_send_status(self.system_data_old).code_telegramm():
            #    self.system_data_old["HDLC_SEND_STATUS"] = None
            #    self.system_data_old["HDLC_SEND_STATUS"] = create_hdlc(self.system_data_old["ORDER_STATUS"]

        elif status == 110:
            logger_client_eha.debug("Lost Communication\nTransfer status with old counters and Increase the counter")
            # order_count_A = self.system_data["ORDER_Count_A"]
            # order_count_B = self.system_data["ORDER_Count_B"]
            self.system_data["Count_A"] = self.system_data["ORDER_Count_A"]
            self.system_data["Count_B"] = self.system_data["ORDER_Count_B"]

        elif status == 0:

            for ok in self.system_data["OK"]:
                _ok = self.system_data["OK"][ok]
                self.system_data["WORK_OK"][ok] = _ok.copy()

            if stat.from_ok(self.system_data).create_status():
                self.system_data["HDLC_SEND_STATUS"] = None
                self.system_data["HDLC_SEND_STATUS"] = create_hdlc(self.system_data["ORDER_STATUS"])

        elif status == 50:
            logger_client_eha.debug("Discard a telegram")
            self.system_data["Timer_status"] = True

        else:
                self.system_data["HDLC_SEND_STATUS"] = None
                self.system_data["ORDER_STATUS"] = None
                logger_client_eha.debug("Don't send status!!!")

        self.check_timer()
        self.check_timer_ok()



