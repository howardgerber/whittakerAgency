from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class LogLevel(str, enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level = Column(Enum(LogLevel), nullable=False, index=True)
    message = Column(Text, nullable=False)
    exception_type = Column(String(255), nullable=True)
    exception_message = Column(Text, nullable=True)
    stack_trace = Column(Text, nullable=True)
    request_method = Column(String(10), nullable=True)
    request_path = Column(String(500), nullable=True)
    request_ip = Column(String(45), nullable=True)
    user_id = Column(Integer, nullable=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False, index=True)
