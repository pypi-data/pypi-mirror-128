"""Declares :class:`JOSEPayloadDecoder`."""
import ioc


class JOSEPayloadDecoder:
    """Provides an interface to get the payload of a JSON Web Signature (JWS)
    or JSON Web Encryption (JWE).
    """

    @ioc.inject('resolver', 'JOSEKeyResolver')
    async def verify(self, header, signature, resolver):
        """Verifies the integrity of a JSON Web Signature (JWS).

        :meth:`JOSEPayloadDecoder` requires that the ``JOSEKeyResolver``
        dependency is supplied with a concrete subclass instance of
        :class:`unimatrix.ext.jose.JOSEKeyResolver`.
        """
        return await signature.verify(
            await resolver.resolve(header))
