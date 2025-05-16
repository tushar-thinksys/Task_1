
# app/api/v1/user/repository.py

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.v1.auth.model import User


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def update_user_in_db(
    db: AsyncSession,
    user: User,
    name: Optional[str] = None,
    profile_picture: Optional[str] = None,
) -> User:
    if name:
        user.name = name
    if profile_picture:
        user.profile_picture = profile_picture

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
