""" Client-Main"""
import datetime
from sources.client_eha_factory import EbilockClientFactory
import sources.client_parser as c_parser
from twisted.internet import reactor
import logging
import time

logger_main = logging.getLogger("client_main")
logger_main.setLevel(logging.DEBUG)
handler_main = logging.FileHandler("eha.log")
handler_main.setLevel(logging.INFO)
formatter_main = logging.Formatter("%(asctime)s %(levelname)s | %(message)s")
handler_main.setFormatter(formatter_main)
logger_main.addHandler(handler_main)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter("%(asctime)s %(levelname)s in %(module)s - %(lineno)d | %(message)s")
console_handler.setFormatter(console_formatter)
logger_main.addHandler(console_handler)


def client_main():
    logger_main.info("=====Start client EHA from Python=====")

    file_config = c_parser.parse_args()
    start = datetime.datetime.now()

    class GetOrder(object):
        def __init__(self, host, port1, port2, system_data_ok):
            self.connector1 = {"hdlc_receive": None, "hdlc_send": None, "start_time": time.time(), "time_delta": 0.00}
            self.connector2 = {"hdlc_receive": None, "hdlc_send": None, "start_time": time.time(), "time_delta": 0.00}
            self.host = host
            self.port1 = port1
            self.port2 = port2
            self.system_data_ok = system_data_ok
            self.factory1 = EbilockClientFactory(self, self.connector1)
            self.factory2 = EbilockClientFactory(self, self.connector2)
            from twisted.internet import reactor
            reactor.connectTCP(self.host, self.port2, self.factory1)
            reactor.connectTCP(self.host, self.port1, self.factory2)


        def print_callback(self):
            logger_main.debug("callback1: {}, time: {:0.3f}".format(self.connector1["hdlc_receive"], self.connector1["time_delta"]))
            logger_main.debug("callback2: {}, time: {:0.3f}".format(self.connector2["hdlc_receive"], self.connector1["time_delta"]))
            self.send_data()

        def send_data(self):
            self.factory1.connection.dataSend(self.connector1["hdlc_receive"])
            self.factory2.connection.dataSend(self.connector2["hdlc_receive"])

    if file_config:
        if c_parser.start_parser(file_config[0]):
            logger_main.debug(c_parser.data_from_config)

            clientEha = GetOrder(c_parser.data_from_config["host"],\
                                 c_parser.data_from_config["port1"],\
                                 c_parser.data_from_config["port2"],\
                                 c_parser.system_data_ok)

        reactor.run()
        elasped = datetime.datetime.now() - start
        logger_main.warning('=====Stop client EHA, Uptime: {}====='.format(elasped))
    else:
        logger_main.warning("No 'file_config.json' with arguments")


if __name__ == '__main__':
    client_main()
