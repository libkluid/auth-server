from auth.domain import entities, models

from .orm import TxRepo, prisma


class AccessRepository(TxRepo):
    def __init__(self):
        # access logs should not be rolled back
        super().__init__(prisma)

    async def insert_log(
        self,
        action: entities.AccessType,
        uid: str,
        success: bool = False,
    ) -> models.AccessLog:
        access_log = await self.prisma.accesslog.create(
            data={
                "uid": uid,
                "action": action,
                "success": success,
            }
        )

        return access_log
