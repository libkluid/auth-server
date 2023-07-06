from fastapi import APIRouter

from auth.controllers import dto
from auth.usecase.auth import SignIn, SignUp

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
    response_model=dto.Response[dto.response.User],
)
async def sign_in(data: dto.request.EmailPw) -> dto.Response[dto.response.User]:
    signin = SignIn()
    user = await signin.execute(data.email, data.password)

    return dto.Response[dto.response.User](
        ok=True, error=None, data=dto.response.User(**user.dict())
    )
