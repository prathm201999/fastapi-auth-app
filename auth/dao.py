from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth.models import User, RefreshToken
from auth.schemas.user import UserCreate
from auth.utils import get_password_hash


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = await get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def revoke_token(db: AsyncSession, refresh_token: str):
    update_statement = (
        update(RefreshToken)
        .where(RefreshToken.token == refresh_token)
        .values(revoked=True)
    )
    await db.execute(update_statement)
    await db.commit()


async def get_non_revoked_token(db: AsyncSession, refresh_token: str):
    token_result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == refresh_token, RefreshToken.revoked == False)
    )
    return token_result.scalars().first()
