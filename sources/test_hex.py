import binascii
from crc8 import check_crc_8
from crc8 import create_crc_8

# def hex_to_2bytes(size_packet, size_hex=0):
#         item = "{:x}".format(int(hex(size_packet), 16))
#         if len(item) % 2 != 0:
#             item = "0"+item
#         item_unhex = bytearray.fromhex(item)
#         if size_hex < len(item_unhex):
#             size_hex = len(item_unhex)
#         mass = [hex(0) for x in xrange(size_hex)]
#         for item in item_unhex:
#             mass.append(hex(item))
#             del mass[0]
#         return mass
# 
# print(hex_to_2bytes(1232))
# print(hex_to_2bytes(12, 2))
# bb = ""
# tt = ['10', '02', '00', '01', '02', '00', '00', '00', '1A', '00', '9C', '63', '00', '0C', '32', '57', '64', '9C', 'E4', 'A8', '32', '57', '66', '63', '1B', '8E', '76', '53', '10', '83']
# #
# #ascii.unhexlify(x)
# 
# print(bytearray([int(x, 16) for x in tt]))

ww = ['0x32', '0x57', '0x88', '0x55', '0xe8']

ss = create_crc_8(ww)

qq = '01:00:03:00:00:00:2e:00:00:02:32:57:00:1e:32:57:f8:de:00:00:00:00:00:00:00:00:00:00:9e:32:57:fc:21:00:ff:ff:ff:ff:ff:ff:ff:ff:ff:fa:f2:c8'
ok1 = '32 57 f8 00 00 00 00 00 00 00 00 00'
srs_ok1 = check_crc_8(ok1)
zz = "['0x1', '0x0', '0x3', '0x0', '0x0', '0x0', '0x20', '0x0', '0x0', '0x2', '0x32', '0x57', '0x0', '0x10', '0x32', '0x57','0x88', '0xa9', '0x0', '0x55', '0xe8', '0xa6', '0xcd', '0xa8', '0x73', '0xa9', '0xff', '0xaa', '0x17', '0x29', '0x6', '0x44']"
tt = '32 57 88 55 e8'

srs = check_crc_8(tt)

a = '32 57 88 55 e8'
b = '32 57 8c aa 17'
aa = check_crc_8(a)
bb = check_crc_8(b)
pass

