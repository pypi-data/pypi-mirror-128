# pylint: skip-file
import os

from unimatrix.ext.crypto.pkcs import RSAPrivateKey


RSA_PUBLIC_KEY = os.path.join(os.path.dirname(__file__), 'pub.rsa')
RSA_PRIVATE_KEY = os.path.join(os.path.dirname(__file__), 'key.rsa')

RSA_KEY = RSAPrivateKey({'path': RSA_PRIVATE_KEY}, keyid='default-asymmetric-sign')
