"""Declares :class:`JOSEHeader`."""
import json

from unimatrix.ext.crypto.oid import OID_JOSE_JWE_ENC
from unimatrix.ext.crypto.oid import OID_JOSE_JWE_ALG
from .algorithms import ALGORITHM_MAPPING
from .exceptions import UnsupportedAlgorithm
from .exceptions import UnsupportedEncryptionAlgorithm
from .jwt import JSONWebToken
from .utils import base64url_decode
from .utils import base64url_encode
from .utils import json_encode


PROTECTED_PARAMETERS = ["alg", "jku", "jwk", "kid", "x5u", "x5c", "x5t",
    "5t#S256", "typ", "cty", "crit"]


class JOSEHeader:
    """Wraps the header of a JSON Web Signature and Encryption (JOSE)
    object.
    """
    __module__ = 'unimatrix.ext.jose'

    @property
    def algorithm(self):
        """Return the OID identifying the algorithm used with the JOSE
        object.
        """
        return ALGORITHM_MAPPING[ self['alg'] ]

    @property
    def kid(self):
        """Return the ``kid`` header parameter."""
        return self.params.get('kid')

    @classmethod
    def parse(cls, encoded):
        params = json.loads(base64url_decode(encoded))

        # If the `enc` parameter is present, the input is JSON Web
        # Encryption (JWE) and must be supported. When the `enc` parameter
        # is not present, we're dealing with a JWS.
        if params.get('enc'):
            if params.get('alg') not in OID_JOSE_JWE_ALG:
                raise UnsupportedEncryptionAlgorithm(
                    f"Unsupported algorithm: {params.get('alg')}")
            if params['enc'] not in OID_JOSE_JWE_ENC:
                raise UnsupportedEncryptionAlgorithm(
                    f"Unsupported encryption algorithm: {params['enc']}")
        elif params.get('alg') not in ALGORITHM_MAPPING:
            raise UnsupportedAlgorithm(params['alg'])

        return cls(params)

    def __init__(self, params=None):
        self.params = params or {}

    def get_payload(self, payload):
        """Return the approprate instance for the payload."""
        return JSONWebToken.parse(payload)\
            if self.is_jwt() else payload

    def is_jwt(self):
        """Return a boolean indicating if the header was part of a JSON
        Web Token (JWT).
        """
        return str.lower(self.params.get('typ') or '') == 'jwt'

    def setdefault(self, key, value):
        return self.params.setdefault(key, value)

    def __setitem__(self, key, value):
        self.params[key] = value

    def __getitem__(self, key):
        return self.params[key]

    def __bytes__(self):
        return base64url_encode(json_encode(self.params))
