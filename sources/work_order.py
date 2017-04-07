""" Work orders """
import threading
import time
import datetime
from twisted.internet import defer


class WorkTimer(object):

    def __init__(self, sys_data):
        self.sys_data = sys_data
        self.timer_err = threading.Timer(1.5, self.do_timer_err)
        self.timer_err.start()
        if self.isalive():
            self.sys_data["Timer_status"] = True
            print"Safe timer start!!!"
        #   print("System status: {}".format(self.sys_data["System_Status"]))

    def do_timer_err(self):
        self.switch_to_pass()
        self.sys_data["Timer_status"] = False
        print("Safe timer stop = 1.5sec.")
        print("Safe timer status: {}".format(self.sys_data["Timer_status"]))

    def isalive(self):
        return self.timer_err.is_alive()

    def isstart(self):
        self.timer_err.finished.cle
        if not self.timer_err.is_alive():
            self.timer_err.run()
            print("Safe timer start (RUN)!!!, STATUS: {}".format(self.timer_err.is_alive()))
        return self.timer_err.is_alive()

    def isstop(self):
        if self.timer_err.is_alive():
            self.timer_err.cancel()
            print("Safe timer stop")
        return self.timer_err.is_alive()

    def switch_to_pass(self):
        """ system to switch to the safe mode """
        self.sys_data["System_Status"] = "SAFE"
        #self.sys_data["FIRST_START"] = True
        print("System status: {}".format(self.sys_data["System_Status"]))

    def check_timer(self):
        print("Check timer status: {}".format(self.sys_data["Timer_status"]))
        #print("Check timer: {}".format(self.timer_err.is_alive()))
        if not self.sys_data["Timer_status"] and self.sys_data["System_Status"] == "WORK":
            self.isstart()
        else:
            self.isstop()


