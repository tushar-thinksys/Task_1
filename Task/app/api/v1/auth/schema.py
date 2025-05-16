# auth/schema.py
from pydantic import BaseModel, EmailStr, Field, validator
from app.utils.password_validation import validate_password_strength  # import the function
import re


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, v):
        return validate_password_strength(v)


class RegisterResponse(BaseModel):
    message: str


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str


class VerifyOTPResponse(BaseModel):
    message: str


class ResendOTPRequest(BaseModel):
    email: EmailStr


class ResendOTPResponse(BaseModel):
    message: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
    email: EmailStr
    # otp:str
    


class PasswordResetOTPResponse(BaseModel):
    message: str


class VerifyPasswordResetOTPRequest(BaseModel):
    email: EmailStr
    otp: str


class VerifyPasswordResetOTPResponse(BaseModel):
    message: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

    @validator("new_password")
    def validate_password(cls, v):
        return validate_password_strength(v)


class ResetPasswordResponse(BaseModel):
    message: str
