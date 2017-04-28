""" Module for parsing config """
import time
import json
import os
import optparse
from pprint import pprint

# Data from parcer config file
data_from_config = {}
# OK for work
system_data_ok = {}
# Default DATA from OK
default_data_ok = {
            "STATUS_OK": "SAFE",
            "Timer_status": False,
            "Start_timer": False,
            "LOOP_OK": False,
            "AREA_OK": False,
            "HUB_OK": False,
            "NUMBER_OK": False,
            "ADDRESS_OK": False,
            "Err_Count": 0,
            "count_a": 1,
            "count_b": 254,
            "ORDER_WORK": None,
            "ZONE_FROM_CNS": dict.fromkeys(range(36), 0),
            "ZONE_FOR_CNS": dict.fromkeys(range(36), 0),
            "CODE_ALARM": None,
            "DESC_ALARM": None,
            "TELEGRAMM_A": None,
            "TELEGRAMM_B": None,
            "RETURN_OK": 0,
        }


system_data = {
            "start_time": time.time(),
            "hdlc": bytearray(),
            "time_delta": "",
            "System_Status": "SAFE",
            "Lost_Connect": False,
            "FIRST_START": True,
            "Count_A": 1,
            "Count_B": 254,
            "Err_Count": 0,
            "Timer_status": False,
            "Start_timer": False,
            "ORDER_Count_A": 1,
            "ORDER_Count_B": 254,
            "ORDER_CODE_ALARM": None,
            "ORDER_DESC_ALARM": None,
            "ORDER": None,
            "ORDER_STATUS": None,
            "HDLC_SEND_STATUS": None,
            "OK": False,
            "WORK_OK": {},
            "Timer_OK": {},
        }


def parse_args():

    parser = optparse.OptionParser()
    _, file_config = parser.parse_args()
    if len(file_config) == 1:
        if os.path.isfile(file_config[0]):
            return file_config
        else:
            print("Arguments: '{}'\nThe specified file does not exist. Specify the correct file name and path!".format(', '.join(file_config)))
            return False
    else:
        print("Arguments: '{}'\nUsage: python client_main.py file_config.json".format(', '.join(file_config)))
        return False


def from_address_ok(address_ok, default_data_ok, reason=None):
        # print(type(address_ok))
        def_data = default_data_ok.copy()
        if type(address_ok) == int:
            address_ok = "{}".format(address_ok)

        def _code_address_ok(def_data, reason):
            address_ok = ""
            result = def_data["LOOP_OK"] << 4
            temp = def_data["AREA_OK"] << 1
            result = result | temp
            address_ok = address_ok + "{:02x}".format(int(hex(result), 16))
            result = 0
            temp = def_data["HUB_OK"] << 4
            result = result | temp
            temp = def_data["NUMBER_OK"] << 1
            temp = temp | 1
            result = result | temp
            address_ok = address_ok + "{:02x}".format(int(hex(result), 16))
            def_data["ADDRESS_OK"] = address_ok

        if len(address_ok) == 4:
            loop = int(address_ok[0], 16)
            area = int(address_ok[1], 16)
            hub = int(address_ok[2], 16)
            number = int(address_ok[3], 16)
            if area & 1 != 0:
                reason = "Invalid configure AREA OK!"
                print("Invalid configure AREA OK!")
                return False, reason
            elif number & 1 != 1:
                reason = "Invalid configure Number OK!"
                print("Invalid configure Number OK!")
                return False
            else:
                area = area >> 1
                number = number >> 1
                def_data["LOOP_OK"], def_data["AREA_OK"], def_data["HUB_OK"], def_data["NUMBER_OK"] = loop, area, hub, number
                _code_address_ok(def_data, reason)
                diction = {}
                diction[def_data["ADDRESS_OK"]] = def_data
                return diction
        else:
            reason = "number of characters to be equal to 4"
            print("number of characters to be equal to 4")
            return False


def zone_for_cns(data_from_config, system_data_ok):
    telegrams = data_from_config['Telegrams']
    
    for ok in system_data_ok:
        for tlg in telegrams:
            if tlg['ocAddr'] == ok:
                zone = tlg['Zones']
                zone_dict = {x: zone[x] for x in range(len(zone))}
                zone_from_cns = dict.fromkeys(range(36), 0)
                zone_from_cns.update(zone_dict)
                system_data_ok[ok]["ZONE_FROM_CNS"] = zone_from_cns



def read_config_file(file_name):
    try:
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8') as conf:
                data = (json.load(conf))
                return data.copy()
        else:
            print("Wronf file name or No file in the directory")
            return False
    except json.JSONDecodeError as e:
        print("Irregular structure json format from file: {}.\n{}".format(file_name, e))
        return False


def check_header_config(data):
    if not type(data['port1']) is int:
        data['port1'] = None
    if not type(data['port2']) is int:
        data['port2'] = None
    if data['port1'] is None and data['port2'] is None:
        print("At least one port must be int")
        return False
    if not type(data['host']) is str:
        print("Type 'host' must be a string")
        return False
    if len(data['host']) < 7:
        print("Wrong host address: {}".format(data['host']))
        return False
    return True


def create_ok(data_from_config, system_data_ok, default_data_ok, from_address_ok):

        addresses_ok = data_from_config["Telegrams"]
        try:
            for ok in addresses_ok:
                system_data_ok.update(from_address_ok(ok['ocAddr'], default_data_ok))
            return True
        except:
            print("Wrong adress OK: '{}'".format(ok))
            return False


def start_parser(file_config):
    try:
        data_from_config.update(read_config_file(file_config))
        if check_header_config(data_from_config):
            if create_ok(data_from_config, system_data_ok, default_data_ok, from_address_ok):
                zone_for_cns(data_from_config, system_data_ok)
                system_data["OK"] = system_data_ok
                return True
        return False
    except:
        return False


#parse_args()
#start_parser('./tests_from_eha/client_eha_config_1ok_ok.json')
# zone_for_cns(data_from_config, system_data_ok)

#data_from_config = read_config_file('./tests_from_eha/client_eha_config_1ok_ok.json')
#create_ok(data_from_config, system_data_ok, default_data_ok, from_address_ok)
#pass

# pass

# проверка корректности формата json -ok
# проверка на максимальное количество зон макс = 36
# проверка корректности адреса ОК
# Максимальное количество ОК