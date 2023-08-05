# pylint: skip-file
import json
import unittest

from ..header import JOSEHeader
from ..exceptions import UnsupportedAlgorithm
from ..exceptions import UnsupportedEncryptionAlgorithm
from ..utils import base64url_encode


class JOSEHeaderTestCase(unittest.TestCase):

    def test_kid_returns_none_if_not_provided(self):
        h = base64url_encode(json.dumps({'alg': 'HS256'}).encode())
        j = JOSEHeader.parse(h)
        self.assertEqual(j.kid, None)

    def test_kid_returns_value_if_provided(self):
        h = base64url_encode(json.dumps({'alg': 'HS256', 'kid': 1}).encode())
        j = JOSEHeader.parse(h)
        self.assertEqual(j.kid, 1)

    def test_unsupported_alg_is_rejected(self):
        with self.assertRaises(UnsupportedAlgorithm):
            h = base64url_encode(json.dumps({'alg': 'foo'}).encode())
            JOSEHeader.parse(h)

    def test_unsupported_alg_enc_is_rejected(self):
        with self.assertRaises(UnsupportedEncryptionAlgorithm):
            h = base64url_encode(json.dumps({'alg': 'foo', 'enc': 'A256GCM'}).encode())
            JOSEHeader.parse(h)

    def test_unsupported_enc_is_rejected(self):
        with self.assertRaises(UnsupportedEncryptionAlgorithm):
            h = base64url_encode(json.dumps({'alg': 'A256KW', 'enc': 'foo'}).encode())
            JOSEHeader.parse(h)
