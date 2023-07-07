from auth.domain import entities
from auth.repository import TokenRepository

class VerifyToken:
    async def execute(
            self, token: str
        ) -> entities.AccessTokenPayload | entities.RefreshTokenPayload:

        token_repository = TokenRepository()
        token_payload = token_repository.verify(token)

        return token_payload
