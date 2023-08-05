"""Declares common exceptions for the :mod:`unimatrix.ext.crypto.lib.jose`
package.
"""
from unimatrix.ext.model.exc import CanonicalException


class BaseJoseException(CanonicalException):
    message = "The presented JSON Web Token (JWT) is not valid."


class Expired(BaseJoseException):
    code = 'CREDENTIAL_EXPIRED'
    http_status_code = 403
    message = "The JSON Web Token (JWT) is expired."
    hint = "Provide a valid token."

    def __init__(self, token, now):
        detail = (
            f"At {now}, the token was expired for {int(now-token.exp)} "
            f"seconds."
        )
        super().__init__(detail=detail)


class InsufficientScope(BaseJoseException):
    code = 'INSUFFICIENT_SCOPE'
    http_status_code = 401
    message = "The token is not allowed to perform this operation."

    def __init__(self, provided, required):
        detail = (
            "The operation requires the following scope(s): "
            f"{str.join(', ', required)}. The token provided the "
            f"scope(s): {str.join(', ', provided)}"
        )
        super().__init__(detail=detail)


class InvalidAudience(BaseJoseException):
    code = 'INVALID_AUDIENCE'
    http_status_code = 403

    def __init__(self, token, audiences):
        self.token = token
        if not token.aud:
            detail = "The `aud` claim is not specified."
        else:
            detail = (
                f"The audiences specified by the `aud` claim are not valid: "
                f"{str.join(',', token.aud)}"
            )
        hint = (
            f"Present a token with any of the following audiences: "
            f"{str.join(',', audiences)}"
        )
        super().__init__(detail=detail, hint=hint)


class InvalidIssuer(BaseJoseException):
    code = 'INVALID_ISSUER'
    http_status_code = 403

    def __init__(self, token, issuers):
        self.token = token
        if not token.iss:
            detail = "The 'iss' claim is not specified."
        else:
            detail = (
                f"The issuer specified by the 'iss' claim is not valid: "
                f"{token.iss}"
            )
        hint = (
            f"Present a token with the 'iss' claim for one of these issuers: "
            f"{str.join(',', issuers)}"
        )
        super().__init__(detail=detail, hint=hint)


class MalformedToken(BaseJoseException):
    code = 'MALFORMED_TOKEN'
    http_status_code = 403
    message = "The token is malformed and could not be interpreted."


class UnsupportedAlgorithm(BaseJoseException):
    code = 'UNSUPPORTED_ALGORITHM'
    http_status_code = 403

    def __init__(self, algorithm):
        detail = f"The '{algorithm}' is not supported."
        super().__init__(detail=detail)


class UnsupportedEncryptionAlgorithm(BaseJoseException):
    code = 'UNSUPPORTED_ENCRYPTION_ALGORITHM'
    http_status_code = 403

    def __init__(self, algorithm):
        detail = f"The '{algorithm}' is not supported."
        super().__init__(detail=detail)


class NotEffective(BaseJoseException):
    code = 'CREDENTIAL_NOT_EFFECTIVE'
    http_status_code = 403
    message = "The JSON Web Token (JWT) is not effective yet."


class MissingClaims(BaseJoseException):
    code = 'CREDENTIAL_NOT_EFFECTIVE'
    http_status_code = 403
    message = (
        "The JSON Web Token (JWT) didn't provide the required claims."
    )
