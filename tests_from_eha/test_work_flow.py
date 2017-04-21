""" Check post-processing of telegrams """

import time
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sources.ebilockorder_new import Ebilock_order as order
from sources.work_order import WorkFlow as wf
from tests_from_eha.data import *

skipped = True


def print_OK(system_data):
    _ok = system_data["OK"]
    result = ""

    for x in _ok:
        result = result + "OK: {}, code alarm: {}, description: {}\n".format(x, _ok[x]['CODE_ALARM'], _ok[x]['DESC_ALARM'])
    result + "*"*10
    return print("\nMain Code alarm: {}, deck: {},\n{}".format(\
                                         system_data["ORDER_CODE_ALARM"],\
                                         system_data["ORDER_DESC_ALARM"], result))


class TestWork_Flow(unittest.TestCase):

    def setUp(self):
        self.system_data_1 = system_data_1
        self.system_data_2 = system_data_2

    @unittest.skipIf(skipped, " ")
    def test_work_order_ok(self):
        self.system_data_1["hdlc"] = hdlc_telegramm
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        self.assertEqual(work_f.work_order(), 0)

    @unittest.skipIf(skipped, " ")
    def test_work_err_10(self):
        self.system_data_1["hdlc"] = hdlc_less
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 10, print_OK(self.system_data_1))

    @unittest.skipIf(skipped, " ")
    def test_work_err_crc16_51(self):
        self.system_data_1["hdlc"] = hdlc_crc16_wrong
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 51, print_OK(self.system_data_1))

    @unittest.skipIf(skipped, " ")
    def test_work_err_send_21(self):
        self.system_data_1["hdlc"] = hdlc_err_send
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 21, print_OK(self.system_data_1))

    @unittest.skipIf(skipped, " ")
    def test_work_err_recv_22(self):
        self.system_data_1["hdlc"] = hdlc_err_recv
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 22, print_OK(self.system_data_1))

    @unittest.skipIf(skipped, " ")
    def test_work_err_type_23(self):
        self.system_data_1["hdlc"] = hdlc_err_type
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 23, print_OK(self.system_data_1))

    @unittest.skipIf(skipped, " ")
    def test_work_err_len_24(self):
        self.system_data_1["hdlc"] = hdlc_err_len
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 24, print_OK(self.system_data_1))

    @unittest.skipIf(skipped, " ")
    def test_work_err_null_byte_26(self):
        self.system_data_1["hdlc"] = hdlc_null_byte
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 26, print_OK(self.system_data_1))

    @unittest.skipIf(skipped, " ")
    def test_work_err_incons_glAB_30(self):
        self.system_data_1["hdlc"] = hdlc_incons_gl_AB_30
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 30, print_OK(self.system_data_1))

    @unittest.skipIf(skipped, " ")
    def test_work_forbidden_combination_countsAB_31(self):
        self.system_data_1["hdlc"] = hdlc_forbiden_counts_31
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 31, print_OK(self.system_data_1))

    #@unittest.skipIf(skipped, " ")
    def test_work_forbidden_combination_countA_31(self):
        self.system_data_1["hdlc"] = hdlc_forbiden_count_A
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 39, print_OK(self.system_data_1))

if __name__ == "__main__":
    unittest.main()

