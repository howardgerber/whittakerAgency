# Backend Architecture Patterns

**Project:** Whittaker Agency
**Created:** 2025-10-23
**Based on:** SageSteppe exception handling patterns

---

## Overview

This document defines the architectural patterns for the FastAPI backend, particularly focusing on **thin controllers**, **service layer business logic**, **global exception handling**, and **comprehensive logging**.

---

## Core Principles

### 1. Thin Controllers (Routers in FastAPI)

**Controllers should ONLY:**
- Accept HTTP requests
- Validate request data (via Pydantic schemas)
- Call service layer methods
- Return HTTP responses
- Handle explicit null/false checks for semantic clarity

**Controllers should NOT:**
- Contain business logic
- Catch exceptions (except for very specific cases)
- Perform database operations directly
- Transform data beyond basic serialization

### 2. Service Layer Pattern

**Services contain ALL business logic:**
- Data validation and business rule enforcement
- Database operations (via ORM)
- Orchestration of multiple operations
- Exception throwing with meaningful messages

**Services should:**
- Throw appropriate exception types:
  - `ValueError` for validation errors (maps to 400 Bad Request)
  - `KeyError` for not found errors (maps to 404 Not Found)
  - Custom exceptions as needed
- Include meaningful error messages in exceptions
- Return `None` or `False` for "not found" cases where appropriate
- Let database exceptions bubble up naturally

**Services should NOT:**
- Catch exceptions unless transforming them
- Return HTTP status codes
- Access request/response objects

### 3. Global Exception Handling

**GlobalExceptionMiddleware handles:**
- All unhandled exceptions
- Automatic HTTP status code mapping
- Comprehensive logging to SystemLog
- User context tracking (from JWT)
- IP address tracking
- Request details (path, method)

**Status Code Mappings:**
```python
ValueError -> 400 Bad Request
KeyError -> 404 Not Found
PermissionError -> 403 Forbidden
LookupError -> 404 Not Found
All others -> 500 Internal Server Error
```

### 4. Dual Logging System

**System Log:**
- All exceptions (via GlobalExceptionMiddleware)
- System-level events
- Database errors
- Performance issues
- Uses separate database context to prevent logging failures

**Audit Log:**
- User actions (successful operations)
- Data modifications
- Authentication events
- Business-critical operations
- Logged in service layer for successful operations

---

## Exception Handling Strategy

### When to Let Exceptions Bubble

✅ **DO let bubble up:**
- Database connection errors
- ORM exceptions
- Validation errors (ValueError)
- Not found errors (KeyError)
- Permission errors (PermissionError)
- Any exception with a meaningful message

### When to Catch Exceptions

❌ **DO NOT catch exceptions in controllers** except for:
- Very specific scenarios where you need to transform exception types
- Cleanup operations in finally blocks

✅ **DO catch in services** when:
- Transforming one exception type to another more meaningful type
- Adding context to an exception message
- Wrapping external library exceptions

### Exception Best Practices

**Good Exception Throwing (in Services):**
```python
# Validation error
if not email:
    raise ValueError("Email is required")

# Not found
user = await db.get(User, user_id)
if not user:
    raise KeyError(f"User with ID {user_id} not found")

# Business rule violation
if duplicate_exists:
    raise ValueError("A user with this email already exists")
```

**Bad Exception Handling (in Controllers):**
```python
# DON'T DO THIS - let GlobalExceptionMiddleware handle it
try:
    result = await service.create_user(data)
    return result
except ValueError as e:
    return JSONResponse(status_code=400, content={"message": str(e)})
except Exception as e:
    logger.error(f"Error creating user: {e}")
    return JSONResponse(status_code=500, content={"message": "Internal error"})
```

**Good Controller Pattern:**
```python
# DO THIS - thin controller, let exceptions bubble
@router.post("/users")
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    result = await user_service.create_user(db, data)
    logger.info(f"User created: {result.id}")  # Audit log success
    return result
```

---

## Logging Strategy

### System Log (Error Logging)

**What to log:**
- All exceptions (automatically by GlobalExceptionMiddleware)
- Database connection issues
- External API failures
- Performance warnings

**Where to log:**
- GlobalExceptionMiddleware (automatic)
- Critical system operations

**Format:**
```python
# Automatic in GlobalExceptionMiddleware
{
    "timestamp": "2025-10-23T10:30:00Z",
    "level": "ERROR",
    "user_id": 123,
    "user_name": "john@example.com",
    "ip_address": "192.168.1.1",
    "request_path": "/api/v1/users",
    "request_method": "POST",
    "exception_type": "ValueError",
    "exception_message": "Email is required",
    "stack_trace": "..."
}
```

