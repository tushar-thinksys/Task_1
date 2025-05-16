from app.db.session import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, desc
from app.api.v1.auth.model import User, OTP
from datetime import datetime
from typing import Optional


# Get a user by email
async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


# Create a new user
async def create_user(session: AsyncSession, name: str, email: str, password_hash: str) -> User:
    user = User(name=name, email=email, password_hash=password_hash)
    session.add(user)
    await session.flush()
    return user


# Create a new OTP for a user
async def create_otp(session: AsyncSession, user_id: int, otp_code: str, purpose: str, expires_at: datetime) -> OTP:
    otp = OTP(user_id=user_id, otp_code=otp_code, purpose=purpose, expires_at=expires_at)
    session.add(otp)
    await session.flush()
    return otp


# Get the latest valid OTP for a user and purpose
async def get_latest_valid_otp(session: AsyncSession, user_id: int, purpose: str):
    now = datetime.utcnow()
    result = await session.execute(
        select(OTP)
        .where(
            and_(
                OTP.user_id == user_id,
                OTP.purpose == purpose,
                OTP.expires_at >= now
            )
        )
        .order_by(desc(OTP.created_at))
        .limit(1)
    )
    return result.scalar_one_or_none()


# Delete an OTP record from the database
async def delete_otp(session: AsyncSession, otp: OTP):
    await session.delete(otp)
    await session.flush()


# Validate OTP based on email, otp_code, and purpose
async def get_valid_otp(session: AsyncSession, email: str, otp_code: str, purpose: str) -> Optional[OTP]:
    result = await session.execute(
        select(OTP).join(User).where(
            and_(
                User.email == email,
                OTP.otp_code == otp_code,
                OTP.purpose == purpose,
                OTP.expires_at > datetime.utcnow()
            )
        )
    )
    return result.scalar_one_or_none()


# Update user's password
async def update_user_password(session: AsyncSession, user: User, new_hash: str):
    user.password_hash = new_hash
    session.add(user)
    await session.flush()


# Get a user by ID
async def get_user_by_id(session: AsyncSession, user_id: str) -> Optional[User]:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_or_create_user_from_google(user_info: dict, db: AsyncSession) -> User:
    email = user_info.get("email")
    name = user_info.get("name")
    picture = user_info.get("picture")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        user = User(
            name=name,
            email=email,
            is_verified=True,
            profile_picture=picture,
            created_at=datetime.utcnow(),
            password_hash=""
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        updated = False
        if not user.profile_picture and picture:
            user.profile_picture = picture
            updated = True
        if not user.name and name:
            user.name = name
            updated = True
        if updated:
            db.add(user)
            await db.commit()
            await db.refresh(user)

    return user

