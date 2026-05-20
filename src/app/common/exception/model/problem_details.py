from src.app.common.exception.exception_rfc_schema import InvalidParam
from .base_exception import ProblemDetailsException


class NotFoundException(ProblemDetailsException):
    """HTTP 404"""
    def __init__(self, detail: str, instance: str | None = None):
        super().__init__(status=404, title="Resource Not Found", detail=detail, instance=instance)


class BadRequestException(ProblemDetailsException):
    """HTTP 400 - General bad requests or business rules violations."""
    def __init__(self, detail: str, instance: str | None = None):
        super().__init__(status=400, title="Bad Request", detail=detail, instance=instance)


class InvalidParametersException(ProblemDetailsException):
    """HTTP 400 - Specifically for invalid fields or input parameters."""
    def __init__(self, detail: str, invalid_params: list[InvalidParam], instance: str | None = None):
        super().__init__(
            status=400,
            title="Invalid Request Parameters",
            detail=detail,
            instance=instance,
            invalid_params=invalid_params,
        )


class UnauthorizedException(ProblemDetailsException):
    """HTTP 401"""
    def __init__(self, detail: str, instance: str | None = None):
        super().__init__(status=401, title="Unauthorized", detail=detail, instance=instance)


class ForbiddenException(ProblemDetailsException):
    """HTTP 403"""
    def __init__(self, detail: str, instance: str | None = None):
        super().__init__(status=403, title="Forbidden", detail=detail, instance=instance)


class ConflictException(ProblemDetailsException):
    """HTTP 409"""
    def __init__(self, detail: str, instance: str | None = None):
        super().__init__(status=409, title="Conflict", detail=detail, instance=instance)