from dbm import error
from fastapi import APIRouter, HTTPException

from app.schemas import ErrorResponse

def create_router(prefix: str, tag: str) -> APIRouter:
    """Create a standardized APIRouter with prefix and tag.

    Args:
        prefix (str): The URL prefix for the router.
        tag (str): The tag for the router.

    Returns:
        APIRouter: The configured APIRouter instance.
    """
    return APIRouter(prefix=prefix, tags=[tag])

def not_found(resource: str):
    """Return a standardized 404 error response.

    Args:
        resource (str): The name of the resource that was not found.

    Raises:
        HTTPException: 404 error for resource not found.
    """
    error = ErrorResponse(code=404, message=f"{resource} not found", resource=resource)
    raise HTTPException(status_code=404, detail=error.model_dump())