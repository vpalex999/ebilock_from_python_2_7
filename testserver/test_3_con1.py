"""Test Service EHA client - test_3_con1 -"""
import pytest
import allure


@pytest.fixture()
def maket3_test_3_con1(test_server_3_1, data_maket_mea1209_1211):
    print("maket3_test_3_con1")
    return test_server_3_1(data_maket_mea1209_1211, data_maket_mea1209_1211["server_port1"])


@allure.step("Test Checking the disconnection after connection from port1")
def test_3_con1(maket3_test_3_con1):
    """Test Checking the disconnection after connection from port1"""
    # print("test_3_con1")
    d = maket3_test_3_con1

    def check_disconnect_after_connect(status):
        # print(status)
        stat, desc = status
        assert stat, desc

    d.addCallback(check_disconnect_after_connect)
    return d

