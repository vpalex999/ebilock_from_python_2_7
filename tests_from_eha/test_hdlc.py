""" Verification of an order telegram """
import time
import unittest
import sys
import os
import struct
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sources.ebilockorder_new import Ebilock_order as order
from tests_from_eha.data import *
from sources.hdlc import hdlc_work

skipped = False


def print_OK(system_data):
    _ok = system_data["OK"]
    result = ""

    for x in _ok:
        result = result + "OK: {}, code alarm: {}, description: {}\n".format(x, _ok[x]['CODE_ALARM'], _ok[x]['DESC_ALARM'])
    result + "*"*10
    return print("\nMain Code alarm: {}, deck: {},\n{}".format(\
                                         system_data["ORDER_CODE_ALARM"],\
                                         system_data["ORDER_DESC_ALARM"], result))


class TestHdlc(unittest.TestCase):

    def setUp(self):
        self.system_data = system_data_1.copy()
        _ok = self.system_data["OK"]
        for x in _ok:
            _ok[x]["CODE_ALARM"] = None
            _ok[x]["DESC_ALARM"] = None
        self.wrong_hdlc = b'\x10\x02\x00\x01\x02\x00\x00\x00*\x00\xeb\x14\x00\x1c2W\xe4\xeb\xe4\x1b\xe4\x1b\xe4\x1b\xe4\x1b@\xad2W\xe6\x14\x1b\xe4\x1b\xe4\x1b\xe4\x1b\xe4\xbf(\xe6\x10\x10\x10\x83'
        self.hdlc_discard = hdlc_discard[:]
        self.buff1 = b'\x10'
        self.buff2 = b'\x02\x00\x01\x02'
        self.buff3 = b'\x00\x00\x00*\x00\xeb\x14\x00\x1c2W\xe4\xeb\xe4\x1b\xe4\x1b\xe4\x1b\xe4\x1b@\xad2W\xe6\x14\x1b\xe4\x1b\xe4\x1b\xe4\x1b\xe4\xbf(\xe6\x10\x10\x10\x83\xe6\x10'

    @unittest.skipIf(skipped, "")
    def test_check_hdlc_byte_flow10(self):
        self.system_data['hdlc'] = hdlc_work(self.wrong_hdlc)
        orders = order.from_hdlc(self.system_data).check_telegramm()
        self.assertTrue(orders, print_OK(self.system_data))

    #@unittest.skipIf(skipped, "")
    def test_check_hdlc_no_bufer(self):
        buffer = bytearray()
        hdlc_work(self.buff1, buffer)
        hdlc_work(self.buff2, buffer)
        hdlc_work(self.buff3, buffer)
        self.system_data['hdlc'] = hdlc_work(buffer)
        orders = order.from_hdlc(self.system_data).check_telegramm()
        self.assertTrue(orders, print_OK(self.system_data))



if __name__ == "__main__":
    unittest.main()

