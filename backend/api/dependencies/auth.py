from fastapi import HTTPException, Header, status
from config import settings


def verify_api_key(api_key: str = Header(..., alias="X-API-Key")):
    """Verify API key from request header."""
    if api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return api_key
