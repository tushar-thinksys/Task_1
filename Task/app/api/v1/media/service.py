from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from PIL import Image
import io
import logging
from app.services.file_service import S3FileService
from app.api.v1.media.model import AudioFile, ImageFile
from app.api.v1.media.schema import AudioFileOut, ImageFileOut
from app.utils.file_utils import  get_audio_duration, get_image_dimensions
from app.core.config import settings
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3_service = S3FileService()

async def upload_audio(db: AsyncSession, user_id: UUID, file: UploadFile) -> AudioFileOut:
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large (max 20MB)")

    # if not is_allowed_audio(file.content_type):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported audio format")

    file.file.seek(0)
    try:
        file_url = s3_service.upload_file(file=file, user_id=str(user_id))
        logger.info(f"Audio uploaded to S3: {file_url}")
    except Exception as e:
        logger.error(f"Failed to upload audio to S3: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload file: {str(e)}")

    duration = get_audio_duration(io.BytesIO(content))
    audio = AudioFile(
        user_id=user_id,
        file_name=file.filename,
        file_url=file_url,
        content_type=file.content_type,
        duration=duration,
        size=len(content),
    )
    db.add(audio)
    await db.commit()
    await db.refresh(audio)

    # presigned_url = None
    # try:
        # presigned_url = s3_service.generate_presigned_url(audio.file_url)
        # logger.info(f"Generated presigned URL for audio: {presigned_url}")
    # except Exception as e:
        # logger.warning(f"Failed to generate presigned URL for audio: {str(e)}")

    audio_out = AudioFileOut.from_orm(audio)
    #audio_out.presigned_url = presigned_url
    return audio_out

async def upload_image(db: AsyncSession, user_id: UUID, file: UploadFile)-> ImageFileOut:
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large (max 20MB)")

    # if not is_allowed_image(file.content_type):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported image format")

    file.file.seek(0)
    try:
        file_url = s3_service.upload_file(file=file, user_id=str(user_id))
        logger.info(f"Image uploaded to S3: {file_url}")
    except Exception as e:
        logger.error(f"Failed to upload image to S3: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload file: {str(e)}")

    width, height = get_image_dimensions(io.BytesIO(content))
    if width is None or height is None:
        logger.error("Invalid image file")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file")

    image_file = ImageFile(
        user_id=user_id,
        file_name=file.filename,
        file_url=file_url,
        content_type=file.content_type,
        width=width,
        height=height,
        size=len(content),
    )
    db.add(image_file)
    await db.commit()
    await db.refresh(image_file)

    # presigned_url = None
    # try:
    #     presigned_url = s3_service.generate_presigned_url(image_file.file_url)
    #     logger.info(f"Generated presigned URL for image: {presigned_url}")
    # except Exception as e:
    #     logger.warning(f"Failed to generate presigned URL for image: {str(e)}")

    image_out = ImageFileOut.from_orm(image_file)
    # image_out.presigned_url = presigned_url
    return image_out

async def get_audio(db: AsyncSession, user_id: UUID, audio_id: UUID) -> AudioFileOut:
    audio = await db.get(AudioFile, audio_id)
    if not audio or audio.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio file not found or unauthorized")
    # presigned_url = None
    # try:
    #     presigned_url = s3_service.generate_presigned_url(audio.file_url)
    #     logger.info(f"Generated presigned URL for audio: {presigned_url}")
    # except Exception as e:
    #     logger.warning(f"Failed to generate presigned URL for audio: {str(e)}")
    audio_out = AudioFileOut.from_orm(audio)
    #audio_out.presigned_url = presigned_url
    return audio_out

async def get_image(db: AsyncSession, user_id: UUID, image_id: UUID) -> ImageFileOut:
    image = await db.get(ImageFile, image_id)
    if not image or image.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image file not found or unauthorized")
    # presigned_url = None
    # try:
    #     presigned_url = s3_service.generate_presigned_url(image.file_url)
    #     logger.info(f"Generated presigned URL for image: {presigned_url}")
    # except Exception as e:
    #     logger.warning(f"Failed to generate presigned URL for image: {str(e)}")
    image_out = ImageFileOut.from_orm(image)
    # image_out.presigned_url = presigned_url
    return image_out

async def update_audio(db: AsyncSession, user_id: UUID, audio_id: UUID, data: dict) -> AudioFileOut:
    audio = await db.get(AudioFile, audio_id)
    if not audio or audio.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio file not found or unauthorized")
    if data.get("file_name"):
        audio.file_name = data["file_name"]
        audio.updated_at = datetime.utcnow()
    db.add(audio)
    await db.commit()
    await db.refresh(audio)
    # presigned_url = None
    # try:
    #     presigned_url = s3_service.generate_presigned_url(audio.file_url)
    #     logger.info(f"Generated presigned URL for audio: {presigned_url}")
    # except Exception as e:
    #     logger.warning(f"Failed to generate presigned URL for audio: {str(e)}")
    audio_out = AudioFileOut.from_orm(audio)
#    audio_out.presigned_url = presigned_url
    return audio_out

async def update_image(db: AsyncSession, user_id: UUID, image_id: UUID, data: dict) -> ImageFileOut:
    image = await db.get(ImageFile, image_id)
    if not image or image.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image file not found or unauthorized")
    if data.get("file_name"):
        image.file_name = data["file_name"]
        image.updated_at = datetime.utcnow()
    db.add(image)
    await db.commit()
    await db.refresh(image)
    # presigned_url = None
    # try:
        # presigned_url = s3_service.generate_presigned_url(image.file_url)
        # logger.info(f"Generated presigned URL for image: {presigned_url}")
    # except Exception as e:
        # logger.warning(f"Failed to generate presigned URL for image: {str(e)}")
    image_out = ImageFileOut.from_orm(image)
    # image_out.presigned_url = presigned_url
    return image_out

async def delete_audio(db: AsyncSession, user_id: UUID, audio_id: UUID) -> None:
    audio = await db.get(AudioFile, audio_id)
    if not audio or audio.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio file not found or unauthorized")
    try:
        s3_service.delete_file(audio.file_url)
        logger.info(f"Audio file deleted from S3: {audio.file_url}")
    except Exception as e:
        logger.error(f"Failed to delete audio from S3: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete file: {str(e)}")
    await db.delete(audio)
    await db.commit()

async def delete_image(db: AsyncSession, user_id: UUID, image_id: UUID) -> None:
    image = await db.get(ImageFile, image_id)
    if not image or image.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image file not found or unauthorized")
    try:
        s3_service.delete_file(image.file_url)
        logger.info(f"Image file deleted from S3: {image.file_url}")
    except Exception as e:
        logger.error(f"Failed to delete image from S3: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete file: {str(e)}")
    await db.delete(image)
    await db.commit()