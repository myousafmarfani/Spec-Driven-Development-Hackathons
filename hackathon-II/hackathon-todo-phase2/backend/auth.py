from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from models import User

# Load environment variables
load_dotenv()

# Get secret key from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_key_for_development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Initialize security scheme
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a new access token with the provided data.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verifies a JWT token and returns the decoded payload.
    Raises HTTPException if token is invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return payload
    except JWTError:
        raise credentials_exception


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get the current user ID from the JWT token.
    """
    token = credentials.credentials
    payload = verify_token(token)
    user_id: str = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


def verify_jwt_token(token: str) -> dict:
    """
    Verifies a JWT token and returns the decoded payload.
    This function can be used in endpoints to verify tokens manually.
    """
    return verify_token(token)


def verify_user_owns_token(user_id: str, current_user_id: str) -> bool:
    """
    Verifies that the user_id from the path matches the user_id from the JWT token.
    Raises HTTPException if they don't match.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to access this resource"
    )

    if user_id != current_user_id:
        raise credentials_exception

    return True


async def get_current_active_user(current_user_id: str = Depends(get_current_user)):
    """
    Extends get_current_user to ensure the user is active.
    In this implementation, we just return the user ID since we're not storing user objects in our DB.
    """
    # In a real implementation, we would fetch the user from the database
    # and verify they are active. For now, we just return the ID.
    return current_user_id