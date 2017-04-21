""" Verification of an order telegram """
import time
import unittest
from sources.ebilockorder_new import Ebilock_order as order

# own 3257
hdlc_telegramm = "00 01 02 00 00 00 1C 00 04 FB 00 0E 32 57 74 04 C1 81 2F 32 57 76 FB 3E 7E F5 60 2D"
hdlc_less = "00 01 02 00 00 00 1c"
hdlc_crc16_wrong = "00 01 02 00 00 00 1c 00 c3 3c 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b 2e 7w"
# Error ID Send
hdlc_err_send = "01 01 02 00 00 00 1c 00 c3 3c 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b 82 1C"
# Error ID Reveive
hdlc_err_recv = "00 02 02 00 00 00 1c 00 c3 3c 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b e0 a1"
# Type out of range
hdlc_err_type = "00 01 03 00 00 00 1c 00 c3 3c 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b 19 7e"
# Error len Packet
hdlc_err_len = "00 01 02 00 00 00 1d 00 c3 3c 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b 1b ce"
# Wrong length block telegramm
hdlc_wrong_len_block_tel = "00 01 02 00 00 00 1e 00 c3 3c 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b 00 00 51 63"
# Wrong Null byte
hdlc_null_byte = "00 01 02 00 00 00 1c 01 c3 3c 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b f0 62"
# Error not ab
hdlc_err_not_ab_41 = "00 01 02 00 00 00 0E 00 04 FB 00 00 DB CB"
# Error len A/B
hdlc_err_len_ab_43 = "00 01 02 00 00 00 1C 00 03 FC 01 1E 32 57 74 03 C1 81 2F 32 57 76 FC 3E 7E F5 7C 68"
# Inconsistent global A/B
hdlc_incons_gl_AB_30 = "00 01 02 00 00 00 1c 00 c2 3c 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b de 4c"
# Forbidden combination of counters
hdlc_forbiden_counts_31 = "00 01 02 00 00 00 1c 00 00 ff 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b 8b a5"
# Forbidden combination of counter A
hdlc_forbiden_count_A = "00 01 02 00 00 00 1c 00 00 f1 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b 6e f9"
# Forbidden combination of counter B
hdlc_forbiden_count_B = "00 01 02 00 00 00 1c 00 02 ff 00 0e 32 57 74 c3 e4 1b b1 32 57 76 3c 1b e4 6b 7b e6"
# Error not tlg a
hdlc_err_not_a_71 = "00 01 02 00 00 00 15 00 03 FC 00 07 32 57 76 FC 3E 7E F5 9C 48"
# Error not tlg b
hdlc_err_not_b_72 = "00 01 02 00 00 00 15 00 02 FD 00 07 32 57 74 02 C1 81 2F F4 7B"
# Error crc_a
hdlc_err_crca_75 = "00 01 02 00 00 00 1C 00 03 FC 00 0E 32 57 74 03 C1 81 34 32 57 76 FC 3E 7E F5 71 DD"
# Error crc_b
hdlc_err_crcb_76 = "00 01 02 00 00 00 1C 00 03 FC 00 0E 32 57 74 03 C1 81 2F 32 57 76 FC 3E 7E FA 6B 29"
# Error crcab
hdlc_err_crcab_74 = "00 01 02 00 00 00 1C 00 03 FC 00 0E 32 57 74 03 C1 81 34 32 57 76 FC 3E 7E FA 80 32"
# Error conc
hdlc_err_conc = "00 01 02 00 00 00 1C 00 03 FC 00 0E 32 57 74 03 C1 81 2F 32 57 76 FC C1 81 5C 72 99"
# Error CO
hdlc_err_co_a_81 = "00 01 02 00 00 00 1C 00 04 FB 00 0E 32 57 78 04 C1 81 80 32 57 7C FB 3E 7E CF F8 CD"



