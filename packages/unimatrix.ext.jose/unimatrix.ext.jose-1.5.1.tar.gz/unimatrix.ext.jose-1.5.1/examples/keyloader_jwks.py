import asyncio
from unimatrix.ext import crypto
from unimatrix.ext.crypto.truststore import trust


crypto.configure.sync(
    loaders=[
        {
            'loader': "unimatrix.ext.jose.OAuth2MetadataLoader",
            'options': {'server_url': "https://example.com"}
        },
    ]
)

async def f():
    print(trust.get('noop.rsa'))

loop = asyncio.get_event_loop()
loop.run_until_complete(f())