### Audit Log (Success Logging)

**What to log:**
- User registrations
- Login/logout events
- Quote requests submitted
- Claim requests submitted
- Contact messages sent
- Data modifications (CRUD operations)

**Where to log:**
- Service layer (after successful operations)

**Format:**
```python
# In service layer after success
await audit_log_service.log(
    user_id=user.id,
    action="USER_REGISTERED",
    details=f"User {user.email} registered successfully",
    entity_type="User",
    entity_id=user.id
)
```

### When to Use Each Logger

**Use structured logging (logger.info/error):**
```python
# Success logging in controllers
logger.info(f"Quote request created: ID={result.id}, User={current_user.email}")

# NEVER log errors in controllers - let GlobalExceptionMiddleware handle it
```

**Use AuditLog service:**
```python
# In service layer after successful business operations
await audit_log_service.log_user_action(
    user_id=user.id,
    action="QUOTE_REQUESTED",
    details={"insurance_type": quote.insurance_type}
)
```

---

## Folder Structure

```
backend/
├── app/
│   ├── routers/              # Controllers (thin, route handlers)
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── quotes.py         # Quote request endpoints
│   │   ├── claims.py         # Claim request endpoints
│   │   ├── contact.py        # Contact form endpoints
│   │   ├── team.py           # Team members endpoints
│   │   └── users.py          # User profile endpoints
│   │
│   ├── services/             # Business logic layer
│   │   ├── auth_service.py   # Authentication logic
│   │   ├── quote_service.py  # Quote request logic
│   │   ├── claim_service.py  # Claim request logic
│   │   ├── contact_service.py
│   │   ├── team_service.py
│   │   ├── user_service.py
│   │   ├── audit_log_service.py
│   │   └── email_service.py  # Brevo integration
│   │
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── quote_request.py
│   │   ├── claim_request.py
│   │   ├── contact_message.py
│   │   ├── team_member.py
│   │   ├── system_log.py
│   │   └── audit_log.py
│   │
│   ├── schemas/              # Pydantic models (request/response)
│   │   ├── auth.py
│   │   ├── quote.py
│   │   ├── claim.py
│   │   ├── contact.py
│   │   ├── team.py
│   │   └── user.py
│   │
│   ├── middleware/           # Custom middleware
│   │   ├── exception_handler.py  # GlobalExceptionMiddleware
│   │   └── logging_middleware.py
│   │
│   ├── core/                 # Core configuration
│   │   ├── config.py         # Settings (env vars)
│   │   ├── database.py       # Database connection
│   │   ├── security.py       # JWT, password hashing
│   │   └── logging_config.py
│   │
│   ├── utils/                # Utility functions
│   │   ├── email.py
│   │   └── validators.py
│   │
│   └── main.py               # FastAPI app entry point
│
└── alembic/                  # Database migrations
    ├── versions/
    └── env.py
```

---

## Example: Quote Request Flow

### 1. Router (Thin Controller)

**File:** `backend/app/routers/quotes.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.quote import QuoteRequestCreate, QuoteRequestResponse
from app.services.quote_service import QuoteService
from app.models.user import User
import logging

router = APIRouter(prefix="/api/v1/quotes", tags=["quotes"])
logger = logging.getLogger(__name__)

@router.post("", response_model=QuoteRequestResponse)
async def create_quote_request(
    quote_data: QuoteRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new quote request.
    Requires authentication.
    """
    # Thin controller - just call service
    result = await QuoteService.create_quote_request(db, current_user.id, quote_data)

    # Audit log success
    logger.info(
        f"Quote request created",
        extra={
            "quote_id": result.id,
            "user_id": current_user.id,
            "insurance_type": result.insurance_type
        }
    )

    return result


@router.get("", response_model=list[QuoteRequestResponse])
async def get_user_quote_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all quote requests for current user.
    """
    # Thin controller - just call service
    return await QuoteService.get_user_quote_requests(db, current_user.id)
```

### 2. Service (Business Logic)

**File:** `backend/app/services/quote_service.py`

