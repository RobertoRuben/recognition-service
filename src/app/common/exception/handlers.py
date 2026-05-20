from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.common.exception.exception_rfc_schema import ProblemDetailsModel
from src.app.common.exception.model.base_exception import ProblemDetailsException


async def problem_details_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, ProblemDetailsException)
    body = ProblemDetailsModel(
        type=exc.type,
        title=exc.title,
        status=exc.status,
        detail=exc.detail,
        instance=exc.instance or request.url.path,
        invalid_params=exc.invalid_params,
    )
    return JSONResponse(
        status_code=exc.status,
        content=body.model_dump(exclude_none=True),
        media_type="application/problem+json",
    )

