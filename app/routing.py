from fastapi import APIRouter, HTTPException

from app.schemas import ErrorResponse

def create_router(prefix: str, tag: str) -> APIRouter:
    """
    Create a standardized APIRouter with prefix and tag.
    Keeps router setup consistent across resources.
    """
    return APIRouter(prefix=prefix, tags=[tag])

def not_found(resource: str):
    """Return a standardized 404 error."""
    error = ErrorResponse(code=404, message=f"{resource} not found", resource=resource)
    raise HTTPException(status_code=404, detail=error.model_dump())