from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.quote_schemas import QuoteRequestCreate, QuoteRequestResponse
from app.services.quote_service import QuoteService

router = APIRouter()


@router.post("/", response_model=QuoteRequestResponse, status_code=status.HTTP_201_CREATED)
def create_quote_request(
    quote_data: QuoteRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new quote request.
    Requires authentication.
    """
    return QuoteService.create_quote_request(
        db=db,
        user_id=current_user.id,
        quote_data=quote_data
    )


@router.get("/", response_model=List[QuoteRequestResponse])
def get_user_quote_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all quote requests for the current user.
    Requires authentication.
    """
    return QuoteService.get_user_quote_requests(db=db, user_id=current_user.id)


@router.get("/{quote_id}", response_model=QuoteRequestResponse)
def get_quote_request(
    quote_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific quote request by its ID.
    Requires authentication.
    User must own the quote.
    """
    return QuoteService.get_quote_request_by_id(
        db=db,
        quote_id=quote_id,
        user_id=current_user.id
    )
