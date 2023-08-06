# pylint: skip-file
import unittest

from ..jwt import JSONWebToken


class JSONWebTokenTestCase(unittest.TestCase):
    scope = 'foo'

    def test_verify_valid_scope_list(self):
        jwt = JSONWebToken({'scope': self.scope})
        self.assertTrue(jwt.verify_scopes([self.scope]))

    def test_verify_valid_scope_list_list(self):
        jwt = JSONWebToken({'scopes': [self.scope]})
        self.assertTrue(jwt.verify_scopes([self.scope]))

    def test_verify_invalid_returns_false(self):
        jwt = JSONWebToken({'scope': self.scope})
        self.assertFalse(jwt.verify_scopes([self.scope + 'bar'], False))

    def test_verify_invalid_returns_false_with_more(self):
        jwt = JSONWebToken({'scope': self.scope})
        self.assertFalse(jwt.verify_scopes([self.scope, 'bar'], False))

    def test_verify_invalid_returns_false(self):
        jwt = JSONWebToken({'scope': self.scope})
        self.assertFalse(jwt.verify_scopes([self.scope + 'bar'], False))

    def test_verify_invalid_raises(self):
        jwt = JSONWebToken({'scope': self.scope})
        with self.assertRaises(jwt.InsufficientScope):
            jwt.verify_scopes([self.scope + 'bar'])

    def test_verify_invalid_no_scope_raises(self):
        jwt = JSONWebToken({})
        with self.assertRaises(jwt.InsufficientScope):
            jwt.verify_scopes([self.scope + 'bar'])

    def test_can_not_have_scope_and_scopes(self):
        jwt = JSONWebToken({'scope': 'foo', 'scopes': ['bar']})
        with self.assertRaises(jwt.MalformedToken):
            jwt.verify_scopes([self.scope])

    def test_scope_must_be_str(self):
        jwt = JSONWebToken({'scope': ['foo']})
        with self.assertRaises(jwt.MalformedToken):
            jwt.verify_scopes([self.scope])

    def test_scopes_must_be_list(self):
        jwt = JSONWebToken({'scopes': 'foo'})
        with self.assertRaises(jwt.MalformedToken):
            jwt.verify_scopes([self.scope])
