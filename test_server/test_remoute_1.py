from remote_1 import RemoteCalculationFactory
from twisted.trial import unittest
from twisted.test import proto_helpers
import binascii


class RemoteCalculationTestCase(unittest.TestCase):
    def setUp(self):
        factory = RemoteCalculationFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 1000))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def _test(self, operation, a, b, expected):
        self.proto.lineReceived('%s %d %d' % (operation, a, b))
        self.assertEqual(int(self.tr.value()), expected)

    def test_add(self):
        return self._test('add', 7, 6, 13)

    def test_subtract(self):
        return self._test('subtract', 82, 78, 4)

    def test_multiply(self):
        return self._test('multiply', 2, 8, 16)

    def test_divide(self):
        return self._test('divide', 14, 3, 4)
