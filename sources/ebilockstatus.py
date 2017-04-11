from crccheck.crc import Crc16CcittFalse
from sources.crc8 import create_crc_8 as crc8
from sources.error import EbException
import binascii


class Ebilock_status(object):
    """ class Ebilock status """

    ID_SOURCE = hex(1)
    ID_DEST = hex(0)
    TYPE_PACKET = hex(3)
    SIZE_PACKET = hex(0)
    ZERO_BYTE = hex(0)

    @staticmethod
    def hex_to_2bytes(size_packet, size_hex=0):
        item = "{:x}".format(int(hex(size_packet), 16))
        if len(item) % 2 != 0:
            item = "0"+item
        item_unhex = bytearray.fromhex(item)
        if size_hex < len(item_unhex):
            size_hex = len(item_unhex)
        mass = [hex(0) for x in xrange(size_hex)]
        for item in item_unhex:
            mass.append(hex(item))
            del mass[0]
        return mass

    def __init__(self, system_data, count_a, count_b):
        self._system_data = system_data
        self._count_a = count_a
        self._count_b = count_b
        self._zone_hex = []
        self._telegramm_a_hex = []
        self._telegramm_b_hex = []
        self._telegramm_b_hex_inversion = []
        self._telegramm_ab = []
        self._crc16 = []
        self._order = []
        self._size_packet = []
        self._size_ab = []
        self._alarm_code = hex(0)
        # print("count_a: {}, count_b: {}, CountA: {}, CountB: {}".format(count_a, count_b, self.system_data["Count_A"], self.system_data["Count_B"]))

    @classmethod
    def from_ok(cls, object):
        count_a = object["Count_A"]
        count_b = object["Count_B"]

        if count_a == 1 and count_b == 254:
            count_a = 255
            count_b = 0
        else:
            count_a -= 1
            count_b += 1
        # print("count_a: {}, count_b: {}, CountA: {}, CountB: {}".format(count_a, count_b, object["Count_A"], object["Count_B"]))
        return cls(object, count_a, count_b)

    @classmethod
    def from_loss_connect(cls, object):
        count_a = object["Count_A"]
        count_b = object["Count_B"]
        if count_a == 254 and count_b == 1:
            object["Count_A"] = 1
            object["Count_B"] = 254
        else:
            object["Count_A"] = object["Count_A"] + 1
            object["Count_B"] = object["Count_B"] - 1

        return cls(object, count_a, count_b)

    @classmethod
    def from_send_status(cls, object):
        count_a = object["Count_A"]
        count_b = object["Count_B"]
        return cls(object, count_a, count_b)

    def _code_zone_to_hex(self):
        offset_by = 0
        result = 0
        temp = 0
        zone = self._system_data["ZONE_CNS"]
        #print("status_zone: {}".format(zone))
        for j in range(int(len(list(zone.keys())))):
            temp = zone[j+1]
            temp = temp << offset_by
            offset_by += 2
            result = result | temp
            if j and (j+1) % 4 == 0:
                self._zone_hex.insert(0, hex(result))
                result = 0
                offset_by = 0
        print("zone_hex: {}".format(self._zone_hex))

    #def _code_size_packet(self):
    #    offset_by = 0
    #    result = 0
    #    temp = 0
    #    sum_size = 12+len(self._telegramm_a_hex)*2

    def _code_address_ok(self, telegramm):
        offset_by = 12
        mass = [self._system_data["LOOP_OK"], self._system_data["AREA_OK"], self._system_data["HUB_OK"], self._system_data["NUMBER_OK"]]
        # print(mass)
        result = self._system_data["LOOP_OK"] << 4
        temp = self._system_data["AREA_OK"] << 1
        result = result | temp
        telegramm.insert(0, hex(result))
        result = 0
        temp = self._system_data["HUB_OK"] << 4
        result = result | temp
        temp = self._system_data["NUMBER_OK"] << 1
        temp = temp | 1
        result = result | temp
        telegramm.insert(1, hex(result))

    def _code_telegramm_a(self):
        self._code_address_ok(self._telegramm_a_hex)
        ml = 6 + len(self._zone_hex) << 4
        co = 8
        result = ml | co
        self._telegramm_a_hex.insert(2, hex(result))
        self._telegramm_a_hex.insert(3, hex(self._count_a))
        self._telegramm_a_hex.insert(4, self._alarm_code)
        for item in self._zone_hex:
            self._telegramm_a_hex.append(item)
        # calculate CRC-8

    def _code_telegramm_b(self):
        self._code_address_ok(self._telegramm_b_hex)
        ml = 6 + len(self._zone_hex) << 4
        co = 12
        result = ml | co
        self._telegramm_b_hex.insert(2, hex(result))
        self._telegramm_b_hex.insert(3, hex(self._count_b))
        self._telegramm_b_hex.insert(4, self._alarm_code)
        for item in self._zone_hex:
            self._telegramm_b_hex.append(item)
        # calculate CRC-8

    def _inversion_byte(self, telegramm):
        return [hex(int(telegramm[x], 16).__xor__(255)) for x in range(len(telegramm))]

    def _create_crc_8(self, telegramm):
        data = telegramm[:]
        del data[4]
        del data[3]
        crc_8 = crc8(data)
        telegramm.append(crc_8)

    def _create_crc_16(self, telegramm):
        r_c = bytearray([int(telegramm[x], 16) for x in range(len(telegramm))])
        # print("r_c: {}".format(r_c))
        get_check_rc = Crc16CcittFalse.calchex(r_c)
        # print("get_check_rc16_hex: {}".format(get_check_rc))
        self._crc16 = self.hex_to_2bytes(int(get_check_rc, 16), 2)

    def _add_to_paket(self, data_src, data_dst):
        for item in data_src:
            data_dst.append(item)

    def _create_packet(self):
        status = False
        self._add_to_paket(self._telegramm_a_hex, self._telegramm_ab)
        self._add_to_paket(self._telegramm_b_hex_inversion, self._telegramm_ab)
        size_ab = len(self._telegramm_ab)
        self._size_ab = self.hex_to_2bytes(size_ab, 2)
        size_packet = 14 + size_ab
        self._size_packet = self.hex_to_2bytes(size_packet, 4)
        self._order.append(self.ID_SOURCE)
        self._order.append(self.ID_DEST)
        self._order.append(self.TYPE_PACKET)
        self._add_to_paket(self._size_packet, self._order)
        self._order.append(self.ZERO_BYTE)
        self._order.append(hex(self._count_a))
        self._order.append(hex(self._count_b))
        self._add_to_paket(self._size_ab, self._order)
        self._add_to_paket(self._telegramm_ab, self._order)
        self._create_crc_16(self._order)
        self._add_to_paket(self._crc16, self._order)
        if size_packet == len(self._order):
            self._system_data["ORDER_STATUS"] = self._order
            status = True
        return status

    def code_telegramm(self):
        status = False
        self._code_zone_to_hex()
        self._code_telegramm_a()
        # print("Status telegramm a: {}".format(self._telegramm_a_hex))
        self._code_telegramm_b()
        # print("Status telegramm b: {}".format(self._telegramm_b_hex))
        self._telegramm_b_hex_inversion = self._inversion_byte(self._telegramm_b_hex)
        self._create_crc_8(self._telegramm_a_hex)
        self._create_crc_8(self._telegramm_b_hex_inversion)
        if self._create_packet():
            status = True
            print("Status telegramm a: {}".format(self._telegramm_a_hex))
            print("Status telegramm inv b: {}".format(self._telegramm_b_hex_inversion))
            print("size_packet: {}".format(self._size_packet))
            print("CRC-16: {}".format(self._crc16))
            # print("Order: {}".format(self._order))
        return status
        


