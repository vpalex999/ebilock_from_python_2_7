""" Client-Main"""
import datetime
from sources.client_eha import *
from sources.client_parser import *
from twisted.internet import defer
from twisted.internet import reactor


def client_main():
    """
    EHM_STATUS: 'PASS' - silence mode, 'WORK' - work mode
    """
    
    file_config = parse_args()

    status_start = True
    start = datetime.datetime.now()
    
    def get_order(host, port, system_data_ok):

        d = defer.Deferred()
        from twisted.internet import reactor
        factory = EbilockClientFactory(d, system_data_ok)
        reactor.connectTCP(host, port, factory)
        return d

    def got_order(data):
        print("delta time: {1}".format(data["time_delta"]))

    def order_filed(err):
        print("Order filed: {}".format(err))
        order_done()

    def order_done():
        print("Reactor stop!!!")
        reactor.stop()

    if file_config:
        if start_parser(file_config[0]):
            # print(data_from_config)
            d = get_order(data_from_config["host"], data_from_config["port1"], system_data_ok)
            d.addCallbacks(got_order, order_filed)
            reactor.run()
            elasped = datetime.datetime.now() - start
            print('Uptime client EHA: {}'.format(elasped))


if __name__ == '__main__':
    client_main()
