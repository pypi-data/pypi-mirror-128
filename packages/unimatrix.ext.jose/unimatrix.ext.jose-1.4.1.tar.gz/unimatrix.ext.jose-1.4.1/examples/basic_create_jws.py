import os
from unimatrix.ext import crypto
from unimatrix.ext import jose


os.environ.setdefault('SECRET_KEY', "my secret key")


obj = jose.jwt.sync(
    {'sub': "alice@acme.inc"},
    signer=crypto.get_signer()
)
print(obj)
