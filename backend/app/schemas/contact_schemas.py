from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional, Literal


class ContactMessageCreate(BaseModel):
    """Schema for creating a contact message"""
    full_name: str = Field(..., min_length=1, max_length=200, description="Full name (First Last)")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, max_length=12, description="Phone number in format XXX.XXX.XXXX")
    subject: Literal["general", "quote", "claim", "policy", "other"] = Field(..., description="Message subject category")
    message: str = Field(..., min_length=50, max_length=250, description="Message content")

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        """Validate full name has at least first and last name"""
        v = v.strip()
        if len(v.split()) < 2:
            raise ValueError("Full name must include first and last name")
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone format if provided"""
        if v is None:
            return v
        v = v.strip()
        if v and not v.replace('.', '').isdigit():
            raise ValueError("Phone must be in format XXX.XXX.XXXX")
        if v and len(v) != 12:
            raise ValueError("Phone must be exactly 12 characters (XXX.XXX.XXXX)")
        return v


class ContactMessageResponse(BaseModel):
    """Schema for contact message list response"""
    id: int
    subject: str
    status: str
    created_at: datetime
    has_response: bool

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        """Convert ORM object to response schema"""
        return cls(
            id=obj.id,
            subject=obj.subject,
            status=obj.status,
            created_at=obj.created_at,
            has_response=obj.admin_response is not None
        )


class ContactMessageDetail(BaseModel):
    """Schema for detailed contact message view"""
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    subject: str
    message: str
    status: str
    admin_response: Optional[str]
    responded_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ContactMessageCreateResponse(BaseModel):
    """Schema for contact message creation response"""
    id: int
    status: str
    created_at: datetime
    message: str = "Your message has been received. We'll get back to you soon."

    class Config:
        from_attributes = True
