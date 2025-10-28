from sqlalchemy.orm import Session
from app.models.contact_message import ContactMessage
from app.schemas.contact_schemas import ContactMessageCreate
from app.services.audit_log_service import AuditLogService
from typing import List, Optional


class ContactService:
    """Business logic for contact messages"""

    @staticmethod
    def create_contact_message(
        db: Session,
        contact_data: ContactMessageCreate,
        user_id: Optional[int] = None
    ) -> ContactMessage:
        """
        Create a new contact message.

        Args:
            db: Database session
            contact_data: Contact message data
            user_id: ID of the user (None for guest messages)

        Returns:
            Created ContactMessage object

        Raises:
            ValueError: If validation fails
        """
        # Validation is handled by Pydantic schema
        # Additional business rule validation can go here if needed

        new_message = ContactMessage(
            user_id=user_id,
            full_name=contact_data.full_name,
            email=contact_data.email,
            phone=contact_data.phone,
            subject=contact_data.subject,
            message=contact_data.message,
            status="new"
        )

        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        # Audit logging
        message_type = "Guest" if user_id is None else "User"
        AuditLogService.log_user_action(
            db=db,
            user_id=user_id,
            action="CONTACT_MESSAGE_CREATED",
            entity_type="ContactMessage",
            entity_id=new_message.id,
            details=f"{message_type} submitted contact message: {contact_data.subject}"
        )

        # TODO: Send email notification to admin (Slice 7: Email & Notifications)

        return new_message

    @staticmethod
    def get_user_messages(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[ContactMessage]:
        """
        Get all contact messages for a specific user.

        Args:
            db: Database session
            user_id: ID of the user
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of ContactMessage objects
        """
        return db.query(ContactMessage).filter(
            ContactMessage.user_id == user_id
        ).order_by(
            ContactMessage.created_at.desc()
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_message_detail(
        db: Session,
        message_id: int,
        user_id: int
    ) -> Optional[ContactMessage]:
        """
        Get a single contact message by its ID.
        Ensures that the user requesting the message is the owner.

        Args:
            db: Database session
            message_id: ID of the contact message
            user_id: ID of the user making the request

        Returns:
            ContactMessage object or None if not found

        Raises:
            PermissionError: If user doesn't own the message
        """
        message = db.query(ContactMessage).filter(
            ContactMessage.id == message_id
        ).first()

        if not message:
            return None

        # Check ownership - user can only access their own messages
        if message.user_id != user_id:
            raise PermissionError("You do not have permission to view this message")

        return message
