# FastAPI Security Best Practices

## Authentication and Authorization

### OAuth2 with Password (and hashing)

```python
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Secret key for JWT tokens (use environment variable in production)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    # Retrieve user from database
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### API Key Authentication

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security

security = HTTPBearer()

async def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != "expected-api-key":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return credentials.credentials

@app.get("/secure-endpoint")
async def secure_endpoint(api_key: str = Security(get_api_key)):
    return {"message": "Secure access granted"}
```

## Input Validation and Sanitization

Always validate and sanitize user inputs using Pydantic models:

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class UserCreate(BaseModel):
    email: str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v
```

## CORS Configuration

Properly configure CORS to prevent security vulnerabilities:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Be specific, avoid ["*"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Additional security headers
    # expose_headers=["Access-Control-Allow-Origin"]
)
```

## Rate Limiting

Implement rate limiting to prevent abuse:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/limited-endpoint")
@limiter.limit("5/minute")  # 5 requests per minute per IP
async def limited_endpoint(request: Request):
    return {"message": "This endpoint is rate limited"}
```

## SQL Injection Prevention

Use parameterized queries or ORM methods to prevent SQL injection:

```python
# Using SQLAlchemy (safe approach)
from sqlalchemy.orm import Session

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Unsafe approach (avoid this)
def unsafe_get_user_by_email(db: Session, email: str):
    result = db.execute(f"SELECT * FROM users WHERE email = '{email}'")  # Vulnerable!
    return result.fetchone()
```

## Secure Password Handling

Always hash passwords before storing:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
```

## Environment Variables for Sensitive Data

Never hardcode sensitive information:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
```

## Exception Handling

Handle exceptions properly without exposing sensitive information:

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the actual error for debugging
    print(f"Error: {exc}")
    # Return generic response to prevent information disclosure
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred"}
    )
```

## Secure Session Management

For session-based authentication:

```python
from itsdangerous import URLSafeTimedSerializer
import secrets

# Generate a secure secret key
SECRET_KEY = secrets.token_urlsafe(32)

def create_session_token(user_id: int):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(str(user_id))

def verify_session_token(token: str, max_age: int = 3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        user_id = serializer.loads(token, max_age=max_age)
        return int(user_id)
    except:
        return None
```

## Additional Security Headers

Add security headers to responses:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)
```