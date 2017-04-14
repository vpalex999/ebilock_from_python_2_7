""" Module for processing and outputting information """
import time
from pprint import pprint

class PrintStatus(object):
    def __init__(self, system_data):
        # self.system_data_old = system_data_old
        self.system_data = system_data


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

    def show_receive_packet(self):
        if self.system_data["ORDER"] is None:
            print("Empty receive packet")
        else:
            print("{} receive order: status system: {}, order status: {}, err_code: {}, delta time: {}, CountA: {}, CountB: {}, Zone: {}".format(time.ctime(), self.system_data["System_Status"],\
                    self.system_data["ORDER"]["DESC_ALARM"], self.system_data["ORDER"]["CODE_ALARM"], self.system_data["time_delta"],\
                     hex(self.system_data["Count_A"]), hex(self.system_data["Count_B"]), self.system_data["ORDER"]["STATUS_ZONE"]))