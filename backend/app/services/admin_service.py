from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_, desc
from typing import List, Optional, Tuple
from datetime import datetime, date, timedelta

from app.models.quote_request import QuoteRequest
from app.models.claim import Claim
from app.models.contact_message import ContactMessage
from app.models.user import User
from app.schemas.admin_schemas import (
    DashboardStatsResponse,
    QuoteStats,
    ClaimStats,
    MessageStats,
    UserStats,
    RecentActivityItemSummary,
    RecentActivityItem,
    AttentionItem,
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
    UserActivitySummary,
)
from app.services.audit_log_service import AuditLogService


class AdminService:
    """Business logic for admin dashboard and management"""

    # ===== Dashboard Methods =====

    @staticmethod
    def get_dashboard_stats(db: Session) -> DashboardStatsResponse:
        """
        Get summary statistics for admin dashboard.

        Args:
            db: Database session

        Returns:
            Dashboard statistics with nested structure
        """
        # Quote stats - calculate all required counts
        quotes_pending = db.query(QuoteRequest).filter(QuoteRequest.status == "pending").count()
        quotes_in_review = db.query(QuoteRequest).filter(QuoteRequest.status == "in_review").count()
        quotes_quoted = db.query(QuoteRequest).filter(QuoteRequest.status == "quoted").count()
        quotes_total = db.query(QuoteRequest).count()

        # Claim stats - calculate all required counts
        claims_submitted = db.query(Claim).filter(Claim.status == "submitted").count()
        claims_contacted = db.query(Claim).filter(Claim.status == "contacted").count()
        claims_closed = db.query(Claim).filter(Claim.status == "closed").count()
        claims_total = db.query(Claim).count()

        # Message stats - calculate all required counts
        messages_new = db.query(ContactMessage).filter(ContactMessage.status == "new").count()
        messages_read = db.query(ContactMessage).filter(ContactMessage.status == "read").count()
        messages_responded = db.query(ContactMessage).filter(ContactMessage.status == "responded").count()
        messages_closed = db.query(ContactMessage).filter(ContactMessage.status == "closed").count()
        messages_total = db.query(ContactMessage).count()

        # User stats - calculate all required counts
        users_active = db.query(User).filter(User.is_active == True).count()
        users_inactive = db.query(User).filter(User.is_active == False).count()
        users_total = db.query(User).count()

        # Get recent activity (last 10 items across all types)
        recent_activity = AdminService._get_recent_activity_summary(db, limit=10)

        return DashboardStatsResponse(
            quotes=QuoteStats(
                pending=quotes_pending,
                in_review=quotes_in_review,
                quoted=quotes_quoted,
                total=quotes_total,
            ),
            claims=ClaimStats(
                submitted=claims_submitted,
                contacted=claims_contacted,
                closed=claims_closed,
                total=claims_total,
            ),
            messages=MessageStats(
                new=messages_new,
                read=messages_read,
                responded=messages_responded,
                closed=messages_closed,
                total=messages_total,
            ),
            users=UserStats(
                active=users_active,
                inactive=users_inactive,
                total=users_total,
            ),
            recent_activity=recent_activity,
        )

    @staticmethod
    def _get_recent_activity_summary(db: Session, limit: int = 10) -> List[RecentActivityItemSummary]:
        """
        Get recent activity summary for dashboard (simplified format).

        Args:
            db: Database session
            limit: Maximum number of items to return

        Returns:
            List of recent activity items in simplified format
        """
        activities = []

        # Get recent quotes with user info
        recent_quotes = (
            db.query(QuoteRequest, User.full_name)
            .join(User)
            .order_by(QuoteRequest.created_at.desc())
            .limit(limit)
            .all()
        )

        for quote, customer_name in recent_quotes:
            activities.append({
                "type": "quote",
                "customer": customer_name,
                "action": "submitted" if quote.status == "pending" else quote.status,
                "date": quote.created_at,
            })

        # Get recent claims with user info
        recent_claims = (
            db.query(Claim, User.full_name)
            .join(User)
            .order_by(Claim.created_at.desc())
            .limit(limit)
            .all()
        )

        for claim, customer_name in recent_claims:
            activities.append({
                "type": "claim",
                "customer": customer_name,
                "action": claim.status,
                "date": claim.created_at,
            })

        # Get recent messages (both authenticated and guest)
        recent_messages = (
            db.query(ContactMessage)
            .order_by(ContactMessage.created_at.desc())
            .limit(limit)
            .all()
        )

        for message in recent_messages:
            activities.append({
                "type": "message",
                "customer": message.full_name,
                "action": message.status,
                "date": message.created_at,
            })

        # Sort all activities by date and take the most recent
        activities.sort(key=lambda x: x["date"], reverse=True)
        activities = activities[:limit]

        return [RecentActivityItemSummary(**activity) for activity in activities]

    @staticmethod
    def get_recent_activity(db: Session, limit: int = 10) -> List[RecentActivityItem]:
        """
        Get recent activity across all submission types.

        Args:
            db: Database session
            limit: Maximum number of items to return (default: 10)

        Returns:
            List of recent activity items
        """
        activities = []

        # Get recent quotes
        recent_quotes = (
            db.query(QuoteRequest, User.full_name, User.email)
            .join(User)
            .order_by(QuoteRequest.created_at.desc())
            .limit(limit)
            .all()
        )

        for quote, customer_name, _ in recent_quotes:
            activities.append({
                "id": quote.id,
                "type": "quote",
                "customer_name": customer_name,
                "category": quote.category,
                "subject": None,
                "status": quote.status,
                "created_at": quote.created_at,
            })

        # Get recent claims
        recent_claims = (
            db.query(Claim, User.full_name, User.email)
            .join(User)
            .order_by(Claim.created_at.desc())
            .limit(limit)
            .all()
        )

        for claim, customer_name, _ in recent_claims:
            activities.append({
                "id": claim.id,
                "type": "claim",
                "customer_name": customer_name,
                "category": claim.category,
                "subject": None,
                "status": claim.status,
                "created_at": claim.created_at,
            })

        # Get recent messages (both authenticated and guest)
        recent_messages = (
            db.query(ContactMessage)
            .order_by(ContactMessage.created_at.desc())
            .limit(limit)
            .all()
        )

        for message in recent_messages:
            activities.append({
                "id": message.id,
                "type": "message",
                "customer_name": message.full_name,
                "category": None,
                "subject": message.subject,
                "status": message.status,
                "created_at": message.created_at,
            })

        # Sort all activities by created_at and take the most recent
        activities.sort(key=lambda x: x["created_at"], reverse=True)
        activities = activities[:limit]

        return [RecentActivityItem(**activity) for activity in activities]

    @staticmethod
    def get_attention_items(db: Session) -> AttentionItemsResponse:
        """
        Get items requiring admin attention based on age and submission patterns.

        Business logic:
        1. Age-based triggers:
           - Quotes with status "pending" or "in_review" for > 2 days
           - Claims with status "submitted" for > 2 days
           - Messages with status "new" or "read" (any age)

        2. Multiple submissions (grouped by user):
           - Users with 2+ quotes in "pending" or "in_review" status
           - Users with 2+ claims in "submitted" status

        3. Appointment reminders:
           - Quotes with appointment_date = today
           - Claims with appointment_requested = today
           - Messages with appointment_date = today

        Args:
            db: Database session

        Returns:
            AttentionItemsResponse with sorted list of attention items
        """
        items = []
        now = datetime.utcnow()
        two_days_ago = now - timedelta(days=2)

        # 1. Age-based: Overdue quotes (pending or in_review > 2 days)
        overdue_quotes = (
            db.query(QuoteRequest, User.full_name)
            .join(User)
            .filter(
                QuoteRequest.status.in_(["pending", "in_review"]),
                QuoteRequest.created_at < two_days_ago
            )
            .all()
        )

        for quote, customer_name in overdue_quotes:
            age_days = (now - quote.created_at).days
            items.append(AttentionItem(
                type="quote",
                id=quote.id,
                user_id=quote.user_id,
                customer_name=customer_name,
                title=f"Quote Request - {quote.category}",
                category="Overdue",
                detail=f"Status: {quote.status.replace('_', ' ').title()}",
                age=AdminService._format_age(age_days),
                priority="high" if age_days > 5 else "medium",
                icon="⚠️",
                link=f"/admin/quotes/{quote.id}"
            ))

        # 2. Age-based: Overdue claims (submitted > 2 days)
        overdue_claims = (
            db.query(Claim, User.full_name)
            .join(User)
            .filter(
                Claim.status == "submitted",
                Claim.created_at < two_days_ago
            )
            .all()
        )

        for claim, customer_name in overdue_claims:
            age_days = (now - claim.created_at).days
            items.append(AttentionItem(
                type="claim",
                id=claim.id,
                user_id=claim.user_id,
                customer_name=customer_name,
                title=f"Claim - {claim.category}",
                category="Overdue",
                detail=f"Incident: {claim.incident_date.strftime('%m/%d/%Y')}",
                age=AdminService._format_age(age_days),
                priority="high" if age_days > 5 else "medium",
                icon="⚠️",
                link=f"/admin/claims/{claim.id}"
            ))

        # 3. Age-based: New or unread messages (any age)
        unread_messages = (
            db.query(ContactMessage)
            .filter(ContactMessage.status.in_(["new", "read"]))
            .all()
        )

        for message in unread_messages:
            age_days = (now - message.created_at).days
            items.append(AttentionItem(
                type="message",
                id=message.id,
                user_id=message.user_id,
                customer_name=message.full_name,
                title=f"Message - {message.subject.replace('_', ' ').title()}",
                category="New Message" if message.status == "new" else "Unread Message",
                detail=message.message[:50] + "..." if len(message.message) > 50 else message.message,
                age=AdminService._format_age(age_days),
                priority="high" if message.status == "new" else "medium",
                icon="📧",
                link=f"/admin/messages/{message.id}"
            ))

        # 4. Multiple submissions: Users with 2+ pending/in_review quotes
        multiple_quotes = (
            db.query(
                User.id,
                User.full_name,
                func.count(QuoteRequest.id).label("quote_count")
            )
            .join(QuoteRequest)
            .filter(QuoteRequest.status.in_(["pending", "in_review"]))
            .group_by(User.id, User.full_name)
            .having(func.count(QuoteRequest.id) >= 2)
            .all()
        )

        for user_id, customer_name, quote_count in multiple_quotes:
            items.append(AttentionItem(
                type="multiple_quotes",
                id=None,
                user_id=user_id,
                customer_name=customer_name,
                title=f"{quote_count} Pending Quotes",
                category="Multiple Submissions",
                detail=f"User has {quote_count} active quote requests",
                age="Multiple submissions",
                priority="medium",
                icon="📊",
                link=f"/admin/users/{user_id}"
            ))

        # 5. Multiple submissions: Users with 2+ submitted claims
        multiple_claims = (
            db.query(
                User.id,
                User.full_name,
                func.count(Claim.id).label("claim_count")
            )
            .join(Claim)
            .filter(Claim.status == "submitted")
            .group_by(User.id, User.full_name)
            .having(func.count(Claim.id) >= 2)
            .all()
        )

        for user_id, customer_name, claim_count in multiple_claims:
            items.append(AttentionItem(
                type="multiple_claims",
                id=None,
                user_id=user_id,
                customer_name=customer_name,
                title=f"{claim_count} Submitted Claims",
                category="Multiple Submissions",
                detail=f"User has {claim_count} active claims",
                age="Multiple submissions",
                priority="medium",
                icon="📊",
                link=f"/admin/users/{user_id}"
            ))

        # 6. Appointments scheduled for today
        today = now.date()

        # Appointments from quotes
        quote_appointments = (
            db.query(QuoteRequest, User.full_name)
            .join(User)
            .filter(QuoteRequest.appointment_date == today)
            .all()
        )

        for quote, customer_name in quote_appointments:
            items.append(AttentionItem(
                type="appointment",
                id=quote.id,
                user_id=quote.user_id,
                customer_name=customer_name,
                title=f"Appointment Today - {quote.category}",
                category="Appointment",
                detail=f"Quote request appointment",
                age="Today",
                priority="high",
                icon="📅",
                link=f"/admin/quotes/{quote.id}"
            ))

        # Appointments from claims
        claim_appointments = (
            db.query(Claim, User.full_name)
            .join(User)
            .filter(Claim.appointment_requested == today)
            .all()
        )

        for claim, customer_name in claim_appointments:
            items.append(AttentionItem(
                type="appointment",
                id=claim.id,
                user_id=claim.user_id,
                customer_name=customer_name,
                title=f"Appointment Today - {claim.category}",
                category="Appointment",
                detail=f"Claim appointment",
                age="Today",
                priority="high",
                icon="📅",
                link=f"/admin/claims/{claim.id}"
            ))

        # Appointments from messages
        message_appointments = (
            db.query(ContactMessage)
            .filter(ContactMessage.appointment_date == today)
            .all()
        )

        for message in message_appointments:
            items.append(AttentionItem(
                type="appointment",
                id=message.id,
                user_id=message.user_id,
                customer_name=message.full_name,
                title=f"Appointment Today - {message.subject.replace('_', ' ').title()}",
                category="Appointment",
                detail=f"Contact message appointment",
                age="Today",
                priority="high",
                icon="📅",
                link=f"/admin/messages/{message.id}"
            ))

        # Sort by priority (high first) then by age (oldest first)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        items.sort(key=lambda x: (
            priority_order.get(x.priority, 3),
            0 if x.age in ["Multiple submissions", "Today"] else -int(x.age.split()[0]) if x.age.split()[0].isdigit() else 0
        ))

        return AttentionItemsResponse(items=items)

    @staticmethod
    def _format_age(days: int) -> str:
        """
        Format age in days to human-readable string.

        Args:
            days: Number of days old

        Returns:
            Human-readable age string
        """
        if days == 0:
            return "Today"
        elif days == 1:
            return "1 day old"
        else:
            return f"{days} days old"

    # ===== Quote Management Methods =====

    @staticmethod
    def get_all_quotes(
        db: Session,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> Tuple[List[AdminQuoteListItem], int]:
        """
        Get all quote requests with optional filtering and pagination.

        Args:
            db: Database session
            category: Filter by category
            subcategory: Filter by subcategory
            status: Filter by status
            search: Search by customer name or email
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Tuple of (list of quotes, total count)
        """
        query = db.query(QuoteRequest, User.full_name, User.email).join(User)

        # Apply filters
        if category:
            query = query.filter(QuoteRequest.category == category)
        if subcategory:
            query = query.filter(QuoteRequest.subcategory == subcategory)
        if status:
            query = query.filter(QuoteRequest.status == status)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.full_name.ilike(search_term),
                    User.email.ilike(search_term)
                )
            )

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        results = query.order_by(QuoteRequest.created_at.desc()).offset(offset).limit(limit).all()

        # Build response items
        items = [
            AdminQuoteListItem(
                id=quote.id,
                customer_name=customer_name,
                customer_email=customer_email,
                category=quote.category,
                subcategory=quote.subcategory,
                status=quote.status,
                quote_amount=quote.quote_amount,
                created_at=quote.created_at,
                updated_at=quote.updated_at,
            )
            for quote, customer_name, customer_email in results
        ]

        return items, total

    @staticmethod
    def get_quote_detail(db: Session, quote_id: int) -> Optional[AdminQuoteDetail]:
        """
        Get full details for a specific quote.

        Args:
            db: Database session
            quote_id: ID of the quote

        Returns:
            Quote detail or None if not found
        """
        result = (
            db.query(QuoteRequest, User.full_name, User.email, User.phone)
            .join(User)
            .filter(QuoteRequest.id == quote_id)
            .first()
        )

        if not result:
            return None

        quote, customer_name, customer_email, customer_phone = result

        return AdminQuoteDetail(
            id=quote.id,
            user_id=quote.user_id,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            category=quote.category,
            subcategory=quote.subcategory,
            status=quote.status,
            quote_data=quote.quote_data,
            customer_notes=quote.customer_notes,
            agent_notes=quote.agent_notes,
            quote_amount=quote.quote_amount,
            quoted_at=quote.quoted_at,
            created_at=quote.created_at,
            updated_at=quote.updated_at,
        )

    @staticmethod
    def update_quote(
        db: Session,
        quote_id: int,
        update_data: AdminQuoteUpdate,
        admin_user_id: int,
    ) -> Optional[AdminQuoteDetail]:
        """
        Update a quote request (admin only).

        Args:
            db: Database session
            quote_id: ID of the quote to update
            update_data: Update data
            admin_user_id: ID of the admin user making the update

        Returns:
            Updated quote detail or None if not found

        Raises:
            ValueError: If status is invalid
        """
        quote = db.query(QuoteRequest).filter(QuoteRequest.id == quote_id).first()

        if not quote:
            return None

        # Validate status if provided
        valid_statuses = ["pending", "in_review", "quoted", "accepted", "declined"]
        if update_data.status and update_data.status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

        # Track changes for audit log
        changes = {}

        # Update fields
        if update_data.status is not None:
            if quote.status != update_data.status:
                changes["status"] = {"old": quote.status, "new": update_data.status}
                quote.status = update_data.status
                if update_data.status == "quoted":
                    quote.quoted_at = datetime.utcnow()

        if update_data.quote_amount is not None:
            if quote.quote_amount != update_data.quote_amount:
                changes["quote_amount"] = {"old": float(quote.quote_amount) if quote.quote_amount else None, "new": float(update_data.quote_amount)}
                quote.quote_amount = update_data.quote_amount

        if update_data.agent_notes is not None:
            if quote.agent_notes != update_data.agent_notes:
                changes["agent_notes"] = {"updated": True}
                quote.agent_notes = update_data.agent_notes

        # Commit changes
        db.commit()
        db.refresh(quote)

        # Audit logging
        if changes:
            AuditLogService.log_user_action(
                db=db,
                user_id=admin_user_id,
                action="QUOTE_UPDATED_BY_ADMIN",
                entity_type="QuoteRequest",
                entity_id=quote.id,
                details=f"Admin updated quote request: {changes}",
            )

        # Return updated detail
        return AdminService.get_quote_detail(db, quote_id)

    # ===== Claim Management Methods =====

    @staticmethod
    def get_all_claims(
        db: Session,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> Tuple[List[AdminClaimListItem], int]:
        """
        Get all claims with optional filtering and pagination.

        Args:
            db: Database session
            category: Filter by category
            subcategory: Filter by subcategory
            status: Filter by status
            search: Search by customer name or email
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Tuple of (list of claims, total count)
        """
        query = db.query(Claim, User.full_name, User.email).join(User)

        # Apply filters
        if category:
            query = query.filter(Claim.category == category)
        if subcategory:
            query = query.filter(Claim.subcategory == subcategory)
        if status:
            query = query.filter(Claim.status == status)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.full_name.ilike(search_term),
                    User.email.ilike(search_term)
                )
            )

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        results = query.order_by(Claim.created_at.desc()).offset(offset).limit(limit).all()

        # Build response items
        items = [
            AdminClaimListItem(
                id=claim.id,
                customer_name=customer_name,
                customer_email=customer_email,
                category=claim.category,
                subcategory=claim.subcategory,
                incident_date=claim.incident_date,
                status=claim.status,
                created_at=claim.created_at,
                updated_at=claim.updated_at,
            )
            for claim, customer_name, customer_email in results
        ]

        return items, total

    @staticmethod
    def get_claim_detail(db: Session, claim_id: int) -> Optional[AdminClaimDetail]:
        """
        Get full details for a specific claim.

        Args:
            db: Database session
            claim_id: ID of the claim

        Returns:
            Claim detail or None if not found
        """
        result = (
            db.query(Claim, User.full_name, User.email, User.phone)
            .join(User)
            .filter(Claim.id == claim_id)
            .first()
        )

        if not result:
            return None

        claim, customer_name, customer_email, customer_phone = result

        return AdminClaimDetail(
            id=claim.id,
            user_id=claim.user_id,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            category=claim.category,
            subcategory=claim.subcategory,
            incident_date=claim.incident_date,
            incident_summary=claim.incident_summary,
            claim_data=claim.claim_data,
            appointment_requested=claim.appointment_requested,
            contact_preference=claim.contact_preference,
            preferred_contact_time=claim.preferred_contact_time,
            additional_notes=claim.additional_notes,
            status=claim.status,
            admin_notes=claim.admin_notes,
            contacted_at=claim.contacted_at,
            created_at=claim.created_at,
            updated_at=claim.updated_at,
        )

    @staticmethod
    def update_claim(
        db: Session,
        claim_id: int,
        update_data: AdminClaimUpdate,
        admin_user_id: int,
    ) -> Optional[AdminClaimDetail]:
        """
        Update a claim (admin only).

        Args:
            db: Database session
            claim_id: ID of the claim to update
            update_data: Update data
            admin_user_id: ID of the admin user making the update

        Returns:
            Updated claim detail or None if not found

        Raises:
            ValueError: If status is invalid
        """
        claim = db.query(Claim).filter(Claim.id == claim_id).first()

        if not claim:
            return None

        # Validate status if provided
        valid_statuses = ["submitted", "contacted", "closed"]
        if update_data.status and update_data.status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

        # Track changes for audit log
        changes = {}

        # Update fields
        if update_data.status is not None:
            if claim.status != update_data.status:
                changes["status"] = {"old": claim.status, "new": update_data.status}
                claim.status = update_data.status
                if update_data.status == "contacted":
                    claim.contacted_at = datetime.utcnow()

        if update_data.admin_notes is not None:
            if claim.admin_notes != update_data.admin_notes:
                changes["admin_notes"] = {"updated": True}
                claim.admin_notes = update_data.admin_notes

        if update_data.appointment_requested is not None:
            if claim.appointment_requested != update_data.appointment_requested:
                changes["appointment_requested"] = {
                    "old": str(claim.appointment_requested) if claim.appointment_requested else None,
                    "new": str(update_data.appointment_requested)
                }
                claim.appointment_requested = update_data.appointment_requested

        # Commit changes
        db.commit()
        db.refresh(claim)

        # Audit logging
        if changes:
            AuditLogService.log_user_action(
                db=db,
                user_id=admin_user_id,
                action="CLAIM_UPDATED_BY_ADMIN",
                entity_type="Claim",
                entity_id=claim.id,
                details=f"Admin updated claim: {changes}",
            )

        # Return updated detail
        return AdminService.get_claim_detail(db, claim_id)

    # ===== Contact Message Management Methods =====

    @staticmethod
    def get_all_messages(
        db: Session,
        subject: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        include_guest: bool = True,
        page: int = 1,
        limit: int = 20,
    ) -> Tuple[List[AdminMessageListItem], int]:
        """
        Get all contact messages with optional filtering and pagination.

        Args:
            db: Database session
            subject: Filter by subject
            status: Filter by status
            search: Search by sender name or email
            include_guest: Whether to include guest messages
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Tuple of (list of messages, total count)
        """
        query = db.query(ContactMessage)

        # Apply filters
        if subject:
            query = query.filter(ContactMessage.subject == subject)
        if status:
            query = query.filter(ContactMessage.status == status)
        if not include_guest:
            query = query.filter(ContactMessage.user_id.isnot(None))
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    ContactMessage.full_name.ilike(search_term),
                    ContactMessage.email.ilike(search_term)
                )
            )

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        results = query.order_by(ContactMessage.created_at.desc()).offset(offset).limit(limit).all()

        # Build response items
        items = [
            AdminMessageListItem(
                id=message.id,
                sender_name=message.full_name,
                sender_email=message.email,
                subject=message.subject,
                status=message.status,
                is_guest=(message.user_id is None),
                admin_response=message.admin_response,
                created_at=message.created_at,
                updated_at=message.updated_at,
            )
            for message in results
        ]

        return items, total

    @staticmethod
    def get_message_detail(db: Session, message_id: int) -> Optional[AdminMessageDetail]:
        """
        Get full details for a specific contact message.

        Args:
            db: Database session
            message_id: ID of the message

        Returns:
            Message detail or None if not found
        """
        message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()

        if not message:
            return None

        return AdminMessageDetail(
            id=message.id,
            user_id=message.user_id,
            sender_name=message.full_name,
            sender_email=message.email,
            sender_phone=message.phone,
            subject=message.subject,
            message=message.message,
            status=message.status,
            is_guest=(message.user_id is None),
            admin_response=message.admin_response,
            responded_at=message.responded_at,
            created_at=message.created_at,
            updated_at=message.updated_at,
        )

    @staticmethod
    def update_message(
        db: Session,
        message_id: int,
        update_data: AdminMessageUpdate,
        admin_user_id: int,
    ) -> Optional[AdminMessageDetail]:
        """
        Update a contact message (admin only).

        Args:
            db: Database session
            message_id: ID of the message to update
            update_data: Update data
            admin_user_id: ID of the admin user making the update

        Returns:
            Updated message detail or None if not found

        Raises:
            ValueError: If status is invalid
        """
        message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()

        if not message:
            return None

        # Validate status if provided
        valid_statuses = ["new", "read", "responded", "closed"]
        if update_data.status and update_data.status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

        # Track changes for audit log
        changes = {}

        # Update fields
        if update_data.status is not None:
            if message.status != update_data.status:
                changes["status"] = {"old": message.status, "new": update_data.status}
                message.status = update_data.status

        if update_data.admin_response is not None:
            if message.admin_response != update_data.admin_response:
                changes["admin_response"] = {"updated": True}
                message.admin_response = update_data.admin_response
                message.responded_at = datetime.utcnow()
                # Auto-update status to responded if not already
                if message.status == "new" or message.status == "read":
                    message.status = "responded"
                    changes["status"] = {"auto_updated": "responded"}

        # Commit changes
        db.commit()
        db.refresh(message)

        # Audit logging
        if changes:
            AuditLogService.log_user_action(
                db=db,
                user_id=admin_user_id,
                action="MESSAGE_UPDATED_BY_ADMIN",
                entity_type="ContactMessage",
                entity_id=message.id,
                details=f"Admin updated message: {changes}",
            )

        # Return updated detail
        return AdminService.get_message_detail(db, message_id)

    # ===== User Management Methods =====

    @staticmethod
    def get_all_users(
        db: Session,
        status: Optional[str] = None,
        search: Optional[str] = None,
        recently_contacted: Optional[str] = None,
        sort_by: str = "activity",
        sort_order: str = "desc",
        page: int = 1,
        limit: int = 20,
    ) -> Tuple[List[AdminUserListItem], int]:
        """
        Get all users with optional filtering, sorting, and pagination.

        Args:
            db: Database session
            status: Filter by account status ("active" or "inactive")
            search: Search by username, email, or full name
            recently_contacted: Filter by recent activity ("2weeks", "1month", "3months", "6months", "1year")
            sort_by: Sort field ("activity", "name", "status")
            sort_order: Sort order ("asc" or "desc")
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Tuple of (list of users, total count)

        Raises:
            ValueError: If sort_by or sort_order is invalid
        """
        # Validate sort parameters
        valid_sort_by = ["activity", "name", "status"]
        if sort_by not in valid_sort_by:
            raise ValueError(f"Invalid sort_by. Must be one of: {', '.join(valid_sort_by)}")

        valid_sort_order = ["asc", "desc"]
        if sort_order not in valid_sort_order:
            raise ValueError(f"Invalid sort_order. Must be one of: {', '.join(valid_sort_order)}")

        # Calculate the most recent activity across quotes, claims, and messages
        # Using separate MAX calls and then GREATEST in the outer query
        max_quote_date = func.max(QuoteRequest.created_at)
        max_claim_date = func.max(Claim.created_at)
        max_message_date = func.max(ContactMessage.created_at)

        # Use GREATEST to find the most recent date across all three
        # COALESCE handles NULL values (when user has no activity of that type)
        last_activity = func.greatest(
            func.coalesce(max_quote_date, '1970-01-01'),
            func.coalesce(max_claim_date, '1970-01-01'),
            func.coalesce(max_message_date, '1970-01-01')
        ).label("last_activity")

        # Base query with counts for quotes, claims, messages, and last activity
        query = (
            db.query(
                User,
                func.count(QuoteRequest.id.distinct()).label("quotes_count"),
                func.count(Claim.id.distinct()).label("claims_count"),
                func.count(ContactMessage.id.distinct()).label("messages_count"),
                last_activity,
            )
            .outerjoin(QuoteRequest, User.id == QuoteRequest.user_id)
            .outerjoin(Claim, User.id == Claim.user_id)
            .outerjoin(ContactMessage, User.id == ContactMessage.user_id)
            .group_by(User.id)
        )

        # Apply filters
        if status:
            if status == "active":
                query = query.filter(User.is_active == True)
            elif status == "inactive":
                query = query.filter(User.is_active == False)
            else:
                raise ValueError("Invalid status. Must be 'active' or 'inactive'")

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.username.ilike(search_term),
                    User.email.ilike(search_term),
                    User.full_name.ilike(search_term)
                )
            )

        if recently_contacted:
            # Calculate cutoff date based on recently_contacted filter
            now = datetime.now()
            if recently_contacted == "2weeks":
                cutoff_date = now - timedelta(days=14)
            elif recently_contacted == "1month":
                cutoff_date = now - timedelta(days=30)
            elif recently_contacted == "3months":
                cutoff_date = now - timedelta(days=90)
            elif recently_contacted == "6months":
                cutoff_date = now - timedelta(days=180)
            elif recently_contacted == "1year":
                cutoff_date = now - timedelta(days=365)
            else:
                raise ValueError("Invalid recently_contacted value")

            # Filter users who have activity after cutoff date
            query = query.having(last_activity >= cutoff_date)

        # Apply sorting
        if sort_by == "activity":
            # Sort by last activity (using COALESCE we already have old date for nulls, so no need for nullslast)
            if sort_order == "asc":
                query = query.order_by(last_activity.asc())
            else:
                query = query.order_by(last_activity.desc())
        elif sort_by == "name":
            order_col = User.full_name
            if sort_order == "asc":
                query = query.order_by(order_col.asc())
            else:
                query = query.order_by(order_col.desc())
        elif sort_by == "status":
            order_col = User.is_active
            if sort_order == "asc":
                query = query.order_by(order_col.asc())
            else:
                query = query.order_by(order_col.desc())
        else:
            # Default to activity
            if sort_order == "asc":
                query = query.order_by(last_activity.asc())
            else:
                query = query.order_by(last_activity.desc())

        # Get total count (before pagination)
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        results = query.offset(offset).limit(limit).all()

        # Get last login info from audit logs
        user_ids = [user.id for user, _, _, _, _ in results]
        last_logins = AdminService._get_last_logins(db, user_ids)

        # Build response items
        items = [
            AdminUserListItem(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
                email=user.email,
                phone=user.phone,
                is_active=user.is_active,
                is_admin=user.is_admin,
                created_at=user.created_at,
                last_login_at=last_logins.get(user.id),
                quotes_count=quotes_count,
                claims_count=claims_count,
                messages_count=messages_count,
            )
            for user, quotes_count, claims_count, messages_count, _ in results
        ]

        return items, total

    @staticmethod
    def _get_last_logins(db: Session, user_ids: List[int]) -> dict:
        """
        Get last login timestamps for a list of users.

        Args:
            db: Database session
            user_ids: List of user IDs

        Returns:
            Dictionary mapping user_id to last login datetime
        """
        from app.models.audit_log import AuditLog

        if not user_ids:
            return {}

        # Get most recent LOGIN action for each user
        subquery = (
            db.query(
                AuditLog.user_id,
                func.max(AuditLog.created_at).label("last_login")
            )
            .filter(
                AuditLog.user_id.in_(user_ids),
                AuditLog.action == "LOGIN"
            )
            .group_by(AuditLog.user_id)
            .subquery()
        )

        results = db.query(subquery).all()
        return {user_id: last_login for user_id, last_login in results}

    @staticmethod
    def get_user_detail(db: Session, user_id: int, date_range: Optional[str] = None) -> Optional[AdminUserDetail]:
        """
        Get full details for a specific user including activity summary.

        Args:
            db: Database session
            user_id: ID of the user
            date_range: Optional date range filter for activity ("30days", "6months", "ytd", "last_year", "all")

        Returns:
            User detail with activity or None if not found
        """
        # Get user with counts
        result = (
            db.query(
                User,
                func.count(QuoteRequest.id.distinct()).label("quotes_count"),
                func.count(Claim.id.distinct()).label("claims_count"),
                func.count(ContactMessage.id.distinct()).label("messages_count"),
            )
            .outerjoin(QuoteRequest, User.id == QuoteRequest.user_id)
            .outerjoin(Claim, User.id == Claim.user_id)
            .outerjoin(ContactMessage, User.id == ContactMessage.user_id)
            .filter(User.id == user_id)
            .group_by(User.id)
            .first()
        )

        if not result:
            return None

        user, quotes_count, claims_count, messages_count = result

        # Get last login
        last_logins = AdminService._get_last_logins(db, [user_id])
        last_login_at = last_logins.get(user_id)

        # Get activity summary with date range filter
        activity = AdminService._get_user_activity(db, user_id, date_range)

        return AdminUserDetail(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login_at=last_login_at,
            quotes_count=quotes_count,
            claims_count=claims_count,
            messages_count=messages_count,
            activity=activity,
        )

    @staticmethod
    def _get_user_activity(db: Session, user_id: int, date_range: Optional[str] = None) -> UserActivitySummary:
        """
        Get activity summary for a user with optional date filtering.

        Args:
            db: Database session
            user_id: User ID
            date_range: Optional date range filter ("30days", "6months", "ytd", "last_year", "all")

        Returns:
            UserActivitySummary with activity filtered by date range
        """
        # Calculate date filter
        date_filter = None
        if date_range and date_range != "all":
            now = datetime.utcnow()
            if date_range == "30days":
                date_filter = now - timedelta(days=30)
            elif date_range == "6months":
                date_filter = now - timedelta(days=180)
            elif date_range == "ytd":
                date_filter = datetime(now.year, 1, 1)
            elif date_range == "last_year":
                date_filter = datetime(now.year - 1, 1, 1)

        # Build base queries with date filter
        quotes_query = db.query(QuoteRequest).filter(QuoteRequest.user_id == user_id)
        claims_query = db.query(Claim).filter(Claim.user_id == user_id)
        messages_query = db.query(ContactMessage).filter(ContactMessage.user_id == user_id)

        if date_filter:
            quotes_query = quotes_query.filter(QuoteRequest.created_at >= date_filter)
            claims_query = claims_query.filter(Claim.created_at >= date_filter)
            messages_query = messages_query.filter(ContactMessage.created_at >= date_filter)

        # Get all quotes (no limit)
        recent_quotes = quotes_query.order_by(QuoteRequest.created_at.desc()).all()

        quotes_list = [
            {
                "id": q.id,
                "category": q.category,
                "status": q.status,
                "created_at": q.created_at.isoformat(),
            }
            for q in recent_quotes
        ]

        # Get all claims (no limit)
        recent_claims = claims_query.order_by(Claim.created_at.desc()).all()

        claims_list = [
            {
                "id": c.id,
                "category": c.category,
                "status": c.status,
                "created_at": c.created_at.isoformat(),
            }
            for c in recent_claims
        ]

        # Get all messages (no limit)
        recent_messages = messages_query.order_by(ContactMessage.created_at.desc()).all()

        messages_list = [
            {
                "id": m.id,
                "subject": m.subject,
                "status": m.status,
                "created_at": m.created_at.isoformat(),
            }
            for m in recent_messages
        ]

        # Combine all activity (no longer used, but kept for backward compatibility)
        all_activity = []

        for q in recent_quotes:
            all_activity.append({
                "type": "quote",
                "id": q.id,
                "category": q.category,
                "status": q.status,
                "created_at": q.created_at.isoformat(),
                "timestamp": q.created_at,
            })

        for c in recent_claims:
            all_activity.append({
                "type": "claim",
                "id": c.id,
                "category": c.category,
                "status": c.status,
                "created_at": c.created_at.isoformat(),
                "timestamp": c.created_at,
            })

        for m in recent_messages:
            all_activity.append({
                "type": "message",
                "id": m.id,
                "subject": m.subject,
                "status": m.status,
                "created_at": m.created_at.isoformat(),
                "timestamp": m.created_at,
            })

        # Sort by timestamp
        all_activity.sort(key=lambda x: x["timestamp"], reverse=True)

        # Remove timestamp field (used only for sorting)
        for item in all_activity:
            del item["timestamp"]

        return UserActivitySummary(
            quotes=quotes_list,
            claims=claims_list,
            messages=messages_list,
            recent_activity=all_activity,
        )

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        update_data: AdminUserUpdate,
        admin_user_id: int,
    ) -> Optional[AdminUserDetail]:
        """
        Update a user (admin only).

        Args:
            db: Database session
            user_id: ID of the user to update
            update_data: Update data
            admin_user_id: ID of the admin user making the update

        Returns:
            Updated user detail or None if not found

        Raises:
            ValueError: If trying to update own admin status
        """
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        # Prevent admin from removing their own admin privileges
        if user_id == admin_user_id and update_data.is_admin is False:
            raise ValueError("Cannot remove your own admin privileges")

        # Track changes for audit log
        changes = {}

        # Update fields
        if update_data.is_active is not None:
            if user.is_active != update_data.is_active:
                changes["is_active"] = {"old": user.is_active, "new": update_data.is_active}
                user.is_active = update_data.is_active

        if update_data.is_admin is not None:
            if user.is_admin != update_data.is_admin:
                changes["is_admin"] = {"old": user.is_admin, "new": update_data.is_admin}
                user.is_admin = update_data.is_admin

        # Commit changes
        db.commit()
        db.refresh(user)

        # Audit logging
        if changes:
            AuditLogService.log_user_action(
                db=db,
                user_id=admin_user_id,
                action="USER_UPDATED_BY_ADMIN",
                entity_type="User",
                entity_id=user.id,
                details=f"Admin updated user: {changes}",
            )

        # Return updated detail
        return AdminService.get_user_detail(db, user_id)
