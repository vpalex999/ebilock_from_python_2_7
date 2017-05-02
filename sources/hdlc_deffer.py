""" Read HDLC """
# import binascii
from twisted.internet import defer
import struct

#     DLE = '10'
#     STX = '02'
#     ETX = '83'


class SizeHdlcExceeded(Exception): pass
class SizeBufferHdlcExceeded(Exception): pass


def hdlc_start(*args, **kwargs):

    if kwargs[buffers] not in kwargs:
        local_buffer = bytearray()
    else:
        local_buffer = kwargs['buffers']

    size_hdlc = len(["{:02x}".format(int(hex(x), 16)) for x in kwargs['hdlc']])

    if size_hdlc <= 6:
        return {'hdlc': kwargs[hdlc], 'buffers': local_buffer}
    else:
        raise SizeHdlcExceeded(kwargs)

    size_buffer = len(local_buffer)
    if size_buffer <= 6:
        return {'hdlc': kwargs[hdlc], 'buffers': local_buffer}
    else:
        raise SizeBufferHdlcExceeded(local_buffer)



def hdlc_error_size(err):
    if err.check(SizeHdlcExceeded):
        print("The data size is more than 4096 bytes: {}".format(len(err.value.args[0]['hdlc'])))
    if err.check(SizeBufferHdlcExceeded):
        print("The buffer size is more than 4096 bytes: {}".format(len(err.value.args[1][''])))
    return err


d_hdlc = defer.Deferred()
d_hdlc.addCallback(hdlc_start)
d_hdlc.addErrback(hdlc_error_size)

hdlc = {
        'hdlc': b'\x10\x02\x00\x01\x02\x00\x00\x00*\x00\xeb\x14\x00\x1c2W\xe4\xeb\xe4\x1b\xe4\x1b\xe4\x1b\xe4\x1b@\xad2W\xe6\x14\x1b\xe4\x1b\xe4\x1b\xe4\x1b\xe4\xbf(\xe6\x10\x10\x10\x83',
        'hdlc_buffer': bytearray()
}

hdlc_start(hdlc)
# d_hdlc.callback(hdlc)


def hdlc_work(hdlc, buffers=None):
    start = (16, 2)
    end = (16, 131)
    middle = (16, 16)
    start_order = []
    end_order = []
    middle_order = []
    status = False
    return_order = bytearray()
    if buffers is None:
        local_buffer = bytearray()
    else:
        local_buffer = buffers

    size_hdlc = len(["{:02x}".format(int(hex(x), 16)) for x in hdlc])
    if size_hdlc > 4096:
        print("the data size is more than 4096 bytes {}".format(size))
        return False
    
    size_buffer = len(local_buffer)
    if size_buffer > 4096:
        print("the buffer size is more than 4096 bytes {}".format(size))
        local_buffer.clear()
        return False
        
    # count_hdlc = size_hdlc
    pass
    # print("\nreceive hdlc: {}".format(hdlc))

    def _check_hdlc(hdlc, local_buffer):
        status = False
        if len(hdlc) >= 4:
            # find start label
            for x in range(len(hdlc)):
                if x != len(hdlc)-1:
                    start_byte = struct.unpack('>BB', hdlc[x:x+2])
                    if start_byte == start:
                        start_order = hdlc[x:]
                        status = True
                        break
            # find end label
            if status:
                for x in range(len(start_order)):
                    if x != len(start_order)-1:
                        end_byte = struct.unpack('>BB', start_order[x:x+2])
                        if end_byte == end:
                            end_order = start_order[:x+2]
                            status = True
                            break
                        else:
                            status = False
            # find duble combination '0x10\0x10\' label and delete it
            if status:
                middle_order = end_order[2:-2]
                count_10 = ["{:02x}".format(int(hex(x), 16)) for x in middle_order]
                if count_10.count('10') % 2 != 0:
                    local_buffer.clear()
                    print("\nThe line of bytes contains odd number of elements '\\x10', buffer clear()")
                    status = False
                else:
                    i = 0
                    while i < len(middle_order):
                        if i == len(middle_order)-1:
                            return_order.append(middle_order[i])
                            break
                        middle_byte = struct.unpack('>BB', middle_order[i:i+2])
                        if middle_byte == middle:
                            return_order.append(middle_order[i])
                            # return_order += struct.pack('>B', middle_order[i])
                            i += 2
                        else:
                            return_order.append(middle_order[i])
                            i += 1

            # print(start_order)
            if status:
                return return_order
        return status

    

    work_order = _check_hdlc(hdlc, local_buffer)

    if work_order:
        return work_order
    else:
        [local_buffer.append(i) for i in hdlc]
        work_order = _check_hdlc(local_buffer, local_buffer)
        if work_order:
            return work_order
        else:
            return False

#         else:
#             [buffer.append(i) for i in hdlc]
#     else:
#         [buffer.append(i) for i in hdlc]
#     return status


# def read_hdlc(hdlc):
# 
#     DLE = '10'
#     STX = '02'
#     ETX = '83'
#     telegramm = []
#     #for item in hdlc:
#     #    telegramm.append("{:02x}".format(int(item), 16).upper())
#     print(hdlc)
#     for item in hdlc:
#         
#         telegramm.append("{:02x}".format(int(hex(item), 16)).upper())
#     # print(telegramm)
#     if len(hdlc) >= 2:
#         t0 = telegramm[0]
#         t1 = telegramm[1]
#         t2 = telegramm[len(telegramm)-2]
#         t3 = telegramm[len(telegramm)-1]
#         if t0 == DLE and t1 == STX:
#             cnt = 0
#             tmptlg = telegramm[2:]
#             for i in range(len(tmptlg)):
#                 if tmptlg[i] == DLE and tmptlg[i+1] == DLE:
#                     del tmptlg[i]
#                 if tmptlg[i] == DLE and tmptlg[i+1] == ETX:
#                     del tmptlg[i]
#                     del tmptlg[i]
#                     #print("tmptlg: {}".format(tmptlg))
#                     #print("Order HDLC: {}".format(hdlc[2:i+2]))
#                     # for python3-6:
#                     return (bytearray([int(x, 16) for x in tmptlg]))
#                     # for python 2-7:
#                     #return ''.join([binascii.unhexlify(hex(int(tmptlg[x], 16))) for x in range(len(tmptlg))])
#         else:
#             print("wrong format hdlc: {}".format(telegramm))
#             return None
#     else:
#         print("wrong format hdlc: {}".format(telegramm))
#         return None

def create_hdlc(telegramm):
    DLE = hex(16)
    STX = hex(2)
    ETX = hex(131)
    temp = []
    for item in telegramm:
        temp.append(item)
        if item == hex(16):
            temp.append(hex(16))
    temp.insert(0, DLE)
    temp.insert(1, STX)
    temp.append(DLE)
    temp.append(ETX)
    #print("send status hdlc: {}".format(temp))
    # for python 3-6:
    return bytes([int(temp[x], 16) for x in range(len(temp))])
    # for python 2-7:
    # return ''.join(([binascii.unhexlify("{:02x}".format(int(temp[x], 16))) for x in range(len(temp))]))
    #return '\\'.join(temp[:])