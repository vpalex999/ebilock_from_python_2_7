""" Module for processing and outputting information """

class PrintStatus(object):
    def __init__(self, system_data):
        self.system_data = system_data

    def show_admin_address_ok(self):
        print("Administrative settings EHA: LOOP: {}, AREA: {}, HUB: {}, NUMBER: {}".format(self.system_data["LOOP_OK"],\
              self.system_data["AREA_OK"], self.system_data["HUB_OK"], self.system_data["NUMBER_OK"]))

    def show_receive_address_ok(self):
        tlg_a = self.system_data["order_work"]["TLG_A"]
        if tlg_a:
            print("Receive address OK from the EBilock: LOOP: {}, AREA: {}, HUB: {}, NUMBER: {}, ADDRES: {}".format(tlg_a["LOOP_OK"],\
              tlg_a["AREA_OK"], tlg_a["HUB_OK"], tlg_a["NUMBER_OK"], tlg_a["ADDR_OK"]))
        else:
            print("No data received")

    def show_zone_cns(self):
        print("Status zone from CNS: {}".format(self.system_data["ZONE_CNS"]))

    def show_status_telegramm(self):
        if self.system_data[ORDER_STATUS] is None:
            print("Empty status telegramm!!!")
        else:
            print("Status telegramm: {}".format(ORDER_STATUS))
