from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class MessageStatus(str, enum.Enum):
    NEW = "new"
    READ = "read"
    RESPONDED = "responded"


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.NEW, nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False, index=True)
