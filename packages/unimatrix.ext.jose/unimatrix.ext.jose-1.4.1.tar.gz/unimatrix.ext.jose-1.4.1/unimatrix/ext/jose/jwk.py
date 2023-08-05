"""Provides an API to serialize and deserialize JSON Web Keys (JWKs)
from and to :class:`~unimatrix.ext.crypto.PublicKey` implementations.
"""
import base64
from typing import Union

from unimatrix.ext.crypto import pkcs
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers


def base64url_decode(input: Union[str, bytes]) -> bytes:
    if isinstance(input, str):
        input = input.encode("ascii")
    rem = len(input) % 4
    if rem > 0:
        input += b"=" * (4 - rem)
    return base64.urlsafe_b64decode(input)


def from_base64url_uint(val: Union[str, bytes]) -> int:
    if isinstance(val, str):
        val = val.encode("ascii")
    data = base64url_decode(val)
    return int.from_bytes(data, byteorder="big")


def parse_rsa(obj):
    """Parse a :class:`~unimatrix.ext.crypto.pkcs.PEMPublicKey` from a JSON
    Web Key.
    """
    if not set(['n', 'e']) <= set(obj.keys()):
        raise ValueError(obj)
    numbers = RSAPublicNumbers(
        from_base64url_uint(obj['e']),
        from_base64url_uint(obj['n']),
    )
    return pkcs.PEMPublicKey(numbers.public_key())


def parse(obj):
    """One big ugly function."""
    if 'kty' not in obj:
        raise ValueError('Algorithm must be specified.')
    kty = obj.pop('kty')
    kid = obj.pop('kid', None)
    key = None
    if kty == 'RSA':
        key = parse_rsa(obj)
    else:
        raise NotImplementedError
    assert key is not None # nosec
    key.id = kid
    return key
