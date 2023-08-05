# pylint: skip-file
import unittest

from .. import jwk


class JSONWebKeyRSATestCase(unittest.TestCase):
    jwk = {
      "n": "yRdZ6VSfnd8BaBG8pbrDIDRnkMKHW6f7lut9-QzBH94sqT91G1lcMa8a1h3PNmUd_xf3wF86Z8RUU2aY26M8o6UIxPep5acLulvRfvdcEg8pErOA5pqWWTEWxKbbnTTCn0zhs6J2yxo7NToTBWF9r5f8kRU7iUbxfbN4fWHAxgnSYbHGHibQjgkBhc_b5R944kC0BqO1sNdeaJMvTHjkc7X8-RkTejFBdpaE3S-2gY4hsu32OKWIYxt2kKPWQzSrZ1ol9nCGJL6UCtLUFVUqiDEXxZF1AC1y4txem9aNpHEc2M0wzuQZtB4Ew7MAoJJcSFcVm2o5NKG0gMBi17UNPQ",
      "e": "AQAB",
      "kty": "RSA",
      "kid": "noop.rsa",
      "use": "sig"
    }

    def get_json_web_key(self):
        return dict(self.jwk)

    def test_parse(self):
        k = jwk.parse(self.get_json_web_key())

    def test_parse_sets_id(self):
        k = jwk.parse(self.get_json_web_key())
        self.assertEqual(k.id, 'noop.rsa')
