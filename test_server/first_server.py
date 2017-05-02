# This is the Twisted Fast Poetry Server, version 1.0

import optparse
import os

from twisted.internet.protocol import ServerFactory, Protocol


def parse_args():
    usage = """usage: %prog [options] poetry-file

This is the Fast Poetry Server, Twisted edition.
Run it like this:

  python fastpoetry.py <path-to-poetry-file>

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-server-1/fastpoetry.py poetry/ecstasy.txt

to serve up John Donne's Ecstasy, which I know you want to do.
"""

    parser = optparse.OptionParser(usage)

    help = "The port to listen on. Default to a random available port."
    parser.add_option('--port1', type='int', help=help)
    parser.add_option('--port2', type='int', help=help)

    help = "The interface to listen on. Default is localhost."
    parser.add_option('--iface', help=help, default='localhost')

    options, args = parser.parse_args()
    print(args)
    # if len(args) != 1:
    #     parser.error('Provide exactly one poetry file.')

    # poetry_file = args[0]

    # if not os.path.exists(args[0]):
    #     parser.error('No such file: %s' % poetry_file)

    return options  # , poetry_file


class PoetryProtocol(Protocol):

    def connectionMade(self):
        print("Detect connect from: {}")
        self.transport.write(self.factory.poem)
        # self.transport.loseConnection()


class PoetryFactory(ServerFactory):

    protocol = PoetryProtocol

    def __init__(self, poem):
        self.poem = poem


def main():
    # options, poetry_file = parse_args()
    options = parse_args()

    poem = b'\x10\x02\x00\x01\x02\x00\x00\x00*\x00\xeb\x14\x00\x1c2W\xe4\xeb\xe4\x1b\xe4\x1b\xe4\x1b\xe4\x1b@\xad2W\xe6\x14\x1b\xe4\x1b\xe4\x1b\xe4\x1b\xe4\xbf(\xe6\x10\x10\x10\x83'

    factory = PoetryFactory(poem)

    from twisted.internet import reactor

    port1 = reactor.listenTCP(options.port1 or 10000, factory, interface=options.iface)
    port2 = reactor.listenTCP(options.port2 or 10001, factory, interface=options.iface)


    print('Serving on {}.'.format(port1.getHost()))
    print('Serving on {}.'.format(port2.getHost()))
    # print('Serving {} on {}.'.format(poetry_file, port1.getHost()))
    # print('Serving {} on {}.'.format(poetry_file, port2.getHost()))

    reactor.run()


if __name__ == '__main__':
    main()