```python
from sqlalchemy.orm import Session
from app.models.quote_request import QuoteRequest
from app.schemas.quote import QuoteRequestCreate
from app.services.email_service import EmailService
from app.services.audit_log_service import AuditLogService
from typing import List

class QuoteService:

    @staticmethod
    async def create_quote_request(
        db: Session,
        user_id: int,
        quote_data: QuoteRequestCreate
    ) -> QuoteRequest:
        """
        Create a new quote request.

        Raises:
            ValueError: If validation fails
        """
        # Business rule validation
        if not quote_data.insurance_type:
            raise ValueError("Insurance type is required")

        valid_types = [
            "Auto", "Home", "Business", "Life",
            "Health", "Motorcycle", "Boat", "Rental"
        ]
        if quote_data.insurance_type not in valid_types:
            raise ValueError(f"Invalid insurance type. Must be one of: {', '.join(valid_types)}")

        # Create quote request
        quote = QuoteRequest(
            user_id=user_id,
            insurance_type=quote_data.insurance_type,
            preferred_contact_method=quote_data.preferred_contact_method,
            message=quote_data.message,
            status="Pending"
        )

        db.add(quote)
        db.commit()
        db.refresh(quote)

        # Log to audit log
        await AuditLogService.log_user_action(
            db=db,
            user_id=user_id,
            action="QUOTE_REQUESTED",
            entity_type="QuoteRequest",
            entity_id=quote.id,
            details={"insurance_type": quote.insurance_type}
        )

        # Send email notification (async, non-blocking)
        try:
            await EmailService.send_quote_notification(quote)
        except Exception as e:
            # Log email failure but don't fail the operation
            import logging
            logging.error(f"Failed to send quote notification email: {e}")

        return quote

    @staticmethod
    async def get_user_quote_requests(
        db: Session,
        user_id: int
    ) -> List[QuoteRequest]:
        """
        Get all quote requests for a user.
        """
        return db.query(QuoteRequest)\
            .filter(QuoteRequest.user_id == user_id)\
            .order_by(QuoteRequest.created_at.desc())\
            .all()
```

### 3. Global Exception Middleware

**File:** `backend/app/middleware/exception_handler.py`

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.system_log_service import SystemLogService
import logging

logger = logging.getLogger(__name__)

class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # Extract user context from JWT (if available)
            user_id = None
            user_email = None
            try:
                if hasattr(request.state, "user"):
                    user_id = request.state.user.id
                    user_email = request.state.user.email
            except:
                pass

            # Get client IP
            client_ip = request.client.host if request.client else "unknown"

            # Map exception types to HTTP status codes
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            if isinstance(exc, ValueError):
                status_code = status.HTTP_400_BAD_REQUEST
            elif isinstance(exc, KeyError):
                status_code = status.HTTP_404_NOT_FOUND
            elif isinstance(exc, PermissionError):
                status_code = status.HTTP_403_FORBIDDEN

            # Log to SystemLog (separate DB context)
            try:
                await SystemLogService.log_exception(
                    exception=exc,
                    user_id=user_id,
                    user_email=user_email,
                    ip_address=client_ip,
                    request_path=request.url.path,
                    request_method=request.method
                )
            except Exception as log_error:
                # If logging fails, at least log to console
                logger.error(f"Failed to write to SystemLog: {log_error}")

            # Return error response
            return JSONResponse(
                status_code=status_code,
                content={
                    "error": type(exc).__name__,
                    "message": str(exc)
                }
            )
```

---

## Key Takeaways from SageSteppe Analysis

### ✅ What Works Well

1. **Thin controllers** - All business logic in services
2. **Let exceptions bubble** - GlobalExceptionMiddleware handles everything
3. **Separate logging context** - Prevents logging failures from breaking operations
4. **Meaningful exception messages** - Services throw exceptions with clear messages
5. **Appropriate exception types** - ValueError for validation, KeyError for not found
6. **Explicit null checks** - Controllers check for None/False for semantic clarity

### ❌ What to Avoid

1. **Try-catch in controllers** - Redundant with global middleware
2. **Logging errors in controllers** - GlobalExceptionMiddleware logs everything
3. **Generic error messages** - Exception messages should be specific
4. **Swallowing exceptions** - Let them bubble unless transforming
5. **Business logic in controllers** - Belongs in services

---

## Testing Implications

### Controller Tests
- Should test that correct service methods are called
- Should test route parameters and authentication
- Should NOT test business logic

### Service Tests
- Should test all business rules
- Should test exception throwing
- Should test data transformations
- Should use mocked database

### Integration Tests
- Should test full request/response cycle
- Should test exception handling through middleware
- Should verify audit logging

---

**Document Version:** 1.0
**Last Updated:** 2025-10-23
