# pylint: skip-file
import ioc
from unimatrix.lib import meta

from .decoder import JOSEPayloadDecoder
from .exceptions import BaseJoseException
from .exceptions import MalformedToken
from .header import JOSEHeader
from .jws import JSONWebSignature
from .jwt import JSONWebToken
from .oauth2metadataloader import OAuth2MetadataLoader
from .resolver import JOSEKeyResolver


__all__ = [
    'JOSEKeyResolver',
    'JOSEPayloadDecoder',
    'JSONWebSignature',
    'JSONWebToken',
    'JWT',
    'OAuth2MetadataLoader',
    'parse_jose_object',
]


def parse(value):
    """Parse a JOSE object from the given value. Inspect the JOSE header and
    return the appropriate object.

    Args:
        value: a :class:`str` or :class:`bytes` object holding the compact
            representation of the JOSE object.

    Raises:
        :exc:`MalformedToken`: `value` is not a compact representation of a
            JOSE object.
        :exc:`UnsupportedAlgorithm`: the JOSE header is valid but the
            signing or wrapping algorithm (specified by the ``alg`` header 
            parameter) is not recognized.
        :exc:`UnsupportedEncryptionAlgorithm`: the JOSE header is valid but
            the encryption algorithm (specified by the ``enc`` header parameter)
            is not recognized.

    Returns:
        :class:`JSONWebSignature`,
        :class:`JSONEncryption`

    The :func:`parse()` function selects the appropriate type by inspecting the
    header, which results in returning either a :class:`JSONWebSignature` or a
    :class:`JSONWebEncryption` instance. In neither case is the JOSE object
    verified or decrypted - it is up to the caller to decided when and in
    what order to process it.
    """
    header, *parts = bytes.split(value, b'.')
    if len(parts) != 2:
        raise MalformedToken
    return JSONWebSignature.parse(value)


@meta.allow_sync
@ioc.inject('decoder', 'JOSEPayloadDecoder')
async def payload(value: bytes, decoder: JOSEPayloadDecoder) -> JSONWebToken:
    """Parse the JOSE object from `value` and return a :class:`JSONWebToken`
    instance.

    To invoke :func:`payload`, the following dependencies must be supplied
    through the :mod:`ioc` module:

    - ``JOSEKeyResolver`` - An instance that implements the
      :class:`~JOSEKeyResolver` interface. A default implementation
      is provided.
    - ``JOSEPayloadDecoder`` - An instance of :class:`~JOSEPayloadDecoder`
      or an instance that implements :class:`IJOSEPayloadDecoder`. A basic
      implementation is provided by the :mod:`~unimatrix.ext.jose` package.

    Example:

    .. code:: python

        import ioc
        from app import MyKeyStoreImpl

        ioc.provide('CryptoKeyStore', MyKeyStoreImpl())
    """
    obj = parse(value)
    return await obj.decode(decoder)


@meta.allow_sync
async def JWT(claims: dict, header: dict = None, signer = None):
    """Create a new :class:`JSONWebSignature` holding a signed set of claims
    represented as a :class:`JSONWebToken`. Use `signer` to create a digital
    signature.

    If `signer` is ``None``, the return value is **not** signed, and the caller
    must invoke :meth:`JSONWebSignature.sign()` prior to serializing the
    resulting object.

    >>> from unimatrix.ext import jose
    >>>
    >>> jwt = jose.JWT.sync({'sub': "iamhere"})
    >>> assert jwt.sub == 'iamhere'
    """
    jws = JSONWebSignature(
        JOSEHeader(header or {}),
        JSONWebToken(claims)
    )
    if signer is not None:
        await jws.sign(signer)
    return jws


jwt = JWT
