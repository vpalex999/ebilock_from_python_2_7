""" Ebilock OK """
import binascii



class Ebilock_OK(object):

    def __init__(self, loop_ok=0, area_ok=0, hub_ok=0, number_ok=1):
        self._loop_ok = loop_ok
        self._area_ok = area_ok
        self._hub_ok = hub_ok
        self._number_ok = number_ok
        self._address_ok = self._code_address_ok()

    @classmethod
    def from_address_ok(cls, address_ok):
        if len(address_ok) == 4:
            loop = int(address_ok[0], 16)
            area = int(address_ok[1], 16)
            hub = int(address_ok[2], 16)
            number = int(address_ok[3], 16)
            if area & 1 != 0:
                print("Invalid configure AREA OK!")
                return False
            elif number & 1 != 1:
                print("Invalid configure Number OK!")
                return False
            else:
                area = area >> 1
                number = number >> 1
                return cls(loop, area, hub, number)



    def _code_address_ok(self):
        status = False
        offset_by = 12
        address_ok = ""
        result = self._loop_ok << 4
        temp = self._area_ok << 1
        result = result | temp
        address_ok = address_ok + "{:02x}".format(int(hex(result), 16))
        result = 0
        temp = self._hub_ok << 4
        result = result | temp
        temp = self._number_ok << 1
        temp = temp | 1
        result = result | temp
        address_ok = address_ok + "{:02x}".format(int(hex(result), 16))
        return address_ok
       
    def show_ok(self):
        print("loop: {}, area: {}, hub {}, number: {}, address: {}".format(self._loop_ok,\
              self._area_ok, self._hub_ok, self._number_ok, self._address_ok))
        

    
ok = Ebilock_OK(3,1,5,3)
ok.show_ok()

ok1 = Ebilock_OK.from_address_ok("3257")
ok1.show_ok()


