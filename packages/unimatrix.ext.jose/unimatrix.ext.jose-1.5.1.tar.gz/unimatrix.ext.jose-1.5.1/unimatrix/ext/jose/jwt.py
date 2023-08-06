"""Declares :class:`JSONWebToken`."""
import functools
import json
import re
import time

from . import exceptions
from .utils import base64url_decode
from .utils import base64url_encode
from .utils import json_encode


class JSONWebToken:
    """Represents a JSON Web Token (JWT).

    Args:
        claims (:class:`dict`): the dictionary holding the claims specified
            for the token.
    """
    __module__ = 'unimatrix.ext.jose'
    Expired             = exceptions.Expired
    InsufficientScope   = exceptions.InsufficientScope
    InvalidAudience     = exceptions.InvalidAudience
    InvalidIssuer       = exceptions.InvalidIssuer
    MalformedToken      = exceptions.MalformedToken
    MissingClaims       = exceptions.MissingClaims
    NotEffective        = exceptions.NotEffective

    @property
    def aud(self) -> set:
        """Return the value of the `aud` claim."""
        aud = self.claims.get('aud') or []
        if aud is not None and not isinstance(aud, list):
            if not isinstance(aud, str):
                raise self.MalformedToken
            aud = [aud]
        return set(aud)

    @property
    def exp(self) -> int:
        """Return the expiry date/time, in seconds since the UNIX epoch,
        as specified by the `exp` claim.
        """
        if self.claims.get('exp') is None:
            return None

        try:
            return int(self.claims['exp'])
        except ValueError:
            raise self.MalformedToken

    @property
    def iat(self) -> int:
        """Return the issued at date/time, in seconds since the UNIX epoch,
        as specified by the `iat` claim.
        """
        if self.claims.get('iat') is None:
            return None

        try:
            return int(self.claims['iat'])
        except ValueError:
            raise self.MalformedToken

    @property
    def iss(self) -> str:
        """Return the issues as specified by the `iss` claim."""
        return self.claims.get('iss')

    @property
    def nbf(self) -> int:
        """Return the not before date/time, in seconds since the UNIX epoch,
        as specified by the `nbf` claim.
        """
        if self.claims.get('nbf') is None:
            return None

        try:
            return int(self.claims['nbf'])
        except ValueError:
            raise self.MalformedToken

    @functools.cached_property
    def scopes(self) -> set:
        """Return the scopes specified by the token, either as an array
        in the `scopes` claim, or a space-separated string in the `scope`
        claim. It is an error if both claims are specified.
        """
        if self.claims.get('scope') and self.claims.get('scopes'):
            raise self.MalformedToken(
                detail=(
                    "The `scope` and `scopes` claims are mutually "
                    "exclusive"
                )
            )
        if self.claims.get('scope'):
            if not isinstance(self['scope'], str):
                raise self.MalformedToken(
                    detail=(
                        "The `scope` claim is expected to be an "
                        "instance of StringOrURI"
                    )
                )
            scopes = set(filter(bool, re.split(r'\s+', self['scope'])))
        elif self.claims.get('scopes'):
            if not isinstance(self['scopes'], list):
                raise self.MalformedToken(
                    detail=(
                        "The `scopes` claim is expected to be an array, "
                        f"but deserialized to {type(self['scopes']).__name__}"
                    )
                )
            scopes = set(self['scopes'])
        else:
            scopes = set()
        return scopes

    @classmethod
    def parse(cls, value):
        return cls(json.loads(base64url_decode(value)))

    def __init__(self, claims: dict):
        self.claims = claims

    def verify_audience(self, audiences, raise_exception=True):
        """Verifies that the `aud` claim matches one or more of the specified
        `audiences`.
        """
        if isinstance(audiences, str):
            audiences = [audiences]
        audiences = set(audiences)

        is_valid = bool(self.aud & audiences)
        if not is_valid and raise_exception:
            raise self.InvalidAudience(self, audiences)
        return is_valid

    def verify(self,
        audience: list = None,
        issuers: list = None,
        scope: list = None,
        raise_exception: bool = True,
        max_age: int = None,
        required: set = None
    ) -> bool:
        """Verify if the JWT is not expired, issued by a trusted party, and
        contains the correct scope.

        Args:
            audience (set): the set of audiences that are accepted.
            issuers (set): the set of issuers that are accepted.
            scope (set): the set of scopes that are accepted.
            raise_exception (bool): indicates if an exception must be raised
                on verification failures, instead of returning a boolean.
                Default is ``True``.
            max_age (int): the maximum age of the token, in seconds. Providing
                `max_age` on a token that has not set the ``iat`` claim,
                always causes a failure.
            required (set): the set of claims that must be present on the
                token.

        Returns:
            :class:`bool`
        """
        if required is not None:
            self.verify_presence(required)
        now = int(time.time())
        self.verify_expired(now=now, raise_exception=raise_exception)
        self.verify_not_before(now=now, raise_exception=raise_exception)
        if max_age is not None:
            self.verify_max_age(
                max_age, now=now,
                raise_exception=raise_exception
            )
        if audience is not None:
            self.verify_audience(audience, raise_exception=raise_exception)
        if issuers is not None:
            self.verify_issuer(issuers, raise_exception=raise_exception)
        if scope is not None:
            self.verify_scopes(scope, raise_exception=raise_exception)

    def verify_expired(self, now=None, raise_exception=True):
        """Verifies that the JSON Web Token is not expired, based on the
        `exp` claim.
        """
        if self.exp is None:
            return True

        if now is None:
            now = int(time.time())
        is_valid = self.exp >= now
        if not is_valid and raise_exception:
            raise self.Expired(self, now)
        return is_valid

    def verify_issuer(self, issuers, raise_exception=True):
        """Verifies that the issuer is correct, based on the `iss` claim."""
        if isinstance(issuers, str):
            issuers = [issuers]
        is_valid = self.iss in issuers
        if not is_valid and raise_exception:
            raise self.InvalidIssuer(self, issuers)
        return is_valid

    def verify_max_age(self, max_age, now=None, raise_exception=True):
        """Verifies that the token does not exceed the maximum age defined.
        If there is no ``iat`` claim, then verification always fails.
        """
        now = now or int(time.time())
        if self.iat is None or ((now - self.iat) > max_age):
            raise self.Expired

    def verify_not_before(self, now=None, raise_exception=True):
        """Verifies that the JSON Web Token is not used before it is allowed,
        based on the `nbf` claim.
        """
        if self.nbf is None:
            return True

        if now is None:
            now = int(time.time())
        is_valid = self.nbf <= now
        if not is_valid and raise_exception:
            raise self.NotEffective
        return is_valid

    def verify_presence(self, claims: set, raise_exception=True) -> bool:
        """Verifies that the set of claims is present on the token."""
        missing = set(claims) - set(self.claims.keys())
        if missing and raise_exception:
            raise self.MissingClaims(
                detail=(
                    f"These claims were missing: {', '.join(missing)}"
                )
            )
        return not bool(missing)

    def verify_scopes(self, required_scopes, raise_exception=True):
        """Verifies that the scopes are equal or greater than
        `required_scopes`.
        """
        is_valid = self.scopes >= set(required_scopes)
        if not is_valid and raise_exception:
            raise self.InsufficientScope(self.scopes, required_scopes)
        return is_valid

    def __getitem__(self, key):
        return self.claims[key]

    def __bytes__(self):
        return base64url_encode(json_encode(self.claims))

    def __iter__(self):
        return iter(dict.items(self.claims))

    def __str__(self):
        return bytes.decode(bytes(self))
