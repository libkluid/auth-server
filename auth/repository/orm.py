from abc import ABCMeta, abstractmethod

from prisma import Prisma
from prisma.client import TransactionManager

prisma = Prisma()


def transaction() -> TransactionManager:
    return prisma.tx()


class TxRepo(metaclass=ABCMeta):
    prisma: Prisma

    @abstractmethod
    def __init__(self, prisma: Prisma):
        self.prisma = prisma
