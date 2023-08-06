# pylint: skip-file
from unimatrix.ext import crypto
from unimatrix.ext.crypto import algorithms
from unimatrix.ext.crypto.pkcs import RSAPrivateKey

from ..signature import JOSESignature
from .const import RSA_PRIVATE_KEY


class HMACSigner(crypto.Signer):
    signature_class = JOSESignature
    algorithm = algorithms.HMACSHA256
    key = crypto.get_secret_key()

    async def sign(self, buf, *args, **kwargs):
        return await self.algorithm.sign(self.key, buf)


class RSASigner(crypto.Signer):
    signature_class = JOSESignature
    algorithm = algorithms.RSAPKCS1v15SHA256
    key = RSAPrivateKey({'path': RSA_PRIVATE_KEY}, keyid='foo')

    async def sign(self, buf, *args, **kwargs):
        return await self.algorithm.sign(self.key, buf)
