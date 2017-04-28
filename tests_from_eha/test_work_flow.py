""" Check post-processing of telegrams """

import time
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sources.ebilockorder_new import Ebilock_order as order
from sources.work_order import WorkFlow as wf
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


class TestWork_Flow(unittest.TestCase):

    def setUp(self):
        self.system_data_1 = system_data_1.copy()
        self.system_data_2 = system_data_2.copy()
        _ok = self.system_data_1["OK"]

        for x in _ok:
            _ok[x]["CODE_ALARM"] = None
            _ok[x]["DESC_ALARM"] = None
            _ok[x]["RETURN_OK"] = 0

        _ok = self.system_data_2["OK"]
        for x in _ok:
            _ok[x]["CODE_ALARM"] = None
            _ok[x]["DESC_ALARM"] = None
            _ok[x]["RETURN_OK"] = 0



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
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 10, print_OK(self.system_data_1))
        self.assertIs(status, 50)

    @unittest.skipIf(skipped, " ")
    def test_work_err_crc16_51(self):
        self.system_data_1["hdlc"] = hdlc_crc16_wrong
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 51, print_OK(self.system_data_1))
        self.assertIs(status, 50)

    @unittest.skipIf(skipped, " ")
    def test_work_err_send_21(self):
        self.system_data_1["hdlc"] = hdlc_err_send
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 21, print_OK(self.system_data_1))
        self.assertIs(status, 50)

    @unittest.skipIf(skipped, " ")
    def test_work_err_recv_22(self):
        self.system_data_1["hdlc"] = hdlc_err_recv
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 22, print_OK(self.system_data_1))
        self.assertIs(status, 50)

    @unittest.skipIf(skipped, " ")
    def test_work_err_type_23(self):
        self.system_data_1["hdlc"] = hdlc_err_type
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 23, print_OK(self.system_data_1))
        self.assertIs(status, 50)

    @unittest.skipIf(skipped, " ")
    def test_work_err_len_24(self):
        self.system_data_1["hdlc"] = hdlc_err_len
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 24, print_OK(self.system_data_1))
        self.assertIs(status, 50)

    @unittest.skipIf(skipped, " ")
    def test_work_err_null_byte_26(self):
        self.system_data_1["hdlc"] = hdlc_null_byte
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 26, print_OK(self.system_data_1))
        self.assertIs(status, 50)

    @unittest.skipIf(skipped, " ")
    def test_work_err_incons_glAB_30(self):
        self.system_data_1["hdlc"] = hdlc_incons_gl_AB_30
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 30, print_OK(self.system_data_1))
        self.assertIs(status, 110)

    @unittest.skipIf(skipped, " ")
    def test_work_forbidden_combination_countsAB_31(self):
        self.system_data_1["hdlc"] = hdlc_forbiden_counts_31
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 31, print_OK(self.system_data_1))
        self.assertIs(status, 110)

    @unittest.skipIf(skipped, " ")
    def test_work_forbidden_combination_countA_32(self):
        self.system_data_1["hdlc"] = hdlc_forbiden_count_A
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 32, print_OK(self.system_data_1))
        self.assertIs(status, 110)

    @unittest.skipIf(skipped, " ")
    def test_work_forbidden_combination_countB_33(self):
        self.system_data_1["hdlc"] = hdlc_forbiden_count_B
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 33, print_OK(self.system_data_1))
        self.assertIs(status, 110)

    @unittest.skipIf(skipped, " ")
    def test_work_err_ctab_34(self):
        self.system_data_1["hdlc"] = hdlc_err_ctab_34
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], None, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 34)
        self.assertIs(status, 110)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 110)

    @unittest.skipIf(skipped, " ")
    def test_work_err_ctab_gl_34(self):
        self.system_data_1["hdlc"] = hdlc_err_ctab_gl_34
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], None, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 34)
        self.assertIs(status, 110)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 110)



    @unittest.skipIf(skipped, " ")
    def test_work_err_ctb_36(self):
        self.system_data_1["hdlc"] = hdlc_err_ctb_36
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], None, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 36)
        self.assertIs(status, 110)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 110)

    @unittest.skipIf(skipped, " ")
    def test_work_err_cta_37(self):
        self.system_data_1["hdlc"] = hdlc_err_cta_37
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], None, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 37)
        self.assertIs(status, 110)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 110)

    @unittest.skipIf(skipped, " ")
    def test_work_err_not_ab_41(self):
        self.system_data_1["hdlc"] = hdlc_err_not_ab_41
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 41, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], None)
        self.assertIs(status, 100)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 0)

    @unittest.skipIf(skipped, " ")
    def test_work_err_len_ab_43(self):
        self.system_data_1["hdlc"] = hdlc_err_len_ab_43
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 43, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], None)
        self.assertIs(status, 100)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 0)

    @unittest.skipIf(skipped, " ")
    def test_work_err_not_a_71(self):
        self.system_data_1["hdlc"] = hdlc_err_not_a_71
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 0, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 71)
        self.assertIs(status, 0)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 100)

    @unittest.skipIf(skipped, " ")
    def test_work_err_not_b_72(self):
        self.system_data_1["hdlc"] = hdlc_err_not_b_72
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 0, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 72)
        self.assertIs(status, 0)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 100)

    @unittest.skipIf(skipped, " ")
    def test_work_err_crcab_74(self):
        self.system_data_1["hdlc"] = hdlc_err_crcab_74
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 0, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 74)
        self.assertIs(status, 0)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 100)

    @unittest.skipIf(skipped, " ")
    def test_work_err_crca_75(self):
        self.system_data_1["hdlc"] = hdlc_err_crca_75
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 0, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 75)
        self.assertIs(status, 0)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 100)

    @unittest.skipIf(skipped, " ")
    def test_work_err_crcb_76(self):
        self.system_data_1["hdlc"] = hdlc_err_crcb_76
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 0, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 76)
        self.assertIs(status, 0)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 100)

    @unittest.skipIf(skipped, " ")
    def test_work_err_conc_77(self):
        self.system_data_1["hdlc"] = hdlc_err_conc
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 0, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 77)
        self.assertIs(status, 0)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 100)

    @unittest.skipIf(skipped, " ")
    def test_work_err_co_a_81(self):
        self.system_data_1["hdlc"] = hdlc_err_co_a_81
        order.from_test(self.system_data_1).check_telegramm()
        work_f = wf(self.system_data_1)
        status = work_f.work_order()
        self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], 0, print_OK(self.system_data_1))
        self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 81)
        self.assertIs(status, 0)
        self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 100)

    # @unittest.skipIf(skipped, " ")
    # def test_work_err_co_b_82(self):
    #     self.system_data_1["hdlc"] = hdlc_err_co_b_82
    #     order.from_test(self.system_data_1).check_telegramm()
    #     work_f = wf(self.system_data_1)
    #     status = work_f.work_order()
    #     self.assertEqual(self.system_data_1["ORDER_CODE_ALARM"], None, print_OK(self.system_data_1))
    #     self.assertEqual(self.system_data_1["OK"]["3257"]["CODE_ALARM"], 82)
    #     self.assertIs(status, 0)
    #     self.assertIs(self.system_data_1["OK"]["3257"]["RETURN_OK"], 100)

    @unittest.skipIf(skipped, " ")
    def test_work_no_order_ok_6(self):
        self.system_data_2["hdlc"] = hdlc_6
        order.from_test(self.system_data_2).check_telegramm()
        work_f = wf(self.system_data_2)
        status = work_f.work_order()
        self.assertEqual(self.system_data_2["ORDER_CODE_ALARM"], 0, print_OK(self.system_data_2))
        self.assertEqual(self.system_data_2["OK"]["3259"]["CODE_ALARM"], 6)
        self.assertIs(status, 0)
        self.assertIs(self.system_data_2["OK"]["3257"]["RETURN_OK"], 100)

    @unittest.skipIf(skipped, " ")
    def test_work_duplicated_order_7(self):
        self.system_data_2["hdlc"] = hdlc_6
        order.from_test(self.system_data_2).check_telegramm()
        work_f = wf(self.system_data_2)
        status = work_f.work_order()
        self.assertEqual(self.system_data_2["ORDER_CODE_ALARM"], 0, print_OK(self.system_data_2))
        self.assertEqual(self.system_data_2["OK"]["3257"]["CODE_ALARM"], 7)
        self.assertIs(status, 0)
        self.assertIs(self.system_data_2["OK"]["3257"]["RETURN_OK"], 100)

    #@unittest.skipIf(skipped, " ")
    def test_work_discard_telegramm(self):
        self.system_data_2["hdlc"] = hdlc_work(hdlc_discard)
        order.from_hdlc(self.system_data_2).check_telegramm()
        work_f = wf(self.system_data_2)
        status = work_f.work_order()
        self.assertEqual(self.system_data_2["ORDER_CODE_ALARM"], 0, print_OK(self.system_data_2))
        self.assertEqual(self.system_data_2["OK"]["3257"]["CODE_ALARM"], None)
        self.assertIs(status, 0)
        self.assertIs(self.system_data_2["OK"]["3257"]["RETURN_OK"], 0)



if __name__ == "__main__":
    unittest.main()

