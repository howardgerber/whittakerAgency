from sqlalchemy.orm import Session
from app.models.quote_request import QuoteRequest
from app.schemas.quote_schemas import QuoteRequestCreate
from app.services.audit_log_service import AuditLogService
from typing import List


class QuoteService:
    """Business logic for quote requests"""

    @staticmethod
    def create_quote_request(db: Session, user_id: int, quote_data: QuoteRequestCreate) -> QuoteRequest:
        """
        Create a new quote request.

        Args:
            db: Database session
            user_id: ID of the user creating the quote
            quote_data: Quote request data

        Returns:
            Created QuoteRequest object
        """
        new_quote = QuoteRequest(
            user_id=user_id,
            category=quote_data.category,
            subcategory=quote_data.subcategory,
            quote_data=quote_data.quote_data,
            customer_notes=quote_data.customer_notes,
            status="pending"
        )

        db.add(new_quote)
        db.commit()
        db.refresh(new_quote)

        # Log the action
        insurance_description = f"{new_quote.category}"
        if new_quote.subcategory:
            insurance_description += f" - {new_quote.subcategory}"

        AuditLogService.log_user_action(
            db=db,
            user_id=user_id,
            action="QUOTE_REQUEST_CREATED",
            entity_type="QuoteRequest",
            entity_id=new_quote.id,
            details=f"User requested a {insurance_description} insurance quote"
        )

        # TODO: Send email notification to admin (Slice 7: Email & Notifications)

        return new_quote

    @staticmethod
    def get_user_quote_requests(db: Session, user_id: int) -> List[QuoteRequest]:
        """
        Get all quote requests for a specific user.

        Args:
            db: Database session
            user_id: ID of the user

        Returns:
            List of QuoteRequest objects
        """
        return db.query(QuoteRequest).filter(
            QuoteRequest.user_id == user_id
        ).order_by(QuoteRequest.created_at.desc()).all()

    @staticmethod
    def get_quote_request_by_id(db: Session, quote_id: int, user_id: int) -> QuoteRequest:
        """
        Get a single quote request by its ID.
        Ensures that the user requesting the quote is the owner.

        Args:
            db: Database session
            quote_id: ID of the quote request
            user_id: ID of the user making the request

        Returns:
            QuoteRequest object

        Raises:
            ValueError: If quote not found
            PermissionError: If user doesn't own the quote
        """
        quote = db.query(QuoteRequest).filter(QuoteRequest.id == quote_id).first()

        if not quote:
            raise ValueError(f"Quote request {quote_id} not found")

        if quote.user_id != user_id:
            # In a real-world scenario with admin roles, you would add a role check here
            raise PermissionError("You do not have permission to view this quote request")

        return quote
