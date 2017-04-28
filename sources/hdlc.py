""" Read HDLC """
# import binascii
import struct

#     DLE = '10'
#     STX = '02'
#     ETX = '83'


def hdlc_work(hdlc, buffer=None):
    start = (16, 2)
    end = (16, 131)
    middle = (16, 16)
    start_order = []
    middle_order = []
    status = False
    return_order = bytearray()

    # print("\nreceive hdlc: {}".format(hdlc))

    def _check_hdlc(hdlc):
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
                            start_order = start_order[:x+2]
                            status = True
                            break
                        else:
                            status = False
            # find duble combination '0x10' label and delete it
            if status:
                middle_order = start_order[2:-2]
                for x in range(len(middle_order)):
                    if x == len(middle_order)-1:
                        return_order.append(middle_order[x])
                        break
                    middle_byte = struct.unpack('>BB', middle_order[x:x+2])
                    if middle_byte == middle:
                        continue
                    else:
                        return_order.append(middle_order[x])
            # print(start_order)
            if status:
                return return_order
        return status

    if buffer is None:
        buffer = bytearray()

    work_order = _check_hdlc(hdlc)

    if work_order:
        return work_order
    else:
        [buffer.append(i) for i in hdlc]
        work_order = _check_hdlc(buffer)
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