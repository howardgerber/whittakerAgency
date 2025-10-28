from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.admin_schemas import (
    DashboardStatsResponse,
    RecentActivityItem,
    AttentionItemsResponse,
    AdminQuoteListItem,
    AdminQuoteDetail,
    AdminQuoteUpdate,
    AdminClaimListItem,
    AdminClaimDetail,
    AdminClaimUpdate,
    AdminMessageListItem,
    AdminMessageDetail,
    AdminMessageUpdate,
    AdminUserListItem,
    AdminUserDetail,
    AdminUserUpdate,
    AdminUserListResponse,
)
from app.services.admin_service import AdminService
from typing import List


router = APIRouter()


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that requires the current user to be an admin.

    Args:
        current_user: Current authenticated user

    Returns:
        User object if admin

    Raises:
        PermissionError: If user is not an admin (maps to 403)
    """
    if not current_user.is_admin:
        raise PermissionError("Admin access required")
    return current_user


# ===== Dashboard Endpoints =====

@router.get("/dashboard/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get summary statistics for admin dashboard.
    Requires admin authentication.
    """
    return AdminService.get_dashboard_stats(db=db)


@router.get("/dashboard/recent-activity", response_model=List[RecentActivityItem])
def get_recent_activity(
    limit: int = Query(10, ge=1, le=50, description="Maximum number of items to return"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get recent activity across all submission types.
    Requires admin authentication.
    """
    return AdminService.get_recent_activity(db=db, limit=limit)


@router.get("/dashboard/attention-items", response_model=AttentionItemsResponse)
def get_attention_items(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get items requiring admin attention based on age and submission patterns.
    Requires admin authentication.
    """
    return AdminService.get_attention_items(db=db)


# ===== Quote Management Endpoints =====

@router.get("/quotes", response_model=dict)
def get_all_quotes(
    category: Optional[str] = Query(None, description="Filter by category"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by customer name or email"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get all quote requests with pagination and filtering.
    Requires admin authentication.
    """
    items, total = AdminService.get_all_quotes(
        db=db,
        category=category,
        subcategory=subcategory,
        status=status,
        search=search,
        page=page,
        limit=limit,
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,  # Ceiling division
    }


@router.get("/quotes/{quote_id}", response_model=AdminQuoteDetail)
def get_quote_detail(
    quote_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get full details for a specific quote.
    Requires admin authentication.
    """
    quote = AdminService.get_quote_detail(db=db, quote_id=quote_id)

    if quote is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote {quote_id} not found"
        )

    return quote


@router.put("/quotes/{quote_id}", response_model=AdminQuoteDetail)
def update_quote(
    quote_id: int,
    update_data: AdminQuoteUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Update a quote request (admin only).
    Requires admin authentication.
    """
    updated_quote = AdminService.update_quote(
        db=db,
        quote_id=quote_id,
        update_data=update_data,
        admin_user_id=admin_user.id,
    )

    if updated_quote is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote {quote_id} not found"
        )

    return updated_quote


# ===== Claim Management Endpoints =====

@router.get("/claims", response_model=dict)
def get_all_claims(
    category: Optional[str] = Query(None, description="Filter by category"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by customer name or email"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get all claims with pagination and filtering.
    Requires admin authentication.
    """
    items, total = AdminService.get_all_claims(
        db=db,
        category=category,
        subcategory=subcategory,
        status=status,
        search=search,
        page=page,
        limit=limit,
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/claims/{claim_id}", response_model=AdminClaimDetail)
def get_claim_detail(
    claim_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get full details for a specific claim.
    Requires admin authentication.
    """
    claim = AdminService.get_claim_detail(db=db, claim_id=claim_id)

    if claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claim {claim_id} not found"
        )

    return claim


@router.put("/claims/{claim_id}", response_model=AdminClaimDetail)
def update_claim(
    claim_id: int,
    update_data: AdminClaimUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Update a claim (admin only).
    Requires admin authentication.
    """
    updated_claim = AdminService.update_claim(
        db=db,
        claim_id=claim_id,
        update_data=update_data,
        admin_user_id=admin_user.id,
    )

    if updated_claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Claim {claim_id} not found"
        )

    return updated_claim


# ===== Contact Message Management Endpoints =====

@router.get("/messages", response_model=dict)
def get_all_messages(
    subject: Optional[str] = Query(None, description="Filter by subject"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by sender name or email"),
    include_guest: bool = Query(True, description="Include guest messages"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get all contact messages with pagination and filtering.
    Requires admin authentication.
    """
    items, total = AdminService.get_all_messages(
        db=db,
        subject=subject,
        status=status,
        search=search,
        include_guest=include_guest,
        page=page,
        limit=limit,
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/messages/{message_id}", response_model=AdminMessageDetail)
def get_message_detail(
    message_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get full details for a specific contact message.
    Requires admin authentication.
    """
    message = AdminService.get_message_detail(db=db, message_id=message_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message {message_id} not found"
        )

    return message


@router.put("/messages/{message_id}", response_model=AdminMessageDetail)
def update_message(
    message_id: int,
    update_data: AdminMessageUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Update a contact message (admin only).
    Requires admin authentication.
    """
    updated_message = AdminService.update_message(
        db=db,
        message_id=message_id,
        update_data=update_data,
        admin_user_id=admin_user.id,
    )

    if updated_message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message {message_id} not found"
        )

    return updated_message


# ===== User Management Endpoints =====

@router.get("/users", response_model=AdminUserListResponse)
def get_all_users(
    status: Optional[str] = Query(None, description="Filter by status: active or inactive"),
    search: Optional[str] = Query(None, description="Search by username, email, or full name"),
    recently_contacted: Optional[str] = Query(None, description="Filter by recent activity: 2weeks, 1month, 3months, 6months, 1year"),
    sort_by: str = Query("activity", description="Sort field: activity, name, or status"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get all users with pagination, filtering, and sorting.
    Requires admin authentication.
    """
    items, total = AdminService.get_all_users(
        db=db,
        status=status,
        search=search,
        recently_contacted=recently_contacted,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit,
    )

    return AdminUserListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit,
    )


@router.get("/users/{user_id}", response_model=AdminUserDetail)
def get_user_detail(
    user_id: int,
    date_range: Optional[str] = Query(None, description="Date range filter: 30days, 6months, ytd, last_year, all"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Get full details for a specific user including activity summary.
    Supports optional date range filtering for activity data.
    Requires admin authentication.
    """
    user = AdminService.get_user_detail(db=db, user_id=user_id, date_range=date_range)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )

    return user


@router.put("/users/{user_id}", response_model=AdminUserDetail)
def update_user(
    user_id: int,
    update_data: AdminUserUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """
    Update a user (admin only).
    Requires admin authentication.
    """
    updated_user = AdminService.update_user(
        db=db,
        user_id=user_id,
        update_data=update_data,
        admin_user_id=admin_user.id,
    )

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )

    return updated_user
