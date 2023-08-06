"""Declares :class:`Service`."""
import os

import aiohttp
from fastapi import Request
from unimatrix.conf import settings
from unimatrix.ext import crypto

from .asgi import Application
from .exceptions import UpstreamServiceNotAvailable


class Service(Application):
    """A :class:`Application` implementation that integrates with Security
    Token Service (STS) providers.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signing_keys = []
        self.add_api_route(
            '/.well-known/jwks.json',
            self.jwks,
            tags=['OAuth 2.0'],
            name='oauth2.jwks',
            summary='oauth2.jwks - JSON Web Key Set (JWKS)',
        )
        self.add_api_route(
            '/.well-known/openid-configuration',
            self.openid_configuration,
            tags=['OAuth 2.0'],
            name='openid.configuration',
            summary='openid.configuration - OpenID configuration',
        )

        @self.on_event('startup')
        async def on_startup(): # pylint: disable=unused-variable
            # Import the OAuth 2.0 signing key for tokens. If
            # the value is a string, assume it is a filepath. A
            # dictionary indicates that it is a key loaded using
            # the unimatrix.ext.crypto framework.
            if settings.OAUTH2_ACTOR_KEY is None:
                return

            if isinstance(settings.OAUTH2_ACTOR_KEY, dict):
                raise NotImplementedError

            if isinstance(settings.OAUTH2_ACTOR_KEY, str):
                if os.path.exists(settings.OAUTH2_ACTOR_KEY):
                    self.signing_keys = [crypto.fromfile(
                        settings.OAUTH2_ACTOR_KEY, public=True
                    )]
                else:
                    self.logger.error("No key present at %s",
                        settings.OAUTH2_ACTOR_KEY)

    async def jwks(self):
        """Serves the OP's JSON Web Key Set [JWK] document.
        This contains the signing key(s) the RP uses to validate
        signatures from the OP. The JWK Set MAY also contain the
        Server's encryption key(s), which are used by RPs to
        encrypt requests to the Server. When both signing and
        encryption keys are made available, a use (Key Use)
        parameter value is REQUIRED for all keys in the referenced
        JWK Set to indicate each key's intended usage. Although
        some algorithms allow the same key to be used for both
        signatures and encryption, doing so is NOT RECOMMENDED,
        as it is less secure. The JWK x5c parameter MAY be used
        to provide X.509 representations of keys provided. When
        used, the bare key values MUST still be present and MUST
        match those in the certificate.
        """
        return {
            "keys": [x.jwk for x in self.signing_keys]
        }

    async def openid_configuration(self, request: Request):
        # If the OAUTH2_UPSTREAM setting is provided, then
        # the metadata/configuration URI returns the details
        # of the OAuth 2.0 server in this setting, with
        # the issuer and jwks_uri values replaced by those
        # of this server.
        upstream = getattr(settings, 'OAUTH2_UPSTREAM', None)
        metadata = {}
        if upstream:
            metadata = await self._get_upstream_metadata(upstream)
        return {
            **(metadata),
            "issuer": f"{request.url.scheme}://{request.url.netloc}",
            "jwks_uri": request.url_for('oauth2.jwks')
        }

    async def _get_upstream_metadata(self, upstream):
        url = f"{upstream}/.well-known/openid-configuration"
        metadata = {}
        try:
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                response = await session.get(url, ssl=settings.DEBUG)
                if response.status != 200:
                    self.logger.error(
                        "OAuth 2.0 discovery failed for %s", upstream
                    )
                    raise UpstreamServiceNotAvailable
                else:
                    metadata = await response.json()
        except (ValueError, aiohttp.ContentTypeError):
            self.logger.error(
                "OAuth 2.0 discovery failed for %s, invalid response format",
                upstream
            )
            raise UpstreamServiceNotAvailable
        except aiohttp.ClientConnectorCertificateError:
            self.logger.error(
                "OAuth 2.0 discovery failed for %s, certificate error", upstream
            )
            raise UpstreamServiceNotAvailable
        except (aiohttp.ClientConnectorError, aiohttp.ClientConnectionError):
            self.logger.error(
                "OAuth 2.0 discovery failed for %s, unreachable", upstream
            )
            raise UpstreamServiceNotAvailable
        return metadata
