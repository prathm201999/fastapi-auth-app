from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from jose import jwt, JWTError
from datetime import datetime
from pydantic import ValidationError

from auth import dao
from auth.schemas.token import Token
from auth.schemas.user import UserRead, UserCreate
from db.connection import get_db
from config.settings import settings
from auth.models import User
from auth.utils import create_access_token, create_refresh_token, authenticate_user
from auth.dependencies import get_current_user

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user_in_db = await dao.get_user_by_email(db, user.email)
        if user_in_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already registered."
            )
        return await dao.create_user(db, user)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = await create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)
    refresh_token = await create_refresh_token(
        data={"sub": form_data.username}, expires_delta=refresh_token_expires, db=db
    )

    return {"token_type": "bearer", "refresh_token": refresh_token, "access_token": access_token}


@router.post("/token/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        stored_token = await dao.get_non_revoked_token(db, refresh_token)
        if not stored_token or stored_token.expires_at < datetime.utcnow():
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = await create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return {"token_type": "bearer", "refresh_token": refresh_token, "access_token": access_token}


@router.get("/users/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token/revoke")
async def revoke_refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    await dao.revoke_token(db, refresh_token)
    return {"message": "Token revoked successfully"}
