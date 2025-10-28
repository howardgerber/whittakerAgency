from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal


# Dashboard Schemas
class QuoteStats(BaseModel):
    """Quote statistics for dashboard"""
    pending: int = Field(..., description="Number of pending quote requests")
    in_review: int = Field(..., description="Number of quotes in review")
    quoted: int = Field(..., description="Number of quoted requests")
    total: int = Field(..., description="Total number of quote requests")


class ClaimStats(BaseModel):
    """Claim statistics for dashboard"""
    submitted: int = Field(..., description="Number of submitted claims")
    contacted: int = Field(..., description="Number of contacted claims")
    closed: int = Field(..., description="Number of closed claims")
    total: int = Field(..., description="Total number of claims")


class MessageStats(BaseModel):
    """Message statistics for dashboard"""
    new: int = Field(..., description="Number of new messages")
    read: int = Field(..., description="Number of read messages")
    responded: int = Field(..., description="Number of responded messages")
    closed: int = Field(..., description="Number of closed messages")
    total: int = Field(..., description="Total number of messages")


class UserStats(BaseModel):
    """User statistics for dashboard"""
    active: int = Field(..., description="Number of active users")
    inactive: int = Field(..., description="Number of inactive users")
    total: int = Field(..., description="Total number of users")


class RecentActivityItemSummary(BaseModel):
    """Recent activity item for dashboard feed"""
    type: str = Field(..., description="Type: quote, claim, or message")
    customer: str = Field(..., description="Customer's full name")
    action: str = Field(..., description="Action taken (e.g., submitted, contacted)")
    date: datetime = Field(..., description="When the activity occurred")


class DashboardStatsResponse(BaseModel):
    """Summary statistics for admin dashboard"""
    quotes: QuoteStats = Field(..., description="Quote statistics")
    claims: ClaimStats = Field(..., description="Claim statistics")
    messages: MessageStats = Field(..., description="Message statistics")
    users: UserStats = Field(..., description="User statistics")
    recent_activity: List[RecentActivityItemSummary] = Field(..., description="Recent activity across all types")


class RecentActivityItem(BaseModel):
    """Single item in recent activity feed"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str = Field(..., description="Type of activity: quote, claim, or message")
    customer_name: str = Field(..., description="Customer's full name")
    category: Optional[str] = Field(None, description="Category for quotes/claims")
    subject: Optional[str] = Field(None, description="Subject for messages")
    status: str = Field(..., description="Current status")
    created_at: datetime = Field(..., description="When the item was created")


# Quote Management Schemas
class AdminQuoteListItem(BaseModel):
    """Quote list item for admin table view"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_name: str = Field(..., description="User's full name")
    customer_email: str = Field(..., description="User's email")
    category: str
    subcategory: Optional[str]
    status: str
    quote_amount: Optional[Decimal]
    created_at: datetime
    updated_at: datetime


class AdminQuoteDetail(BaseModel):
    """Full quote details for admin view"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    customer_name: str
    customer_email: str
    customer_phone: Optional[str]
    category: str
    subcategory: Optional[str]
    status: str
    quote_data: Dict[str, Any]
    customer_notes: Optional[str]
    agent_notes: Optional[str]
    quote_amount: Optional[Decimal]
    quoted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class AdminQuoteUpdate(BaseModel):
    """Update request for quote (admin only)"""
    status: Optional[str] = Field(None, description="New status: pending, in_review, quoted, accepted, declined")
    quote_amount: Optional[Decimal] = Field(None, ge=0, description="Quote amount in dollars")
    agent_notes: Optional[str] = Field(None, max_length=2000, description="Agent notes")


# Claim Management Schemas
class AdminClaimListItem(BaseModel):
    """Claim list item for admin table view"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_name: str
    customer_email: str
    category: str
    subcategory: Optional[str]
    incident_date: date
    status: str
    created_at: datetime
    updated_at: datetime


