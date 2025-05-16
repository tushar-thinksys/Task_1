# import uuid
# from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from uuid import uuid4
# from datetime import datetime
# from app.db.base import Base
# #from app.api.v1.media.model import Media  # Make sure Media is imported


# class User(Base):
#     __tablename__ = "users"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String(100), nullable=False)
#     email = Column(String(255), unique=True, nullable=False, index=True)
#     password_hash = Column(String(255), nullable=True)
#     is_verified = Column(Boolean, default=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     profile_picture = Column(String(255), nullable=True)

    
#     otps = relationship("OTP", back_populates="user")
#     media = relationship("Media", back_populates="user")

#     def __repr__(self):
#         return f"<User(id={self.id}, email={self.email}, verified={self.is_verified})>"


# class OTP(Base):
#     __tablename__ = "otps"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
#     otp_code = Column(String(10), nullable=False)
#     purpose = Column(String(50), nullable=False)
#     expires_at = Column(DateTime, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     user = relationship("User", back_populates="otps")

#     def __repr__(self):
#         return f"<OTP(id={self.id}, purpose={self.purpose}, user_id={self.user_id})>"



# class BlacklistedToken(Base):
#     __tablename__ = "blacklisted_tokens"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     token = Column(String(500), nullable=False, unique=True)
#     blacklisted_at = Column(DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return f"<BlacklistedToken(id={self.id}, blacklisted_at={self.blacklisted_at})>"
    


# # Inside User class (in app/api/v1/auth/model.py or user/model.py)



# app/api/v1/auth/model.py
import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    profile_picture = Column(String(255), nullable=True)

    otps = relationship("OTP", back_populates="user")
    audio_files = relationship("AudioFile", back_populates="user")
    image_files = relationship("ImageFile", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, verified={self.is_verified})>"

class OTP(Base):
    __tablename__ = "otps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    otp_code = Column(String(10), nullable=False)
    purpose = Column(String(50), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="otps")

    def __repr__(self):
        return f"<OTP(id={self.id}, purpose={self.purpose}, user_id={self.user_id})>"

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String(500), nullable=False, unique=True)
    blacklisted_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BlacklistedToken(id={self.id}, blacklisted_at={self.blacklisted_at})>"