# own 3257 - own 3259
hdlc_2 = "00 01 02 00 00 00 28 00 06 F9 00 1A 32 57 74 06 C1 81 2F 32 57 76 F9 3E 7E F5 32 59 64 06 FF 2E 32 59 66 F9 00 08 BB 94"
# own 3237 - own 3259 - other 3261
hdlc_3 = "00 01 02 00 00 00 34 00 04 FB 00 26 32 57 74 04 C1 81 2F 32 57 76 FB 3E 7E F5 32 59 64 04 FF 2E 32 59 66 FB 00 08 32 61 64 04 AA 2F 32 61 66 FB 55 09 59 FF"
# own 3257 - other 3263 - own 3259 - other 3261
hdlc_4 = "00 01 02 00 00 00 40 00 03 FC 00 32 32 57 74 03 C1 81 2F 32 57 76 FC 3E 7E F5 32 63 64 03 55 D1 32 63 66 FC AA F7 32 59 64 03 FF 2E 32 59 66 FC 00 08 32 61 64 03 AA 2F 32 61 66 FC 55 09 1A AD"
# other 3253 - own 3257 - other 3263 - own 3259 - other 3261
hdlc_5 = "00 01 02 00 00 00 4C 00 02 FD 00 3E 32 53 64 02 00 99 32 53 66 FD FF BF 32 57 74 02 C1 81 2F 32 57 76 FD 3E 7E F5 32 63 64 02 55 D1 32 63 66 FD AA F7 32 59 64 02 FF 2E 32 59 66 FD 00 08 32 61 64 02 AA 2F 32 61 66 FD 55 09 DD 5F"
# own 3257 - other 3263 - own 3257
hdlc_6 = "00 01 02 00 00 00 36 00 03 FC 00 28 32 57 74 03 C1 81 2F 32 57 76 FC 3E 7E F5 32 63 64 03 55 D1 32 63 66 FC AA F7 32 57 74 03 C1 81 2F 32 57 76 FC 3E 7E F5 0D 64"
# own 3257 - own 3259 - own 3257
hdlc_7 = "00 01 02 00 00 00 36 00 06 F9 00 28 32 57 74 06 C1 81 2F 32 57 76 F9 3E 7E F5 32 59 64 06 FF 2E 32 59 66 F9 00 08 32 57 74 06 C1 81 2F 32 57 76 F9 3E 7E F5 3C 35"
# own 3257 - own 3257 - own 3259 - own 3259
hdlc_8 = "00 01 02 00 00 00 42 00 06 F9 00 34 32 57 74 06 C1 81 2F 32 57 76 F9 3E 7E F5 32 59 64 06 FF 2E 32 59 66 F9 00 08 32 57 74 06 C1 81 2F 32 57 76 F9 3E 7E F5 32 59 64 06 FF 2E 32 59 66 F9 00 08 5C D0"
# other 3261 - own 3257 - other 3261 - own 3259 - own 3257 - own 3259 - own 3261
hdlc_9 = "00 01 02 00 00 00 66 00 06 F9 00 58 32 61 64 04 AA 2F 32 61 66 FB 55 09 32 57 74 06 C1 81 2F 32 57 76 F9 3E 7E F5 32 61 64 04 AA 2F 32 61 66 FB 55 09 32 59 64 06 FF 2E 32 59 66 F9 00 08 32 57 74 06 C1 81 2F 32 57 76 F9 3E 7E F5 32 59 64 06 FF 2E 32 59 66 F9 00 08 32 61 64 04 AA 2F 32 61 66 FB 55 09 25 DB"

system_data = {
            "start_time": time.time(),
            "hdlc": "",
            "time_delta": "",
            "System_Status": "SAFE",
            "Lost_Connect": False,
            "FIRST_START": True,
            "Count_A": 1,
            "Count_B": 254,
            "Err_Count": 0,
            "Timer_status": False,
            "Start_timer": False,
            "ORDER": False,
            "ORDER_STATUS": None,
            "HDLC_SEND_STATUS": None,
            "OK": {"3257": {
                            "STATUS_OK": "SAFE",
                            "LOOP_OK": False,
                            "AREA_OK": False,
                            "HUB_OK": False,
                            "NUMBER_OK": False,
                            "ADDRESS_OK": False,
                            "Err_Count": 0,
                            "count_a": 1,
                            "count_b": 254,
                            "ORDER_WORK": None,
                            #"ZONE_DATA": None,
                            "ZONE_FROM_CNS": {1: 3, 2: 1, 3: 1, 4: 1, 5: 0, 6: 2, 7: 2, 8: 3},
                            "ZONE_FOR_CNS": None,
                            "CODE_ALARM": None,
                            "DESC_ALARM": None,
                            "TELEGRAMM_A": None,
                            "TELEGRAMM_B": None,
                            },
                    "3259": {
                            "STATUS_OK": "SAFE",
                            "LOOP_OK": False,
                            "AREA_OK": False,
                            "HUB_OK": False,
                            "NUMBER_OK": False,
                            "ADDRESS_OK": False,
                            "Err_Count": 0,
                            "count_a": 1,
                            "count_b": 254,
                            "ORDER_WORK": None,
                            #"ZONE_DATA": None,
                            "ZONE_FROM_CNS": {1: 3, 2: 1, 3: 1, 4: 1, 5: 0, 6: 2, 7: 2, 8: 3},
                            "ZONE_FOR_CNS": None,
                            "CODE_ALARM": None,
                            "DESC_ALARM": None,
                            "TELEGRAMM_A": None,
                            "TELEGRAMM_B": None,
                            }},

}

skipped = False

