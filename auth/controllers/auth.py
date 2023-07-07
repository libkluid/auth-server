from fastapi import APIRouter

from auth.controllers import dto
from auth.domain import entities
from auth.usecase.auth import SignIn, SignOut, SignUp, VerifySession, VerifyToken

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/signup",
    status_code=200,
    response_model=dto.Response[dto.response.User],
)
async def sign_up(data: dto.request.EmailPw) -> dto.Response[dto.response.User]:
    signup = SignUp()
    user = await signup.execute(data.email, data.password)

    return dto.Response[dto.response.User](
        ok=True, error=None, data=dto.response.User(**user.dict())
    )


@router.post(
    path="/signin",
    status_code=200,
    response_model=dto.Response[dto.response.Token],
)
async def sign_in(data: dto.request.EmailPw) -> dto.Response[dto.response.Token]:
    signin = SignIn()
    token = await signin.execute(data.email, data.password)

    return dto.Response[dto.response.Token](ok=True, error=None, data=token)

@router.post(
    path="/signout",
    status_code=200,
    response_model=dto.Response[None],
)
async def sign_out(data: dto.request.Token) -> dto.Response[None]:
    verify_token = VerifyToken()
    token_payload = await verify_token.execute(data.token)

    signout = SignOut()
    token = await signout.execute(token_payload)

    return dto.Response[dto.response.Token](ok=True, error=None)


@router.post(
    path="/verify",
    status_code=200,
    response_model=dto.Response[dto.response.Verify],
)
async def verify(data: dto.request.Token) -> dto.Response[dto.response.Verify]:
    verify_token = VerifyToken()
    token_payload = await verify_token.execute(data.token)

    if token_payload.tty == entities.TokenType.ACCESS:
        assert isinstance(token_payload, entities.AccessTokenPayload)

        verify_session = VerifySession()
        token_payload = await verify_session.execute(token_payload)

    return dto.Response[dto.response.Verify](
        ok=True,
        error=None,
        data=dto.response.Verify(
            sub=token_payload.sub,
            ssn=token_payload.ssn,
            iat=token_payload.iat,
            exp=token_payload.exp,
            tty=token_payload.tty,
        )
    )
