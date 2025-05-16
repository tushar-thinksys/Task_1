# app/api/v1/user/endpoints.py

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.api.v1.user.schema import UserProfileResponse
from app.db.session import get_db
from app.core.security import get_current_user
from app.api.v1.auth.model import User
from app.api.v1.user.service import (
    validate_and_process_profile_update,
    get_profile_picture_url
)

router = APIRouter()


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(request:Request,current_user: User = Depends(get_current_user)):
    return {
        **current_user.__dict__,
        "profile_picture_url": get_profile_picture_url(current_user.profile_picture,request)
    }



@router.patch("/profile", response_model=UserProfileResponse)
async def update_user_profile(
    request: Request,
    name: str = Form(None),
    profile_picture: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_user = await validate_and_process_profile_update(db, current_user, name, profile_picture)
    return UserProfileResponse(
        id=updated_user.id,
        name=updated_user.name,
        email=updated_user.email,
        is_verified=updated_user.is_verified,
        created_at=updated_user.created_at,
        profile_picture_url=get_profile_picture_url(updated_user.profile_picture, request)
    )