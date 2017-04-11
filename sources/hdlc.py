""" Read HDLC """
import binascii

def read_hdlc(hdlc):

    DLE = '10'
    STX = '02'
    ETX = '83'
    telegramm = []
    #for item in hdlc:
    #    telegramm.append("{:02x}".format(int(item), 16).upper())
    #print(hdlc)
    for item in hdlc:
        telegramm.append("{:02x}".format(int(binascii.hexlify(item), 16)).upper())
    if len(hdlc) >= 2:
        t0 = telegramm[0]
        t1 = telegramm[1]
        t2 = telegramm[len(telegramm)-2]
        t3 = telegramm[len(telegramm)-1]
        if t0 == DLE and t1 == STX:
            cnt = 0
            tmptlg = telegramm[2:]
            for i in range(len(tmptlg)):
                if tmptlg[i] == DLE and tmptlg[i+1] == ETX:
                    return hdlc[2:i+2]
        else:
            print("wrong format hdlc: {}".format(telegramm))
            return None
    else:
        print("wrong format hdlc: {}".format(telegramm))
        return None

def create_hdlc(telegramm):
    DLE = hex(16)
    STX = hex(2)
    ETX = hex(131)
    temp = telegramm[:]
    temp.insert(0, DLE)
    temp.insert(1, STX)
    temp.append(DLE)
    temp.append(ETX)
    #return bytes([int(temp[x], 16) for x in range(len(temp))])
    return ''.join(([binascii.unhexlify("{:02x}".format(int(temp[x], 16))) for x in range(len(temp))]))
    #eturn '\\'.join(temp[:])