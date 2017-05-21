""" test EHA client """
import pytest
import allure
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.defer import Deferred




@allure.step("test_1")
def test_1():
    allure.attach("Return True", "True")
    return True

@allure.step("test_2")
def test_2():
    allure.attach("Return True", "True")
    return True

@allure.step("test_3")
def test_3():
    allure.attach("Return True", "True")
    return True
