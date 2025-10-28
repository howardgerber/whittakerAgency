from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime, date


class ClaimCreate(BaseModel):
    """
    Schema for creating a lightweight claim report.
    This is NOT a full claim submission - just basic incident info for agent preparation.
    """
    category: str = Field(..., max_length=30, description="Insurance category (e.g., vehicle, property, life)")
    subcategory: Optional[str] = Field(None, max_length=30, description="Insurance subcategory (e.g., auto, homeowners)")
    incident_date: date = Field(..., description="Date of incident (required, not future, max 2 years past)")
    incident_summary: str = Field(..., min_length=10, max_length=500, description="Brief incident description (10-500 chars)")
    claim_data: Dict[str, Any] = Field(..., description="Category-specific form data")
    appointment_requested: Optional[date] = Field(None, description="Preferred appointment date (optional)")
    contact_preference: str = Field(..., description="How customer prefers to be contacted")
    preferred_contact_time: Optional[str] = Field(None, max_length=20, description="Preferred contact time: morning, afternoon, evening, anytime")
    additional_notes: Optional[str] = Field(None, max_length=500, description="Optional additional notes")

    @field_validator('incident_date')
    @classmethod
    def validate_incident_date(cls, v: date) -> date:
        """Validate incident date is not in the future and not older than 2 years"""
        today = date.today()
        if v > today:
            raise ValueError('Incident date cannot be in the future')

        # Calculate 2 years ago from today
        two_years_ago = date(today.year - 2, today.month, today.day)
        if v < two_years_ago:
            raise ValueError('Incident date cannot be older than 2 years')

        return v


class ClaimUpdate(BaseModel):
    """Schema for updating a claim (admin only - defer to Slice 6)"""
    status: Optional[str] = None
    contacted_at: Optional[datetime] = None


class ClaimResponse(BaseModel):
    """Schema for claim responses"""
    id: int
    user_id: int
    category: str
    subcategory: Optional[str] = None
    incident_date: date
    incident_summary: str
    claim_data: Dict[str, Any]
    appointment_requested: Optional[datetime] = None
    contact_preference: str
    preferred_contact_time: Optional[str] = None
    additional_notes: Optional[str] = None
    status: str
    contacted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
