from crccheck.crc import Crc16CcittFalse
#from sources.crc8 import create_crc_8 as crc8
#from sources.error import EbException
import binascii

#from sources.hdlc import read_hdlc
#from sources.ebilockstatus import Ebilock_status as es


class Ebilock_decode_status(object):
    """ class Ebilock status """

    ID_SOURCE = hex(1)
    ID_DEST = hex(0)
    TYPE_PACKET = hex(3)
    SIZE_PACKET = hex(0)
    ZERO_BYTE = hex(0)

    def __init__(self, status_hdlc):
        self.status_hdlc = status_hdlc
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
            "STATUS_ZONE": "",
            "ADDRESS_OK": None,
            "STATUS": None,

        }
        if self.status_hdlc is None:
            print("Empty HDLC packet!!!")
            return
        else:
            tmp = read_hdlc(self.status_hdlc)
            telegramm = []
            for item in tmp:
                #telegramm.append("{:02x}".format(hex(int(binascii.hexlify(item), 16))))
                telegramm.append("{}".format(hex(int(binascii.hexlify(item), 16))))
                self.telegramm_decode["STATUS"] = telegramm
            print("Decode status: {}".format(self.telegramm_decode["STATUS"]))
            self._check_CRC16()



    def _check_CRC16(self):
        tlg = self.telegramm_decode["STATUS"]
        r_c = bytearray([int(tlg[x], 16) for x in range(len(tlg)-2)])
        #print("r_c: {}".format(r_c))
        #print("r_c1: {}".format(r_c1))
        get_check_rc = Crc16CcittFalse.calchex(r_c)
        #print("get_check_rc16_hex: {}".format(get_check_rc))
        print("Decode status CRC-16 {}".format(es.hex_to_2bytes(int(get_check_rc, 16), 2)))


    

    def decode_status(self):
        status = False
        
        return status
        


tt = "00 01 02 00 00 00 1c 00 02 ff 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b"
len_t = "{:02x}".format(int(hex(len(tt.split(" "))+2), 16))
len_ok = "{:02x}".format(int(hex(len(tt.split(" "))-12), 16))

r_c = bytearray.fromhex(tt)
get_check = Crc16CcittFalse.calchex(r_c)
pass
new_tt = "00 01 02 00 00 00 1c 00 02 ff 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b 7b e6"

