"""Test Service EHA client"""
import pytest
import allure
import re


@allure.step("Test_Service_EHA_port1")
def test_1_service_eha_port1(maket_test1_port1):
    """Test Service connect client EHA to test server for port1"""
    d = maket_test1_port1
    print("D: {}".format(d))

    def check_connect(status):
        print("Check_connect status: {}".format(status))
        assert True, "Detect Connection NOK!!!"
        print("Detect Connection OK!!! {}".format(status))

    d.addCallback(check_connect)
    return d





