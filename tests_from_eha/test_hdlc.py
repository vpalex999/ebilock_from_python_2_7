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
        self.buffer = bytearray()
        self.wrong_hdlc = b'\x10\x02\x00\x01\x02\x00\x00\x00*\x00\xeb\x14\x00\x1c2W\xe4\xeb\xe4\x1b\xe4\x1b\xe4\x1b\xe4\x1b@\xad2W\xe6\x14\x1b\xe4\x1b\xe4\x1b\xe4\x1b\xe4\xbf(\xe6\x10\x10\x10\x83'
        self.hdlc_discard = hdlc_discard[:]
        self.buff1 = b'\x10'
        self.buff2 = b'\x02\x00\x01\x02'
        self.buff3 = b'\x00\x00\x00*\x00\xeb\x14\x00\x1c2W\xe4\xeb\xe4\x1b\xe4\x1b\xe4\x1b\xe4\x1b@\xad2W\xe6\x14\x1b\xe4\x1b\xe4\x1b\xe4\x1b\xe4\xbf(\xe6\x10\x10\x10\x83\xe6\x10'
        self.hdlc_ok = b'\x10\x02\x00\x01\x02\x00\x00\x00*\x10\x83'
        self.hdlc_start_10_10 = b'\x10\x02\x10\x10\x00\x01\x02\x00\x00\x00*\x10\x83'
        self.hdlc_start_10_10_10_odd = b'\x10\x02\x10\x10\x10\x00\x01\x02\x00\x00\x00*\x10\x83'
        self.hdlc_start_10_10_10_10_even = b'\x10\x02\x10\x10\x10\x10\x00\x01\x02\x00\x00\x00*\x10\x83'

    @unittest.skipIf(skipped, "")
    def test_check_hdlc_byte_flow10(self):
        self.system_data['hdlc'] = hdlc_work(self.wrong_hdlc)
        orders = order.from_hdlc(self.system_data).check_telegramm()
        self.assertTrue(orders, print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_check_hdlc_no_bufer(self):
        buffers = bytearray()
        hdlc_work(self.buff1, buffers)
        hdlc_work(self.buff2, buffers)
        hdlc_work(self.buff3, buffers)
        self.system_data['hdlc'] = hdlc_work(buffers)
        orders = order.from_hdlc(self.system_data).check_telegramm()
        self.assertTrue(orders, print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_hdlc_ok(self):
        self.assertEqual(hdlc_work(self.hdlc_ok, self.buffer), b'\x00\x01\x02\x00\x00\x00*')

    @unittest.skipIf(skipped, "")
    def test_hdlc_double_start_10_10(self):
        self.assertEqual(hdlc_work(self.hdlc_start_10_10, self.buffer), b'\x10\x00\x01\x02\x00\x00\x00*')

    @unittest.skipIf(skipped, "")
    def test_hdlc_double_start_10_10_10_odd(self):
        buffers = bytearray('\x10\x08', 'utf8')
        self.assertFalse(hdlc_work(self.hdlc_start_10_10_10_odd, buffers))
        pass

    @unittest.skipIf(skipped, "")
    def test_hdlc_double_start_10_10_10_10_even(self):
        self.assertEqual(hdlc_work(self.hdlc_start_10_10_10_10_even, self.buffer), b'\x10\x10\x00\x01\x02\x00\x00\x00*')
        pass

if __name__ == "__main__":
    unittest.main()

