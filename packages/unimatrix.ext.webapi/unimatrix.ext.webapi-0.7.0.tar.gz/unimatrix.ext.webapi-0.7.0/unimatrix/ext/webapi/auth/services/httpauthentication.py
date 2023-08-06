"""Declares :class:`HTTPAuthenticationService`."""
from unimatrix.ext import crypto
from unimatrix.ext import jose

from ...exceptions import TrustIssues
from ..ihttpauthenticationservice import IHTTPAuthenticationService


class HTTPAuthenticationService(IHTTPAuthenticationService):

    async def resolve(self,
        bearer: bytes,
        audience: set = None,
        issuers: set = None,
        scope: set = None,
        policy = None
    ):
        """Decode JWT `bearer` and return the principal described by the
        claimset.

        Args:
            bearer (str): the bearer token as received by the ``Authorization``
                header.
            audience (set): a list of string indicating the audiences that
                are valid for this bearer token. If `audience` is ``None`` or
                empty, then no validation of the ``aud`` claim is performed.
            issuers (set): the list of issuers that should be trusted.
            scope (set): the required scope.
            policy: the policy to apply when verifying the signature.
        """
        # Get the header from the JWS. If the header does not contain the
        # `kid` claim, then we assume that the token was issued using our
        # own secret key (HS256 or similar). A JWS that specifies the `kid`
        # claim in its header, was signed by a third party. This key is
        # retrieved from the key registry and matched against the policy
        # specified by the invocation parameters.
        jws = jose.parse(bearer)

        # If there is a `kid` claim on the JWS, then there MUST be a
        # policy to determine if we trust the key.
        if jws.header.kid is not None and not policy: # pragma: no cover
            raise ValueError(
                "The policy argument is required for identified keys."
            )
        await self.verify(jws.header.kid, jws, policy)
        jwt = jws.payload
        jwt.verify(
            audience=audience or None,
            issuers=issuers or None,
            scope=scope or None
        )

        return jwt.claims

    async def verify(self, kid, jws, policy):
        """Verify the digital signature of the JWS."""

        try:
            key = (await self.get_public_key(kid))\
                if kid else\
                crypto.get_secret_key()
        except LookupError:
            raise TrustIssues
        await jws.verify(key)
        if policy is not None:
            await policy.enforce(key)

    async def get_public_key(self, kid):
        """Returns the public key identified by `kid`."""
        return crypto.trust.get(kid)
