from twisted.internet import defer, reactor
from twisted.internet.protocol import Protocol, ClientFactory

stat = {
    "status_system": "WORK",
    "status_tumer": False
}



def dodo(stat):
    if stat["status_system"] == "WORK":
        stat["status_system"] = "SAFE"
        stat["status_tumer"] = False
    print"hello!"

d = defer.Deferred()
d.addCallback(dodo)

#d.callback(stat)
reactor.callLater(10, d.callback, stat)
d.cancel()
print("cansel")
reactor.callLater(10, d.callback, stat)

#def start_timer(systems, stat_timer, dodo):
#    if not stat_timer:
#        reactor.callLater(10, dodo)
#        stat_timer = True
#        print("Start timer")
#    else:
#        print("Timer is Run!!!")

#start_timer(status_system, status_tumer, dodo)
#start_timer(status_system, status_tumer, dodo)

reactor.run()


