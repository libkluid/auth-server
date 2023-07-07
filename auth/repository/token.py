from datetime import datetime, timedelta
from typing import Any

from jose import jwt, JWTError
from pydantic import ValidationError

from auth.config import auth_policy
from auth.domain import entities, errors, models


class TokenRepository:
    def verify_signature(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token=token,
                key=auth_policy.private_key,
                algorithms=["HS256"],
            )
        except JWTError:
            raise errors.InvalidTokenSignatureError()

        return payload

    def verify(
            self, token: str
        ) -> entities.AccessTokenPayload | entities.RefreshTokenPayload:
        payload = self.verify_signature(token)

        tty = payload.get("tty")
        if not tty or tty not in entities.TokenType._value2member_map_:
            raise errors.InvalidTokenPayloadError()

        token_type = entities.TokenType(tty)

        try:
            if token_type == entities.TokenType.ACCESS:
                token_payload = entities.AccessTokenPayload(**payload)
            elif token_type == entities.TokenType.REFRESH:
                token_payload = entities.RefreshTokenPayload(**payload)

            timestamp = int(1000 * datetime.now().timestamp())
            if token_payload.exp <= timestamp:
                raise errors.TokenExpiredError()

        except ValidationError:
            raise errors.InvalidTokenPayloadError()

        return token_payload

    def generate_tokens(self, session: models.Session) -> entities.Token:
        access_token_expires_at = session.created_at + timedelta(
            seconds=auth_policy.access_token_duration
        )
        refresh_token_expires_at = session.created_at + timedelta(
            seconds=auth_policy.refresh_token_duration
        )

        payload = {
            "sub": session.uid,
            "ssn": session.session,
            "iat": int(1000 * session.created_at.timestamp()),
        }

        access_token = jwt.encode(
            claims=entities.AccessTokenPayload(
                **payload,
                exp=int(1000 * access_token_expires_at.timestamp()),
            ).dict(),
            algorithm="HS256",
            key=auth_policy.private_key,
        )

        refresh_token = jwt.encode(
            claims=entities.RefreshTokenPayload(
                **payload,
                exp=int(1000 * refresh_token_expires_at.timestamp()),
            ).dict(),
            algorithm="HS256",
            key=auth_policy.private_key,
        )

        return entities.Token(access_token=access_token, refresh_token=refresh_token)
