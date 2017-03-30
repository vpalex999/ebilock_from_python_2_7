""" Work orders """
import threading


class WorkTimer(object):
    def __init__(self, sys_data):
        self.timer_err = threading.Timer(1.5, do_timer_err)
        self.sys_data = sys_data

    def do_timer_err(self):
        self.switch_to_pass()
        self.sys_data["Err_timer_status"] = self.timer_err.is_alive()

    def isalive(self):
        return self.timer_err.is_alive()

    def isstart(self):
        self.timer_err.start()
        return self.timer_err.is_alive()

    def isstop(self):
        self.timer_err.cancel()
        return self.timer_err.is_alive()



class WorkFlow(object):

    def __init__(self, sys_data, work_timer):

        self.sys_data = sys_data
        self.work_timer = work_timer

    def timer_err_start(self):
        print("timer err alive: {}".format(self.work_timer.isalive()))
        if not self.work_timer.isalive():
            self.work_timer.isstart()
        self.sys_data["Err_timer_status"] = self.work_timer.isalive()
        print("timer err status: {}".format(self.sys_data["Err_timer_status"]))

    #def switch_to_pass():
    #    """ system to switch to the safe mode """
    #    sys_data["System_Status"] = "SAFE"
    #    sys_data["FIRST_START"] = True
    #    print("switch to pass. time out!!!")

    def check_err_first_stage(self):
        if sys_data["order"]["CODE_ALARM"] == 10 or\
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
            print("The telegram is not taken into account. code: {}, desc: {}".format(self.sys_data["order"]["CODE_ALARM"], self.sys_data["order"]["DESC_ALARM"]))
            return False
        else:
            return True

    def check_err_second_stage(self):
        print("into secong stage")
        if self.sys_data["order"]["CODE_ALARM"] == 31 or\
            self.sys_data["order"]["CODE_ALARM"] == 32 or\
            self.sys_data["order"]["CODE_ALARM"] == 33 or\
            self.sys_data["order"]["CODE_ALARM"] == 34 or\
            self.sys_data["order"]["CODE_ALARM"] == 35 or\
            self.sys_data["order"]["CODE_ALARM"] == 36 or\
            self.sys_data["order"]["CODE_ALARM"] == 37 or\
            self.sys_data["order"]["CODE_ALARM"] == 38 or\
                self.sys_data["order"]["CODE_ALARM"] == 39:
            print("order alarm: {}, desc: {}".format(self.sys_data["order"]["CODE_ALARM"], self.sys_data["order"]["DESC_ALARM"]))
            return False
        else:
            print("True second stage")
            return True

    def checking_number_ok(self):
        """ Checking the OK number """
        print(self.sys_data)
        tlg_a = self.sys_data["order"]["TLG_A"]
        print("TLG: {}".format(tlg_a["NUMBER_OK"]))
        if self.sys_data["Number_OK"] == tlg_a["NUMBER_OK"]:
            return True
        else:
            print("Number OK {} in not equal to the received {}".format(self.sys_data["Number_OK"], tlg_a["NUMBER_OK"]))
            return False

    def check_count_ok(self):
        """ check counters good Telegram """
        status = False
        print("into_check_count")
        if self.check_err_second_stage():
            print("second stage OK")
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
    if not self.work_timer.isalive():
        self.work_timer.isstop()
    self.sys_data["Err_Count"] = 0
    # timer_error = stop
    self.sys_data["System_Status"] = "WORK"

    def send_status(self):
        # status = stat(self.system_data)
    print("Send status OK")


    def increase_count(self):
        count_a = self.sys_data["Count_A"]
        count_b = self.sys_data["Count_B"]
        if count_a == 254 and count_b == 1:
            self.sys_data["Count_A"] = 1
            self.sys_data["Count_B"] = 254
        else:
            self.sys_data["Count_A"] = sys_data["Count_A"] + 1
            self.sys_data["Count_B"] = sys_data["Count_B"] - 1

    def work_order(self):
        # print("Order: {}".format(sys_data))
        if self.sys_data["order"]["DESC_ALARM"] == "This send status":
            print("Send status")
        else:
            if self.check_err_first_stage():
                print("first stage")
                if self.check_count_ok():
                    print("check_count_OK")
                    if self.sys_data["order"]["CODE_ALARM"] == 0:
                        print(self.sys_data["order"]["DESC_ALARM"])
                        if self.checking_number_ok():
                            self.switching_to_work()
                            self.send_status()
                            #print "status system: {0}, order status: {1}, delta time: {2}, CountA: {3}, CountB: {4}\n".format(sys_data["System_Status"],\
                            #        sys_data["order"]["DESC_ALARM"], receive_data["time_delta"],\
                            #            sys_data["Count_A"], sys_data["Count_B"])
                        else:  # not self.checking_number_ok()
                            pass
                    else:  # status_order not OK
                        if self.sys_data["Err_Count"] == 0:
                            print("Timer_error_start!!!")
                            self.timer_err_start()
                        else:
                            pass
                        self.sys_data["Err_Count"] += 1
                else:  # not self.check_count_ok()
                    print("Lost Communication\nTransfer status with old counters and Increase the counter")
                    # Increase by 1
                    self.increase_count()
                    # self.system_data["Count_A"] = self.system_data["Count_A"] + 1
                    # self.system_data["Count_B"] = self.system_data["Count_B"] - 1
                    print("Increase count A/B: {}, {}\n".format(self.sys_data["Count_A"], self.sys_data["Count_B"]))
                    #source_hdlc = ""
                    #return
                    #
            else:  # not check_err_first_stage
                print("Discard a telegram")
            print "status system: {0}, order status: {1}, delta time: {2}, CountA: {3}, CountB: {4}\n".format(self.sys_data["System_Status"],\
                    self.sys_data["order"]["DESC_ALARM"], self.sys_data["time_delta"],\
                     self.sys_data["Count_A"], self.sys_data["Count_B"])










