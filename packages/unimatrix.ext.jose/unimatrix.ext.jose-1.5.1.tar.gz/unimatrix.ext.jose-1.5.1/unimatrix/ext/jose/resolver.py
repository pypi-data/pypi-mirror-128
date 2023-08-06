"""Declares :class:`JOSEKeyResolver`."""
from unimatrix.ext import crypto

from . import const


class JOSEKeyResolver:
    """Resolves JOSE object to a :class:`~unimatrix.ext.crypto.Key`
    instance, based on the header and payload.
    """

    async def resolve(self, header, payload=None):
        """Resolves a decryption or public key using the header and
        optionally the payload of a JOSE object.
        """
        if header.kid is None:
            return crypto.get_secret_key()
        resolve = self.resolve_private_key\
            if (header['alg'] in const.SYMMETRIC_ALGORITHMS)\
            else self.resolve_public_key
        return await resolve(header, payload=payload)

    async def resolve_public_key(self, header, payload=None):
        return crypto.trust.get(header.kid)

    async def resolve_private_key(self, header, payload=None): # pragma: no cover
        return crypto.chain.get(header.kid)
