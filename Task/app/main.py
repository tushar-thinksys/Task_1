from fastapi import FastAPI
from app.api.v1.auth import endpoints as auth_endpoints
from app.api.v1.user import endpoints as user_endpoints
from fastapi.staticfiles import StaticFiles
from app.api.v1.media.endpoints import router as media_router
import boto3
from app.core.config import settings
import os

app = FastAPI()

@app.on_event("startup")
async def startup_create_bucket():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID or "test",
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY or "test",
        region_name=settings.AWS_REGION or "us-east-1",
        endpoint_url=settings.AWS_ENDPOINT_URL or "http://localhost:4566",
    )
    try:
        existing_buckets = s3.list_buckets()["Buckets"]
        if not any(b["Name"] == settings.AWS_S3_BUCKET_NAME for b in existing_buckets):
            s3.create_bucket(Bucket=settings.AWS_S3_BUCKET_NAME)
    except Exception as e:
        print(f"Error creating bucket: {e}")

os.makedirs("uploads/profile_pictures", exist_ok=True)

app.include_router(auth_endpoints.router, prefix="/auth", tags=["Auth"])
app.include_router(user_endpoints.router, prefix="/user", tags=["User"])
app.mount("/uploads/profile_pictures", StaticFiles(directory="uploads/profile_pictures"), name="profile_pictures")
app.include_router(media_router)