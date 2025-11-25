# FastAPI Exception Handling Architecture

## Overview

FastAPI exception handling requires **three independent mechanisms** working together:
1. **Exception handlers** - catch framework exceptions (Pydantic validation, HTTPException)
2. **Middleware** - catch service/business logic exceptions
3. Framework exceptions bypass middleware - handlers execute before middleware runs

All three log to `system_logs` table via `SystemLogService`.

## Core Rules

- **Routers (Controllers)**: NO try-except blocks, NO business logic - extract data, call services, return responses
- **Services**: Throw typed exceptions (ValueError, PermissionError, KeyError), validate all input
- **Exception handlers + Middleware**: Catch everything, log to SystemLog, return consistent error format

## The Three Exception Mechanisms

### 1. RequestValidationError Handler (Pydantic Validation)

**What it catches**: Request body/query parameter validation errors (422)

**When it runs**: BEFORE middleware, when Pydantic schema validation fails

**Purpose**: Log validation errors that would otherwise bypass middleware

**Registration**: `@app.exception_handler(RequestValidationError)`

### 2. HTTPException Handler

**What it catches**: FastAPI `HTTPException` raised anywhere in code

**When it runs**: BEFORE middleware

**Purpose**: Log and standardize HTTPException responses

**Registration**: `@app.exception_handler(HTTPException)`

### 3. Exception Middleware

**What it catches**: Service exceptions (ValueError, KeyError, PermissionError, etc.)

**When it runs**: AFTER exception handlers, during request/response cycle

**Purpose**: Catch business logic exceptions from services, map to HTTP status codes

**Registration**: `app.add_middleware(GlobalExceptionMiddleware)`

## Exception Type Mapping

| Exception Type | HTTP Status | Thrown By | Use Case |
|---|---|---|---|
| `RequestValidationError` | 422 | Pydantic | Request schema validation |
| `HTTPException` | Original status | FastAPI/Routers | Direct HTTP errors |
| `ValueError` | 400 | Services | Input validation, business rule violations |
| `PermissionError` | 403 | Services | Authorization failures |
| `KeyError` | 404 | Services | Resource not found (use custom `KeyNotFoundException`) |
| All others | 500 | Any | Unexpected errors (database, external APIs) |

## Architecture Patterns

### Exception Handler: RequestValidationError

**Purpose**: Log Pydantic validation errors (422) to SystemLog

**Key requirements**:
- Extract validation error details from `exc.errors()`
- Format error messages for user readability
- Log to SystemLog with request context (path, IP, user)
- Return 422 with error details

**Location**: `app/main.py` as decorated function

### Exception Handler: HTTPException

**Purpose**: Log FastAPI HTTPException to SystemLog

**Key requirements**:
- Preserve original status code from exception
- Extract error detail message
- Log to SystemLog with request context
- Return original status code with error detail

**Location**: `app/main.py` as decorated function

### Middleware: GlobalExceptionMiddleware

**Purpose**: Catch all service exceptions and map to HTTP status codes

**Key requirements**:
- Wrap `call_next()` in try-except
- Map exception types to status codes (ValueError→400, PermissionError→403, KeyError→404)
- Log to SystemLog with full stack trace
- Return JSONResponse with appropriate status code

**Location**: `app/middleware/exception_handler.py`

### SystemLogService

**Purpose**: Centralized logging to `system_logs` table

