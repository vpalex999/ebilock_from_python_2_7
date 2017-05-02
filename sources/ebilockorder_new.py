from crccheck.crc import Crc16CcittFalse
from sources.crc8 import check_crc_8 as crc8
# from sources.hdlc import read_hdlc
from sources.hdlc import hdlc_work
from sources.error import EbException
import binascii
import re


class Ebilock_order(object):
    """ class Ebilock
    """
    STATUS_TLG = "OK"

    def __init__(self, telegramm, system_data, *args):
        self.arg = args
        if "hdlc" not in args:
            self.telegramm = telegramm.split(' ')
        else:
            self.telegramm = telegramm
        self.system_data = system_data

        self.telegramm_decode = {
            "CODE_ALARM": 0,
            "DESC_ALARM": "OK",
            "PACKET": "",
            "ID_SOURCE": "",
            "ID_DEST": "",
            "TYPE_PACKET": "",
            "LENGTH_PACKET": "",
            "PACKET_COUNT_A": "",
            "PACKET_COUNT_B": "",
            "SIZE_AB": "",
            "TELEGRAMM_AB": "",
            "RC": "",
        }

    @classmethod
    def from_hdlc(cls, object):
        # source_hdlc = read_hdlc(object["hdlc"])
        # source_hdlc = hdlc_work(object['hdlc'])
        source_hdlc = object['hdlc']
        # print(source_hdlc)
        if source_hdlc:
            telegramm = ["{:02x}".format(int(hex(x), 16)).upper() for x in source_hdlc]
            return cls(telegramm, object, "hdlc")

    @classmethod
    def from_test(cls, object):
        telegramm = object["hdlc"]
        return cls(telegramm, object, "test")

    desc_header_packet = {
        "TYPE_ID":
            {2: "2 - order", 4: "4 - empty order", },
        "TLG_AB":
            {
             "OK_START": 0,
             "OK_END": 1,
             "ML_CO": 2,
             "COUNT_AB": 3,
             "co":
             {
                4: "4 - order, telegramm A (source Ebilock950 R4)",
                6: "6 - order, telegramm B (source Ebilock950 R4)",
                8: "8 - status, telegramm A (source EHA)",
                "C": "C - status, telegramm B (source EHA)"
             },
            },
        }

    # desc_telegramm_ab = {
    #     "pass": ""
    # }

    def _check_byte_flow(self):
        """ Verifying bytes in the packet stream\
        and writing a package to a dictionary.\n
        check_byte_flow("00, ff")\n
        ARG: String of bytes in hex.
        """

        status = True
        sources = self.telegramm
        if len(sources) < 10:
            self.system_data["ORDER_CODE_ALARM"] = 10
            self.system_data["ORDER_DESC_ALARM"] = "Invalid package '{}' 2xByte, min = 10 2xByte".format(len(sources))
            # self.STATUS_TLG = "Invalid package '{}' 2xByte, min = 20 2xByte".format(len(sources))
            status = False

        for item in sources:
            if item == '':
                status = False
                self.system_data["ORDER_CODE_ALARM"] = 11
                self.system_data["ORDER_DESC_ALARM"] = "Empty value by index '{}'".format(sources.index(""))
                # self.STATUS_TLG = "Empty value by index '{}'".format(sources.index(""))
                break
            if len(item) != 2:
                status = False
                self.system_data["ORDER_CODE_ALARM"] = 12
                self.system_data["ORDER_DESC_ALARM"] = "Length value '{}' is not equal to 2".format(item)
                # self.STATUS_TLG = "Length value '{}' is not equal to 2".format(item)
                break
        self.telegramm_decode["PACKET"] = sources
        return status

    def _check_header_packet(self):
        """ Decoding the packet header\
        and writing data to a dictionary.\n
        check_header_packet()\n
        ARG: String of bytes in hex.
        """

        sources = self.telegramm

        # Check ID Sources
        tmp = int(sources[0], 16)
        if tmp != 0:
            self.system_data["ORDER_CODE_ALARM"] = 21
            self.system_data["ORDER_DESC_ALARM"] = "Error!  ID_SEND = '{}' should be 0".format(tmp)
            # self.STATUS_TLG = "Error!  ID_SOURCE = '{}' should be between 0 or 1".format(tmp)
            return False
        else:
            self.telegramm_decode["ID_SOURCE"] = tmp

        # Check ID Destination
        tmp = int(sources[1], 16)
        if tmp != 1:
            self.system_data["ORDER_CODE_ALARM"] = 22
            self.system_data["ORDER_DESC_ALARM"] = "Error!  ID_RECIEVE = '{}' should be 1".format(tmp)
            # self.STATUS_TLG = "Error!  ID_DEST = '{}' should be between 0 or 1".format(tmp)
            return False
        else:
            self.telegramm_decode["ID_DEST"] = tmp

        # Check Type Packet
        tmp = int(sources[2], 16)
        key_stat = False
        type_id = self.desc_header_packet["TYPE_ID"]
        for key, val in type_id.items():
            if int(key) == tmp:
                self.telegramm_decode["TYPE_PACKET"] = key
                key_stat = True
                break
        if not key_stat:
            self.system_data["ORDER_CODE_ALARM"] = 23
            self.system_data["ORDER_DESC_ALARM"] = "Error TYPE_ID: {}".format(tmp)
            return False

        # Check size paket
        tmp = int(''.join(sources[3: 7]), 16)
        if tmp != len(sources):
            self.system_data["ORDER_CODE_ALARM"] = 24
            self.system_data["ORDER_DESC_ALARM"] = "Error Checking length packet!!! data length = '{0}', actual length = '{1}'".format(tmp, len(sources))
            # self.STATUS_TLG = "Error Checking length packet!!! data length = '{0}', actual length = '{1}'".format(tmp, len(sources))
            return False
        else:
            self.telegramm_decode["LENGTH_PACKET"] = tmp

        # Check Null Byte
        tmp = int(sources[7], 16)
        if tmp != 0:
            self.system_data["ORDER_CODE_ALARM"] = 26
            self.system_data["ORDER_DESC_ALARM"] = "Invalid header structure, Zero byte value = '{}', must be 0".format(tmp)
            # self.STATUS_TLG = "Invalid header structure, Zero byte value = '{}', must be 0".format(tmp)
            return False

        # Check status request
        if int(sources[2], 16) == 4 and len(sources) == 10:
            self.system_data["ORDER_CODE_ALARM"] = 80
            self.system_data["ORDER_DESC_ALARM"] = "This status request"
            return False
        return True

    def _check_count_order(self):
        """ Reading and checking the consistency\
        of counters A / B order package\n
        check_count_ab_packet()\n
        ARG: String of bytes in hex.
        """

        try:
            for _ok in self.system_data["OK"]:
                if self.system_data["OK"][_ok]['CODE_ALARM'] is None:
                    ct_a = self.system_data["OK"][_ok]['count_a']
                    ct_b = self.system_data["OK"][_ok]['count_b']
                    ct_A = self.telegramm_decode["PACKET_COUNT_A"]
                    ct_B = self.telegramm_decode["PACKET_COUNT_B"]

                    if ct_a == 0 or ct_b == 255:
                        self.system_data["OK"][_ok]['CODE_ALARM'] = 33
                        self.system_data["OK"][_ok]['DESC_ALARM'] = "The value ct_a can not be 0: '{}' or the value ct_b can not be 255:'{}'".format(ct_a, ct_b)
                        return False

                    if ct_A - ct_a != 0 and ct_B - ct_b != 0:
                        self.system_data["OK"][_ok]['CODE_ALARM'] = 34
                        self.system_data["OK"][_ok]['DESC_ALARM'] = "Error_ctab or ctab Global. cta_gl: {}, ctb_gl: {}, cta: '{}', ctb: '{}'".format(hex(ct_A), hex(ct_B), hex(ct_a), hex(ct_b))
                        return False

                    if ct_A - ct_a != 0:
                        self.system_data["OK"][_ok]['CODE_ALARM'] = 37
                        self.system_data["OK"][_ok]['DESC_ALARM'] = "Error_cta"
                        # bself.STATUS_TLG = "Error_ctb"
                        return False

                    if ct_B - ct_b != 0:
                        self.system_data["OK"][_ok]['CODE_ALARM'] = 36
                        self.system_data["OK"][_ok]['DESC_ALARM'] = "Error_ctb"
                        # self.STATUS_TLG = "Error_cta"
                        return False

                    if ct_A + ct_B == 255:
                        if ct_a + ct_b == 255:
                            if (ct_A - ct_a) == 0 and (ct_B - ct_b) == 0:
                                return True
                            else:
                                self.system_data["OK"][_ok]['CODE_ALARM'] = 35
                                self.system_data["OK"][_ok]['DESC_ALARM'] = "Sum values count packet and count telegramm are not equal"
                                return False
                            if ct_A - ct_a == 0:
                                self.system_data["OK"][_ok]['CODE_ALARM'] = 38
                                self.system_data["OK"][_ok]['DESC_ALARM'] = "Error_ctb_gl"
                                # self.STATUS_TLG = "Error_ctb_gl"
                                return False
                            else:
                                self.system_data["OK"][_ok]['CODE_ALARM'] = 39
                                self.system_data["OK"][_ok]['DESC_ALARM'] = "Error_cta_gl"
                                # self.STATUS_TLG = "Error_cta_gl"
                                return False
                        else:
                            self.system_data["OK"][_ok]['CODE_ALARM'] = 40
                            self.system_data["OK"][_ok]['DESC_ALARM'] = "Err_ctab: a-'{}', b- {}".format(ct_a, ct_b)
                            return False

            return True
        except:
            return False

    def _check_body_telegramm_ab(self):
        """ Check the length of the block of telegrams A / B\n
        check_telegramm_ab("00, ff")\n
        ARG: String of bytes in hex.
        """
        sources = self.telegramm
        size_body = int(len(sources[8:-2]))

        # Check Empty data
        if size_body == 0:
            self.system_data["ORDER_CODE_ALARM"] = 45
            self.system_data["ORDER_DESC_ALARM"] = "Empty body packet - '{}'".format(size_body)
            # self.STATUS_TLG = "Empty data A/B - '{}'".format(size_body)
            return False

        # Check Global Count
        self.telegramm_decode["PACKET_COUNT_A"] = int(self.telegramm[8], 16)
        self.telegramm_decode["PACKET_COUNT_B"] = int(self.telegramm[9], 16)

        ct_A = self.telegramm_decode["PACKET_COUNT_A"]
        ct_B = self.telegramm_decode["PACKET_COUNT_B"]
        if ct_A == 0 and ct_B == 255:
            self.system_data["ORDER_CODE_ALARM"] = 31
            self.system_data["ORDER_DESC_ALARM"] = "The value global_ctA can not be: '{}' or the value global_ctB can not be:'{}'".format(hex(ct_A), hex(ct_B))
            return False
        elif ct_A == 0:
            self.system_data["ORDER_DESC_ALARM"] = "The value global_ctA can not be: '{}'".format(hex(ct_A))
            self.system_data["ORDER_CODE_ALARM"] = 32
            return False
        elif ct_B == 255:
            self.system_data["ORDER_DESC_ALARM"] = "The value global_ctB can not be: '{}'".format(hex(ct_B))
            self.system_data["ORDER_CODE_ALARM"] = 33
            return False

        if ct_A + ct_B != 255:
            self.system_data["ORDER_CODE_ALARM"] = 30
            self.system_data["ORDER_DESC_ALARM"] = "Error! Inconsistent global count: glA-'{}', glB- {}".format(hex(ct_A), hex(ct_B))
            return False

        self.system_data["ORDER_Count_A"] = ct_A
        self.system_data["ORDER_Count_B"] = ct_B

        # Check max size data
        # tmp = int(''.join(sources[10:12]), 16)
        real_len_data_ab = len(sources[12:-2])
        if real_len_data_ab > 4096:
            self.system_data["ORDER_CODE_ALARM"] = 25
            self.system_data["ORDER_DESC_ALARM"] = "Too long data > 4096 bytes - '{}'".format(real_len_data_ab)
            return False

        # Check empty telegramm A/B
        size_ab = int(''.join(sources[10:12]), 16)
        if size_ab == 0:
            self.system_data["ORDER_CODE_ALARM"] = 41
            self.system_data["ORDER_DESC_ALARM"] = "Empty size telegramm A/B - '{}'".format(size_ab)
            return False

        # Check equal zise A/B
        if not size_ab == real_len_data_ab:
            self.system_data["ORDER_CODE_ALARM"] = 43
            self.system_data["ORDER_DESC_ALARM"] = "telegramm length '{}' is not equal to the size A/B '{}'".format(real_len_data_ab, size_ab)
            return False
        else:
            self.telegramm_decode["SIZE_AB"] = size_ab
            self.telegramm_decode["TELEGRAMM_AB"] = sources[12:-2]
            return True

    def _parcer_ok(self):
        status = False
        try:
            tmp_ok = (self.telegramm_decode["TELEGRAMM_AB"])
            _ok = {}
            for x in self.system_data["OK"]:
                _ok[x] = None
                _ok[x+" double"] = 0
            actual_ok = None
            count_start = 0
            for i in range(len(tmp_ok)):
                if i != len(tmp_ok) - 1:
                    firs_ok = tmp_ok[i]+tmp_ok[i+1]
                    if firs_ok in _ok:
                        _ok[firs_ok+" double"] += 1
                        if _ok[firs_ok+" double"] <= 2:
                            if not actual_ok:
                                actual_ok = firs_ok
                                count_start = i
                            else:
                                if firs_ok != actual_ok:
                                    _ok[actual_ok] = (tmp_ok[count_start:i])
                                    actual_ok = firs_ok
                                    count_start = i
                        else:
                            _ok[firs_ok] = None
            if actual_ok and _ok[actual_ok+" double"] <= 2:
                _ok[actual_ok] = tmp_ok[count_start:]

            for x in _ok:
                result = re.search("double", x)
                if result is None:
                    self.system_data["OK"][x]["ORDER_WORK"] = _ok[x]
                    if _ok[x] is None and _ok[x+" double"] <= 2:
                        self.system_data["OK"][x]["CODE_ALARM"] = 6
                        self.system_data["OK"][x]["DESC_ALARM"] = "No order for OK: {}".format(x)
                    elif _ok[x] is None and _ok[x+" double"] > 2:
                        self.system_data["OK"][x]["CODE_ALARM"] = 7
                        self.system_data["OK"][x]["DESC_ALARM"] = "Duplicated order for OK_{}".format(x)
                    else:
                        self.system_data["OK"][x]["CODE_ALARM"] = None
                        self.system_data["OK"][x]["DESC_ALARM"] = None

            status = True
        except:
            print("Wrong parcer OK")
        return status

    def _check_rc_16(self):
        """ checksum packet CRC-16\n
        _check_rc_16("00, ff")\n
        ARG: String of bytes in hex.
        """
        sources = self.telegramm

        r_c = ''.join(sources[len(sources)-2:])
        self.telegramm_decode["RC"] = r_c
        body_packet = bytearray.fromhex(''.join(sources[:len(sources)-2]))
        get_check_rc = Crc16CcittFalse.calchex(body_packet)
        if r_c.upper() == get_check_rc.upper():
            return True
        else:
            self.system_data["ORDER_CODE_ALARM"] = 51
            self.system_data["ORDER_DESC_ALARM"] = "Wrong checksum CRC-16 !!!"
            # self.STATUS_TLG = "Wrong checksum CRC-16 !!!"
            return False

    def _decode_zone_status(self):

        try:
            for _ok in self.system_data["OK"]:
                if self.system_data["OK"][_ok]['CODE_ALARM'] is None:
                    status_zone = {}
                    tlg_a = self.system_data["OK"][_ok]['TELEGRAMM_A']
                    tlg_b = self.system_data["OK"][_ok]['TELEGRAMM_B']
                    zona_a = tlg_a[4:-1]
                    zona_b = ["{:02x}".format(int(x, 16).__xor__(255)).upper() for x in tlg_b[4:-1]]

                    if zona_a != zona_b:
                        self.system_data["OK"][_ok]['CODE_ALARM'] = 61
                        self.system_data["OK"][_ok]['DESC_ALARM'] = "Error decode block DATA"
                        return False
                    zon = zona_a[:]
                    try:
                        key_zone_ = 0
                        key = 0
                        for zone in zon:
                            bin_zones = "{:08b}".format(int(zone, 16))
                            # print(bin_zones)
                            start = None
                            stop = -2
                            for i in range(4):
                                status_zone[key_zone_+ key] = int(bin_zones[stop: start], 2)
                                if start is None:
                                    start = -2
                                else:
                                    start -= 2
                                stop -= 2
                                key += 1
                        zone_for_cns = {}
                        zone_for_cns = self.system_data["OK"][_ok]["ZONE_FOR_CNS"]
                        zone_for_cns.update(status_zone)
                        #self.system_data["OK"][_ok]["ZONE_FOR_CNS"] = status_zone
                    except:
                        self.system_data["OK"][_ok]['CODE_ALARM'] = 61
                        self.system_data["OK"][_ok]['DESC_ALARM'] = "Error decode block DATA"
                        return False
            return True
        except:
            return False

    def _check_decode_ab(self):
        try:
            for _ok in self.system_data["OK"]:
                if self.system_data["OK"][_ok]['CODE_ALARM'] is None:
                    _telegramm_ab = self.system_data["OK"][_ok]['ORDER_WORK']
                    _desc_tlg = self.desc_header_packet["TLG_AB"]
                    mlco_a = _telegramm_ab[2]
                    size_a = int(mlco_a[0], 16)
                    telegramm_a = _telegramm_ab[:size_a]
                    telegramm_b = _telegramm_ab[size_a:]
                    type_co_a = int(mlco_a[1], 16)
                    type_packet = self.telegramm_decode["TYPE_PACKET"]
                    source_id = self.telegramm_decode["ID_SOURCE"]
                    dest_id = self.telegramm_decode["ID_DEST"]

                    if len(telegramm_a) < size_a:
                        self.system_data["OK"][_ok]['CODE_ALARM'] = 71
                        self.system_data["OK"][_ok]['DESC_ALARM'] = "There is no telegramm A"
                        return True

                    crc_a = True
                    crc_b = True

                    # crc telegramm A
                    block_crc = str("".join(telegramm_a[:2])) + str(mlco_a) + str(''.join(telegramm_a[4:-1]))
                    if not telegramm_a[-1].upper() == crc8(block_crc):
                        self.system_data["OK"][_ok]['CODE_ALARM'] = 75
                        self.system_data["OK"][_ok]['DESC_ALARM'] = "Wrong checksum CRC-8 of the telegramm A!!!"
                        crc_a = False
                    else:
                        if type_packet == 2 and type_co_a == 6:
                            self.system_data["OK"][_ok]['CODE_ALARM'] = 71
                            self.system_data["OK"][_ok]['DESC_ALARM'] = "There is not telegram A"
                            return True
                    if type_packet == 2 and type_co_a == 4:
                        if len(telegramm_b) == 0 or len(telegramm_b) < 5 or "".join(telegramm_b[:2]) != _ok:
                            self.system_data["OK"][_ok]['CODE_ALARM'] = 72
                            self.system_data["OK"][_ok]['DESC_ALARM'] = "There is no telegramm B"
                            return True
                        else:
                            mlco_b = telegramm_b[2]
                            size_b = int(mlco_b[0], 16)
                            type_co_b = int(mlco_b[1], 16)
                            telegramm_b = telegramm_b[:size_b]
                    else:
                        self.system_data["OK"][_ok]["CODE_ALARM"] = 81
                        self.system_data["OK"][_ok]["DESC_ALARM"] = "Error checking  type CO of telegramm_a. CO = '{}, TYPE_PACKET = '{}'".format(type_co_a, type_packet)
                        return True

                    # crc telegramm B
                    block_crc = str("".join(telegramm_b[:2])) + str(mlco_b) + str(''.join(telegramm_b[4:-1]))
                    if not telegramm_b[-1].upper() == crc8(block_crc):
                        self.system_data["OK"][_ok]["CODE_ALARM"] = 76
                        self.system_data["OK"][_ok]["DESC_ALARM"] = "Wrong checksum CRC-8 of the telegramm B!!!"
                        crc_b = False
                    else:
                        if crc_a:
                            if type_packet == 2 and type_co_b == 4:
                                self.system_data["OK"][_ok]['CODE_ALARM'] = 72
                                self.system_data["OK"][_ok]['DESC_ALARM'] = "There is not telegram B"
                                return True
                            else:
                                if type_packet != 2 or type_co_b != 6:
                                    self.system_data["OK"][_ok]["CODE_ALARM"] = 82
                                    self.system_data["OK"][_ok]["DESC_ALARM"] = "Error checking  type CO of telegramm_b. CO = '{}, TYPE_PACKET = '{}'".format(type_co_b, type_packet)
                                    return True
                    if not crc_a and not crc_b:
                        self.system_data["OK"][_ok]["CODE_ALARM"] = 74
                        self.system_data["OK"][_ok]["DESC_ALARM"] = "Wrong checksum CRC-8 of the telegramms A and B!!!"
                        return True
                    elif not crc_a or not crc_b:
                        return True
                    if size_a != size_b:
                        self.system_data["OK"][_ok]["CODE_ALARM"] = 73
                        self.system_data["OK"][_ok]["DESC_ALARM"] = "The length telegramm A({0}) - is not equal to the length telegramm B({1})".format(size_a, size_b)
                        return True
                    zone_a = [x.upper() for x in telegramm_a[4:-1]]
                    zone_b = ["{:02x}".format(int(x, 16).__xor__(255)).upper() for x in telegramm_b[4:-1]]
                    if zone_a != zone_b:
                        self.system_data["OK"][_ok]["CODE_ALARM"] = 77
                        self.system_data["OK"][_ok]["DESC_ALARM"] = "The data telegramm A is not equal to the data telegramm B"
                        return True
                    else:
                        self.system_data["OK"][_ok]['count_a'] = int(telegramm_a[3], 16)
                        self.system_data["OK"][_ok]['count_b'] = int(telegramm_b[3], 16)
                        self.system_data["OK"][_ok]['TELEGRAMM_A'] = telegramm_a
                        self.system_data["OK"][_ok]['TELEGRAMM_B'] = telegramm_b
            return True
        except:
            return False

    def check_telegramm(self):
        # print("check_telegramm")
        status = False
        if self._check_byte_flow():
            if self._check_rc_16():
                if self._check_header_packet():
                    if self._check_body_telegramm_ab():
                        if self._parcer_ok():
                            if self._check_decode_ab():
                                if self._check_count_order():
                                    if self._decode_zone_status():
                                        self.system_data["ORDER_CODE_ALARM"] = 0
                                        self.system_data["ORDER_DESC_ALARM"] = "OK"
                                        status = True

        return status
