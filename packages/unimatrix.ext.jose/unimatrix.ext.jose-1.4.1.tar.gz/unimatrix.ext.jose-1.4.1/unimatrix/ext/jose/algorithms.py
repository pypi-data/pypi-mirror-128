# pylint: skip-file
from unimatrix.ext.crypto import algorithms


ALGORITHM_MAPPING = {
    algorithms.HMACSHA256: 'HS256',
    algorithms.HMACSHA384: 'HS384',
    algorithms.HMACSHA512: 'HS512',
    algorithms.RSAPKCS1v15SHA256: 'RS256',
    algorithms.RSAPKCS1v15SHA384: 'RS384',
    algorithms.RSAPKCS1v15SHA512: 'RS512',
    algorithms.SECP256K1SHA256: 'ES256',
}
ALGORITHM_MAPPING.update({y: x for x, y in dict.items(ALGORITHM_MAPPING)})