class WorkFlow(object):

    def __init__(self, sys_data):

        self.sys_data = sys_data

    def timer_err_start(self):
        print("timer err alive: {}".format(self.work_timer.isalive()))
        if not self.work_timer.isalive():
            self.work_timer.isstart()
        self.sys_data["Timer_status"] = self.work_timer.isalive()
        print("timer err status: {}".format(self.sys_data["Timer_status"]))


    def check_err_first_stage(self):
        if self.sys_data["order"]["CODE_ALARM"] == 10 or\
        self.sys_data["order"]["CODE_ALARM"] == 11 or\
        self.sys_data["order"]["CODE_ALARM"] == 12 or\
        self.sys_data["order"]["CODE_ALARM"] == 21 or\
        self.sys_data["order"]["CODE_ALARM"] == 22 or\
        self.sys_data["order"]["CODE_ALARM"] == 23 or\
        self.sys_data["order"]["CODE_ALARM"] == 51 or\
        self.sys_data["order"]["CODE_ALARM"] == 62 or\
        self.sys_data["order"]["CODE_ALARM"] == 63 or\
        self.sys_data["order"]["CODE_ALARM"] == 64 or\
        self.sys_data["order"]["CODE_ALARM"] == 65 or\
        self.sys_data["order"]["CODE_ALARM"] == 66 or\
        self.sys_data["order"]["CODE_ALARM"] == 81:
            return False
        else:
            return True

    def check_err_second_stage(self):
        #print("into secong stage")
        if self.sys_data["order"]["CODE_ALARM"] == 30 or\
            self.sys_data["order"]["CODE_ALARM"] == 31 or\
            self.sys_data["order"]["CODE_ALARM"] == 32 or\
            self.sys_data["order"]["CODE_ALARM"] == 33 or\
            self.sys_data["order"]["CODE_ALARM"] == 34 or\
            self.sys_data["order"]["CODE_ALARM"] == 35 or\
            self.sys_data["order"]["CODE_ALARM"] == 36 or\
            self.sys_data["order"]["CODE_ALARM"] == 37 or\
            self.sys_data["order"]["CODE_ALARM"] == 38 or\
            self.sys_data["order"]["CODE_ALARM"] == 39 or\
                self.sys_data["order"]["CODE_ALARM"] == 40:
            #print("order alarm: {}, desc: {}".format(self.sys_data["order"]["CODE_ALARM"], self.sys_data["order"]["DESC_ALARM"]))
            self.sys_data["Lost_Connect"] = True
            return False
        else:
            #print("True second stage")
            self.sys_data["Lost_Connect"] = False
            return True

    def checking_number_ok(self):
        """ Checking the OK number """
        # print(self.sys_data)
        tlg_a = self.sys_data["order"]["TLG_A"]
        if self.sys_data["Number_OK"] == tlg_a["NUMBER_OK"]:
            return True
        else:
            print("Number OK {} in not equal to the received {}".format(self.sys_data["Number_OK"], tlg_a["NUMBER_OK"]))
            return False

    def check_count_ok(self):
        """ check counters good Telegram """
        status = False
        #print("into_check_count")
        if self.check_err_second_stage():
            #print("second stage OK")
            if self.sys_data["FIRST_START"]:
                self.sys_data["FIRST_START"] = False
                self.sys_data["Count_A"] = self.sys_data["order"]["PACKET_COUNT_A"]
                self.sys_data["Count_B"] = self.sys_data["order"]["PACKET_COUNT_B"]
                status = True
                print("First Start!!!")
            else:
                order_a = self.sys_data["order"]["PACKET_COUNT_A"]
                order_b = self.sys_data["order"]["PACKET_COUNT_B"]
                global_a = self.sys_data["Count_A"]
                global_b = self.sys_data["Count_B"]
                if (order_a) - (global_a) <= 2 and (global_b) - (order_b) <= 2:
                    self.sys_data["Count_A"] = self.sys_data["order"]["PACKET_COUNT_A"]
                    self.sys_data["Count_B"] = self.sys_data["order"]["PACKET_COUNT_B"]
                    status = True
        return status

    def switching_to_work(self):
        """system to switch to the operating mode"""
        self.sys_data["Err_Count"] = 0
        self.sys_data["Timer_status"] = False
        self.sys_data["System_Status"] = "WORK"

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
        # print("Order: {}".format(sys_data))
        if self.sys_data["order"]["DESC_ALARM"] == "This send status":
            status = self.sys_data["order"]["CODE_ALARM"]  # return send status
        else:
            if self.check_err_first_stage():
                # print("first stage")
                if self.check_count_ok():
                    # print("check_count_OK")
                    if self.sys_data["order"]["CODE_ALARM"] == 0:
                        # print(self.sys_data["order"]["DESC_ALARM"])
                        if self.checking_number_ok():
                            self.switching_to_work()
                            status = 0
                        else:  # not self.checking_number_ok()
                            self.sys_data["Timer_status"] = True
                            self.sys_data["Err_Count"] += 1
                            # return 100    
                    else:  # status_order not OK
                        self.sys_data["Timer_status"] = True
                        self.sys_data["Err_Count"] += 1
                        # return 100
                else:  # not self.check_count_ok()
                    #print("Lost Communication\nTransfer status with old counters and Increase the counter")
                    # Increase by 1
                    status = 110
                    #self.increase_count()
                    #print("Increase count A/B: {}, {}\n".format(self.sys_data["Count_A"], self.sys_data["Count_B"]))
            else:  # not check_err_first_stage
                status = 50

            #print "{} status system: {}, order status: {}, delta time: {}, CountA: {}, CountB: {}, Zone: {}\n".format(time.ctime(), self.sys_data["System_Status"],\
            #        self.sys_data["order"]["DESC_ALARM"], self.sys_data["time_delta"],\
            #         self.sys_data["Count_A"], self.sys_data["Count_B"], self.sys_data["order"]["STATUS_ZONE"])
            # print("Return")
            return status










