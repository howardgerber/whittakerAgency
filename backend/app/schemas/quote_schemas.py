from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class QuoteRequestCreate(BaseModel):
    """Schema for creating a new quote request"""
    category: str = Field(..., max_length=30, description="Insurance category (e.g., vehicle, property, life, business)")
    subcategory: Optional[str] = Field(None, max_length=30, description="Insurance subcategory (e.g., auto, homeowners, motorcycle)")
    quote_data: Dict[str, Any] = Field(..., description="Insurance-specific form data")
    customer_notes: Optional[str] = Field(None, max_length=1000)


class QuoteRequestUpdate(BaseModel):
    """Schema for updating a quote request (admin only in future)"""
    status: Optional[str] = None
    agent_notes: Optional[str] = None
    quote_amount: Optional[float] = Field(None, ge=0)


class QuoteRequestResponse(BaseModel):
    """Schema for quote request responses"""
    id: int
    user_id: int
    category: str
    subcategory: Optional[str] = None
    status: str
    quote_data: Dict[str, Any]
    agent_notes: Optional[str] = None
    customer_notes: Optional[str] = None
    quote_amount: Optional[float] = None
    quoted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
