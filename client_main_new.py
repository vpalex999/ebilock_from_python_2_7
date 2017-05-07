""" Client-Main"""
import datetime
import sources.client_eha_new as c_eha
import sources.client_parser as c_parser
from twisted.internet import defer
from twisted.internet import reactor
import logging

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
    """
    EHM_STATUS: 'PASS' - silence mode, 'WORK' - work mode
    """
    logger_main.info("=====Start client EHA from Python=====")

    file_config = c_parser.parse_args()
    # status_start = True
    start = datetime.datetime.now()

    def get_order(host, port1, port2, system_data_ok):

        d = defer.Deferred()
        from twisted.internet import reactor
        factory1 = c_eha.EbilockClientFactory(d, c_parser.system_data)
        # factory2 = c_eha.EbilockClientFactory(d, c_parser.system_data)
        reactor.connectTCP(host, port1, factory1)
        # reactor.connectTCP(host, port2, factory2)
        return d

    def got_order(data):
        print("delta time: {}".format(data["time_delta"]))

    def order_filed(err):
        print("Order filed: {}".format(err))
        order_done()

    def order_done():
        print("Reactor stop!!!")
        reactor.stop()

    if file_config:
        if c_parser.start_parser(file_config[0]):
            logger_main.debug(c_parser.data_from_config)

            d = get_order(c_parser.data_from_config["host"],\
                          c_parser.data_from_config["port1"],\
                          c_parser.data_from_config["port2"],\
                          c_parser.system_data_ok)
            d.addCallbacks(got_order, order_filed)
        reactor.run()
        elasped = datetime.datetime.now() - start
        logger_main.warning('=====Stop client EHA, Uptime: {}====='.format(elasped))
    else:
        logger_main.warning("No 'file_config.json' with arguments")


if __name__ == '__main__':
    client_main()
