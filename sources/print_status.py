""" Module for processing and outputting information """
import time
from pprint import pprint


class PrintStatus(object):
    def __init__(self, system_data):
        # self.system_data_old = system_data_old
        self.system_data = system_data

    def show_status_timer_system(self):
        print("Check System Timer Status: {}, Check System Timer Start: {}, Check System Status: {}, System Err_Count: {}"\
              .format(\
                    self.system_data["Timer_status"],\
                    self.system_data["Start_timer"],\
                    self.system_data["System_Status"],\
                    self.system_data["Err_Count"]))

    def show_OK(self):
        ok = self.system_data["WORK_OK"]
        [print("Status OK: {}, {}".format(x, ok[x]["STATUS_OK"])) for x in ok]

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
ZONE_FOR_CNS: {}\n".format(_ok["ADDRESS_OK"], _ok["ZONE_FOR_CNS"])
        return zones + "\n"

    def show_status_cns_zone(self):
        zones = ""
        for ok in self.system_data["WORK_OK"]:
            _ok = self.system_data["WORK_OK"][ok]
            zones = zones + "\nOK: {},\n\
ZONE_FROM_CNS: {},\nZONE_FOR_CNS: {}".format(_ok["ADDRESS_OK"], _ok["ZONE_FROM_CNS"], _ok["ZONE_FOR_CNS"])
        return zones + "\n"

    def show_receive_packet(self):
        # if self.system_data["ORDER_STATUS"] is None:
        #     print("Empty receive packet")
        # else:
        print("{} Receive Order: Status System: {}, \
order status: {}, \
err_code: {}, \
delta time: {}, \
ORDER_Count_A: {}, \
ORDER_Count_B: {}, \n\
Zone_for_CNS: {}\n"\
                .format(time.ctime(),\
                self.system_data["System_Status"],\
                self.system_data["ORDER_DESC_ALARM"], \
                self.system_data["ORDER_CODE_ALARM"], \
                self.system_data["time_delta"],\
                hex(self.system_data["ORDER_Count_A"]), \
                hex(self.system_data["ORDER_Count_B"]), \
                self.show_status_order_zone()))

    def show_work_packet(self):
            print("{} Work Order: status system: {}, \
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
                hex(self.system_data["Count_A"]), \
                hex(self.system_data["Count_B"]), \
                self.show_status_cns_zone()))
