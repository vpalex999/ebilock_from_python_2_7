""" Read HDLC """
# import binascii
import struct
import logging
logger_hdlc = logging.getLogger("client_main.hdlc")

#     DLE = '10'
#     STX = '02'
#     ETX = '83'


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


def create_hdlc(telegramm):
    logger_hdlc.debug("start creat_hdlc")
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
    logger_hdlc.info("Create status hdlc(hex): {}".format(temp))
    hdlc = bytes([int(temp[x], 16) for x in range(len(temp))])
    logger_hdlc.debug("Create status hdlc: {}".format(hdlc))
    return hdlc
    # for python 2-7:
    # return ''.join(([binascii.unhexlify("{:02x}".format(int(temp[x], 16))) for x in range(len(temp))]))
    #return '\\'.join(temp[:])