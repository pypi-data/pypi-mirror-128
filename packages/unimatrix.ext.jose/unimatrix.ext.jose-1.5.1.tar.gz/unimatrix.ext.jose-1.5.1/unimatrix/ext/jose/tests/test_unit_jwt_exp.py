# pylint: skip-file
import time
import unittest

from ..jwt import JSONWebToken


class JSONWebTokenTestCase(unittest.TestCase):

    def test_verify_no_exp(self):
        jwt = JSONWebToken({})
        self.assertTrue(jwt.verify_expired(time.time()))

    def test_verify_exp_gt_now(self):
        jwt = JSONWebToken({'exp': 1})
        self.assertTrue(jwt.verify_expired(0))

    def test_verify_expired_raises_on_expired(self):
        jwt = JSONWebToken({'exp': 1})
        with self.assertRaises(jwt.Expired):
            jwt.verify_expired()

    def test_verify_expired_returns_false(self):
        jwt = JSONWebToken({'exp': 1})
        self.assertFalse(jwt.verify_expired(raise_exception=False))

    def test_invalid_exp_raises(self):
        jwt = JSONWebToken({'exp': 'a'})
        with self.assertRaises(jwt.MalformedToken):
            self.assertEqual(jwt.exp, None)
