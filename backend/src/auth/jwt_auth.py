from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from typing import Optional
from sqlmodel import Session, select
from ..models.user_model import User
from ..database import get_session
import os
from datetime import datetime, timedelta


security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token with the specified data and expiration"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Short-lived token for security
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    # Add additional security claims
    to_encode.update({
        "iss": "todo-app",  # Issuer
        "aud": "todo-app-users"  # Audience
    })

    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv("BETTER_AUTH_SECRET"),
        algorithm="HS256"
    )
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify a JWT token and return the decoded payload"""
    try:
        payload = jwt.decode(
            token,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"],
            audience="todo-app-users"  # Specify the audience for verification
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """Get the current authenticated user from the JWT token"""
    token = credentials.credentials
    payload = verify_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.exec(select(User).where(User.id == user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def verify_user_id_match(token_user_id: str, path_user_id: str) -> bool:
    """Verify that the user_id in the JWT token matches the user_id in the path"""
    return token_user_id == path_user_id