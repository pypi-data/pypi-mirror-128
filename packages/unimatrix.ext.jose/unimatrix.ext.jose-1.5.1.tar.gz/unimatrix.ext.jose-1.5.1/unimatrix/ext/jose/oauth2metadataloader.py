"""Declares :class:`OAuth2MetadataLoader`."""
import aiohttp
from unimatrix.ext import crypto

from . import jwk


class OAuth2MetadataLoader(crypto.KeyLoader):
    """Loads public keys from metadata endpoint of an OAuth 2.0 authorization
    server, as defined in RFC 8414. As implied by the specification,
    :class:`OAuth2MetadataLoader` will only retrieve public keys.

    By default, :class:`OAuth2MetadataLoader` inspects the well-known
    OAuth 2.0 server metadata URL (``/.well-known/oauth-authorization-server``).
    Optionally, if the metadata URL is exposed on a different endpoint, it
    may be specified with the ``metadata_endpoint`` parameter. From the
    retrieved metadata, the keys present at ``jwks_uri`` are imported by
    :class:`OAuth2MetadataLoader`. If the server metadata does not specify
    ``jwks_uri`` no keys are imported (fails silently).

    Example configuration:

    .. code:: python

        {
            'loader': 'unimatrix.ext.jose.OAuth2MetadataLoader',
            'options': {
                'server_url': "https://example.com"
            }
        }
    """
    __module__ = 'unimatrix.ext.jose'
    default_endpoint = '/.well-known/oauth-authorization-server'

    def setup(self, opts):
        endpoint = opts.get('metadata_endpoint') or self.default_endpoint
        self.server_url = str.rstrip(opts.server_url, '/')\
            + '/' + str.lstrip(endpoint, '/')

    async def get_jwks(self) -> str:
        """Inspect the configured OAuth 2.0 server metadata and return the
        JSON Web Keyset, or ``None`` if it could not be found.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.server_url) as response:
                metadata = await response.json()
            if 'jwks_uri' not in metadata:
                return None
            async with session.get(metadata['jwks_uri']) as response:
                result = await response.json()
                return result.get('keys') or []

    async def list(self):
        """Inspect the OAuth 2.0 server metadata endpoint and parse
        :class:`~unimatrix.ext.crypto.PublicKey` implementations from the
        (public) JSON Web Keys found in the result.
        """
        for key in [jwk.parse(x) for x in await self.get_jwks()]:
            yield key
