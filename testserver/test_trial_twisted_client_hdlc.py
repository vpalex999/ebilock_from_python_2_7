from twisted.internet.defer import Deferred
from twisted.internet.error import ConnectError
from twisted.internet.protocol import ClientFactory, ServerFactory, Protocol
from twisted.trial.unittest import TestCase
from twisted.python import log
import unittest
import sys
import os
import binascii


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from sources.hdlc import hdlc_work
from data_server import *
# Normally we would import the classes we want to test.
# But to make the examples self-contained, we're just
# copying them here, with a few modifications.

skipped = False


class EhaServerProtocol(Protocol):

    def connectionMade(self):
        pass
        # self.transport.write(self.factory.hdlc)
        # self.transport.loseConnection()

    def dataReceived(self, data):
        # print("receive server data: {}".format(str(data, "utf-8")))
        # name_hdlc = int(bytes.hex(data), 16)
        # if number_test == " ":
        typedata = self.factory.hdlc_dict[str(data, "utf-8")]["test"]
        # print("data1: {}".format(type(typedata)))
        if isinstance(typedata, (list)):
            for data in typedata:
                # print("data2: {}".format(data))
                self.transport.write(data)
        else:
            self.transport.write(self.factory.hdlc_dict[str(data, "utf-8")]["test"])
        self.transport.loseConnection()


class EhaServerFactory(ServerFactory):

    protocol = EhaServerProtocol

    def __init__(self, hdlc_dict):
        self.hdlc_dict = hdlc_dict


class EhaClientProtocol(Protocol):

    buffers = bytearray()

    def connectionMade(self):
        # print("send number tests: {}".format(self.factory.name_hdlc))
        self.transport.write(self.factory.name_hdlc)

    def dataReceived(self, data):
        log.msg("data Received: {}".format(data))
        # print("typedata: {}".format(data))
        work_data = hdlc_work(data, self.buffers)
        if work_data is False:
            self.OrderReceived(work_data)
            self.transport.loseConnection()
            return
        work_data = hdlc_work(data, self.buffers)
        if work_data:
        # print("work data: {}".format(work_data))
            log.msg("work_data: {}".format(data))
            self.OrderReceived(work_data)
            self.transport.loseConnection()

    def connectionLost(self, reason):
        self.OrderReceived(self.buffers)

    def OrderReceived(self, work_data):
        self.factory.order_finished(work_data)


class EhaClientFactory(ClientFactory):

    protocol = EhaClientProtocol

    def __init__(self, name_hdlc):
        self.deferred = Deferred()
        self.name_hdlc = name_hdlc

    def order_finished(self, work_data):
        log.msg("order_finished")
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback(work_data)
            log.msg("order_finished d: {}".format(d))

    def clientConnectionFailed(self, connector, reason):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.errback(reason)


def get_order(host, port, number_test):
    # print("get order tests: {}".format(number_test))
    from twisted.internet import reactor
    factory = EhaClientFactory(number_test)
    reactor.connectTCP(host, port, factory)
    return factory.deferred


class EhaTestCase(TestCase):

    def setUp(self):
        self.port1 = 10000
        self.port2 = None
        self.host = "127.0.0.1"
        factory = EhaServerFactory(hdlc_dict)
        from twisted.internet import reactor
        self.port = reactor.listenTCP(self.port1, factory, interface=self.host)
        # self.portnum = self.port.getHost().port

    def tearDown(self):
        port, self.port = self.port, None
        return port.stopListening()

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_ok(self):
        """The correct hdlc order is returned by decode hdlc order."""
        name_test = "hdlc_ok"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_start_line_10_10(self):
        """The correct hdlc order with 10_10 beginning of a line is returned correct order by decode hdlc."""
        name_test = "hdlc_start_10_10"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_middle_line_10_10(self):
        """The correct hdlc order with 10_10 middle of a line is returned correct order by decode hdlc."""
        name_test = "hdlc_middle_10_10"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_end_line_10_10(self):
        """The correct hdlc order with 10_10 End of a line is returned correct order by decode hdlc."""
        name_test = "hdlc_end_10_10"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_start_10_10_10_odd(self):
        """The incorrect hdlc order with odd 10_10_10 beginning of a line is returned False."""
        name_test = "hdlc_start_10_10_10_odd"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_middle_10_10_10_odd(self):
        """The incorrect hdlc order with odd 10_10_10 middle of a line is returned False."""
        name_test = "hdlc_middle_10_10_10_odd"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_end_10_10_10_odd(self):
        """The incorrect hdlc order with odd 10_10_10 End of a line is returned False."""
        name_test = "hdlc_end_10_10_10_odd"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_start_10_10_10_10(self):
        """The incorrect hdlc order with even 10_10_10_10 beginning of a line is returned False."""
        name_test = "hdlc_start_10_10_10_10_even"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_middle_10_10_10_10(self):
        """The incorrect hdlc order with even 10_10_10_10 middle of a line is returned False."""
        name_test = "hdlc_midle_10_10_10_10_even"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_end_10_10_10_10(self):
        """The incorrect hdlc order with even 10_10_10_10 End of a line is returned False."""
        name_test = "hdlc_end_10_10_10_10_even"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_start_garbage(self):
        """The correct hdlc order with garbage bytes beginning of a line."""
        name_test = "hdlc_start_garbage"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_end_garbage(self):
        """The correct hdlc order with garbage bytes End of a line."""
        name_test = "hdlc_end_garbage"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    @unittest.skipIf(skipped, "")
    def test_trial_client_hdlc_buffers(self):
        """The correct hdlc order to return parts by decode hdlc order."""
        name_test = "test_buffers"
        d = get_order('127.0.0.1', 10000, bytearray(name_test, 'utf-8'))

        def got_opder(work_data):
            log.msg("got_order: {}".format(work_data))
            self.assertEquals(hdlc_dict[name_test]["result"], work_data)

        d.addCallback(got_opder)
        log.msg("d.addCallback(got_opder): {}".format(d))
        return d

    # def test_failure(self):
    #     """The correct failure is returned by get_order when
    #     connecting to a port with no server."""
    #     d = get_order('127.0.0.1', 0)
    #     return self.assertFailure(d, ConnectError)
