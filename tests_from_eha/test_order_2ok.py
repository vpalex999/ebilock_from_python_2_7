""" Verification of an order telegram """
import time
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sources.ebilockorder_new import Ebilock_order as order
from tests_from_eha.data import *

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


class TestOrder(unittest.TestCase):

    def setUp(self):
        self.system_data = system_data_2.copy()
        _ok = self.system_data["OK"]
        for x in _ok:
            _ok[x]["CODE_ALARM"] = None
            _ok[x]["DESC_ALARM"] = None

    @unittest.skipIf(skipped, "")
    def test_check_byte_flow(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        self.assertTrue(orders._check_byte_flow(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_check_error_10(self):
        self.system_data['hdlc'] = hdlc_less
        orders = order.from_test(self.system_data)
        self.assertFalse(orders._check_byte_flow(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_crc16(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            self.assertTrue(orders._check_rc_16(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_crc16_wrong_51(self):
        self.system_data['hdlc'] = hdlc_crc16_wrong
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            self.assertFalse(orders._check_rc_16(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_err_send_21(self):
        self.system_data['hdlc'] = hdlc_err_send
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertFalse(orders._check_header_packet(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_err_recv_22(self):
        self.system_data['hdlc'] = hdlc_err_recv
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertFalse(orders._check_header_packet(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_err_type_23(self):
        self.system_data['hdlc'] = hdlc_err_type
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertFalse(orders._check_header_packet(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_err_len_24(self):
        self.system_data['hdlc'] = hdlc_err_len
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertFalse(orders._check_header_packet(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_err_null_byte_26(self):
        self.system_data['hdlc'] = hdlc_null_byte
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertFalse(orders._check_header_packet(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_err_incons_glAB_30(self):
        self.system_data['hdlc'] = hdlc_incons_gl_AB_30
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_forbidden_combination_countsAB_31(self):
        self.system_data['hdlc'] = hdlc_forbiden_counts_31
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_forbidden_combination_countA_32(self):
        self.system_data['hdlc'] = hdlc_forbiden_count_A
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_forbidden_combination_countB_33(self):
        self.system_data['hdlc'] = hdlc_forbiden_count_B
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_err_ctb_36(self):
        self.system_data['hdlc'] = hdlc_err_ctb_36
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            if orders._check_decode_ab():
                                self.assertFalse(orders._check_count_order(), print_OK(self.system_data))
                                self.assertEqual(self.system_data["ORDER_CODE_ALARM"], 0)
                                self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 36)

    @unittest.skipIf(skipped, " ")
    def test_err_cta_37(self):
        self.system_data['hdlc'] = hdlc_err_cta_37
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            if orders._check_decode_ab():
                                self.assertFalse(orders._check_count_order(), print_OK(self.system_data))
                                self.assertEqual(self.system_data["ORDER_CODE_ALARM"], 0)
                                self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 37)

    @unittest.skipIf(skipped, "")
    def test_err_ctab_34(self):
        self.system_data['hdlc'] = hdlc_err_ctab_34
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            if orders._check_decode_ab():
                                self.assertFalse(orders._check_count_order(), print_OK(self.system_data))
                                self.assertEqual(self.system_data["ORDER_CODE_ALARM"], 0)
                                self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 34)

    @unittest.skipIf(skipped, "")
    def test_err_cta_gl_30(self):
        self.system_data['hdlc'] = hdlc_err_cta_gl_30
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(), print_OK(self.system_data))
                    self.assertEqual(self.system_data["ORDER_CODE_ALARM"], 30)

    @unittest.skipIf(skipped, "")
    def test_err_ctb_gl_30(self):
        self.system_data['hdlc'] = hdlc_err_ctb_gl_30
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(), print_OK(self.system_data))
                    self.assertEqual(self.system_data["ORDER_CODE_ALARM"], 30)

    @unittest.skipIf(skipped, "")
    def test_err_ctab_gl_34(self):
        self.system_data['hdlc'] = hdlc_err_ctab_gl_34
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            if orders._check_decode_ab():
                                self.assertFalse(orders._check_count_order(), print_OK(self.system_data))
                                self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 34)

    @unittest.skipIf(skipped, "")
    def test_err_not_ab_41(self):
        self.system_data['hdlc'] = hdlc_err_not_ab_41
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_err_len_ab_43(self):
        self.system_data['hdlc'] = hdlc_err_len_ab_43
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_check_header(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertTrue(orders._check_header_packet(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_check_body(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertTrue(orders._check_body_telegramm_ab(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_parser_1ok(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_parser_2ok(self):
        self.system_data['hdlc'] = hdlc_2
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_parser_3ok(self):
        self.system_data['hdlc'] = hdlc_3
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_parser_4ok(self):
        self.system_data['hdlc'] = hdlc_4
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_parser_5ok(self):
        self.system_data['hdlc'] = hdlc_5
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_parser_6ok(self):
        self.system_data['hdlc'] = hdlc_6
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_parser_7ok(self):
        self.system_data['hdlc'] = hdlc_7
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_parser_8ok(self):
        self.system_data['hdlc'] = hdlc_8
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(), print_OK(self.system_data))

    @unittest.skipIf(skipped, " ")
    def test_parser_9ok(self):
        self.system_data['hdlc'] = hdlc_9
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(), print_OK(self.system_data))

    @unittest.skipIf(skipped, " ")
    def test_decode_ab(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            self.assertTrue(orders._check_decode_ab(), print_OK(self.system_data))
                            self.assertEqual(self.system_data["ORDER_CODE_ALARM"], 0)
                            self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], None)

    @unittest.skipIf(skipped, " ")
    def test_err_not_a_71(self):
        self.system_data['hdlc'] = hdlc_err_not_a_71
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            self.assertTrue(orders._check_decode_ab(), print_OK(self.system_data))
                            self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 71)

    @unittest.skipIf(skipped, " ")
    def test_err_not_b_72(self):
        self.system_data['hdlc'] = hdlc_err_not_b_72
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            self.assertTrue(orders._check_decode_ab(), print_OK(self.system_data))
                            self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 72)

    @unittest.skipIf(skipped, " ")
    def test_err_crca_75(self):
        self.system_data['hdlc'] = hdlc_err_crca_75
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            self.assertTrue(orders._check_decode_ab(), print_OK(self.system_data))
                            self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 75)

    @unittest.skipIf(skipped, " ")
    def test_err_crcb_76(self):
        self.system_data['hdlc'] = hdlc_err_crcb_76
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            self.assertTrue(orders._check_decode_ab(), print_OK(self.system_data))
                            self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 76)

    @unittest.skipIf(skipped, " ")
    def test_err_crcab_74(self):
        self.system_data['hdlc'] = hdlc_err_crcab_74
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            self.assertTrue(orders._check_decode_ab(), print_OK(self.system_data))
                            self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 74)

    @unittest.skipIf(skipped, " ")
    def test_err_conc_77(self):
        self.system_data['hdlc'] = hdlc_err_conc
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            self.assertTrue(orders._check_decode_ab(), print_OK(self.system_data))
                            self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 77)

    @unittest.skipIf(skipped, " ")
    def test_err_co_a_81(self):
        self.system_data['hdlc'] = hdlc_err_co_a_81
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            self.assertTrue(orders._check_decode_ab(), print_OK(self.system_data))
                            self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 81)

    @unittest.skipIf(skipped, " ")
    def test_check_zone_ok(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            if orders._check_decode_ab():
                                if orders._check_count_order():
                                    self.assertTrue(orders._decode_zone_status(), print_OK(self.system_data))
                                    self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], None)

    @unittest.skipIf(skipped, "")
    def test_tresh_2ok(self):
        self.system_data['hdlc'] = hdlc_2
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_tresh_3ok(self):
        self.system_data['hdlc'] = hdlc_3
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_tresh_4ok(self):
        self.system_data['hdlc'] = hdlc_4
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_tresh_5ok(self):
        self.system_data['hdlc'] = hdlc_5
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_tresh_6ok(self):
        self.system_data['hdlc'] = hdlc_6
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_tresh_7ok(self):
        self.system_data['hdlc'] = hdlc_7
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_tresh_8ok(self):
        self.system_data['hdlc'] = hdlc_8
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_tresh_9ok(self):
        self.system_data['hdlc'] = hdlc_9
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(), print_OK(self.system_data))

    @unittest.skipIf(skipped, "")
    def test_no_order_ok_6(self):
        self.system_data['hdlc'] = hdlc_6
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(), print_OK(self.system_data))
        self.assertEqual(self.system_data["ORDER_CODE_ALARM"], 0)
        self.assertEqual(self.system_data["OK"]["3259"]["CODE_ALARM"], 6)

    @unittest.skipIf(skipped, "")
    def test_duplicated_order_7(self):
        self.system_data['hdlc'] = hdlc_6
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(), print_OK(self.system_data))
        self.assertEqual(self.system_data["ORDER_CODE_ALARM"], 0)
        self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], 7)



if __name__ == "__main__":
    unittest.main()

