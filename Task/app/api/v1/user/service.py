import os
from typing import Optional
from fastapi import UploadFile, HTTPException, status,Request
from sqlalchemy.ext.asyncio import AsyncSession
import shutil
from app.api.v1.auth.model import User
from app.api.v1.user.repository import update_user_in_db

# ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
UPLOAD_DIR = "uploads/profile_pictures"

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def validate_and_process_profile_update(
    db: AsyncSession,
    user: User,
    name: Optional[str],
    profile_picture: Optional[UploadFile]
) -> User:
    new_filename = user.profile_picture 
    if profile_picture:
        # if profile_picture.content_type not in ALLOWED_IMAGE_TYPES:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Invalid image type. Only JPEG and PNG are allowed."
        #     )

        ext = profile_picture.filename.split(".")[-1].lower()
        new_filename = f"user_{user.id}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, new_filename)

        if user.profile_picture and user.profile_picture != new_filename:
            old_path = os.path.join(UPLOAD_DIR, user.profile_picture)
            if os.path.exists(old_path):
                os.remove(old_path)

        with open(file_path, "wb") as f:
            shutil.copyfileobj(profile_picture.file, f)

    updated_user = await update_user_in_db(
        db=db,
        user=user,
        name=name,
        profile_picture=new_filename
    )

    return updated_user


def get_profile_picture_url(filename: Optional[str], request: Request) -> Optional[str]:
    if not filename:
        return None
    if filename.startswith("http://") or filename.startswith("https://"):
        return filename
    base_url = request.base_url  
    return str(base_url) + f"uploads/profile_pictures/{filename}"