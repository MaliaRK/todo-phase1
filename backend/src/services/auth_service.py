from sqlmodel import Session, select
from ..models.user_model import User
from ..auth.jwt_auth import create_access_token
from typing import Optional
from passlib.context import CryptContext
from datetime import timedelta
import uuid


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service for handling user registration, login, and session management"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a plain password"""
        # Check password length - bcrypt has a 72 byte limit
        if len(password.encode('utf-8')) > 72:
            raise ValueError("Password must not exceed 72 bytes")
        return pwd_context.hash(password)

    @classmethod
    def register_user(
        cls,
        email: str,
        password: str,
        name: Optional[str] = None,
        session: Session = None
    ) -> User:
        """Register a new user with email and password"""
        # Check if user already exists
        existing_user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if existing_user:
            raise ValueError("Email already registered")

        # Hash the password
        try:
            hashed_password = cls.get_password_hash(password)
        except ValueError as e:
            # Re-raise the password length error
            raise e

        # Create new user
        user = User(
            email=email,
            name=name,
            hashed_password=hashed_password
        )
        user.id = f"user_{str(uuid.uuid4()).replace('-', '')}"  # Generate unique ID
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @classmethod
    def authenticate_user(
        cls,
        email: str,
        password: str,
        session: Session = None
    ) -> Optional[User]:
        """Authenticate a user with email and password"""
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user or not user.hashed_password or not cls.verify_password(password, user.hashed_password):
            return None

        return user

    @classmethod
    def create_access_token_for_user(
        cls,
        user: User,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create an access token for the given user"""
        data = {
            "sub": user.id,
            "email": user.email
        }
        return create_access_token(data=data, expires_delta=expires_delta)