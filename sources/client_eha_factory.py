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

    def __init__(self, factory, connector):
        self.connector = connector
        self.factory = factory
        self.buffer = bytearray()
        logger_client_eha.debug("initialization 'EbilockProtocol'")

    def delta_time(self, receive_time):
        self.connector["time_delta"] = receive_time - self.connector["start_time"]
        self.connector["start_time"] = time.time()

    def connectionMade(self):
        logger_client_eha.warning("Connect to... {}".format(self.transport.connector.getDestination()))

    def dataReceived(self, data):
        host = self.transport.getPeer().host
        port = self.transport.getPeer().port
        logger_client_eha.debug("- Client[{}] {}, received HDLC DATA: {}".format(port, host, data))
        work_data = hdlc_work(data, self.buffer)
        if work_data:
            logger_client_eha.info("{}Receive hdlc data [{}:{}]{}".format("="*30, host, port, "="*30))
            logger_client_eha.info("- Client[{}] received HDLC DATA".format(self.transport.getPeer().port))
            self.delta_time(time.time())
            self.connector["hdlc_receive"] = work_data
            self.factory.getorder.print_callback()
            self.buffer.clear()

    def dataSend(self, data):
        logger_client_eha.info("Send status =>{}".format(data))
        self.transport.write(data)


class EbilockClientFactory(ClientFactory):
    task_num = 1
    result = ""
    protocol = EbilockProtocol

    _SAFE = "SAFE"
    _WORK = "WORK"

    def __init__(self, getorder, connector):
        # self.defered = defered
        self.connector = connector
        self.getorder = getorder

    def buildProtocol(self, addr):
        self.connection = EbilockProtocol(self, self.connector)
        return self.connection

    def clientConnectionFailed(self, connector, reason):
        logger_client_eha.warning("Failed to connect to: {}".format(connector.getDestination()))
        time.sleep(1)
        connector.connect()

    def clientConnectionLost(self, connector, reason):
        logger_client_eha.warning("Client connection Lost: {}".format(connector.getDestination()))
        time.sleep(1)
        connector.connect()

    def factory_data_send(self, data):
        logger_client_eha.warning("factory send data: {}".format(data))
        self.connection.dataSend(data)


