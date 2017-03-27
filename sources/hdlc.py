""" Read HDLC """
import binascii

def read_hdlc(hdlc):

    DLE = '10'
    STX = '02'
    ETX = '83'
    telegramm = []
    #for item in hdlc:
    #    telegramm.append("{:02x}".format(int(item), 16).upper())
    for item in hdlc:
        telegramm.append("{:02x}".format(int(binascii.hexlify(item), 16)).upper())
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
        return None

