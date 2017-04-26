""" Verification of an modele client_main """

import unittest
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests_from_eha.data import *
from client_main import *
from sources.client_parser import read_config_file
from sources.client_parser import check_header_config
from sources.client_parser import from_address_ok
from sources.client_parser import create_ok
from sources.client_parser import default_data_ok

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


class TestClienMain(unittest.TestCase):

    def setUp(self):
        self.config_1ok_json_ok = os.path.abspath(os.path.join(os.path.dirname(__file__), 'client_eha_config_1ok_ok.json'))
        self.config_1ok_err_json = os.path.abspath(os.path.join(os.path.dirname(__file__), 'client_eha_config_1ok_error_json.json'))
        self.config_1ok_err_address_ok = os.path.abspath(os.path.join(os.path.dirname(__file__), 'client_eha_config_1ok_wrong_address_ok.json'))
        self.config_err_header = os.path.abspath(os.path.join(os.path.dirname(__file__),'client_eha_config_wrong_header.json'))
        self.default_data_ok = default_data_ok.copy()
        self.data_for_ok = {}
        self.system_data_ok = {}
        pass
        # self.system_data = system_data_1.copy()
        # _ok = self.system_data["OK"]
        # for x in _ok:
        #     _ok[x]["CODE_ALARM"] = None
        #     _ok[x]["DESC_ALARM"] = None

    @unittest.skipIf(skipped, "")
    def test_client_main_read_format_json_config_ok(self):
        data = read_config_file(self.config_1ok_json_ok)
        self.assertTrue(data)

    @unittest.skipIf(skipped, "")
    def test_client_main_read_format_json_config_err(self):
        data = read_config_file(self.config_1ok_err_json)
        self.assertFalse(data)

    @unittest.skipIf(skipped, "")
    def test_client_main_read_data_1ok(self):
        data = read_config_file(self.config_1ok_json_ok)
        self.assertEqual(4015, data['port1'])
        self.assertEqual(4016, data['port2'])
        self.assertEqual('192.168.101.100', data['host'])
        self.assertEqual("3257", data["Telegrams"][0]["ocAddr"])
        self.assertEqual([0, 1, 2, 3], data["Telegrams"][0]["Zones"])

    @unittest.skipIf(skipped, "")
    def test_client_main_check_header_config_ok(self):
        data = read_config_file(self.config_1ok_json_ok)
        self.assertTrue(check_header_config(data))

    @unittest.skipIf(skipped, "")
    def test_client_main_check_header_config_err(self):
        data = read_config_file(self.config_err_header)
        self.assertFalse(check_header_config(data))

    @unittest.skipIf(skipped, "")
    def test_client_main_check_address_ok(self):
        work_data = {}
        data = read_config_file(self.config_1ok_json_ok)
        for ok in data["Telegrams"]:
            work_data = (from_address_ok(ok["ocAddr"], self.default_data_ok))
            for wd in work_data:
                self.assertEqual(3, work_data[wd]["LOOP_OK"])
                self.assertEqual(1, work_data[wd]["AREA_OK"])
                self.assertEqual(5, work_data[wd]["HUB_OK"])
                self.assertEqual(3, work_data[wd]["NUMBER_OK"])
                self.assertEqual('3257', work_data[wd]["ADDRESS_OK"])

    @unittest.skipIf(skipped, "")
    def test_client_main_check_wrong_address_ok(self):
        data = read_config_file(self.config_1ok_err_address_ok)
        for ok in data["Telegrams"]:
            self.assertFalse(from_address_ok(ok["ocAddr"], self.default_data_ok))

    @unittest.skipIf(skipped, "")
    def test_client_main_create_ok(self):
        data_config = read_config_file(self.config_1ok_json_ok)
        check_header_config(data_config)
        self.assertTrue(create_ok(data_config, self.system_data_ok, self.default_data_ok, from_address_ok))
        for wd in self.system_data_ok:
                self.assertEqual(3, self.system_data_ok[wd]["LOOP_OK"])
                self.assertEqual(1, self.system_data_ok[wd]["AREA_OK"])
                self.assertEqual(5, self.system_data_ok[wd]["HUB_OK"])
                self.assertEqual(3, self.system_data_ok[wd]["NUMBER_OK"])
                self.assertEqual('3257', self.system_data_ok[wd]["ADDRESS_OK"])



if __name__ == "__main__":
    unittest.main()

