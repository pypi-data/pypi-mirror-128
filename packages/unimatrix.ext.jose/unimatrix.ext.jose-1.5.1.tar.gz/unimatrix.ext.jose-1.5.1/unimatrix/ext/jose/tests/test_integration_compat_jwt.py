# pylint: skip-file
import asyncio
import os
import unittest

import jwt
from unimatrix.ext import crypto
from unimatrix.ext.crypto import algorithms
from unimatrix.ext.crypto import pkcs

from .. import JOSEHeader
from .. import JSONWebSignature
from .. import JSONWebToken
from ..algorithms import ALGORITHM_MAPPING


class HMACSigner(crypto.Signer):
    algorithm = None

    def __init__(self, secret, alg):
        self.algorithm = alg
        self.key = self.get_key(secret)

    def get_key(self, secret):
        return crypto.SecretKey({'secret': secret})

    async def sign(self, buf, *args, **kwargs):
        return await self.algorithm.sign(self.key, buf)


class RSASigner(HMACSigner):

    def get_key(self, secret):
        return pkcs.RSAPrivateKey({
            'path': os.path.join(os.path.dirname(__file__), 'key.rsa')
        })


class HMACSHA256PyJWTCompatibilityTestCase(unittest.TestCase):
    signer_class = HMACSigner
    algorithm = algorithms.HMACSHA256

    def setUp(self):
        self.key = b'Hello world!'
        self.header = JOSEHeader()
        self.jws = JSONWebSignature(self.header, JSONWebToken({'iss': "queen"}))
        self.signer = self.signer_class(self.key, self.algorithm)

    def get_key(self):
        return self.key

    def test_sign_symmetric(self):
        asyncio.run(self.jws.sign(self.signer))
        jwt.decode(bytes(self.jws), self.get_key(),
            algorithms=[ALGORITHM_MAPPING[self.algorithm]])


class HMACSHA384PyJWTCompatibilityTestCase(HMACSHA256PyJWTCompatibilityTestCase):
    algorithm = algorithms.HMACSHA384


class HMACSHA512PyJWTCompatibilityTestCase(HMACSHA256PyJWTCompatibilityTestCase):
    algorithm = algorithms.HMACSHA512


class RSAPKCS1v15SHA256PyJWTCompatibilityTestCase(HMACSHA256PyJWTCompatibilityTestCase):
    algorithm = algorithms.RSAPKCS1v15SHA256
    signer_class = RSASigner

    def get_key(self):
        return open(os.path.join(os.path.dirname(__file__), 'pub.rsa'), 'rb').read()


class RSAPKCS1v15SHA384PyJWTCompatibilityTestCase(RSAPKCS1v15SHA256PyJWTCompatibilityTestCase):
    algorithm = algorithms.RSAPKCS1v15SHA384


class RSAPKCS1v15SHA512PyJWTCompatibilityTestCase(RSAPKCS1v15SHA256PyJWTCompatibilityTestCase):
    algorithm = algorithms.RSAPKCS1v15SHA512
