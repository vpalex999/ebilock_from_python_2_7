""" Client-Main"""
import datetime
from sources.client_eha import *
from twisted.internet import defer
from twisted.internet import reactor


def client_main():
    """
    EHM_STATUS: 'PASS' - silence mode, 'WORK' - work mode
    """
    status_start = True
    start = datetime.datetime.now()
    #port = 4016
    port = 9090
    #host = '192.168.200.6'
    #host = '192.168.101.100'
    host = '192.168.10.168'
    #port = 10000
    #host = "localhost"

    addresses_ok = [3257, "3259"]
    system_data_ok = {}

    def from_address_ok(address_ok):
        #print(type(address_ok))
        if type(address_ok) == int:
            address_ok = "{}".format(address_ok)
        sys_data_ok = {
            "STATUS_OK": "SAFE",
            "LOOP_OK": False,
            "AREA_OK": False,
            "HUB_OK": False,
            "NUMBER_OK": False,
            "ADDRESS_OK": False,
            "Err_Count": 0,
            "count_a": 1,
            "count_b": 254,
            "ORDER_WORK": None,
            "ZONE_FROM_CNS": {1: 3, 2: 1, 3: 1, 4: 1, 5: 0, 6: 2, 7: 2, 8: 3},
            "ZONE_FOR_CNS": None,
            "CODE_ALARM": 0,
            "DESC_ALARM": "OK",
        }

        def _code_address_ok(sys_data_ok):
            address_ok = ""
            result = sys_data_ok["LOOP_OK"] << 4
            temp = sys_data_ok["AREA_OK"] << 1
            result = result | temp
            address_ok = address_ok + "{:02x}".format(int(hex(result), 16))
            result = 0
            temp = sys_data_ok["HUB_OK"] << 4
            result = result | temp
            temp = sys_data_ok["NUMBER_OK"] << 1
            temp = temp | 1
            result = result | temp
            address_ok = address_ok + "{:02x}".format(int(hex(result), 16))
            sys_data_ok["ADDRESS_OK"] = address_ok

        if len(address_ok) == 4:
            loop = int(address_ok[0], 16)
            area = int(address_ok[1], 16)
            hub = int(address_ok[2], 16)
            number = int(address_ok[3], 16)
            if area & 1 != 0:
                print("Invalid configure AREA OK!")
                return False
            elif number & 1 != 1:
                print("Invalid configure Number OK!")
                return False
            else:
                area = area >> 1
                number = number >> 1
                sys_data_ok["LOOP_OK"], sys_data_ok["AREA_OK"], sys_data_ok["HUB_OK"], sys_data_ok["NUMBER_OK"] = loop, area, hub, number
                _code_address_ok(sys_data_ok)
                diction = {}
                diction[sys_data_ok["ADDRESS_OK"]] = sys_data_ok
                return diction
        else:
            print("number of characters to be equal to 4")
            return False

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

    for ok in addresses_ok:
        try:
            system_data_ok.update(from_address_ok(ok))
        except:
            status_start = False
            print("Wrong adress OK: '{}'".format(ok))

    if status_start:
        d = get_order(host, port, system_data_ok)
        d.addCallbacks(got_order, order_filed)
        reactor.run()
        elasped = datetime.datetime.now() - start
        print('Got orders in {}'.format(elasped))

if __name__ == '__main__':
    client_main()
