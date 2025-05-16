from pydantic import BaseModel, HttpUrl
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

class MediaBase(BaseModel):
    file_name: str
    file_url: str
    content_type: str
    size: int

class AudioFileCreate(BaseModel):
    media_type: Literal["audio"]

class AudioFileUpdate(BaseModel):
    file_name: Optional[str]

class AudioFileOut(MediaBase):
    id: UUID
    user_id: UUID
    duration: Optional[float]
    created_at: datetime
    updated_at: datetime
    presigned_url: Optional[HttpUrl]

    class Config:
        from_attributes = True

class ImageFileCreate(BaseModel):
    media_type: Literal["image"]

class ImageFileUpdate(BaseModel):
    file_name: Optional[str]

class ImageFileOut(MediaBase):
    id: UUID
    user_id: UUID
    width: Optional[int]
    height: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True