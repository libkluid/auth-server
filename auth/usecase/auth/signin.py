from auth.domain import errors, models
from auth.repository import AuthRepository, orm
from auth.utils.crypto import generate_hash


class SignIn:
    async def execute(self, email: str, password: str) -> models.User:
        async with orm.transaction() as tx:
            auth_repository = AuthRepository(tx)

            user = await auth_repository.find_user_by_email(email=email)
            if not user:
                raise errors.UserNotExistsError(email=email)

            if user.hash != generate_hash(password, user.salt):
                raise errors.PasswordNotMatchError(email=email)

            user = await auth_repository.update_last_access(user)
            return user