**Key requirements**:
- Use separate database session (not main request session)
- Accept exception details: type, message, stack trace
- Accept request context: path, IP, method, user ID
- Handle logging failures gracefully (don't crash on log failure)

**Location**: `app/services/system_log_service.py`

## Registration Order (main.py)

**CRITICAL**: Exception handlers must be registered BEFORE middleware

```python
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

app = FastAPI()

# 1. Exception handlers (catch framework exceptions)
@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    # Log to SystemLog, return 422
    pass

@app.exception_handler(HTTPException)
async def http_handler(request, exc):
    # Log to SystemLog, return original status
    pass

# 2. Middleware (catches service exceptions)
app.add_middleware(GlobalExceptionMiddleware)

# 3. Routers
app.include_router(products_router)
```

## Router Layer (Controllers)

Routers are thin - extract data, call services, check return values, respond.

**DO**:
- Extract data from request (path params, query params, request body)
- Call service methods
- Check for None/False return values explicitly
- Raise `HTTPException` or custom exceptions for not-found scenarios
- Return appropriate HTTP responses

**DON'T**:
- Add try-except blocks (let exceptions bubble)
- Add business logic or validation
- Log exceptions (handlers/middleware do this)
- Catch exceptions to return error responses

**Example**:
```python
@router.get("/{id}")
async def get_product(id: int, service: ProductService = Depends()):
    product = await service.get_product(id)
    if product is None:
        raise KeyNotFoundException(f"Product {id} not found")  # → 404
    return product

@router.post("/")
async def create_product(dto: CreateProductRequest, service: ProductService = Depends()):
    # Service throws ValueError on validation error → middleware returns 400
    product = await service.create_product(dto)
    return product
```

## Service Layer

Services contain ALL business logic.

**Validation**:
- Check input parameters (empty strings, negative numbers, invalid formats)
- Throw `ValueError` with specific, user-friendly messages
- Example: `raise ValueError("Product price must be greater than zero")`

**Business Rules**:
- Check for duplicates, invalid states, constraint violations
- Throw `ValueError` for business rule violations
- Example: `raise ValueError("SKU 'ABC123' already exists")`

**Authorization**:
- Check user permissions
- Throw `PermissionError` with specific message
- Example: `raise PermissionError("User cannot access this resource")`

**Not Found**:
- For GET operations: return `None`
- For UPDATE/DELETE operations: return `False`
- Router checks return value and raises exception if needed

**Database Operations**:
- Let database exceptions bubble up (IntegrityError, OperationalError, etc.)
- Middleware catches and maps to 500
- Convert to business exceptions only when adding user context

**Example**:
```python
async def create_product(self, dto: CreateProductRequest) -> ProductResponse:
    # Validation → ValueError (400)
    if not dto.name or dto.name.strip() == "":
        raise ValueError("Product name is required")
    if dto.price <= 0:
        raise ValueError("Product price must be greater than zero")

    # Business rules → ValueError (400)
    existing = await self.db.execute(select(Product).where(Product.sku == dto.sku))
    if existing.scalar_one_or_none():
        raise ValueError(f"SKU '{dto.sku}' already exists")

    # Database operations - let exceptions bubble
    product = Product(name=dto.name, sku=dto.sku, price=dto.price)
    self.db.add(product)
    await self.db.commit()  # IntegrityError bubbles → 500
    await self.db.refresh(product)

    return ProductResponse.model_validate(product)
```

### When Services CAN Use Try-Except

**1. Graceful Degradation (Non-critical Operations)**

```python
async def register_user(self, dto: CreateUserRequest) -> UserResponse:
    user = User(email=dto.email)
    self.db.add(user)
    await self.db.commit()  # Critical - let bubble

    try:
        await self.email_service.send_welcome_email(user.email)
    except Exception as ex:
        logger.warning(f"Welcome email failed: {ex}")
        # Don't fail registration

    return UserResponse.model_validate(user)
```

**2. Converting Database to Business Exceptions**

```python
async def delete_product(self, id: int):
    product = await self.db.get(Product, id)
    if product is None:
        return False

    try:
        await self.db.delete(product)
        await self.db.commit()
    except IntegrityError as ex:
        if "FOREIGN KEY" in str(ex):
            raise ValueError("Cannot delete product with active orders") from ex
        raise  # Re-throw if not FK constraint
```

**3. Adding Context Before Re-throwing**

```python
try:
    await self.external_api.verify_data(data)
except Exception as ex:
    logger.error(f"External API verification failed: {ex}")
    raise  # Re-throw so user is notified
```

## Logging

- **Exception handlers + middleware**: Log ALL exceptions to SystemLog table
- **Services**: Only log for graceful degradation or adding context before re-throw
- **Routers**: NEVER log - handlers/middleware do it

## Error Response Format

All three mechanisms return consistent JSON format:

```json
{
  "detail": "Product name is required"
}
```

For validation errors (422), include details:

```json
{
  "detail": "name: field required; price: value must be greater than 0",
  "errors": [
    {"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"},
    {"loc": ["body", "price"], "msg": "value must be greater than 0", "type": "value_error"}
  ]
}
```

## Testing

**Unit Tests**: Expect exceptions thrown from services

```python
async def test_create_product_invalid_price():
    with pytest.raises(ValueError, match="price must be greater than zero"):
        await service.create_product(CreateProductRequest(name="Test", price=-10))
```

**Integration Tests**: Expect proper HTTP status codes and error format

```python
async def test_create_product_returns_400(client):
    response = await client.post("/api/products", json={"name": "Test", "price": -10})
    assert response.status_code == 400
    assert "price must be greater than zero" in response.json()["detail"]
```

## Custom Exceptions

Define custom exceptions for clearer intent:

```python
class KeyNotFoundException(Exception):
    """Raised when a resource is not found (maps to 404)"""
    pass

class BusinessRuleViolation(ValueError):
    """Raised when business rule is violated (maps to 400)"""
    pass
```

Register custom exceptions in middleware:

```python
if isinstance(exc, KeyNotFoundException):
    status_code = status.HTTP_404_NOT_FOUND
```

## Migration Checklist

- [ ] Create `RequestValidationError` exception handler in main.py
- [ ] Create `HTTPException` exception handler in main.py
- [ ] Create `GlobalExceptionMiddleware` in middleware/exception_handler.py
- [ ] Create or update `SystemLogService` with separate database session
- [ ] Register exception handlers BEFORE middleware in main.py
- [ ] Add middleware after exception handlers
- [ ] Remove all try-except blocks from routers
- [ ] Review services - ensure proper exception types (ValueError, PermissionError, KeyError)
- [ ] Define custom exceptions (KeyNotFoundException, etc.)
- [ ] Update service layer to throw appropriate exceptions
- [ ] Verify all three mechanisms log to SystemLog
- [ ] Update unit tests to expect exceptions from services
- [ ] Update integration tests to expect proper status codes

## Common Pitfalls

**FastAPI-Specific**:
- ❌ Only using middleware - misses RequestValidationError (422) and HTTPException
- ❌ Only using exception handlers - misses service exceptions (ValueError, KeyError)
- ❌ Wrong registration order - middleware added before exception handlers
- ❌ Creating SystemLogService instance in handlers - should use dependency injection
- ❌ Using `raise HTTPException(400)` in services - use `ValueError` instead
- ❌ Not defining custom exceptions - relying on generic KeyError instead of KeyNotFoundException
- ❌ Catching all exceptions in routers - defeats the purpose of centralized handling

**General**:
- ❌ Try-except in routers (controllers)
- ❌ Business logic in routers
- ❌ Returning None/False from services on validation errors (hides errors from users)
- ❌ Generic exception messages ("Invalid input", "Error occurred")
- ❌ Logging to main database session instead of separate session
- ❌ Swallowing exceptions in services without re-throwing

## Key Differences: .NET vs FastAPI

| Aspect | .NET | FastAPI |
|---|---|---|
| **Handler Count** | ONE global middleware | THREE separate mechanisms |
| **Validation Errors** | Caught by middleware | Caught by RequestValidationError handler |
| **HTTP Exceptions** | Caught by middleware | Caught by HTTPException handler |
| **Service Exceptions** | Caught by middleware | Caught by middleware |
| **Execution Order** | All → middleware | Framework → handlers, then middleware |
| **Registration** | Single middleware | Handlers + middleware (order matters) |

## Quick Reference

### When to Throw vs Return None/False

- **Throw ValueError**: Invalid input, business rule violations
- **Throw PermissionError**: Authorization failures
- **Throw KeyNotFoundException**: Resource not found (custom exception)
- **Return None**: Entity not found in GET operations
- **Return False**: Entity not found in UPDATE/DELETE operations
- **NEVER**: Catch exceptions to return None/False

### Service Method Patterns

- **GET**: Return `Optional[EntityDto]` - None if not found, throw on errors
- **POST**: Return `EntityDto` - throw ValueError on validation/business rule errors
- **PUT**: Return `bool` - False if not found, throw ValueError on validation errors
- **DELETE**: Return `bool` - False if not found, throw ValueError on constraint violations
