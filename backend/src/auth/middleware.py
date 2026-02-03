from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Dict, Optional
import os
from dotenv import load_dotenv
from functools import wraps
from ..auth.jwt_auth import verify_token, get_current_user as base_get_current_user

load_dotenv()

security = HTTPBearer()

def validate_user_id_match(jwt_user_id: int, path_user_id: int) -> bool:
    """
    Validate that the user_id in the JWT matches the user_id in the path parameter.

    Args:
        jwt_user_id: User ID from JWT token
        path_user_id: User ID from path parameter

    Returns:
        True if IDs match, False otherwise
    """
    return str(jwt_user_id) == str(path_user_id)

def require_authenticated_user():
    """
    Decorator to require authenticated user for endpoints.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract token from kwargs or request
            token = kwargs.get('token') or kwargs.get('credentials')
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                )

            user_payload = verify_token(token)
            if not user_payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                )

            return await func(*args, **kwargs, current_user=user_payload)
        return wrapper
    return decorator

def get_current_user_with_validation(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get current user from JWT token with validation.

    Args:
        credentials: HTTP Authorization credentials containing the JWT token

    Returns:
        User payload if token is valid

    Raises:
        HTTPException: If token is invalid or missing
    """
    return base_get_current_user(credentials)