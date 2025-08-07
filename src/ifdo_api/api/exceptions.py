from fastapi import HTTPException
from fastapi import status


class AppException(HTTPException):
    """Base application exception."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(AppException):
    """Exception raised when an item is not found."""

    def __init__(self, name: str = "Item"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} not found")


class ValueErrorException(AppException):
    """Exception raised for value errors."""

    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
