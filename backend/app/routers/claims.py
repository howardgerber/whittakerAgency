from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.claim_schemas import ClaimCreate, ClaimResponse
from app.services.claim_service import ClaimService

router = APIRouter()


@router.post("/", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
def create_claim(
    claim_data: ClaimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new lightweight claim report.
    Requires authentication.

    This is NOT a full claim submission - just basic incident info to help agents
    prepare for customer visits. No PII or financial information is collected.
    """
    return ClaimService.create_claim(
        db=db,
        user_id=current_user.id,
        claim_data=claim_data
    )


@router.get("/my-claims", response_model=List[ClaimResponse])
def get_user_claims(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all claim reports for the current user.
    Requires authentication.
    Supports pagination via skip and limit parameters.
    """
    return ClaimService.get_user_claims(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )


@router.get("/{claim_id}", response_model=ClaimResponse)
def get_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific claim report by its ID.
    Requires authentication.
    User must own the claim.
    """
    claim = ClaimService.get_claim_by_id(
        db=db,
        claim_id=claim_id,
        user_id=current_user.id
    )
    if not claim:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim


@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cancel a claim report.
    Requires authentication.
    User must own the claim.
    Only claims with SUBMITTED status can be cancelled.
    """
    success = ClaimService.delete_claim(
        db=db,
        claim_id=claim_id,
        user_id=current_user.id
    )
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Claim not found")
    return None
