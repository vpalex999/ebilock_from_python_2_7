"""Test2 EHA client"""
import pytest
import allure
import re


@allure.step("Test_EHA_port2")
def test_2_eha_port2(from_port_2):
    """Test connect client EHA to test server for port2"""
    d, data = from_port_2["defer"], from_port_2["data"]

    @allure.step("Call connected")
    def connected(status):
        allure.attach("Check connected client from test server",\
                      "Callback is return result connect for server\
                       {}:{} from: {}".format(data["server_host"],\
                                              data["server_port2"],\
                                              status))
    
        if data["double"]:
            assert re.search(data["client_eha_side_1"], status) or re.search(data["client_eha_side_2"], status),\
             "Detection connection to local port {} from an unexpected ip address: {}.\n\
             The system waits for connection from the addreses: {} or {}\n"\
            .format(data["server_port2"], status, data["client_eha_side_1"], data["client_eha_side_2"])
        else:
            assert re.search(data["client_eha_float"], status),\
             "Detection connection to local port {} from an unexpected ip address: {}.\n\
             The system waits for connection from the addreses: {} or {}\n"\
            .format(data["server_port2"], status, data["client_eha_float"])

    @allure.step("Call connected_err")
    def connected_err(reason):
        allure.attach("Return Error from test server",\
                      "Callback is return Error result connect for server\
                       {}:{} from: {}".format(data["server_host"],\
                                              data["server_port2"],\
                                              reason))
        assert reason.value, "Delay {} seconds connection to local port \{} from EHA"\
                                      .format(data["timeout_connect"], data["server_port2"])

    with pytest.allure.step("Add: d.addCallbacks"):
        allure.attach("Add callbacks function connected() and connected_err()"\
                      , "d.addcallback port2 {}, {}".format(connected, connected_err))

    d.addCallbacks(connected, connected_err)
    return d

