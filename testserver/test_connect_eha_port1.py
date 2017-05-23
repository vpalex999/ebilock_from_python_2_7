"""Test1 EHA client"""
import pytest
import allure
import re


@allure.step("Test_EHA_port1")
def test_1_eha_port1(from_port_1):
    """Test connect client EHA to test server for port1"""
    d, data = from_port_1["defer"], from_port_1["data"]

    @allure.step("Call connected")
    def connected(status):
        allure.attach("Check connected client from test server",\
                      "Callback is return result connect for server\
                       {}:{} from: {}".format(data["server_host"],\
                                              data["server_port1"],\
                                              status))
        if data["double"]:
            assert re.search(data["client_eha_side_1"], status) or re.search(data["client_eha_side_2"], status),\
             "Detection connection to local port {} from an unexpected ip address: {}.\n\
             The system waits for connection from the addreses: {} or {}\n"\
            .format(data["server_port1"], status, data["client_eha_side_1"], data["client_eha_side_2"])
        else:
            assert re.search(data["client_eha_float"], status),\
             "Detection connection to local port {} from an unexpected ip address: {}.\n\
             The system waits for connection from the addreses: {} or {}\n"\
            .format(data["server_port1"], status, data["client_eha_float"])

    @allure.step("Call connected_err")
    def connected_err(reason):
        allure.attach("Return Error from test server",\
                      "Callback is return Error result connect for server\
                       {}:{} from: {}".format(data["server_host"],\
                                              data["server_port1"],\
                                              reason))
        assert reason.value, "Delay {} seconds connection to local port \{} from EHA"\
                             .format(data["timeout_connect"], data["server_port1"])
        count_connect = reason.value
        reconnect = 0
        other_ip = 0
        for client in count_connect:
            print("Search client", "Search client: {}".format(client))
            if data["double"]:
                if re.search(data["client_eha_side_1"], str(client)) or re.search(data["client_eha_side_2"], str(client)):
                    reconnect += 1
                else:
                    other_ip += 1
            else:
                if re.search(data["client_eha_float"], str(client)):
                    reconnect += 1
                else:
                    other_ip +=1

        assert reconnect <= 1 and other_ip == 0, "Detection Reconnect to local port {} from client EHA: {}."\
            .format(data["server_port1"], count_connect)

        assert reconnect <= 1 and other_ip <= 1, "Detection Reconnect  and Connection from Other IP to local port {} from client EHA: {}."\
            .format(data["server_port1"], count_connect)

        assert not reconnect and other_ip <= 1, "Detection Connection from Other IP to local port {} from client EHA: {}."\
            .format(data["server_port1"], count_connect)

    with pytest.allure.step("Add: d.addCallbacks"):
        allure.attach("Add callbacks function connected() and connected_err()"\
                      , "d.addcallback port1 {}, {}".format(connected, connected_err))

    d.addCallbacks(connected, connected_err)
    return d





