""" Module for processing and outputting information """
import time
from pprint import pprint


class PrintStatus(object):
    def __init__(self, system_data):
        # self.system_data_old = system_data_old
        self.system_data = system_data

    def show_OK(self):
        ok = self.system_data["OK"]
        [print("Status OK: {}, {}".format(x, ok[x]["STATUS_OK"])) for x in ok]

    #def show_admin_address_ok(self):
    #    print("Administrative settings EHA: LOOP: {}, AREA: {}, HUB: {}, NUMBER: {}, ADDRESS_OK: {}".format(self.system_data_old["LOOP_OK"],\
    #          self.system_data_old["AREA_OK"], self.system_data_old["HUB_OK"], self.system_data_old["NUMBER_OK"], self.system_data_old["ADDRESS_OK"]))

    #def show_receive_address_ok(self):
    #    if self.system_data_old["order_work"] is None:
    #        return
    #    tlg_a = self.system_data_old["order_work"]["TLG_A"]
    #    if tlg_a:
    #        print("Receive address OK from the EBilock: LOOP: {}, AREA: {}, HUB: {}, NUMBER: {}, ADDRES: {}".format(tlg_a["LOOP_OK"],\
    #        tlg_a["AREA_OK"], tlg_a["HUB_OK"], tlg_a["NUMBER_OK"], tlg_a["ADDR_OK"]))
    #    else:
    #        print("No data received")

    #def show_zone_cns(self):
    #    print("Status zone from CNS: {}".format(self.system_data_old["ZONE_CNS"]))

    #def show_status_telegramm(self):
    #    if self.system_data_old["ORDER_STATUS"] is None:
    #        print("Empty status telegramm!!!")
    #    else:
    #        print("Status telegramm: {}".format(self.system_data_old["ORDER_STATUS"]))

    def show_all_data(self):
        pprint(self.system_data)

    def show_status_ok(self):
        for ok in self.system_data["WORK_OK"]:
            _ok = self.system_data["WORK_OK"][ok]
            print("OK: {}, STATUS_OK: {}, Timer_status: {}, Start_timer: {}, Err_Count: {}, count_a: {}, count_b: {}, RETURN_OK: {}"\
            .format(_ok["ADDRESS_OK"],\
                    _ok["STATUS_OK"],\
                    _ok["Timer_status"],\
                    _ok["Start_timer"],\
                    _ok["Err_Count"],\
                    hex(_ok["count_a"]),\
                    hex(_ok["count_b"]),\
                    _ok["RETURN_OK"]))

    def show_status_order_zone(self):
        zones = ""
        for ok in self.system_data["OK"]:
            _ok = self.system_data["OK"][ok]
            zones = zones + "\nOK: {}, \
ZONE_FROM_CNS: {}, \
ZONE_FOR_CNS: {}"\
                             .format(_ok["ADDRESS_OK"],\
                             _ok["ZONE_FROM_CNS"],\
                             _ok["ZONE_FOR_CNS"])
        return zones + "\n"

    def show_status_work_zone(self):
        zones = ""
        for ok in self.system_data["WORK_OK"]:
            _ok = self.system_data["WORK_OK"][ok]
            zones = zones + "\nOK: {}, \
ZONE_FROM_CNS: {}, \
ZONE_FOR_CNS: {}"\
                             .format(_ok["ADDRESS_OK"],\
                             _ok["ZONE_FROM_CNS"],\
                             _ok["ZONE_FOR_CNS"])
        return zones + "\n"


    def show_receive_packet(self):
        # if self.system_data["ORDER_STATUS"] is None:
        #     print("Empty receive packet")
        # else:
        print("{} receive order: status system: {}, \
order status: {}, \
err_code: {}, \
delta time: {}, \
ORDER_Count_A: {}, \
ORDER_Count_B: {}, \n\
Zone_for_CNS: {}"\
                .format(time.ctime(),\
                self.system_data["System_Status"],\
                self.system_data["ORDER_DESC_ALARM"], \
                self.system_data["ORDER_CODE_ALARM"], \
                self.system_data["time_delta"],\
                hex(self.system_data["ORDER_Count_A"]), \
                hex(self.system_data["ORDER_Count_B"]), \
                self.show_status_order_zone()))

    def show_work_packet(self):
            print("{} work order: status system: {}, \
order status: {}, \
err_code: {}, \
delta time: {}, \
Count_A: {}, \
Count_B: {}, \n\
Zone_for_CNS: {}"\
                .format(time.ctime(),\
                self.system_data["System_Status"],\
                self.system_data["ORDER_DESC_ALARM"], \
                self.system_data["ORDER_CODE_ALARM"], \
                self.system_data["time_delta"],\
                hex(self.system_data["ORDER_Count_A"]), \
                hex(self.system_data["ORDER_Count_B"]), \
                self.show_status_work_zone()))
