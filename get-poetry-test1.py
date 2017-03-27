# This is the Twisted Get Poetry Now! client, version 1.0.

# NOTE: This should not be used as the basis for production code.
# It uses low-level Twisted APIs as a learning exercise.
import binascii
import datetime, errno, optparse, socket
from sources.ebilockcmain import Edilock as eb
from sources.hdlc import read_hdlc

from twisted.internet import main


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, Twisted version 1.0.
Run it like this:

  python get-poetry.py port1 port2 port3 ...

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-client-1/get-poetry.py 10001 10002 10003

to grab poetry from servers on ports 10001, 10002, and 10003.

Of course, there need to be servers listening on those ports
for that to work.
"""

    parser = optparse.OptionParser(usage)

    _, addresses = parser.parse_args()

    if not addresses:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return host, int(port)

    return map(parse_address, addresses)


class PoetrySocket(object):

    #orders = []

    def __init__(self, orders):
        self.orders = orders
        #self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('192.168.101.100',4017))
        self.sock.setblocking(0)

        # tell the Twisted reactor to monitor this socket for reading
        from twisted.internet import reactor
        reactor.addReader(self)

    def fileno(self):
        try:
            return self.sock.fileno()
        except socket.error:
            return -1

    def connectionLost(self, reason):
        self.sock.close()

        # stop monitoring this socket
        from twisted.internet import reactor
        reactor.removeReader(self)

        # see if there are any poetry sockets left
        for reader in reactor.getReaders():
            if isinstance(reader, PoetrySocket):
                return

        reactor.stop() # no more poetry

    def doRead(self):
        #bytes = '22'
        bytes = ''

        #while True:
        #    try:
        #        bytesread = self.sock.recv(1024)
        #        if not bytesread:
        #            break
        #        else:
        #            self.orders.append(bytesread)
                    #test = []
                    #for order in self.orders:
                    #for item in bytesread:
                    #    test.append(binascii.hexlify(item))
                    #print("-"*10)
                    #print len(bytesread)
                    #print test
                    #test1 = ' '.join(test[:])
                    #print(test1)
                    #test2 = binascii.a2b_hex(binascii.hexlify(item))
                    #print(test2)
         #           print(eb.from_hdlc(read_hdlc(bytesread)).check_telegramm())

                    
          #          if len(self.orders) == 1000:
           #             bytes = None
           # except socket.error, e:
           #     if e.args[0] == errno.EWOULDBLOCK:
           #         break
           #     return main.CONNECTION_LOST

        try:
            bytesread = self.sock.recv(1024)
            if bytesread:
                bytes = bytesread
        except socket.error, e:
            if not e.args[0] == errno.EWOULDBLOCK:
                return main.CONNECTION_LOST

        if not bytes:
            print 'Task finished'
            return main.CONNECTION_DONE
        else:
            print(eb.from_hdlc(read_hdlc(bytesread)).check_telegramm())

        #self.poem += bytes

    def logPrefix(self):
        return 'poetry'

    def format_addr(self):
        #host, port = self.address
        return '%s:%s' % ('127.0.0.1', 4016)


def poetry_main():
    #addresses = parse_args()
    orders = []
    start = datetime.datetime.now()

    socket = PoetrySocket(orders)

    from twisted.internet import reactor
    reactor.run()

    elapsed = datetime.datetime.now() - start

    
pass



if __name__ == '__main__':
    poetry_main()
