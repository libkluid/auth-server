from datetime import datetime

from auth.domain import entities, errors
from auth.repository import SessionRepository
from auth.repository.orm import transaction


class VerifySession:
    async def execute(
        self, access_token_payload: entities.AccessTokenPayload
    ) -> entities.AccessTokenPayload:
        async with transaction() as tx:
            session_repository = SessionRepository(tx)

            session = await session_repository.find_session(access_token_payload.ssn)
            if not session:
                raise errors.SessionExpiredError(access_token_payload.ssn)
            else:
                timestamp_now = int(1000 * datetime.now().timestamp())
                expires_at = int(1000 * session.expires_at.timestamp())
                if expires_at <= timestamp_now:
                    raise errors.SessionExpiredError(access_token_payload.ssn)

        return access_token_payload
