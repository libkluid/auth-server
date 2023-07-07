from base64 import b64decode
from datetime import timedelta
from os import environ

from .policy import AuthPolicy

AUTH_PRIVATE_KEY = environ.get("RSA_PRIVATE_KEY", None)
assert AUTH_PRIVATE_KEY is not None, "RSA_PRIVATE_KEY is not set"

auth_policy = AuthPolicy(
    access_token_duration=int(timedelta(hours=2).total_seconds()),
    refresh_token_duration=int(timedelta(days=7).total_seconds()),
    max_sessions=5,
    private_key=b64decode(AUTH_PRIVATE_KEY)
)

__all__ = [
    "auth_policy",
]
