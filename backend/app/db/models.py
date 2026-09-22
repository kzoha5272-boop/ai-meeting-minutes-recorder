from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text

from app.db.database import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(String, primary_key=True)
    original_filename = Column(String, nullable=False)
    audio_path = Column(String, nullable=False)
    status = Column(String, nullable=False, default="uploaded")
    created_at = Column(DateTime, default=datetime.utcnow)
    error_message = Column(Text, nullable=True)