from auth.domain import entities, errors, models
from auth.repository import (
    orm,
    AccessRepository,
    AuthRepository,
    SessionRepository
)
from auth.utils.crypto import generate_hash, generate_salt

class ChangePassword:
    async def execute(self, token: entities.AccessTokenPayload, password: str) -> models.User:
        async with orm.transaction() as tx:
            try:
                access_repository = AccessRepository()
                auth_repository = AuthRepository(tx)
                session_repository = SessionRepository(tx)

                session = await session_repository.find_session(token.ssn)
                if not session:
                    raise errors.SessionExpiredError(token.ssn)

                user = await auth_repository.find_user_by_uid(uid=session.uid)
                if not user:
                    raise errors.UserNotExistsError(uid=token.sub)

                salt = generate_salt()
                hash = generate_hash(password, salt)
                user = await auth_repository.update_password(user=user, hash=hash, salt=salt)
            except errors.AuthDomainError as e:
                await access_repository.insert_log(
                    action=entities.AccessType.CHANGE_PASSWORD,
                    uid=user.uid,
                    success=False,
                )
                raise e
            else:
                await access_repository.insert_log(
                    action=entities.AccessType.CHANGE_PASSWORD,
                    uid=user.uid,
                    success=True,
                )

                return user
