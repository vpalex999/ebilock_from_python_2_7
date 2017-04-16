from crccheck.crc import Crc16CcittFalse
from sources.crc8 import create_crc_8 as crc8
from sources.error import EbException
import binascii


class Ebilock_status(object):
    """ class Ebilock status """
    count = 0
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
        # for python 3-6:
        mass = [hex(0) for x in range(size_hex)]
        # for python 2-7:
        # mass = [hex(0) for x in xrange(size_hex)]
        for item in item_unhex:
            mass.append(hex(item))
            del mass[0]
        return mass

    def __init__(self, system_data, count_a, count_b):

        # self.count += 1
        # print("status_count: {}".format(self.count))
        self._system_data = system_data
        self._count_a = count_a
        self._count_b = count_b
        self._block_ab = []
        self._crc16 = []
        self._order = []
        self._size_packet = []
        self._size_block_ab = []
        self._alarm_code = hex(0)
        self._count_work_ok = 0
        self._addresses_ok = []
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

    def _code_zone_to_hex(self, zone_hex, telegramm_data):
        offset_by = 0
        result = 0
        temp = 0
        zone = telegramm_data["ZONE_FROM_CNS"]
        # print("status_zone: {}".format(zone))
        for j in range(int(len(list(zone.keys())))):
            temp = zone[j+1]
            temp = temp << offset_by
            offset_by += 2
            result = result | temp
            if j and (j+1) % 4 == 0:
                zone_hex.append(hex(result))
                result = 0
                offset_by = 0
        # print("zone_hex: {}".format(zone_hex))

    def _code_address_ok(self, telegramm, telegramm_data):
        offset_by = 12
        result = telegramm_data["LOOP_OK"] << 4
        temp = telegramm_data["AREA_OK"] << 1
        result = result | temp
        telegramm.append(hex(result))
        result = 0
        temp = telegramm_data["HUB_OK"] << 4
        result = result | temp
        temp = telegramm_data["NUMBER_OK"] << 1
        temp = temp | 1
        result = result | temp
        telegramm.append(hex(result))

    def _code_telegramm_a(self, zone_hex, telegramm_a_hex, telegramm_data):
        self._code_address_ok(telegramm_a_hex, telegramm_data)
        ml = 6 + len(zone_hex) << 4
        co = 8
        result = ml | co
        telegramm_a_hex.insert(2, hex(result))
        telegramm_a_hex.insert(3, hex(self._count_a))
        telegramm_a_hex.insert(4, self._alarm_code)
        telegramm_a_hex.extend(zone_hex)

    def _code_telegramm_b(self, zone_hex, telegramm_b_hex, telegramm_data):
        self._code_address_ok(telegramm_b_hex, telegramm_data)
        ml = 6 + len(zone_hex) << 4
        co = 12
        result = ml | co
        telegramm_b_hex.insert(2, hex(result))
        telegramm_b_hex.insert(3, hex(self._count_b))
        telegramm_b_hex.insert(4, self._alarm_code)
        # inversion data:
        telegramm_b_hex.extend([hex(int(x, 16).__xor__(255)) for x in zone_hex])

    def _create_crc_8(self, telegramm):
        data = telegramm[:]
        del data[4]
        del data[3]
        # print("telegramm-CRC-8 data: {}".format(data))
        crc_8 = crc8(data)
        telegramm.append(crc_8)
        # print("telegramm-CRC-8: {}".format(telegramm))

    def _create_crc_16(self, telegramm):
        r_c = bytearray([int(telegramm[x], 16) for x in range(len(telegramm))])
        # print("r_c: {}".format(r_c))
        get_check_rc = Crc16CcittFalse.calchex(r_c)
        # print("get_check_rc16_hex: {}".format(get_check_rc))
        self._crc16 = self.hex_to_2bytes(int(get_check_rc, 16), 2)

    # def _add_to_paket(self, data_src, data_dst):
    #     for item in data_src:
    #         data_dst.append(item)

    def _create_packet(self):
        status = False

        add_hex_ok = []
        for addr in self._addresses_ok:
            bin_ok = bytearray.fromhex(addr)
            [add_hex_ok.append("{}".format(hex(int(x)))) for x in bin_ok]
        size_addreses_ok = self.hex_to_2bytes(len(add_hex_ok), 2)
        #print(size_addreses_ok)
        size_block_ab = len(self._block_ab)
        self._size_block_ab = self.hex_to_2bytes(size_block_ab, 2)
        body_packet = []
        body_packet.extend(size_addreses_ok)
        body_packet.extend(add_hex_ok)
        body_packet.extend(self._size_block_ab)
        body_packet.extend(self._block_ab)
        # print("Body packet: {}".format(body_packet))
        size_packet = 10 + len(body_packet)
        self._size_packet = self.hex_to_2bytes(size_packet, 4)
        self._order.append(self.ID_SOURCE)
        self._order.append(self.ID_DEST)
        self._order.append(self.TYPE_PACKET)
        self._order.extend(self._size_packet)
        self._order.append(self.ZERO_BYTE)
        self._order.extend(body_packet)
        self._create_crc_16(self._order)
        self._order.extend(self._crc16)

        if size_packet == len(self._order):
            self._system_data["ORDER_STATUS"] = self._order
            # print(self._order)
            status = True
        return status

    def create_status(self):
        status = False
        for ok in self._system_data["OK"]:
            _ok = self._system_data["OK"][ok]
            if _ok["STATUS_OK"] == "WORK":
                # print("WORK")
                if self._code_telegramm(_ok):
                    # print("WORK")
                    self._count_work_ok += 1
                    self._addresses_ok.append(_ok["ADDRESS_OK"])
                    # print("Work count OK: {}".format(self._count_work_ok))
        if self._create_packet():
            status = True
        return status

    def _code_telegramm(self, telegramm_data):
        # print(telegramm_data)
        _zone_hex = []
        _telegramm_a_hex = []
        _telegramm_b_hex = []
        _telegramm_ab = []
        try:
            # print(telegramm_data)
            self._code_zone_to_hex(_zone_hex, telegramm_data)
            self._code_telegramm_a(_zone_hex, _telegramm_a_hex, telegramm_data)
            # print("Status telegramm a: {}".format(_telegramm_a_hex))
            self._code_telegramm_b(_zone_hex, _telegramm_b_hex, telegramm_data)
            # print("Status telegramm b: {}".format(_telegramm_b_hex))
            self._create_crc_8(_telegramm_a_hex)
            # self._create_crc_8(_telegramm_b_hex_inversion)
            self._create_crc_8(_telegramm_b_hex)
            _telegramm_ab.extend(_telegramm_a_hex)
            _telegramm_ab.extend(_telegramm_b_hex)
            self._block_ab.extend(_telegramm_ab)
            # print("Status telegramm a: {}".format(_telegramm_a_hex))
            # print("Status telegramm b: {}".format(_telegramm_b_hex))
            # print("Status telegramm ab : {}".format(_telegramm_ab))
            # print("Block ab: {}".format(self._block_ab))
            return True
        except:
            return False


