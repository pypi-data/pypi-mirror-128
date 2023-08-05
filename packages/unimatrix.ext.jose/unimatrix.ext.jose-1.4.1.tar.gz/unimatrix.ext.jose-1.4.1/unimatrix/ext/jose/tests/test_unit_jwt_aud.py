# pylint: skip-file
import unittest

from ..jwt import JSONWebToken


class JSONWebTokenTestCase(unittest.TestCase):
    aud = 'foo'

    def test_verify_valid_audience_string(self):
        jwt = JSONWebToken({'aud': self.aud})
        self.assertTrue(jwt.verify_audience(self.aud))

    def test_verify_valid_audience_list(self):
        jwt = JSONWebToken({'aud': self.aud})
        self.assertTrue(jwt.verify_audience([self.aud]))

    def test_verify_valid_audience_list_list(self):
        jwt = JSONWebToken({'aud': [self.aud]})
        self.assertTrue(jwt.verify_audience([self.aud]))

    def test_verify_invalid_returns_false(self):
        jwt = JSONWebToken({'aud': self.aud})
        self.assertFalse(jwt.verify_audience([self.aud + 'bar'], False))

    def test_verify_invalid_returns_false(self):
        jwt = JSONWebToken({'aud': self.aud})
        self.assertFalse(jwt.verify_audience([self.aud + 'bar'], False))

    def test_verify_invalid_raises(self):
        jwt = JSONWebToken({'aud': self.aud})
        with self.assertRaises(jwt.InvalidAudience):
            jwt.verify_audience([self.aud + 'bar'])

    def test_verify_invalid_no_aud_raises(self):
        jwt = JSONWebToken({})
        with self.assertRaises(jwt.InvalidAudience):
            jwt.verify_audience([self.aud + 'bar'])

    def test_invalid_aud_raises_int(self):
        jwt = JSONWebToken({'aud': 1})
        with self.assertRaises(jwt.MalformedToken):
            self.assertNotEqual(jwt.aud, 1)

    def test_invalid_aud_raises_dict(self):
        jwt = JSONWebToken({'aud': {'foo': 1}})
        with self.assertRaises(jwt.MalformedToken):
            self.assertNotEqual(jwt.aud, {})

    def test_invalid_aud_raises_float(self):
        jwt = JSONWebToken({'aud': 0.1})
        with self.assertRaises(jwt.MalformedToken):
            self.assertNotEqual(jwt.aud, 0.1)
