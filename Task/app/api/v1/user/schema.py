from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from fastapi import UploadFile

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_verified: bool
    created_at: datetime
    profile_picture_url: Optional[str] = None 

    class Config:
        from_attributes = True
