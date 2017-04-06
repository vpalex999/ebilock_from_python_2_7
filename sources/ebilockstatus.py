from crccheck.crc import Crc16CcittFalse
from sources.crc8 import check_crc_8 as crc8
from sources.error import EbException
import binascii

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


class Ebilock_status(object):
    """ class Ebilock status
    """
    STATUS_TLG = "OK"

    def __init__(self, telegramm):
            self.telegramm = telegramm.copy()


