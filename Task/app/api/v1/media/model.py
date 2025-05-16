# # # app/api/v1/media/model.py

# # from sqlalchemy import Column, String, DateTime, Enum, Integer, ForeignKey
# # from sqlalchemy.dialects.postgresql import UUID
# # from sqlalchemy.orm import relationship
# # from datetime import datetime
# # import enum
# # import uuid
# # #from app.api.v1.auth.model import User

# # from app.db.base import Base

# # class MediaType(str, enum.Enum):
# #     image = "image"
# #     audio = "audio"

# # class Media(Base):
# #     __tablename__ = "media"

# #     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
# #     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
# #     media_type = Column(Enum(MediaType), nullable=False)

# #     file_name = Column(String, nullable=False)
# #     file_url = Column(String, nullable=False)
# #     content_type = Column(String, nullable=False)
# #     size = Column(Integer, nullable=False)

# #     image_width = Column(Integer, nullable=True)
# #     image_height = Column(Integer, nullable=True)
# #     audio_duration = Column(Integer, nullable=True)

# #     created_at = Column(DateTime, default=datetime.utcnow)
# #     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# #     user = relationship("User", back_populates="media")

# #     def __repr__(self):
# #         return f"<Media(id={self.id}, file_name={self.file_name}, user_id={self.user_id})>"


# # app/api/v1/media/model.py
# from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from datetime import datetime
# import uuid
# from app.db.base import Base

# class AudioFile(Base):
#     __tablename__ = "audio_files"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
#     file_name = Column(String, nullable=False)
#     file_url = Column(String, nullable=False)
#     content_type = Column(String, nullable=False)
#     duration = Column(Float, nullable=True)
#     size = Column(Integer, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     user = relationship("User", back_populates="audio_files")

#     def __repr__(self):
#         return f"<AudioFile(id={self.id}, file_name={self.file_name}, user_id={self.user_id})>"

# class ImageFile(Base):
#     __tablename__ = "image_files"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
#     file_name = Column(String, nullable=False)
#     file_url = Column(String, nullable=False)
#     content_type = Column(String, nullable=False)
#     width = Column(Integer, nullable=True)
#     height = Column(Integer, nullable=True)
#     size = Column(Integer, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     user = relationship("User", back_populates="image_files")

#     def __repr__(self):
#         return f"<ImageFile(id={self.id}, file_name={self.file_name}, user_id={self.user_id})>"
    


from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.base import Base

class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    duration = Column(Float, nullable=True)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="audio_files")

    def __repr__(self):
        return f"<AudioFile(id={self.id}, file_name={self.file_name}, user_id={self.user_id})>"

class ImageFile(Base):
    __tablename__ = "image_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="image_files")

    def __repr__(self):
        return f"<ImageFile(id={self.id}, file_name={self.file_name}, user_id={self.user_id})>"