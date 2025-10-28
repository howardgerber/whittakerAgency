from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.security import decode_access_token
from app.models.user import User
from app.schemas.contact_schemas import (
    ContactMessageCreate,
    ContactMessageResponse,
    ContactMessageDetail,
    ContactMessageCreateResponse
)
from app.services.contact_service import ContactService

router = APIRouter()
security = HTTPBearer(auto_error=False)


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional authentication - returns User if authenticated, None if not.
    Used for endpoints that work for both authenticated and guest users.
    """
    if credentials is None:
        return None

    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        return None

    user_id: str = payload.get("sub")
    if user_id is None:
        return None

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.is_active:
        return None

    return user


@router.post("/submit", response_model=ContactMessageCreateResponse, status_code=status.HTTP_201_CREATED)
def submit_contact_message(
    contact_data: ContactMessageCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Submit a contact message.
    No authentication required - works for both guests and authenticated users.
    If user is authenticated, message is linked to their account.
    """
    user_id = current_user.id if current_user else None

    message = ContactService.create_contact_message(
        db=db,
        contact_data=contact_data,
        user_id=user_id
    )

    return ContactMessageCreateResponse(
        id=message.id,
        status=message.status,
        created_at=message.created_at
    )


@router.get("/messages", response_model=List[ContactMessageResponse])
def get_user_messages(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all contact messages for the current user.
    Requires authentication.
    """
    messages = ContactService.get_user_messages(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

    return [ContactMessageResponse.from_orm(msg) for msg in messages]


@router.get("/{message_id}", response_model=ContactMessageDetail)
def get_message_detail(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific contact message by its ID.
    Requires authentication.
    User must own the message.
    """
    message = ContactService.get_message_detail(
        db=db,
        message_id=message_id,
        user_id=current_user.id
    )

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact message {message_id} not found"
        )

    return message
