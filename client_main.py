""" Client-Main"""
import datetime
import sources.client_eha as c_eha
import sources.client_parser as c_parser
from twisted.internet import defer
from twisted.internet import reactor


def client_main():
    """
    EHM_STATUS: 'PASS' - silence mode, 'WORK' - work mode
    """

    file_config = c_parser.parse_args()
    # status_start = True
    start = datetime.datetime.now()

    def get_order(host, port, system_data_ok):

        d = defer.Deferred()
        from twisted.internet import reactor
        factory = c_eha.EbilockClientFactory(d, c_parser.system_data)
        reactor.connectTCP(host, port, factory)
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
            # print(data_from_config)
            d = get_order(c_parser.data_from_config["host"],\
                          c_parser.data_from_config["port1"], c_parser.system_data_ok)
            d.addCallbacks(got_order, order_filed)
        reactor.run()
        elasped = datetime.datetime.now() - start
        print('Uptime client EHA: {}'.format(elasped))
    else:
        print("No 'file_config.json' with arguments")


if __name__ == '__main__':
    client_main()
