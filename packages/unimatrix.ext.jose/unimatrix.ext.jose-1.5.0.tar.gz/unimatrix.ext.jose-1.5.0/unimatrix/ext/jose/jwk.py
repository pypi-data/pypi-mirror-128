"""Provides an API to serialize and deserialize JSON Web Keys (JWKs)
from and to :class:`~unimatrix.ext.crypto.PublicKey` implementations.
"""
import base64
from typing import Union

from unimatrix.ext import crypto



parse = crypto.fromjwk
