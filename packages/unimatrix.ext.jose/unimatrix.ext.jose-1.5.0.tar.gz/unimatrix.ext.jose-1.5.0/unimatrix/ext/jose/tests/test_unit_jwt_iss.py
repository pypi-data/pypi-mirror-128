# pylint: skip-file
import unittest

from ..jwt import JSONWebToken


class JSONWebTokenTestCase(unittest.TestCase):
    iss = 'foo'

    def test_verify_valid_issuer_string(self):
        jwt = JSONWebToken({'iss': self.iss})
        self.assertTrue(jwt.verify_issuer(self.iss))

    def test_verify_valid_issuer_list(self):
        jwt = JSONWebToken({'iss': self.iss})
        self.assertTrue(jwt.verify_issuer([self.iss]))

    def test_verify_invalid_returns_false(self):
        jwt = JSONWebToken({'iss': self.iss})
        self.assertFalse(jwt.verify_issuer([self.iss + 'bar'], False))

    def test_verify_invalid_returns_false(self):
        jwt = JSONWebToken({'iss': self.iss})
        self.assertFalse(jwt.verify_issuer([self.iss + 'bar'], False))

    def test_verify_invalid_raises(self):
        jwt = JSONWebToken({'iss': self.iss})
        with self.assertRaises(jwt.InvalidIssuer):
            jwt.verify_issuer([self.iss + 'bar'])

    def test_verify_invalid_no_iss_raises(self):
        jwt = JSONWebToken({})
        with self.assertRaises(jwt.InvalidIssuer):
            jwt.verify_issuer([self.iss + 'bar'])
