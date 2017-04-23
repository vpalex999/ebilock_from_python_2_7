""" Work orders """
import threading
import time
import datetime
from twisted.internet import defer


class WorkFlow(object):

    count = 0

    def __init__(self, sys_data):

        self.sys_data = sys_data
        self.count += 1
        # print("count wf: {}".format(self.count))
        # self.sys_data_old = sys_data_old

    def check_err_first_stage(self):
        if self.sys_data["ORDER_CODE_ALARM"] is None:
            return True
        elif self.sys_data["ORDER_CODE_ALARM"] == 10 or\
            self.sys_data["ORDER_CODE_ALARM"] == 11 or\
            self.sys_data["ORDER_CODE_ALARM"] == 12 or\
            self.sys_data["ORDER_CODE_ALARM"] == 21 or\
            self.sys_data["ORDER_CODE_ALARM"] == 22 or\
            self.sys_data["ORDER_CODE_ALARM"] == 23 or\
            self.sys_data["ORDER_CODE_ALARM"] == 24 or\
            self.sys_data["ORDER_CODE_ALARM"] == 25 or\
            self.sys_data["ORDER_CODE_ALARM"] == 26 or\
                self.sys_data["ORDER_CODE_ALARM"] == 51:
                    return False
        else:
            return True

    def check_err_second_stage(self):
        #print("into secong stage")
        status = True
        try:
            if self.sys_data["ORDER_CODE_ALARM"] == 30 or\
                    self.sys_data["ORDER_CODE_ALARM"] == 31 or\
                    self.sys_data["ORDER_CODE_ALARM"] == 32 or\
                    self.sys_data["ORDER_CODE_ALARM"] == 33:
                        status = False

            for x in self.sys_data["OK"]:
                _ok = self.sys_data["OK"][x]
                if _ok["CODE_ALARM"] is None:
                    continue
                else:
                    if _ok["CODE_ALARM"] == 33 or\
                       _ok["CODE_ALARM"] == 35 or\
                       _ok["CODE_ALARM"] == 36 or\
                       _ok["CODE_ALARM"] == 37 or\
                       _ok["CODE_ALARM"] == 38 or\
                       _ok["CODE_ALARM"] == 39 or\
                            _ok["CODE_ALARM"] == 40:
                            _ok["RETURN_OK"] = 110
                            status = False
            if status:
                self.sys_data["Lost_Connect"] = False
            else:
                self.sys_data["Lost_Connect"] = True
            return status
        except:
            print("'Problem with check_err_second_stage'")
            return False

    # def checking_address_ok(self):
    #     status = True
    #     address_ok = None
    #     if status:
    #         offset_by = 12
    #         result = self.sys_data_old["LOOP_OK"] << 4
    #         temp = self.sys_data_old["AREA_OK"] << 1
    #         result = result | temp
    #         address_ok = "{:2x}".format(int(hex(result), 16))
    #         result = 0
    #         temp = self.sys_data_old["HUB_OK"] << 4
    #         result = result | temp
    #         temp = int(self.sys_data_old["NUMBER_OK"]) << 1
    #         temp = temp | 1
    #         result = result | temp
    #         address_ok = address_ok + "{:2x}".format(int(hex(result), 16))
    #         if address_ok:
    #             self.sys_data_old["ADDRESS_OK"] = address_ok
    #         else:
    #             status = False
    #     return status

    # def checking_number_ok(self):
    #     """ Checking the OK number """
    #     status = False
    #     # print(self.sys_data_old)
    #     if self.sys_data["ORDER"]["CODE_ALARM"] == 6 or\
    #         self.sys_data["ORDER"]["CODE_ALARM"] == 7:
    #         status = False
    #     else:
    #         for ok in self.sys_data["OK"]:
    #             _ok = self.sys_data["OK"][ok]
    #             if _ok["ADDRESS_OK"] == self.sys_data["ORDER"]["ADDRESS_OK"]:
    #                 status = True
    #                 print("Address receved OK: {}".format(self.sys_data["ORDER"]["ADDRESS_OK"]))
    #     return status

    def check_count_ok(self):
        """ check counters good Telegram """
        status = False
        #print("into_check_count")
        if self.check_err_second_stage():
            #print("second stage OK")
            if self.sys_data["FIRST_START"]:
                self.sys_data["FIRST_START"] = False
                self.sys_data["Count_A"] = self.sys_data["ORDER_Count_A"]
                self.sys_data["Count_B"] = self.sys_data["ORDER_Count_B"]
                status = True
                print("First Start!!!")
            else:
                order_a = self.sys_data["ORDER_Count_A"]
                order_b = self.sys_data["ORDER_Count_B"]
                global_a = self.sys_data["Count_A"]
                global_b = self.sys_data["Count_B"]
                if (order_a) - (global_a) <= 2 and (global_b) - (order_b) <= 2:
                    self.sys_data["Count_A"] = order_a
                    self.sys_data["Count_B"] = order_b
                    status = True
        return status

    def switching_to_work(self):
        """system to switch to the operating mode"""
        self.sys_data["Err_Count"] = 0
        self.sys_data["Timer_status"] = False
        self.sys_data["System_Status"] = "WORK"
        # for OK:
        for x in self.sys_data["OK"]:
            _ok = self.sys_data["OK"][x]
            if _ok["CODE_ALARM"] is None:
                _ok["Err_Count"] = 0
                _ok["Timer_status"] = False
                _ok["STATUS_OK"] = "WORK"
            else:
                _ok["Timer_status"] = True
                _ok["Err_Count"] += 1
                _ok["RETURN_OK"] = 100

    def increase_count(self):
        count_a = self.sys_data["Count_A"]
        count_b = self.sys_data["Count_B"]
        if count_a == 254 and count_b == 1:
            self.sys_data["Count_A"] = 1
            self.sys_data["Count_B"] = 254
        else:
            self.sys_data["Count_A"] = self.sys_data["Count_A"] + 1
            self.sys_data["Count_B"] = self.sys_data["Count_B"] - 1

    def work_order(self):
            status = 100
            #if not self.checking_number_ok():
            #    status = 50
            # print("Order: {}".format(sys_data))
            # if not self.checking_number_ok_old():
                # status = 50
            if self.sys_data["ORDER_CODE_ALARM"] == 80:
                status = self.sys_data["ORDER_CODE_ALARM"]  # return send status    
            # elif self.sys_data_old["order"]["DESC_ALARM"] == "This send status":
            #    status = self.sys_data_old["order"]["CODE_ALARM"]  # return send status
            else:
                if self.check_err_first_stage():
                    # print("first stage")
                    if self.check_count_ok():
                        # print("check_count_OK")
                        if self.sys_data["ORDER_CODE_ALARM"] is None:
                            # print(self.sys_data_old["order"]["DESC_ALARM"])
                            self.switching_to_work()
                            status = 0
                        else:  # status_order not OK
                            self.sys_data["Timer_status"] = True
                            self.sys_data["Err_Count"] += 1
                            # return 100
                    else:  # not self.check_count_ok()
                        # print("Lost Communication\nTransfer status with old counters and Increase the counter")
                        # Increase by 1
                        status = 110
                        # self.increase_count()
                        # print("Increase count A/B: {}, {}\n".format(self.sys_data_old["Count_A"], self.sys_data_old["Count_B"]))
                else:  # not check_err_first_stage
                    status = 50
            return status










