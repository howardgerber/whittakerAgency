from sqlalchemy.orm import Session
from app.models.claim import Claim
from app.schemas.claim_schemas import ClaimCreate
from app.services.audit_log_service import AuditLogService
from typing import List, Optional
from datetime import date


class ClaimService:
    """
    Business logic for lightweight claim reporting system.
    This is NOT a full claim processing system - just basic incident info for agent preparation.
    """

    # Valid insurance categories and their subcategories (from CATEGORIES.md)
    VALID_CATEGORIES = {
        'vehicle': ['auto', 'motorcycle', 'atv_off_road', 'roadside', 'snowmobile', 'boat', 'rv', 'vehicle_protection'],
        'property': ['homeowners', 'renters', 'condo', 'landlord', 'mobile_home'],
        'life': None,  # No subcategories
        'business': None,  # No subcategories
        'identity_protection': None,  # No subcategories
        'other': ['personal_umbrella_policy', 'individual_health', 'pet', 'event', 'travel', 'jewelry', 'collectibles']
    }

    @staticmethod
    def create_claim(db: Session, user_id: int, claim_data: ClaimCreate) -> Claim:
        """
        Create a new lightweight claim report.

        Args:
            db: Database session
            user_id: ID of the user creating the claim
            claim_data: Claim data from request

        Returns:
            Created Claim object

        Raises:
            ValueError: If validation fails (invalid input - maps to 400)
        """
        # Validate category (throw ValueError for invalid input)
        if claim_data.category not in ClaimService.VALID_CATEGORIES:
            valid_cats = ', '.join(ClaimService.VALID_CATEGORIES.keys())
            raise ValueError(f"Invalid category. Must be one of: {valid_cats}")

        # Validate subcategory if provided
        valid_subcats = ClaimService.VALID_CATEGORIES[claim_data.category]
        if claim_data.subcategory:
            if valid_subcats is None:
                raise ValueError(f"Category '{claim_data.category}' does not have subcategories")
            if claim_data.subcategory not in valid_subcats:
                raise ValueError(f"Invalid subcategory for {claim_data.category}. Must be one of: {', '.join(valid_subcats)}")
        elif valid_subcats is not None:
            # Category requires a subcategory but none provided
            raise ValueError(f"Category '{claim_data.category}' requires a subcategory. Must be one of: {', '.join(valid_subcats)}")

        # Validate incident summary length (50-500 chars) - already validated by Pydantic but double-check
        if len(claim_data.incident_summary) < 10:
            raise ValueError("Incident summary must be at least 50 characters")
        if len(claim_data.incident_summary) > 500:
            raise ValueError("Incident summary must not exceed 500 characters")

        # Validate additional notes length if provided (max 500 chars)
        if claim_data.additional_notes and len(claim_data.additional_notes) > 500:
            raise ValueError("Additional notes must not exceed 500 characters")

        # Validate preferred_contact_time if provided
        valid_contact_times = ['morning', 'afternoon', 'evening', 'anytime']
        if claim_data.preferred_contact_time and claim_data.preferred_contact_time not in valid_contact_times:
            raise ValueError(f"Invalid preferred contact time. Must be one of: {', '.join(valid_contact_times)}")

        # Create claim
        new_claim = Claim(
            user_id=user_id,
            category=claim_data.category,
            subcategory=claim_data.subcategory,
            incident_date=claim_data.incident_date,
            incident_summary=claim_data.incident_summary,
            claim_data=claim_data.claim_data,
            appointment_requested=claim_data.appointment_requested,
            contact_preference=claim_data.contact_preference,
            preferred_contact_time=claim_data.preferred_contact_time,
            additional_notes=claim_data.additional_notes,
            status="submitted"
        )

        db.add(new_claim)
        db.commit()  # Let database exceptions bubble
        db.refresh(new_claim)

        # Log the action
        insurance_description = f"{new_claim.category}"
        if new_claim.subcategory:
            insurance_description += f" - {new_claim.subcategory}"

        AuditLogService.log_user_action(
            db=db,
            user_id=user_id,
            action="CLAIM_SUBMITTED",
            entity_type="Claim",
            entity_id=new_claim.id,
            details=f"User submitted a {insurance_description} insurance claim report"
        )

        # TODO: Send email notification to admin (Slice 7: Email & Notifications)

        return new_claim

    @staticmethod
    def get_user_claims(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[Claim]:
        """
        Get all claims for a specific user with pagination.

        Args:
            db: Database session
            user_id: ID of the user
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return

        Returns:
            List of Claim objects
        """
        return db.query(Claim).filter(
            Claim.user_id == user_id
        ).order_by(Claim.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_claim_by_id(db: Session, claim_id: int, user_id: int) -> Optional[Claim]:
        """
        Get a single claim by its ID.
        Ensures that the user requesting the claim is the owner.

        Args:
            db: Database session
            claim_id: ID of the claim
            user_id: ID of the user making the request

        Returns:
            Claim object if found and user is owner, None if not found

        Raises:
            PermissionError: If user doesn't own the claim
        """
        claim = db.query(Claim).filter(Claim.id == claim_id).first()

        if not claim:
            return None

        if claim.user_id != user_id:
            # In a real-world scenario with admin roles, you would add a role check here
            raise PermissionError("You do not have permission to view this claim")

        return claim

    @staticmethod
    def delete_claim(db: Session, claim_id: int, user_id: int) -> bool:
        """
        Delete (cancel) a claim report.
        Only allows deletion if claim status is SUBMITTED.
        Only the owner can delete their claim.

        Args:
            db: Database session
            claim_id: ID of the claim to delete
            user_id: ID of the user making the request

        Returns:
            True if deleted successfully, False if claim not found

        Raises:
            PermissionError: If user doesn't own the claim
            ValueError: If claim is not in SUBMITTED status
        """
        # Get the claim and verify ownership
        claim = ClaimService.get_claim_by_id(db, claim_id, user_id)

        if not claim:
            return False

        # Only allow deletion if status is SUBMITTED
        if claim.status != "submitted":
            raise ValueError("Only claims with SUBMITTED status can be cancelled")

        # Log the action before deletion
        insurance_description = f"{claim.category}"
        if claim.subcategory:
            insurance_description += f" - {claim.subcategory}"

        AuditLogService.log_user_action(
            db=db,
            user_id=user_id,
            action="CLAIM_CANCELLED",
            entity_type="Claim",
            entity_id=claim.id,
            details=f"User cancelled {insurance_description} claim report"
        )

        # Delete the claim
        db.delete(claim)
        db.commit()  # Let database exceptions bubble

        return True
