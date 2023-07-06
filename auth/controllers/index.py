from fastapi import APIRouter

from . import dto

router = APIRouter(tags=["index"])


@router.get(
    path="/",
    status_code=200,
    response_model=dto.Response[dto.response.Index],
)
def index() -> dto.Response[dto.response.Index]:
    return dto.Response[dto.response.Index](
        ok=True,
        error=None,
        data=dto.response.Index(
            message="Hello, world!",
        ),
    )
