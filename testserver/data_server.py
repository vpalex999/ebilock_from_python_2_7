""" DATA FOR SERVER TEST"""

server_port1 = 10000
server_port2 = 10001

# ========== order hdlc ==========
hdlc_dict = {
    "hdlc_ok":
            {"test": b'\x10\x02\x00\x01\x02\x00\x00\x00*\x10\x83',
             "result": b'\x00\x01\x02\x00\x00\x00*'},
    "hdlc_start_10_10":
            {"test": b'\x10\x02\x10\x10\x00\x01\x02\x00\x00\x00*\x10\x83',
             "result": b'\x10\x00\x01\x02\x00\x00\x00*'},
    "hdlc_middle_10_10":
            {"test": b'\x10\x02\x00\x01\x02\x10\x10\x00\x00\x00*\x10\x83',
             "result": b'\x00\x01\x02\x10\x00\x00\x00*'},
    "hdlc_end_10_10":
            {"test": b'\x10\x02\x00\x01\x02\x00\x00\x00*\x10\x10\x10\x83',
             "result": b'\x00\x01\x02\x00\x00\x00*\x10'},
    "hdlc_start_10_10_10_odd":
            {"test": b'\x10\x02\x10\x10\x10\x00\x01\x02\x00\x00\x00*\x10\x83',
             "result": False},
    "hdlc_middle_10_10_10_odd":
            {"test": b'\x10\x02\x00\x01\x02\x10\x10\x10\x00\x00\x00*\x10\x83',
             "result": False},
    "hdlc_end_10_10_10_odd":
            {"test": b'\x10\x02\x00\x01\x02\x00\x00\x00*\x10\x10\x10\x10\x83',
             "result": False},
    "hdlc_start_10_10_10_10_even":
            {"test": b'\x10\x02\x10\x10\x10\x10\x00\x01\x02\x00\x00\x00*\x10\x83',
             "result": b'\x10\x10\x00\x01\x02\x00\x00\x00*'},
    "hdlc_midle_10_10_10_10_even":
            {"test": b'\x10\x02\x00\x01\x02\x00\x10\x10\x10\x10\x00\x00*\x10\x83',
             "result": b'\x00\x01\x02\x00\x10\x10\x00\x00*'},
    "hdlc_end_10_10_10_10_even":
            {"test": b'\x10\x02\x00\x01\x02\x00\x00\x00*\x10\x10\x10\x10\x10\x83',
             "result": b'\x00\x01\x02\x00\x00\x00*\x10\x10'},
    "test_buffers":
            {"test": [
                      b'\x10',
                      b'\x02\x00\x01\x02',
                      b'\x00\x00\x00*\x00\xeb\x14\x00\x1c2W\xe4\xeb\xe4\x1b\xe4\x1b\xe4\x1b\xe4\x1b@\xad2W\xe6\x14\x1b\xe4\x1b\xe4\x1b\xe4\x1b\xe4\xbf(\xe6\x10\x10\x10\x83\xe6\x10'
                     ],
             "result": b'\x00\x01\x02\x00\x00\x00*\x00\xeb\x14\x00\x1c2W\xe4\xeb\xe4\x1b\xe4\x1b\xe4\x1b\xe4\x1b@\xad2W\xe6\x14\x1b\xe4\x1b\xe4\x1b\xe4\x1b\xe4\xbf(\xe6\x10'},
    "hdlc_start_garbage":
            {"test": b'\x10\x10\x00\x01\x10\x02\x10\x10\x10\x10\x00\x01\x02\x00\x00\x00*\x10\x83',
             "result": b'\x10\x10\x00\x01\x02\x00\x00\x00*'},
    "hdlc_end_garbage":
            {"test": b'\x10\x02\x10\x10\x10\x10\x00\x01\x02\x00\x00\x00*\x10\x83\x10\x10\x00\x01',
             "result": b'\x10\x10\x00\x01\x02\x00\x00\x00*'},
}



