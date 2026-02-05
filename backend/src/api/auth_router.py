from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..database import get_session
from ..models.user_model import User
from ..services.auth_service import AuthService
from ..auth.jwt_auth import create_access_token
from datetime import timedelta
from pydantic import BaseModel
from typing import Optional


router = APIRouter(prefix="/auth", tags=["auth"])


class UserRegister(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", response_model=User)
async def register(user_data: UserRegister, session: Session = Depends(get_session)):
    """Register a new user with email and password"""
    # Validate password length before attempting to hash
    if len(user_data.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must not exceed 72 bytes"
        )

    try:
        user = AuthService.register_user(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name,
            session=session
        )
        return user
    except ValueError as e:
        # Catch both email already registered and password too long errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Catch any other unexpected errors (like bcrypt errors)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, session: Session = Depends(get_session)):
    """Authenticate user and return access token"""
    user = AuthService.authenticate_user(
        email=user_data.email,
        password=user_data.password,
        session=session
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = AuthService.create_access_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout():
    """Logout the current user"""
    # In a stateless JWT system, the client simply discards the token
    # The backend doesn't need to maintain session state
    return {"message": "Successfully logged out"}