from auth.domain import entities, errors
from auth.repository import SessionRepository, orm


class SignOut:
    async def execute(
        self,
        token_payload: entities.AccessTokenPayload | entities.RefreshTokenPayload,
    ) -> entities.AccessTokenPayload | entities.RefreshTokenPayload:
        async with orm.transaction() as tx:
            session_repository = SessionRepository(tx)

            session = await session_repository.find_session(token_payload.ssn)
            if not session:
                raise errors.SessionExpiredError(token_payload.ssn)

            session_count = await session_repository.delete_sessions(sessions=[session])
            assert session_count <= 1, "session must be deleted zero or one"

            return token_payload
