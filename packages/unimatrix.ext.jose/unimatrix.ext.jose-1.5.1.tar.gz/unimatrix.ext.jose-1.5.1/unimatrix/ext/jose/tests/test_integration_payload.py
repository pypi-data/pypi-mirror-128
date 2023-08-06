# pylint: skip-file
import asyncio
import unittest
from unittest.mock import AsyncMock

import ioc
from unimatrix.ext import crypto

from unimatrix.ext import jose
from ..decoder import JOSEPayloadDecoder
from ..resolver import JOSEKeyResolver
from .const import RSA_KEY
from .signer import HMACSigner


class PayloadDecodingTestCase(unittest.TestCase):

    def setUp(self):
        self.signer = HMACSigner()
        self.jws = jose.jwt.sync({'sub': 'Foo Bar'}, signer=self.signer)
        ioc.provide('JOSEPayloadDecoder', JOSEPayloadDecoder(), force=True)
        ioc.provide('JOSEKeyResolver', JOSEKeyResolver(), force=True)

    def test_decode_jws_payload(self):
        self.assertTrue(self.jws.is_signed())
        jwt = jose.payload.sync(bytes(self.jws))


class PayloadWithIdentifiedKeyDecodingTestCase(unittest.TestCase):

    def setUp(self):
        # TODO: hack
        RSA_KEY.alias = RSA_KEY.name = None
        public = RSA_KEY.get_public_key()
        public.alias = public.name = None
        crypto.chain.register(RSA_KEY)
        crypto.trust.register(public)
        self.key = crypto.chain.get(RSA_KEY.id)
        self.signer = crypto.get_signer(
            algorithm=crypto.algorithms.RSAPKCS1v15SHA256,
            key=self.key
        )
        self.jws = jose.jwt.sync({'sub': 'Foo Bar'}, signer=self.signer)
        ioc.provide('JOSEPayloadDecoder', JOSEPayloadDecoder(), force=True)
        ioc.provide('JOSEKeyResolver', JOSEKeyResolver(), force=True)

    def tearDown(self):
        crypto.chain.keys.pop(self.key.id, None)
        crypto.trust.keys.pop(self.key.id, None)

    def test_decode_jws_payload(self):
        self.assertNotEqual(self.jws.header.kid, None)
        self.assertEqual(self.jws.header.kid, self.key.id)
        self.assertTrue(self.jws.is_signed())


        jwt = jose.payload.sync(bytes(self.jws))
