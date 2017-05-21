""" test EHA client """
import pytest
import allure
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.defer import Deferred




@allure.step("test_4")
def test_4():
    allure.attach("Return True", "True")
    return True

@allure.step("test_5")
def test_5():
    allure.attach("Return True", "True")
    return True

@allure.step("test_6")
def test_6():
    allure.attach("Return True", "True")
    return True
