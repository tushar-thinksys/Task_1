from datetime import datetime, timedelta
from jose import jwt,JWTError
from typing import Union
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
#from app.api.v1.auth.repository import get_user_by_id
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.auth.repository import get_user_by_id
#from app.api.v1.auth.service import is_token_blacklisted


load_dotenv()
security= HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "eL8aQJ0F5FtZaQ7Lqlw1RQ3b0kF2u97exRP_8T3q8SE")  
ALGORITHM = os.getenv("ALGORITHM", "HS256")  
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) 

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    #print("Decoded JWT payload:", payload)

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        # try:
        #     user_id = int(user_id_str)  
        # except ValueError:
        #     raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(db, user_id_str)
    if not user or not user.is_verified:
        raise credentials_exception
    return user


