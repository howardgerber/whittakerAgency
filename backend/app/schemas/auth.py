from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=254)  # RFC 5321 standard
    full_name: str = Field(..., min_length=1, max_length=200)
    phone: Optional[str] = Field(None, max_length=12)  # XXX.XXX.XXXX format
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator('username')
    @classmethod
    def username_must_be_lowercase_alphanumeric(cls, v: str) -> str:
        """Validate username: lowercase, alphanumeric + underscore/dash"""
        # Convert to lowercase
        v = v.lower()

        # Check if contains only allowed characters
        if not all(c.isalnum() or c in ['_', '-'] for c in v):
            raise ValueError('Username can only contain lowercase letters, numbers, underscores, and dashes')

        # Must start with a letter
        if not v[0].isalpha():
            raise ValueError('Username must start with a letter')

        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    """Schema for user profile (no password)"""
    id: int
    username: str
    email: str
    full_name: str
    phone: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)
