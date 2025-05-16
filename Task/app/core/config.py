# from typing import Optional
# from pydantic import validator
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int
#     DATABASE_URL: str
#     MAIL_SENDER: str = "noreply@example.com"
#     OTP_LIFETIME_MINUTES: int = 10
#     GOOGLE_CLIENT_ID: str
#     GOOGLE_CLIENT_SECRET: str
#     GOOGLE_REDIRECT_URI: str
#     MAX_FILE_SIZE: int   
#     AWS_ACCESS_KEY_ID: str ="test"
#     AWS_SECRET_ACCESS_KEY: str ="test"
#     AWS_REGION: str = "us-east-1"
#     AWS_ENDPOINT_URL: str = "http://localhost:4566"
#     AWS_S3_BUCKET_NAME: str = "my-local-bucket"
#     ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png"]
#     ALLOWED_AUDIO_TYPES: list[str] = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/m4a"]
   



#     @validator("ALLOWED_IMAGE_TYPES", "ALLOWED_AUDIO_TYPES", pre=True)
#     def split_comma_separated(cls, v):
#         if isinstance(v, str):
#             return [item.strip() for item in v.split(",") if item.strip()]
#         return v
    
# @validator("MAX_FILE_SIZE", pre=True)
#        def parse_max_file_size(cls, v):
#            if isinstance(v, str):
#                v = v.split("#")[0].strip()
#                return int(v)
#            return v

#     class Config:
#         env_file = ".env"
#         #env_file_encoding = "utf-8"
#         extra="allow"



# settings = Settings()

from typing import Optional
from pydantic import validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    MAIL_SENDER: str = "noreply@example.com"
    OTP_LIFETIME_MINUTES: int = 10
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    MAX_FILE_SIZE: int
    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"
    AWS_REGION: str = "us-east-1"
    AWS_ENDPOINT_URL: str = "http://localhost:4566"
    AWS_S3_BUCKET_NAME: str = "my-local-bucket"
    

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
