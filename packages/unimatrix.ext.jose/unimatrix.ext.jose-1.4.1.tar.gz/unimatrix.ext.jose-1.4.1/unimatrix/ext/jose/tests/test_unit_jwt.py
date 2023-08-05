# pylint: skip-file
import unittest

from ..jwt import JSONWebToken


class JSONWebTokenParsingTestCase(unittest.TestCase):
    aud = 'foo'

    def test_to_and_from_string(self):
        t1 = JSONWebToken({'aud': self.aud})
        enc = str(t1)
        t2 = JSONWebToken.parse(enc)
        self.assertEqual(t1['aud'], t2['aud'])

    def test_to_and_from_bytes(self):
        t1 = JSONWebToken({'aud': self.aud})
        enc = bytes(t1)
        t2 = JSONWebToken.parse(enc)
        self.assertEqual(t1['aud'], t2['aud'])

