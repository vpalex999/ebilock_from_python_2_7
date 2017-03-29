""" Work orders """


sys_data = {}
sys_data1 ={}

def timer_err_start():
        if not timer_err.is_alive():
            timer_err.start()
        print("timer Error START!!!")
        sys_data["Err_timer_status"] = True


def work_timer_err():
        switch_to_pass()
        pass


def check_err_first_stage():
    if sys_data["order"]["CODE_ALARM"] == 10 or\
    sys_data["order"]["CODE_ALARM"] == 11 or\
    sys_data["order"]["CODE_ALARM"] == 12 or\
    sys_data["order"]["CODE_ALARM"] == 21 or\
    sys_data["order"]["CODE_ALARM"] == 22 or\
    sys_data["order"]["CODE_ALARM"] == 23 or\
    sys_data["order"]["CODE_ALARM"] == 51 or\
    sys_data["order"]["CODE_ALARM"] == 62 or\
    sys_data["order"]["CODE_ALARM"] == 63 or\
    sys_data["order"]["CODE_ALARM"] == 64 or\
    sys_data["order"]["CODE_ALARM"] == 65 or\
    sys_data["order"]["CODE_ALARM"] == 66 or\
    sys_data["order"]["CODE_ALARM"] == 81:
        print("The telegram is not taken into account. code: {}, desc: {}".format(sys_data["order"]["CODE_ALARM"], sys_data["order"]["DESC_ALARM"]))
        return False
    else:
        return True


def check_err_second_stage():
        print("into secong stage")
        if sys_data["order"]["CODE_ALARM"] == 31 or\
            sys_data["order"]["CODE_ALARM"] == 32 or\
            sys_data["order"]["CODE_ALARM"] == 33 or\
            sys_data["order"]["CODE_ALARM"] == 34 or\
            sys_data["order"]["CODE_ALARM"] == 35 or\
            sys_data["order"]["CODE_ALARM"] == 36 or\
            sys_data["order"]["CODE_ALARM"] == 37 or\
            sys_data["order"]["CODE_ALARM"] == 38 or\
                sys_data["order"]["CODE_ALARM"] == 39:
            print("order alarm: {}, desc: {}".format(sys_data["order"]["CODE_ALARM"], sys_data["order"]["DESC_ALARM"]))
            return False
        else:
            print("True second stage")
            return True


def checking_number_ok():
        """ Checking the OK number """
        tlg_a = sys_data["order"]["TLG_A"]
        if sys_data["Number_OK"] == tlg_a["NUMBER_OK"]:
            return True
        else:
            print("Number OK {} in not equal to the received {}".format(sys_data["Number_OK"], tlg_a["NUMBER_OK"]))
            return False


def check_count_ok():
        """ check counters good Telegram """
        status = False
        print("into_check_count")
        if check_err_second_stage():
            print("second stage OK")
            if sys_data["FIRST_START"]:
                sys_data["FIRST_START"] = False
                sys_data["Count_A"] = sys_data["order"]["PACKET_COUNT_A"]
                sys_data["Count_B"] = sys_data["order"]["PACKET_COUNT_B"]
                status = True
                print("First Start!!!")
            else:
                order_a = sys_data["order"]["PACKET_COUNT_A"]
                order_b = sys_data["order"]["PACKET_COUNT_B"]
                global_a = sys_data["Count_A"]
                global_b = sys_data["Count_B"]

                if order_a - global_a <= 2 and global_b - order_b <= 2:
                    sys_data["Count_A"] = sys_data["order"]["PACKET_COUNT_A"]
                    sys_data["Count_B"] = sys_data["order"]["PACKET_COUNT_B"]
                    status = True
        return status


def switch_to_pass():
        """ system to switch to the safe mode """
        sys_data["System_Status"] = "SAFE"
        sys_data["FIRST_START"] = True


def switching_to_work():
    """system to switch to the operating mode"""
    sys_data["Err_Count"] = 0
    # timer_error = stop
    sys_data["System_Status"] = "WORK"


def send_status():
    # status = stat(self.system_data)
    print("Send status OK")


def increase_count():
        count_a = sys_data["Count_A"]
        count_b = sys_data["Count_B"]
        if count_a == 254 and count_b == 1:
            sys_data["Count_A"] = 1
            sys_data["Count_B"] = 254
        else:
            sys_data["Count_A"] = sys_data["Count_A"] + 1
            sys_data["Count_B"] = sys_data["Count_B"] - 1


def work_order(system_data, receive_data):
    global sys_data
    sys_data = system_data
    if sys_data["order"]["DESC_ALARM"] == "This send status":
        print("Send status")
    else:
        if check_err_first_stage():
            print("first stage")
            if check_count_ok():
                print("check_count_OK")
                if sys_data["order"]["CODE_ALARM"] == 0:
                    print(sys_data["order"]["DESC_ALARM"])
                    if checking_number_ok():
                        switching_to_work()
                        send_status()
                        print "status system: {0}, order status: {1}, delta time: {2}, CountA: {3}, CountB: {4}\n".format(sys_data["System_Status"],\
                                sys_data["order"]["DESC_ALARM"], receive_data["time_delta"],\
                                    sys_data["Count_A"], sys_data["Count_B"])
                    else:  # not self.checking_number_ok()
                        pass
                else:  # status_order not OK
                    if sys_data["Err_Count"] == 0:
                        timer_err_start()
                    else:
                        pass
                    sys_data["Err_Count"] += 1
            else:  # not self.check_count_ok()
                print("Lost Communication\nTransfer status with old counters and Increase the counter")
                # Increase by 1
                increase_count()
                # self.system_data["Count_A"] = self.system_data["Count_A"] + 1
                # self.system_data["Count_B"] = self.system_data["Count_B"] - 1
                print("Increase count A/B: {}, {}\n".format(sys_data["Count_A"], sys_data["Count_B"]))
                #source_hdlc = ""
                return
                    #
        else:  # not check_err_first_stage
            print("Discard a telegram")

