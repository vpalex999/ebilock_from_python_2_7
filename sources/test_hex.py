import binascii


def hex_to_2bytes(size_packet, size_hex=0):
        item = "{:x}".format(int(hex(size_packet), 16))
        if len(item) % 2 != 0:
            item = "0"+item
        item_unhex = bytearray.fromhex(item)
        if size_hex < len(item_unhex):
            size_hex = len(item_unhex)
        mass = [hex(0) for x in xrange(size_hex)]
        for item in item_unhex:
            mass.append(hex(item))
            del mass[0]
        return mass

print(hex_to_2bytes(1232))
print(hex_to_2bytes(12, 2))

