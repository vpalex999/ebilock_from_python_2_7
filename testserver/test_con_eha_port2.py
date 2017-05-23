"""Test Service EHA client"""
import pytest
import allure
import re


@allure.step("Test connect_for_Service_from EHA_port2")
def test_service_eha_port2(maket3_test1_port2):
    """Test Service connect client EHA to test server for port1"""
    d = maket3_test1_port2

    def check_connect(status):
        print(status)
        stat, desc = status
        assert stat, desc

    d.addCallback(check_connect)
    return d



