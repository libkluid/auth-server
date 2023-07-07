from datetime import datetime, timedelta

from shortuuid import uuid

from auth.domain import models

from .orm import Prisma, TxRepo


class SessionRepository(TxRepo):
    def __init__(self, prisma: Prisma):
        super().__init__(prisma)

    async def generate_session(self) -> str:
        while session := uuid():
            if await self.find_session(session) is None:
                return session

    async def find_session(self, session: str) -> None | models.Session:
        session = await self.prisma.session.find_unique(where={"session": session})
        return session

    async def find_sessions_by_uid(self, uid: str) -> list[models.Session]:
        sessions = await self.prisma.session.find_many(where={"uid": uid})
        return sessions

    async def insert_session(
        self,
        uid: str,
        session: str,
        duration: int,
    ) -> models.Session:
        now = datetime.utcnow()
        expires_at = now + timedelta(seconds=duration)

        session = await self.prisma.session.create(
            data={
                "uid": uid,
                "session": session,
                "expires_at": expires_at,
                "created_at": now,
            }
        )
        return session

    async def delete_sessions(self, sessions: list[models.Session]) -> int:
        count = await self.prisma.session.delete_many(
            where={"session": {"in": [session.session for session in sessions]}}
        )

        return count
