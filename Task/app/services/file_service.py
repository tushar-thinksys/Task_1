import boto3
from uuid import uuid4
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3FileService:
    def __init__(self):
        self.bucket = settings.AWS_S3_BUCKET_NAME
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            endpoint_url=settings.AWS_ENDPOINT_URL,
        )
        self.create_bucket()

    def create_bucket(self):
        try:
            self.client.create_bucket(Bucket=self.bucket)
            logger.info(f"Bucket {self.bucket} created successfully.")
        except ClientError as e:
            if e.response['Error']['Code'] in ['BucketAlreadyExists', 'BucketAlreadyOwnedByYou']:
                logger.info(f"Bucket {self.bucket} already exists or is owned by you.")
            else:
                logger.error(f"Failed to create bucket: {str(e)}")
                raise RuntimeError(f"Failed to create bucket: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error creating bucket: {str(e)}")
            raise RuntimeError(f"Unexpected error creating bucket: {str(e)}")

    def upload_file(self, file: UploadFile, user_id: str) -> str:
        try:
            extension = file.filename.split(".")[-1]
            key = f"media/{user_id}/{uuid4()}.{extension}"

            self.client.upload_fileobj(
                Fileobj=file.file,
                Bucket=self.bucket,
                Key=key,
                ExtraArgs={"ContentType": file.content_type},
            )

            url = f"{settings.AWS_ENDPOINT_URL}/{self.bucket}/{key}"
            logger.info(f"File uploaded: {url}")
            return url
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to upload file: {str(e)}")
            raise RuntimeError(f"Failed to upload file: {str(e)}")

    def generate_presigned_url(self, file_url: str, expires_in: int = 3600) -> str:
        try:
            prefix = f"{settings.AWS_ENDPOINT_URL}/{self.bucket}/"
            key = file_url.replace(prefix, "")
            logger.info(f"Generating presigned URL for bucket: {self.bucket}, key: {key}")
            presigned_url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=expires_in
            )
            logger.info(f"Generated presigned URL: {presigned_url}")
            return presigned_url
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to generate presigned URL: {str(e)}")
            raise RuntimeError(f"Failed to generate presigned URL: {str(e)}")

    def delete_file(self, file_url: str) -> None:
        try:
            prefix = f"{settings.AWS_ENDPOINT_URL}/{self.bucket}/"
            key = file_url.replace(prefix, "")
            if not key:
                raise ValueError("Invalid file URL")
            self.client.delete_object(Bucket=self.bucket, Key=key)
            logger.info(f"File deleted: {key}")
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to delete file: {str(e)}")
            raise RuntimeError(f"Failed to delete file: {str(e)}")