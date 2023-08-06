# pylint: skip-file
from .asgi import Application
from .decorators import action
from .exceptions import UpstreamServiceNotAvailable
from .exceptions import UpstreamConnectionFailure
from .keytrustpolicy import KeyTrustPolicy
from .resourceendpointset import ResourceEndpointSet
from .resourceendpointset import PublicResourceEndpointSet
from .service import Service


__all__ = [
    'action',
    'Application',
    'EndpointSet',
    'PublicEndpointSet',
    'Service',
    'UpstreamConnectionFailure',
    'UpstreamServiceNotAvailable',
]


EndpointSet = ResourceEndpointSet
PublicEndpointSet = PublicResourceEndpointSet


def singleton(cls):
    """Class decorator that indicates that a resource is a singleton."""
    cls.singleton = True
    return cls


def policy(tags: list) -> KeyTrustPolicy:
    """Declares a policy for an endpoint to determine which public keys
    it wants to trust.

    Args:
        tags (list): The list of tags that this policy accepts.

    Returns:
        A :class:`KeyTrustPolicy` instance.
    """
    return KeyTrustPolicy(tags)
