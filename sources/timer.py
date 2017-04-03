from twisted.internet import defer
import threading
import time

d = defer.Deferred()


class TimerStart(threading.Thread):
    
    def __init__(self, todo):
        super().__init__()
        self.interval = 1.5
        self.status = False
        self.todo = todo
    
    def start(self):
        self.run()

    def run(self):
        self.status = True
        print("status: {}".format(self.status))
        print("start run")
        tt = self.interval
        self.status = True
        while True:
            time.sleep(0.01)
            tt -= 0.01
            if tt < 0.01:
                self._inner_stop()
                self.todo()
                break
            if not self.status:
                break
        print("End run")

    def _inner_stop(self):
        self.status = False

    def timer_start(self):
        if not self.status:
            self.status = True
            print("Start timer")
            self.run()

    

t = TimerStart(5)
t.start()
#t.run()
print"jkguiugughjj"


 def __init__(self, sys_data):
        self.sys_data = sys_data
        self.timer_err = Timer(1.5, self.do_timer_err)
        self.timer_err.start()
        if self.isalive():
            print"Safe timer start!!!"
            print("System status: {}".format(self.sys_data["System_Status"]))


    def do_timer_err(self):
        self.switch_to_pass()
        self.sys_data["Err_timer_status"] = False
        print("Safe timer stop = 1.5sec.")
        print("Safe timer status: {}".format(self.sys_data["Err_timer_status"]))

    def isalive(self):
        return self.timer_err.is_alive()

    def isstart(self):
        if not self.timer_err.is_alive():
            self.timer_err.start()
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
        self.sys_data["FIRST_START"] = True
        print("System status: {}".format(self.sys_data["System_Status"]))

    def check_timer(self):
        print("Check timer status: {}".format(self.sys_data["Err_timer_status"]))
        print("Check timer: {}".format(self.timer_err.is_alive()))
        if self.sys_data["Err_timer_status"]:
            self.isstart()
        else:
            self.isstop()

#------------------------------------
class WorkTimer(threading.Thread):
    def __init__(self, switch_to_pass):
        threading.Thread.__init__(self)
        self.interval = 1.5
        self.status = False
        self.switch_to_pass = switch_to_pass
        

    def start(self):
        self.run()

    def run(self):
        self.status = True
        print("status: {}".format(self.status))
        print("start run")
        tt = self.interval
        self.status = True
        while True:
            time.sleep(0.01)
            tt -= 0.01
            if tt < 0.01:
                self._inner_stop()
                self.switch_to_pass()
                break
            if not self.status:
                break
        print("End run")

    def _inner_stop(self):
        self.status = False

    def timer_start(self):
        if not self.status:
            self.status = True
            print("Timer start iner timer")
            self.run()

    def timer_stop(self):
        self.status = False
        print("Timer stop iner timer")
