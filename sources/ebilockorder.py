from crccheck.crc import Crc16CcittFalse
from sources.crc8 import check_crc_8 as crc8
from sources.error import EbException
import binascii


class Ebilock_order(object):
    """ class Ebilock
    """
    STATUS_TLG = "OK"

    def __init__(self, telegramm, *args):
        self.arg = args
        if "hdlc" not in args:
            self.telegramm = telegramm.split(' ')
        else:
            self.telegramm = telegramm

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
            "TLG_A": {
                "BODY_TLG": "",
                "ADDR_OK": "",
                "LOOP_OK": "",
                "AREA_OK": "",
                "HUB_OK": "",
                "NUMBER_OK": "",
                "ML_CO": "",
                "SIZE": "",
                "type_co": "",
                "COUNT": "",
                "DATA": "",
                "RC": ""
            },
            "TLG_B": {},
            "STATUS_ZONE": ""
        }



    @classmethod
    def from_hdlc(cls, object):
        telegramm = []
        for item in object:
            telegramm.append("{:02x}".format(int(binascii.hexlify(item), 16)).upper())
        return cls(telegramm, "hdlc")

    @classmethod
    def from_test(cls, object):
        return cls(object, "test")

    desc_header_packet = {
        "size": 8,
        "ID_SOURCE_IND": 0,
        "ID_DEST_IND": 1,
        "TYPE_PACKET_IND": 2,
        "START_DATA_IND": 3,
        "END_DATA_IND": 6,
        "NUL_BYTE_IND": 7,
        "PACKET_COUNT_A_IND": 8,
        "PACKET_COUNT_B_IND": 9,
        "START_SIZE_AB_IND": 10,
        "END_SIZE_AB_IND": 12,
        "ID":
        {"0": "IPU_GATE_RF",
         "1": "EHA"
        },
        "TYPE_ID":
        {2: "2 - order",
         3: "3 - empty status",
         4: "4 - empty order",
         5: "5 - IPU_GATE_RF -> OK",
         6: "6 - OK -> IPU_GATE_RF"
        },
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

    desc_telegramm_ab = {
        "pass": ""
    }

    
    def _check_byte_flow(self):
        """ Verifying bytes in the packet stream\
        and writing a package to a dictionary.\n
        check_byte_flow("00, ff")\n
        ARG: String of bytes in hex.
        """

        status = True
        sources = self.telegramm
        if len(sources) < 20:
            self.telegramm_decode["CODE_ALARM"] = 10
            self.telegramm_decode["DESC_ALARM"] = "Invalid package '{}' 2xByte, min = 20 2xByte".format(len(sources))
            # self.STATUS_TLG = "Invalid package '{}' 2xByte, min = 20 2xByte".format(len(sources))
            status = False

        for item in sources:
            if item == '':
                status = False
                self.telegramm_decode["CODE_ALARM"] = 11
                self.telegramm_decode["DESC_ALARM"] = "Empty value by index '{}'".format(sources.index(""))
                # self.STATUS_TLG = "Empty value by index '{}'".format(sources.index(""))
                break
            if len(item) != 2:
                status = False
                self.telegramm_decode["CODE_ALARM"] = 12
                self.telegramm_decode["DESC_ALARM"] = "Length value '{}' is not equal to 2".format(item)
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

        status = True
        sources = self.telegramm

        tmp = int(sources[self.desc_header_packet["ID_SOURCE_IND"]], 16)
        if tmp > 1:
            self.telegramm_decode["CODE_ALARM"] = 21
            self.telegramm_decode["DESC_ALARM"] = "Error!  ID_SOURCE = '{}' should be between 0 or 1".format(tmp)
            # self.STATUS_TLG = "Error!  ID_SOURCE = '{}' should be between 0 or 1".format(tmp)
            status = False
        else:
            self.telegramm_decode["ID_SOURCE"] = tmp

        tmp = int(sources[self.desc_header_packet["ID_DEST_IND"]], 16)
        if tmp > 1:
            self.telegramm_decode["CODE_ALARM"] = 22
            self.telegramm_decode["DESC_ALARM"] = "Error!  ID_DEST = '{}' should be between 0 or 1".format(tmp)
            # self.STATUS_TLG = "Error!  ID_DEST = '{}' should be between 0 or 1".format(tmp)
            status = False
        else:
            self.telegramm_decode["ID_DEST"] = tmp

        tmp = int(sources[self.desc_header_packet["TYPE_PACKET_IND"]], 16)
        key_stat = False
        type_id = self.desc_header_packet["TYPE_ID"]
        for key, val in type_id.items():
            if int(key) == tmp:
                self.telegramm_decode["TYPE_PACKET"] = key
                key_stat = True
                break
        if not key_stat:
            self.telegramm_decode["CODE_ALARM"] = 23
            self.telegramm_decode["DESC_ALARM"] = "Value '{}' out of range type telegramm".format(tmp)
            # self.STATUS_TLG = "Value '{}' out of range type telegramm".format(tmp)
            status = False

        tmp = int(''.join(sources[self.desc_header_packet["START_DATA_IND"]:self.desc_header_packet["END_DATA_IND"] + 1]), 16)
        if tmp != len(sources):
            self.telegramm_decode["CODE_ALARM"] = 24
            self.telegramm_decode["DESC_ALARM"] = "Error Checking length packet!!! data length = '{0}', actual length = '{1}'".format(tmp, len(sources))
            # self.STATUS_TLG = "Error Checking length packet!!! data length = '{0}', actual length = '{1}'".format(tmp, len(sources))
            status = False
        else:
            self.telegramm_decode["LENGTH_PACKET"] = tmp

        tmp = int(''.join(sources[self.desc_header_packet["START_SIZE_AB_IND"]:self.desc_header_packet["END_SIZE_AB_IND"]]), 16)
        if tmp > 4096:
            self.telegramm_decode["CODE_ALARM"] = 25
            self.telegramm_decode["DESC_ALARM"] = "Too long data > 4096 bytes - '{}'".format(tmp)
            # self.STATUS_TLG = "Too long data > 4096 bytes - '{}'".format(tmp)
            status = False

        tmp = int(sources[self.desc_header_packet["NUL_BYTE_IND"]])
        if tmp != 0:
            self.telegramm_decode["CODE_ALARM"] = 26
            self.telegramm_decode["DESC_ALARM"] = "Invalid header structure, Zero byte value = '{}', must be 0".format(tmp)
            # self.STATUS_TLG = "Invalid header structure, Zero byte value = '{}', must be 0".format(tmp)
            status = False
        return status

    def _check_global_count_order(self):
        """ Reading and checking the consistency\
        of counters A / B order package\n
        check_count_ab_packet()\n
        ARG: String of bytes in hex.
        """

        ct_A = self.telegramm_decode["PACKET_COUNT_A"]
        if ct_A == 0 or ct_A == 255:
            self.telegramm_decode["CODE_ALARM"] = 31
            self.telegramm_decode["DESC_ALARM"] = "The value global_ctA can not be 0 or 255:'{}'".format(ct_A)
            # self.STATUS_TLG = "The value can not be 0 or 255:'{}'".format(ct_A)
            return False
        ct_B = self.telegramm_decode["PACKET_COUNT_B"]
        if ct_B == 0 or ct_B == 255:
            self.telegramm_decode["CODE_ALARM"] = 32
            self.telegramm_decode["DESC_ALARM"] = "The value global_ctB can not be 0 or 255:'{}'".format(ct_B)
            # self.STATUS_TLG = "The value can not be 0 or 255:'{}'".format(ct_B)
            return False
        ct_a = self.telegramm_decode["TLG_A"]["COUNT"]
        if ct_a == 0 or ct_a == 255:
            self.telegramm_decode["CODE_ALARM"] = 33
            self.telegramm_decode["DESC_ALARM"] = "The value ct_a can not be 0 or 255:'{}'".format(ct_a)
            self.STATUS_TLG = "The value can not be 0 or 255:'{}'".format(ct_a)
            return False
        ct_b = self.telegramm_decode["TLG_B"]["COUNT"]
        if ct_b == 0 or ct_b == 255:
            self.telegramm_decode["CODE_ALARM"] = 34
            self.telegramm_decode["DESC_ALARM"] = "The value ct_b can not be 0 or 255:'{}'".format(ct_b)
            self.STATUS_TLG = "The value can not be 0 or 255:'{}'".format(ct_b)
            return False
        if ct_A + ct_B == 255:
            if ct_a + ct_b == 255:
                if ct_A - ct_a == 0 and ct_B - ct_b == 0:
                    return True
                else:
                    self.telegramm_decode["CODE_ALARM"] = 35
                    self.telegramm_decode["DESC_ALARM"] = "Sum values count packet and count telegramm are not equal"
                    # self.STATUS_TLG = "Sum values count packet and count telegramm are not equal"
                    return False
            else:
                if ct_A - ct_a == 0:
                    self.telegramm_decode["CODE_ALARM"] = 36
                    self.telegramm_decode["DESC_ALARM"] = "Error_ctb"
                    # bself.STATUS_TLG = "Error_ctb"
                    return False
                else:
                    self.telegramm_decode["CODE_ALARM"] = 37
                    self.telegramm_decode["DESC_ALARM"] = "Error_cta"
                    # self.STATUS_TLG = "Error_cta"
                    return False
        else:
            if ct_A - ct_a == 0:
                self.telegramm_decode["CODE_ALARM"] = 38
                self.telegramm_decode["DESC_ALARM"] = "Error_ctb_gl"
                # self.STATUS_TLG = "Error_ctb_gl"
                return False
            else:
                self.telegramm_decode["CODE_ALARM"] = 39
                self.telegramm_decode["DESC_ALARM"] = "Error_cta_gl"
                # self.STATUS_TLG = "Error_cta_gl"
                return False

    def _check_body_telegramm_ab(self):
        """ Check the length of the block of telegrams A / B\n
        check_telegramm_ab("00, ff")\n
        ARG: String of bytes in hex.
        """
        sources = self.telegramm
        size_ab = int(''.join(sources[self.desc_header_packet["START_SIZE_AB_IND"]:self.desc_header_packet["END_SIZE_AB_IND"]]), 16)
        if size_ab == 0:
            self.telegramm_decode["CODE_ALARM"] = 41
            self.telegramm_decode["DESC_ALARM"] = "Empty data A/B - '{}'".format(size_ab)
            # self.STATUS_TLG = "Empty data A/B - '{}'".format(size_ab)
            return False

        len_tlg_ab = self.telegramm_decode["LENGTH_PACKET"] - 14
        if not len_tlg_ab == size_ab:
            self.telegramm_decode["CODE_ALARM"] = 42
            self.telegramm_decode["DESC_ALARM"] = "Error len A/B"
            # self.STATUS_TLG = "Error len A/B"
            return False
        self.telegramm_decode["SIZE_AB"] = size_ab
        start_ab = self.desc_header_packet["END_SIZE_AB_IND"]
        end_ab = size_ab + start_ab
        tlg_ab = sources[start_ab:end_ab]
        if not size_ab == len(tlg_ab):
            self.telegramm_decode["CODE_ALARM"] = 43
            self.telegramm_decode["DESC_ALARM"] = "packet length '{0}' is not equal to the value size A/B '{}'".format(len(tlg_ab), size_ab)
            # self.STATUS_TLG = "packet length '{0}' is not equal to the value size A/B '{}'".format(len(tlg_ab), size_ab)
            return False
        else:
            self.telegramm_decode["TELEGRAMM_AB"] = tlg_ab
            if size_ab == len_tlg_ab:
                return True
            else:
                self.telegramm_decode["CODE_ALARM"] = 44
                self.telegramm_decode["DESC_ALARM"] = "Packet length '{0}' is not equal to the value size A/B '{}'".format(len_tlg_ab, size_ab)
                # self.STATUS_TLG = "Packet length '{0}' is not equal to the value size A/B '{}'".format(len_tlg_ab, size_ab)
            return False

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
        if r_c == get_check_rc.upper():
            return True
        else:
            self.telegramm_decode["CODE_ALARM"] = 51
            self.telegramm_decode["DESC_ALARM"] = "Wrong checksum CRC-16 !!!"
            # self.STATUS_TLG = "Wrong checksum CRC-16 !!!"
            return False

    def _bit_shift_right(self, string_byte):
        tmp = int(string_byte, 16)
        return tmp >> 1

    def _inversion_byte(self, hex_list):
        tmp = []
        for item in hex_list:
            str_up = "{:02x}".format(int(item, 16).__xor__(255))
            tmp.append(str_up.upper())
        return tmp

    def _decode_telegram(self, dsc_tel, telegramm_dec, type=None):
        """
        type = TLG_A or TLG_B
        """
        _dsc_tlg = dsc_tel["TLG_AB"]
        telegramm = telegramm_dec[type]["BODY_TLG"]

        _ok = ''.join(telegramm[_dsc_tlg["OK_START"]:_dsc_tlg["OK_END"]+1])

        telegramm_dec[type]["ADDR_OK"] = _ok

        telegramm_dec[type]["LOOP_OK"] = _ok[0]

        telegramm_dec[type]["AREA_OK"] = self._bit_shift_right(_ok[1])

        telegramm_dec[type]["HUB_OK"] = _ok[2]

        telegramm_dec[type]["NUMBER_OK"] = self._bit_shift_right(_ok[3])

        telegramm_dec[type]["ML_CO"] = telegramm[_dsc_tlg["ML_CO"]]

        telegramm_dec[type]["SIZE"] = int(telegramm_dec[type]["ML_CO"][0], 16)

        telegramm_dec[type]["type_co"] = int(telegramm_dec[type]["ML_CO"][1], 16)

        telegramm_dec[type]["COUNT"] = int(telegramm[_dsc_tlg["COUNT_AB"]], 16)

        telegramm_dec[type]["DATA"] = telegramm[_dsc_tlg["COUNT_AB"]+1:telegramm_dec[type]["SIZE"]-1]

        telegramm_dec[type]["RC"] = telegramm[telegramm_dec[type]["SIZE"]-1]

        block_crc = str(telegramm_dec[type]["ADDR_OK"]) + \
            str(telegramm_dec[type]["ML_CO"]) + \
            str(''.join(self.telegramm_decode[type]["DATA"]))
        if not telegramm_dec[type]["RC"] == crc8(block_crc):
            return False
        else:
            return True

    def _decode_zone_status(self, data_list):
        status_zone = {}
        zon = data_list[::-1]
        try:
            key_zone_ = 1
            for zone in zon:
                bin_zones = "{:08b}".format(int(zone, 16))
                zon_offset = -2
                zon_offset_str = 8
                print("")
                for key in range(0, 4):
                    status_zone[key_zone_+key] = int(bin_zones[zon_offset:zon_offset_str], 2)
                    if "zone" in self.arg:
                        print("Zona_{} = {}".format(
                            key_zone_ + key, int(bin_zones[zon_offset:zon_offset_str], 2)))
                    zon_offset += -2
                    zon_offset_str -= 2
                key_zone_ += key + 1
            self.telegramm_decode["STATUS_ZONE"] = status_zone
            return True
        except:
            self.telegramm_decode["CODE_ALARM"] = 61
            self.telegramm_decode["DESC_ALARM"] = "Error decode block DATA"
            # self.STATUS_TLG = "Error decode block DATA"
            return False

    def _check_id_packet(self):
        type_packet = self.telegramm_decode["TYPE_PACKET"]
        source_id = self.telegramm_decode["ID_SOURCE"]
        dest_id = self.telegramm_decode["ID_DEST"]

        if source_id == dest_id:

            if type_packet == 2 or type_packet == 4 or type_packet == 5:
                if source_id == 0:
                    self.telegramm_decode["CODE_ALARM"] = 62
                    self.telegramm_decode["DESC_ALARM"] = "Error ID resive."
                    # self.STATUS_TLG = "Error ID resive."
                    return False
                else:
                    self.telegramm_decode["CODE_ALARM"] = 63
                    self.telegramm_decode["DESC_ALARM"] = "Error ID Send."
                    # self.STATUS_TLG = "Error ID Send."
                    return False
        else:
            return True

    def _check_type_packet(self):
        type_packet = self.telegramm_decode["TYPE_PACKET"]
        source_id = self.telegramm_decode["ID_SOURCE"]
        dest_id = self.telegramm_decode["ID_DEST"]
        if source_id == 0 and dest_id == 1 and type_packet == 3 or\
           source_id == 0 and dest_id == 1 and type_packet == 6 or\
           source_id == 1 and dest_id == 0 and type_packet == 2 or\
           source_id == 1 and dest_id == 0 and type_packet == 4 or\
           source_id == 1 and dest_id == 0 and type_packet == 6:
            self.telegramm_decode["CODE_ALARM"] = 64
            self.telegramm_decode["DESC_ALARM"] = "Error TYPE_ID"
            # self.STATUS_TLG = "Error TYPE_ID"
            return False
        else:
            return True

    def _check_decode_ab(self):

        _desc_tlg = self.desc_header_packet["TLG_AB"]

        _telegramm_ab = self.telegramm_decode["TELEGRAMM_AB"]

        mlco = _telegramm_ab[_desc_tlg["ML_CO"]]
        type_co = int(mlco[1], 16)
        type_packet = self.telegramm_decode["TYPE_PACKET"]
        source_id = self.telegramm_decode["ID_SOURCE"]
        dest_id = self.telegramm_decode["ID_DEST"]

        if (type_packet == 2 and type_co == 4 or type_packet == 2 and type_co == 6):
            if source_id != 0:
                self.telegramm_decode["CODE_ALARM"] = 65
                self.telegramm_decode["DESC_ALARM"] = "Error ID Send."
                # self.STATUS_TLG = "Error ID Send."
                return False
            if dest_id == 0:
                self.telegramm_decode["CODE_ALARM"] = 66
                self.telegramm_decode["DESC_ALARM"] = "Error ID Resive."
                # self.STATUS_TLG = "Error ID Resive."
                return False
            if type_co == 6:
                self.telegramm_decode["CODE_ALARM"] = 71
                self.telegramm_decode["DESC_ALARM"] = "There is no telegram A"
                # self.STATUS_TLG = "There is no telegram A"
                return False
            elif type_co == 4:
                self.telegramm_decode["TLG_A"]["ML_CO"] = _telegramm_ab[_desc_tlg["ML_CO"]]

                self.telegramm_decode["TLG_A"]["SIZE"] = int(self.telegramm_decode["TLG_A"]["ML_CO"][0], 16)

                self.telegramm_decode["TLG_A"]["BODY_TLG"] = _telegramm_ab[:self.telegramm_decode["TLG_A"]["SIZE"]]

                self.telegramm_decode["TLG_B"]["BODY_TLG"] = _telegramm_ab[self.telegramm_decode["TLG_A"]["SIZE"]:]

                len_a = len(self.telegramm_decode["TLG_A"]["BODY_TLG"])
                len_b = len(self.telegramm_decode["TLG_B"]["BODY_TLG"])

                if len_b == 0:
                    self.telegramm_decode["CODE_ALARM"] = 72
                    self.telegramm_decode["DESC_ALARM"] = "There is no telegram B"
                    # self.STATUS_TLG = "There is no telegram B"
                    return False

                if not len_a == len_b:
                    self.telegramm_decode["CODE_ALARM"] = 73
                    self.telegramm_decode["DESC_ALARM"] = "The length telegramm A({0}) - is not equal to the length telegramm B({1})".format(len_a, len_b)
                    # self.STATUS_TLG = "The length telegramm A({0}) - is not equal to the length telegramm B({1})".format(len_a, len_b)

                    return False
                else:

                    crc_a_status = self._decode_telegram(self.desc_header_packet, self.telegramm_decode, "TLG_A")
                    crc_b_status = self._decode_telegram(self.desc_header_packet, self.telegramm_decode, "TLG_B")
                    if not crc_a_status and not crc_b_status:
                        self.telegramm_decode["CODE_ALARM"] = 74
                        self.telegramm_decode["DESC_ALARM"] = "Wrong checksum CRC-8 of the telegramms A and B!!!"
                        # self.STATUS_TLG = "Wrong checksum CRC-8 of the telegramms A and B!!!"
                        return False
                    if not crc_a_status:
                        self.telegramm_decode["CODE_ALARM"] = 75
                        self.telegramm_decode["DESC_ALARM"] = "Wrong checksum CRC-8 of the telegramm A!!!"
                        # self.STATUS_TLG = "Wrong checksum CRC-8 of the telegramm A!!!"
                        return False

                    if not crc_b_status:
                        self.telegramm_decode["CODE_ALARM"] = 76
                        self.telegramm_decode["DESC_ALARM"] = "Wrong checksum CRC-8 of the telegramm B!!!"
                        # self.STATUS_TLG = "Wrong checksum CRC-8 of the telegramm B!!!"
                        return False

                    if not self.telegramm_decode["TLG_A"]["DATA"] == self._inversion_byte(self.telegramm_decode["TLG_B"]["DATA"]):
                        self.telegramm_decode["CODE_ALARM"] = 77
                        self.telegramm_decode["DESC_ALARM"] = "The data telegramm A is not equal to the data telegramm B"
                        # self.STATUS_TLG = "The data telegramm A is not equal to the data telegramm B"
                        return False
                    else:
                        self.telegramm_decode["PACKET_COUNT_A"] = int(self.telegramm[self.desc_header_packet["PACKET_COUNT_A_IND"]], 16)
                        self.telegramm_decode["PACKET_COUNT_B"] = int(self.telegramm[self.desc_header_packet["PACKET_COUNT_B_IND"]], 16)
                        return True

        if (type_packet == 3 and type_co == 8 or type_packet == 3 and type_co == 8):
            self.telegramm_decode["CODE_ALARM"] = 80
            self.telegramm_decode["DESC_ALARM"] = "This send status"
            # self.STATUS_TLG = "This send status"
        else:
            self.telegramm_decode["CODE_ALARM"] = 81
            self.telegramm_decode["DESC_ALARM"] = "Error checking  type CO of telegramm. CO = '{}, TYPE_PACKET = '{}'".format(type_co, type_packet)
            # self.STATUS_TLG = "Error checking  type CO of telegramm. CO = '{}, TYPE_PACKET = '{}'".format(type_co, type_packet)
            return False

    def check_telegramm(self):
    
        if self._check_byte_flow():
            if self._check_rc_16():
                if self._check_header_packet():
                    if self._check_body_telegramm_ab():
                        if self._check_id_packet():
                            if self._check_type_packet():
                                if self._check_decode_ab():
                                    if self._check_global_count_order():
                                        self._decode_zone_status(''.join(self.telegramm_decode['TLG_A']['DATA']))
        return self.telegramm_decode
