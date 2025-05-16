from datetime import datetime, timedelta
import random
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.hashing import hash_password, verify_password
from app.services.email_service import send_mock_email
from app.api.v1.auth.repository import (
    get_user_by_email,
    create_user,
    create_otp,
    get_latest_valid_otp,
    delete_otp,
    get_valid_otp,
    update_user_password
)
from app.api.v1.auth.schema import PasswordResetRequest, RegisterRequest, ResetPasswordRequest, VerifyOTPRequest, VerifyPasswordResetOTPRequest
from app.core.security import create_access_token
from app.core.config import settings

# Helper function to generate OTP code
def generate_otp_code(length: int = 6) -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

# User registration

# async def register_user(data: RegisterRequest):
#     existing_user = await get_user_by_email(db, data.email)
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered."
#         )

#     password_hash = hash_password(data.password)
#     user = await create_user(db, data.name, data.email, password_hash)

#     otp_code = generate_otp_code()
#     expires_at = datetime.utcnow() + timedelta(minutes=10)

#     await create_otp(db, user.id, otp_code, purpose="email_verification", expires_at=expires_at)
#     await db.commit()

#     send_mock_email(user.email, otp_code,"verify_email",user.name)
#     return {"message": "Verification OTP sent to your email."}


async def register_user(data: RegisterRequest, db: AsyncSession):
    existing_user = await get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    password_hash = hash_password(data.password)
    user = await create_user(db, data.name, data.email, password_hash)

    otp_code = generate_otp_code()
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    await create_otp(db, user.id, otp_code, purpose="email_verification", expires_at=expires_at)
    await db.commit()

    send_mock_email(user.email, otp_code,"verify_email",user.name)
    return {"message": "Verification OTP sent to your email."}

# Verify OTP for email
async def verify_otp(data: VerifyOTPRequest, db: AsyncSession):
    user = await get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "User is already verified."}

    otp = await get_latest_valid_otp(db, user.id, purpose="email_verification")
    if not otp or otp.otp_code != data.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user.is_verified = new_func()
    await delete_otp(db, otp)
    await db.commit()

    return {"message": "Email verified successfully."}

def new_func():
    return True

# Resend OTP
async def resend_otp(email: str, db: AsyncSession):
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")

    otp_code = generate_otp_code()
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    await create_otp(db, user.id, otp_code, purpose="email_verification", expires_at=expires_at)
    await db.commit()

    send_mock_email(user.email, otp_code,"verify_email",user.name)

    return {"message": "New OTP has been sent to your email."}

# User login
async def login_user(data, db: AsyncSession):
    user = await get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    # Add token expiry (e.g., 15 minutes)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=15))
    
    return {"access_token": access_token, "token_type": "bearer"}

# Password reset request
async def request_password_reset(data: PasswordResetRequest, db: AsyncSession):
    user = await get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_code = generate_otp_code()
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    await create_otp(db, user.id, otp_code, purpose="password_reset", expires_at=expires_at)
    await db.commit()

    send_mock_email(user.email, otp_code,"Password_reset",user.name)
    return {"message": "Password reset OTP sent to your email."}

# Verify OTP for password reset
async def verify_password_reset_otp(data: VerifyPasswordResetOTPRequest, db: AsyncSession):
    otp = await get_valid_otp(db, data.email, data.otp, purpose="password_reset")
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    return {"message": "OTP is valid. You can now reset your password."}

# Reset password
async def reset_password(data: ResetPasswordRequest, db: AsyncSession):
    otp = await get_valid_otp(db, data.email, data.otp, purpose="password_reset")
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = await get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed = hash_password(data.new_password)
    await update_user_password(db, user, hashed)

    # Optionally: delete used OTP
    await db.delete(otp)
    await db.commit()

    return {"message": "Password reset successful."}


async def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&scope=openid%20email%20profile"
    )
    return RedirectResponse(google_auth_url)