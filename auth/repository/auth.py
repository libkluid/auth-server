from datetime import datetime

from shortuuid import uuid

from auth.domain import entities, models

from .orm import Prisma, TxRepo


class AuthRepository(TxRepo):
    def __init__(self, prisma: Prisma):
        super().__init__(prisma)

    async def generate_uid(self) -> str:
        while uid := uuid():
            user = await self.find_user_by_uid(uid)
            if user is None:
                return uid

    async def find_user_by_uid(self, uid: str) -> None | models.User:
        user = await self.prisma.user.find_unique(where={"uid": uid})
        return user

    async def find_user_by_email(self, email: str) -> None | models.User:
        user = await self.prisma.user.find_unique(where={"email": email})
        return user

    async def insert_user(self, signup: entities.SignUp) -> models.User:
        user = await self.prisma.user.create(
            data={
                "uid": signup.uid,
                "email": signup.email,
                "hash": signup.hash,
                "salt": signup.salt,
            }
        )
        return user

    async def update_last_access(self, user: models.User) -> models.User:
        now = datetime.utcnow()
        user = await self.prisma.user.update(
            where={"uid": user.uid}, data={"last_access": now}
        )

        return user

    async def update_password(
            self,
            user: models.User,
            hash: str,
            salt: str
        ) -> models.User:
        user = await self.prisma.user.update(
            where={"uid": user.uid}, data={"hash": hash, "salt": salt}
        )

        return user