class AdminClaimDetail(BaseModel):
    """Full claim details for admin view"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    customer_name: str
    customer_email: str
    customer_phone: Optional[str]
    category: str
    subcategory: Optional[str]
    incident_date: date
    incident_summary: str
    claim_data: Dict[str, Any]
    appointment_requested: Optional[date]
    contact_preference: str
    preferred_contact_time: Optional[str]
    additional_notes: Optional[str]
    status: str
    admin_notes: Optional[str]
    contacted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class AdminClaimUpdate(BaseModel):
    """Update request for claim (admin only)"""
    status: Optional[str] = Field(None, description="New status: submitted, contacted, closed")
    admin_notes: Optional[str] = Field(None, max_length=2000, description="Admin notes (internal, not visible to customer)")
    appointment_requested: Optional[date] = Field(None, description="Scheduled appointment date")


# Contact Message Management Schemas
class AdminMessageListItem(BaseModel):
    """Contact message list item for admin table view"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    sender_name: str
    sender_email: str
    subject: str
    status: str
    is_guest: bool = Field(..., description="Whether this is a guest message (not authenticated)")
    admin_response: Optional[str]
    created_at: datetime
    updated_at: datetime


class AdminMessageDetail(BaseModel):
    """Full contact message details for admin view"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int]
    sender_name: str
    sender_email: str
    sender_phone: Optional[str]
    subject: str
    message: str
    status: str
    is_guest: bool
    admin_response: Optional[str]
    responded_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class AdminMessageUpdate(BaseModel):
    """Update request for contact message (admin only)"""
    status: Optional[str] = Field(None, description="New status: new, read, responded, closed")
    admin_response: Optional[str] = Field(None, max_length=2000, description="Admin response to customer")


# Attention Items Schemas
class AttentionItem(BaseModel):
    """Single item requiring admin attention"""
    type: str = Field(..., description="Type: quote, claim, message, multiple_quotes, multiple_claims")
    id: Optional[int] = Field(None, description="Item ID (null for grouped items)")
    user_id: Optional[int] = Field(None, description="User who submitted")
    customer_name: str = Field(..., description="Customer's full name")
    title: str = Field(..., description="Display title")
    category: str = Field(..., description="Category: Overdue, Multiple Submissions, New Message")
    detail: str = Field(..., description="Additional context")
    age: str = Field(..., description="Human-readable age (e.g., '3 days old', 'Just now')")
    priority: str = Field(..., description="Priority: high, medium, low")
    icon: str = Field(..., description="Emoji icon for display")
    link: str = Field(..., description="Frontend route to view the item(s)")


class AttentionItemsResponse(BaseModel):
    """Response containing all items requiring attention"""
    items: List[AttentionItem] = Field(..., description="List of items requiring attention")


# User Management Schemas
class AdminUserListItem(BaseModel):
    """User list item for admin table view"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    email: str
    phone: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
    last_login_at: Optional[datetime]
    quotes_count: int
    claims_count: int
    messages_count: int


class UserActivitySummary(BaseModel):
    """Activity summary for user detail view"""
    quotes: List[Dict[str, Any]] = Field(..., description="Recent quotes (last 10)")
    claims: List[Dict[str, Any]] = Field(..., description="Recent claims (last 10)")
    messages: List[Dict[str, Any]] = Field(..., description="Recent messages (last 10)")
    recent_activity: List[Dict[str, Any]] = Field(..., description="Combined recent activity (last 20)")


class AdminUserDetail(BaseModel):
    """Full user details for admin view"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: str
    email: str
    phone: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    quotes_count: int
    claims_count: int
    messages_count: int
    activity: UserActivitySummary


class AdminUserUpdate(BaseModel):
    """Update request for user (admin only)"""
    is_active: Optional[bool] = Field(None, description="Account active status")
    is_admin: Optional[bool] = Field(None, description="Admin privileges")


class AdminUserListResponse(BaseModel):
    """Paginated response for user list"""
    items: List[AdminUserListItem]
    total: int
    page: int
    limit: int
    pages: int


# Pagination Helper
class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper"""
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    items: List[Any] = Field(..., description="List of items")
