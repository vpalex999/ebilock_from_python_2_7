from crccheck.crc import Crc16CcittFalse
from sources.crc8 import check_crc_8 as crc8
from sources.error import EbException
import binascii


class Ebilock_status(object):
    """ class Ebilock status """

    def __init__(self, system_data, count_a, count_b):
        self.system_data = system_data
        self.count_a = count_a
        self.count_b = count_b
        self.zone_hex = []
        #print("count_a: {}, count_b: {}, CountA: {}, CountB: {}".format(count_a, count_b, self.system_data["Count_A"], self.system_data["Count_B"]))

    @classmethod
    def from_ok(cls, object):
        count_a = object["Count_A"]
        count_b = object["Count_B"]

        if count_a == 1 and count_b == 254:
            count_a = 255
            count_b = 1
        else:
            count_a -= 1
            count_b += 1
        #print("count_a: {}, count_b: {}, CountA: {}, CountB: {}".format(count_a, count_b, object["Count_A"], object["Count_B"]))
        return cls(object, count_a, count_b)

    @classmethod
    def from_loss_connect(cls, object):
        count_a = object["Count_A"]
        count_b = object["Count_B"]
        if count_a == 254 and count_b == 1:
            self.object["Count_A"] = 1
            self.object["Count_B"] = 254
        else:
            self.object["Count_A"] = self.object["Count_A"] + 1
            self.object["Count_B"] = self.object["Count_B"] - 1

        return cls(object, count_a+1, count_b-1)

    @classmethod
    def from_send_status(cls, object):
        count_a = object["Count_A"]
        count_b = object["Count_B"]
        return cls(object, count_a, count_b)

    def code_zone(self):
        offset_by = 0
        result = 0
        temp = 0
        zone = self.system_data["order_work"]["STATUS_ZONE"]
        print("status_zone: {}".format(zone))
        for j in range(int(len(list(zone.keys())))):
            temp = zone[j+1]
            temp = temp << offset_by
            offset_by += 2
            result = result | temp
            if j and (j+1) % 4 == 0:
                self.zone_hex.insert(0, hex(result))
                result = 0
                offset_by = 0
        print("zone_hex: {}".format(self.zone_hex))


