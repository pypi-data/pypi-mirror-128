# pylint: skip-file
"""Exposes utility functions for JOSE encoding."""
import base64
import json
from typing import Union


def json_encode(obj):
    return str.encode(json.dumps(obj, separators=(',', ':')))


def base64url_decode(input: Union[str, bytes]) -> bytes:
    if isinstance(input, str):
        input = input.encode("ascii")

    rem = len(input) % 4

    if rem > 0:
        input += b"=" * (4 - rem)

    return base64.urlsafe_b64decode(input)


def base64url_encode(input: bytes) -> bytes:
    return base64.urlsafe_b64encode(input).replace(b"=", b"")
