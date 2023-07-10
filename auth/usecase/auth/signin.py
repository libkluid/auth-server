from auth.config import auth_policy
from auth.domain import entities, errors
from auth.repository import (
    AccessRepository,
    AuthRepository,
    SessionRepository,
    TokenRepository,
    orm,
)
from auth.utils.crypto import generate_hash


class SignIn:
    async def execute(self, email: str, password: str) -> entities.Token:
        async with orm.transaction() as tx:
            auth_repository = AuthRepository(tx)
            access_repository = AccessRepository()
            session_repository = SessionRepository(tx)
            token_repository = TokenRepository()

            user = await auth_repository.find_user_by_email(email=email)
            if not user:
                raise errors.UserNotExistsError(email=email)

            try:
                if user.hash != generate_hash(password, user.salt):
                    raise errors.PasswordNotMatchError(email=email)

                if sessions := await session_repository.find_sessions_by_uid(
                    uid=user.uid
                ):
                    if len(sessions) > auth_policy.max_sessions:
                        sessions = sorted(
                            sessions, key=lambda s: s.created_at, reverse=True
                        )
                        sessions = sessions[auth_policy.max_sessions :]
                        await session_repository.delete_sessions(sessions=sessions)

                session = await session_repository.generate_session()
                session = await session_repository.insert_session(
                    uid=user.uid,
                    session=session,
                    duration=auth_policy.access_token_duration,
                )

                user = await auth_repository.update_last_access(user)
                token = token_repository.generate_tokens(session=session)
            except errors.AuthDomainError as e:
                await access_repository.insert_log(
                    action=entities.AccessType.SIGNIN,
                    uid=user.uid,
                    success=False,
                )
                raise e
            else:
                await access_repository.insert_log(
                    action=entities.AccessType.SIGNIN,
                    uid=user.uid,
                    success=True,
                )

            return token
