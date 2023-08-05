"""Declares :class:`JSONWebSignature`."""
from typing import Any

from unimatrix.ext import crypto
from unimatrix.ext.crypto.trustedpublickey import TrustedPublicKey

from .algorithms import ALGORITHM_MAPPING
from .decoder import JOSEPayloadDecoder
from .header import JOSEHeader
from .jwt import JSONWebToken
from .signature import JOSESignature
from .utils import base64url_decode
from .utils import base64url_encode
from . import exceptions


class JSONWebSignature(crypto.Signable):
    """Represents a JSON Web Signature (JWS) as specified in :rfc:`7515`.

    Args:
        header (:class:`JOSEHeader`): a preconfigured JOSE header, or ``None``.
        payload (:class:`JSONWebToken`, :class:`bytes`): the payload of the
        JSON Web Signature.
    """
    __module__ = 'unimatrix.ext.jose'
    payload: Any
    MalformedToken = exceptions.MalformedToken

    @classmethod
    def parse(cls, token):
        """Parse a :class:`JSONWebSignature` from a byte-sequence or string."""
        if isinstance(token, str):
            token = str.encode(token)
        header, payload, signature = bytes.split(token, b'.')
        header = JOSEHeader.parse(header)
        return cls(
            header,
            header.get_payload(payload),
            JOSESignature(base64url_decode(signature), header.algorithm,
                keyid=header.kid)
        )

    @property
    def kid(self) -> str:
        """Returns the key identifier that was used to create the JWS."""
        return self.header.kid

    @property
    def key(self) -> TrustedPublicKey:
        """Return the :class:`unimatrix.ext.crypto.TrustedPublicKey` instance
        that was used to create the JWS. It is assumed that this property is
        only invoked on signatures that are succesfully verified. If the
        header did not contain the ``kid`` claim, then return ``None``.
        """
        return None if self.kid is None else crypto.trust.get(self.kid)

    def __init__(self, header, payload, signature=None):
        self.header = header or JOSEHeader()
        self.payload = payload
        self.signature = signature
        if isinstance(payload, JSONWebToken):
            self.header.setdefault('typ', 'JWT')

    async def decode(self, decoder: JOSEPayloadDecoder) -> JSONWebToken:
        """Invoke the :class:`~JOSEPayloadDecoder` interface to verify the
        signature and return the decoded :class:`JSONWebToken`.

        .. warning::

            The claims made by the :class:`JSONWebToken` are **not** verified.
            It is up to the caller to decide when and in what order to do
            the verification.
        """
        await decoder.verify(self.header, self)
        return self.payload

    def get_jose_header(self, signer: crypto.Signer):
        """Return a :class:`~unimatrix.ext.crypto.lib.jose.JOSEHeader` instance
        based on the metadata of :class:`~unimatrix.ext.crypto.Signer`
        `signer`.
        """
        self.header['alg'] = ALGORITHM_MAPPING[signer.algorithm]
        return bytes(self.header)

    def get_signable_bytes(self, signer: crypto.Signer):
        """Return a byte-sequence holding the data that needs to be signed
        for the :class:`JSONWebSignature`.
        """
        message = self.get_jose_header(signer) + b'.' + bytes(self.payload)
        return signer.digest(message)

    def is_signed(self) -> bool:
        """Return a boolean indicating if the :class:`JSONWebSignature`
        is signed.
        """
        return self.signature is not None

    async def sign(self, signer, *args, **kwargs):
        """Sign the :class:`JSONWebSignature` and ensure that the `kid`
        header parameter is set, if present on the signing key.
        """
        if signer.key.id:
            self.header['kid'] = signer.key.id
        return await super().sign(signer, *args, **kwargs)

    async def verify(self, key):
        """Verify the :class:`JSONWebSignature` with the given key. Return
        a boolean indicating if the signature was valid.
        """
        digest = self.signature.algorithm.digest(bytes.join(b'.', [
            bytes(self.header),
            bytes(self.payload)
        ]))
        return self.signature.verify(key, digest)

    def __str__(self):
        return str.join('.', [
            bytes.decode(bytes(self.header)),
            bytes.decode(bytes(self.payload)),
            bytes.decode(base64url_encode(bytes(self.signature)))
        ])

    def __bytes__(self):
        return str.encode(str(self))
