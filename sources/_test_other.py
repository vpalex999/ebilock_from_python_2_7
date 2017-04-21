
system_data = {"OK": {"3257": {"1": 1}, "3259": {"1": 2}}}

ww = system_data["OK"]


#dd = {for ok in system_data["OK"]}


[print("Status OK: {}, {}".format(x, ww[x]["1"])) for x in ww]

pass