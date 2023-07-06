from auth.domain import entities, errors
from auth.repository import AuthRepository, orm
from auth.utils.crypto import generate_hash, generate_salt


class SignUp:
    async def execute(self, email: str, password: str) -> entities.Token:
        salt = generate_salt()
        hash = generate_hash(password, salt)

        async with orm.transaction() as tx:
            auth_repository = AuthRepository(tx)

            if await auth_repository.find_user_by_email(email):
                raise errors.EmailAlreadyExistsError(email=email)

            uid = await auth_repository.generate_uid()
            signup = entities.SignUp(
                uid=uid,
                email=email,
                hash=hash,
                salt=salt,
            )

            user = await auth_repository.insert_user(signup)

            return user
