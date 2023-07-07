from datetime import datetime, timedelta

from auth.config import auth_policy
from auth.domain import entities, errors
from auth.repository import SessionRepository, TokenRepository, orm


class Refresh:
    async def execute(
        self, refresh_token_payload: entities.RefreshTokenPayload
    ) -> entities.Token:
        if refresh_token_payload.tty != entities.TokenType.REFRESH:
            raise errors.InvalidTokenTypeError()

        async with orm.transaction() as tx:
            session_repository = SessionRepository(tx)
            token_repository = TokenRepository()

            session = await session_repository.find_session(refresh_token_payload.ssn)
            if not session:
                raise errors.SessionExpiredError(refresh_token_payload.ssn)

            now = datetime.now()
            expires_at = now + timedelta(seconds=auth_policy.access_token_duration)

            access_token_payload = entities.AccessTokenPayload(
                sub=session.uid,
                ssn=session.session,
                iat=int(1000 * now.timestamp()),
                exp=int(1000 * expires_at.timestamp()),
                tty=entities.TokenType.ACCESS,
            )

            access_token = token_repository.encode_token(access_token_payload)

            return access_token
