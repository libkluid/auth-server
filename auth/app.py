from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .controllers import auth, index


def create_app():
    app = FastAPI(
        title="Auth",
        description="Auth API",
        docs_url="/docs",
        redoc_url=None,
    )

    app.include_router(index.router)
    app.include_router(auth.router)

    return app


def formatted_response(
    status: int, data: None | dict = None, error: None | str = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content=jsonable_encoder(
            {
                "ok": 200 <= status < 400,
                "error": error,
                "data": data,
            }
        ),
    )
