# backend/routes/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from typing import Annotated
from datetime import datetime
import uuid

from models import User
from db import get_session
from auth import create_access_token
import bcrypt as _bcrypt

router = APIRouter(prefix="/api/auth", tags=["auth"])


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return _bcrypt.hashpw(password.encode('utf-8'), _bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a bcrypt hash."""
    return _bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

SessionDep = Annotated[Session, Depends(get_session)]


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class SigninRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str


class AuthResponse(BaseModel):
    token: str
    user: UserResponse


@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest, session: SessionDep):
    """
    Register a new user account.
    Persists to the database and enforces unique email constraint.
    """
    # Validate password length
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )

    # Check if email already exists in DB
    existing = session.exec(
        select(User).where(User.email == request.email.lower())
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user with bcrypt-hashed password
    now = datetime.now()
    user = User(
        id=str(uuid.uuid4()),
        email=request.email.lower(),
        name=request.name.strip(),
        password_hash=hash_password(request.password),
        created_at=now,
        updated_at=now,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create JWT token
    token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    return AuthResponse(
        token=token,
        user=UserResponse(id=user.id, email=user.email, name=user.name),
    )


@router.post("/signin", response_model=AuthResponse)
async def signin(request: SigninRequest, session: SessionDep):
    """
    Authenticate user and return JWT token.
    Looks up user in the database and verifies bcrypt password.
    """
    # Find user by email in DB
    user = session.exec(
        select(User).where(User.email == request.email.lower())
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password with bcrypt
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )

    return AuthResponse(
        token=token,
        user=UserResponse(id=user.id, email=user.email, name=user.name),
    )


@router.post("/signout")
async def signout():
    """Sign out (client-side token removal)."""
    return {"success": True, "message": "Signed out successfully"}


@router.get("/verify")
async def verify_token_endpoint():
    """Health check for auth service."""
    return {"status": "ok"}
