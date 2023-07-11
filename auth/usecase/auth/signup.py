from auth.domain import entities, errors, models
from auth.repository import AccessRepository, AuthRepository, orm
from auth.utils.crypto import generate_hash, generate_salt


class SignUp:
    async def execute(self, email: str, password: str) -> models.User:
        salt = generate_salt()
        hash = generate_hash(password, salt)

        async with orm.transaction() as tx:
            auth_repository = AuthRepository(tx)
            access_repository = AccessRepository()

            if await auth_repository.find_user_by_email(email):
                raise errors.EmailAlreadyExistsError(email=email)

            uid = await auth_repository.generate_uid()
            try:
                signup = entities.SignUp(
                    uid=uid,
                    email=email,
                    hash=hash,
                    salt=salt,
                )

                user = await auth_repository.insert_user(signup)
            except errors.AuthDomainError as e:
                await access_repository.insert_log(
                    action=entities.AccessType.SIGNUP,
                    uid=uid,
                    success=False,
                )
                raise e
            else:
                await access_repository.insert_log(
                    action=entities.AccessType.SIGNUP,
                    uid=uid,
                    success=True,
                )

            return user
