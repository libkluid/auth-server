from fastapi import Request, status

from auth.domain import errors
from auth.repository.orm import prisma

from .app import create_app, formatted_response

app = create_app()


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.exception_handler(errors.UserNotExistsError)
@app.exception_handler(errors.PasswordNotMatchError)
def signin_error_handler(
    request: Request, exc: errors.UserNotExistsError | errors.PasswordNotMatchError
):
    return formatted_response(
        status=status.HTTP_400_BAD_REQUEST,
        error="Invalid email or password",
        data={"email": exc.email},
    )


@app.exception_handler(errors.EmailAlreadyExistsError)
def signup_error_handler(request: Request, exc: errors.EmailAlreadyExistsError):
    return formatted_response(
        status=status.HTTP_409_CONFLICT,
        error="Email already exists",
        data={"email": exc.email},
    )