def print_OK(system_data):
    #print("Main Code alarm: {}, deck: {}".format(system_data["CODE_ALARM"], system_data["DESC_ALARM"]))
    _ok = system_data["OK"]
    result = "\n"
    for x in _ok:
        result = result + "OK: {}, code alarm: {}, description: {}\n".format(x, _ok[x]['CODE_ALARM'], _ok[x]['DESC_ALARM'])
    return result + "*"*10

class TestOrder(unittest.TestCase):

    # @unittest.skipIf(skipped, "")
    def setUp(self):
        self.system_data = system_data
    #     self.order = order.from_test(hdlc_telegramm)
    #     self.order_less = order.from_test(hdlc_less)
    #     self.order_crc16_wrong = order.from_test(hdlc_crc16_wrong)

    @unittest.skipIf(skipped, "")
    def test_check_byte_flow(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        self.assertTrue(orders._check_byte_flow(),\
                        print("Main Code alarm: {}, deck: {}, \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_check_error_10(self):
        self.system_data['hdlc'] = hdlc_less
        orders = order.from_test(self.system_data)
        self.assertFalse(orders._check_byte_flow(),\
                         print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_crc16(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            self.assertTrue(orders._check_rc_16(),\
                            print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_crc16_wrong_51(self):
        self.system_data['hdlc'] = hdlc_crc16_wrong
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            self.assertFalse(orders._check_rc_16(),\
                             print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_err_send_21(self):
        self.system_data['hdlc'] = hdlc_err_send
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertFalse(orders._check_header_packet(),\
                                 print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_err_recv_22(self):
        self.system_data['hdlc'] = hdlc_err_recv
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertFalse(orders._check_header_packet(),\
                                 print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_err_type_23(self):
        self.system_data['hdlc'] = hdlc_err_type
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertFalse(orders._check_header_packet(),\
                                 print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_err_len_24(self):
        self.system_data['hdlc'] = hdlc_err_len
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertFalse(orders._check_header_packet(),\
                                 print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_err_null_byte_26(self):
        self.system_data['hdlc'] = hdlc_null_byte
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertFalse(orders._check_header_packet(),\
                                 print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_err_incons_glAB_30(self):
        self.system_data['hdlc'] = hdlc_incons_gl_AB_30
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(),\
                                     print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_forbidden_combination_countsAB_31(self):
        self.system_data['hdlc'] = hdlc_forbiden_counts_31
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(),\
                                     print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_forbidden_combination_countA_31(self):
        self.system_data['hdlc'] = hdlc_forbiden_count_A
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(),\
                                     print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_forbidden_combination_countB_31(self):
        self.system_data['hdlc'] = hdlc_forbiden_count_B
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(),\
                                     print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_err_not_ab_41(self):
        self.system_data['hdlc'] = hdlc_err_not_ab_41
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(),\
                                     print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_err_len_ab_43(self):
        self.system_data['hdlc'] = hdlc_err_len_ab_43
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertFalse(orders._check_body_telegramm_ab(),\
                                     print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_check_header(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                self.assertTrue(orders._check_header_packet(),\
                                print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_check_body(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    self.assertTrue(orders._check_body_telegramm_ab(),\
                                    print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_parser_1ok(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(),\
                                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_parser_2ok(self):
        self.system_data['hdlc'] = hdlc_2
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(),\
                                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_parser_3ok(self):
        self.system_data['hdlc'] = hdlc_3
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(),\
                                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_parser_4ok(self):
        self.system_data['hdlc'] = hdlc_4
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(),\
                                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_parser_5ok(self):
        self.system_data['hdlc'] = hdlc_5
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(),\
                                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_parser_6ok(self):
        self.system_data['hdlc'] = hdlc_6
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(),\
                                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_parser_7ok(self):
        self.system_data['hdlc'] = hdlc_7
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(),\
                                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_parser_8ok(self):
        self.system_data['hdlc'] = hdlc_8
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(),\
                                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, " ")
    def test_parser_9ok(self):
        self.system_data['hdlc'] = hdlc_9
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        self.assertTrue(orders._parcer_ok(),\
                                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                                         orders.telegramm_decode["CODE_ALARM"],\
                                         orders.telegramm_decode["DESC_ALARM"],\
                                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, " ")
    def test_decode_ab(self):
        self.system_data['hdlc'] = hdlc_telegramm
        orders = order.from_test(self.system_data)
        if orders._check_byte_flow():
            if orders._check_rc_16():
                if orders._check_header_packet():
                    if orders._check_body_telegramm_ab():
                        if orders._parcer_ok():
                            self.assertTrue(orders._check_decode_ab(),\
                                            print("Main Code alarm: {}, deck: {} \n {}".format(\
                                             orders.telegramm_decode["CODE_ALARM"],\
                                             orders.telegramm_decode["DESC_ALARM"],\
                                             print_OK(self.system_data))))
                            self.assertEqual(orders.telegramm_decode["CODE_ALARM"], 0)
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
                            self.assertTrue(orders._check_decode_ab(),\
                                            print("Main Code alarm: {}, deck: {} \n {}".format(\
                                             orders.telegramm_decode["CODE_ALARM"],\
                                             orders.telegramm_decode["DESC_ALARM"],\
                                             print_OK(self.system_data))))
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
                            self.assertTrue(orders._check_decode_ab(),\
                                            print("Main Code alarm: {}, deck: {} \n {}".format(\
                                             orders.telegramm_decode["CODE_ALARM"],\
                                             orders.telegramm_decode["DESC_ALARM"],\
                                             print_OK(self.system_data))))
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
                            self.assertTrue(orders._check_decode_ab(),\
                                            print("Main Code alarm: {}, deck: {} \n {}".format(\
                                             orders.telegramm_decode["CODE_ALARM"],\
                                             orders.telegramm_decode["DESC_ALARM"],\
                                             print_OK(self.system_data))))
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
                            self.assertTrue(orders._check_decode_ab(),\
                                            print("Main Code alarm: {}, deck: {} \n {}".format(\
                                             orders.telegramm_decode["CODE_ALARM"],\
                                             orders.telegramm_decode["DESC_ALARM"],\
                                             print_OK(self.system_data))))
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
                            self.assertTrue(orders._check_decode_ab(),\
                                            print("Main Code alarm: {}, deck: {} \n {}".format(\
                                             orders.telegramm_decode["CODE_ALARM"],\
                                             orders.telegramm_decode["DESC_ALARM"],\
                                             print_OK(self.system_data))))
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
                            self.assertTrue(orders._check_decode_ab(),\
                                            print("Main Code alarm: {}, deck: {} \n {}".format(\
                                             orders.telegramm_decode["CODE_ALARM"],\
                                             orders.telegramm_decode["DESC_ALARM"],\
                                             print_OK(self.system_data))))
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
                            self.assertTrue(orders._check_decode_ab(),\
                                            print("Main Code alarm: {}, deck: {} \n {}".format(\
                                             orders.telegramm_decode["CODE_ALARM"],\
                                             orders.telegramm_decode["DESC_ALARM"],\
                                             print_OK(self.system_data))))
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
                                    self.assertTrue(orders._decode_zone_status(),\
                                                    print("Main Code alarm: {}, deck: {} \n {}".format(\
                                                     orders.telegramm_decode["CODE_ALARM"],\
                                                     orders.telegramm_decode["DESC_ALARM"],\
                                                     print_OK(self.system_data))))
                                    self.assertEqual(self.system_data["OK"]["3257"]["CODE_ALARM"], None)
    
    @unittest.skipIf(skipped, "")
    def test_tresh_2ok(self):
        self.system_data['hdlc'] = hdlc_2
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(),\
                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                         orders.telegramm_decode["CODE_ALARM"],\
                         orders.telegramm_decode["DESC_ALARM"],\
                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_tresh_3ok(self):
        self.system_data['hdlc'] = hdlc_3
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(),\
                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                         orders.telegramm_decode["CODE_ALARM"],\
                         orders.telegramm_decode["DESC_ALARM"],\
                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_tresh_4ok(self):
        self.system_data['hdlc'] = hdlc_4
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(),\
                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                         orders.telegramm_decode["CODE_ALARM"],\
                         orders.telegramm_decode["DESC_ALARM"],\
                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_tresh_5ok(self):
        self.system_data['hdlc'] = hdlc_5
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(),\
                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                         orders.telegramm_decode["CODE_ALARM"],\
                         orders.telegramm_decode["DESC_ALARM"],\
                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_tresh_6ok(self):
        self.system_data['hdlc'] = hdlc_6
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(),\
                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                         orders.telegramm_decode["CODE_ALARM"],\
                         orders.telegramm_decode["DESC_ALARM"],\
                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_tresh_7ok(self):
        self.system_data['hdlc'] = hdlc_7
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(),\
                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                         orders.telegramm_decode["CODE_ALARM"],\
                         orders.telegramm_decode["DESC_ALARM"],\
                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_tresh_8ok(self):
        self.system_data['hdlc'] = hdlc_8
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(),\
                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                         orders.telegramm_decode["CODE_ALARM"],\
                         orders.telegramm_decode["DESC_ALARM"],\
                         print_OK(self.system_data))))

    @unittest.skipIf(skipped, "")
    def test_tresh_9ok(self):
        self.system_data['hdlc'] = hdlc_9
        orders = order.from_test(self.system_data)
        self.assertTrue(orders.check_telegramm(),\
                        print("Main Code alarm: {}, deck: {} \n {}".format(\
                         orders.telegramm_decode["CODE_ALARM"],\
                         orders.telegramm_decode["DESC_ALARM"],\
                         print_OK(self.system_data))))



if __name__ == "__main__":
    unittest.main()

