# pylint: skip-file
import unittest

import unimatrix.lib.test

from unimatrix.ext import jose

from .signer import RSASigner



class KeyIdentifierTestCase(unimatrix.lib.test.AsyncTestCase):

    async def setUp(self):
        self.jwt = await jose.jwt({'sub': 'foo'})
        self.signer = RSASigner()

    async def test_sign_sets_kid_in_header(self):
        sig = await self.jwt.sign(self.signer)
        self.assertEqual(self.jwt.header.kid, self.signer.key.id)

    async def test_parse_sets_kid_in_signature(self):
        sig = await self.jwt.sign(self.signer)
        jws = jose.parse(bytes(self.jwt))
        self.assertEqual(jws.signature.keyid, self.signer.key.id)
