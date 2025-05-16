from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, logger, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from app.api.v1.media.model import AudioFile, ImageFile
from app.core.security import get_current_user
from app.db.session import get_db
from app.api.v1.media.schema import AudioFileOut, ImageFileOut, AudioFileCreate, ImageFileCreate, AudioFileUpdate, ImageFileUpdate
from app.api.v1.media import service as media_service
from app.api.v1.auth.model import User

router = APIRouter(tags=["Media"])

@router.post(
    "/file_upload",
    response_model=AudioFileOut | ImageFileOut,
    status_code=status.HTTP_201_CREATED,
    summary="Upload audio or image file",
)
async def upload_media_file(
    file: UploadFile = File(...),
    media_type: str = Query(..., description="audio or image"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if media_type == "audio":
        return await media_service.upload_audio(db=db, user_id=current_user.id, file=file)
    elif media_type == "image":
        return await media_service.upload_image(db=db, user_id=current_user.id, file=file)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid media type")

@router.get("/audio/{audio_id}", response_model=AudioFileOut, summary="Get audio file details")
async def get_audio_file(
    audio_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await media_service.get_audio(db=db, user_id=current_user.id, audio_id=audio_id)

@router.get("/image/{image_id}", response_model=ImageFileOut, summary="Get image file details")
async def get_image_file(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await media_service.get_image(db=db, user_id=current_user.id, image_id=image_id)

@router.get("/audio/", response_model=List[AudioFileOut], summary="List user's audio files")
async def get_user_audio(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(AudioFile).where(AudioFile.user_id == current_user.id).order_by(AudioFile.created_at.desc())
    )
    audio_files = result.scalars().all()
    audio_outs = []
    for audio in audio_files:
        # presigned_url = None
        # try:
        #     presigned_url = media_service.s3_service.generate_presigned_url(audio.file_url)
        # except Exception as e:
        #     logger.warning(f"Failed to generate presigned URL for audio {audio.id}: {str(e)}")
        audio_out = AudioFileOut.from_orm(audio)
        #audio_out.presigned_url = presigned_url
        audio_outs.append(audio_out)
    return audio_outs

@router.get("/image/", response_model=List[ImageFileOut], summary="List user's image files")
async def get_user_image(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ImageFile).where(ImageFile.user_id == current_user.id).order_by(ImageFile.created_at.desc())
    )
    image_files = result.scalars().all()
    image_outs = []
    for image in image_files:
        # presigned_url = None
        # try:
        #     presigned_url = media_service.s3_service.generate_presigned_url(image.file_url)
        # except Exception as e:
        #     logger.warning(f"Failed to generate presigned URL for image {image.id}: {str(e)}")
        image_out = ImageFileOut.from_orm(image)
        #image_out.presigned_url = presigned_url
        image_outs.append(image_out)
    return image_outs

@router.patch("/audio/{audio_id}", response_model=AudioFileOut, summary="Update audio file metadata")
async def update_audio_file(
    audio_id: UUID,
    data: AudioFileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await media_service.update_audio(db=db, user_id=current_user.id, audio_id=audio_id, data=data.dict(exclude_unset=True))

@router.patch("/image/{image_id}", response_model=ImageFileOut, summary="Update image file metadata")
async def update_image_file(
    image_id: UUID,
    data: ImageFileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await media_service.update_image(db=db, user_id=current_user.id, image_id=image_id, data=data.dict(exclude_unset=True))

@router.delete(
    "/audio/{audio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an audio file",
)
async def delete_audio_file(
    audio_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await media_service.delete_audio(db=db, user_id=current_user.id, audio_id=audio_id)

@router.delete(
    "/image/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an image file",
)
async def delete_image_file(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await media_service.delete_image(db=db, user_id=current_user.id, image_id=image_id)