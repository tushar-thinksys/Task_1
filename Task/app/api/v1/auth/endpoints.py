from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from app.core.config import settings
from app.api.v1.auth.repository import get_or_create_user_from_google
from app.core.security import create_access_token

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.api.v1.auth.schema import (
    RegisterRequest,
    RegisterResponse,
    VerifyOTPRequest,
    VerifyOTPResponse,
    ResendOTPRequest,
    ResendOTPResponse,
    LoginRequest,
    LoginResponse,
    PasswordResetRequest,
    PasswordResetOTPResponse,
    ResetPasswordRequest,
    ResetPasswordResponse
)
from app.api.v1.auth.service import (
    register_user,
    verify_otp,
    resend_otp,
    login_user,
    request_password_reset,
    reset_password
)

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await register_user(data, db)


@router.post("/verify-email", response_model=VerifyOTPResponse)
async def verify_otp_route(data: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    return await verify_otp(data, db)


@router.post("/resend-otp", response_model=ResendOTPResponse)
async def resend(data: ResendOTPRequest, db: AsyncSession = Depends(get_db)):
    return await resend_otp(data.email, db)


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login_user(data, db)


@router.post("/request-password-reset", response_model=PasswordResetOTPResponse)
async def request_password_reset_endpoint(data: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    return await request_password_reset(data, db)


@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password_endpoint(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    return await reset_password(data, db)

@router.get("/google/login")
async def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&scope=openid%20email%20profile"
    )
    return RedirectResponse(google_auth_url)

@router.get("/google/callback")
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_res.json()
        if "error" in token_data:
            raise HTTPException(status_code=400, detail=token_data["error"])

        user_info_res = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        user_info = user_info_res.json()

    user = await get_or_create_user_from_google(user_info, db)
    access_token = create_access_token(data={"sub": str(user.id)})
    # return {"access_token": access_token, "token_type": "bearer"}
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
