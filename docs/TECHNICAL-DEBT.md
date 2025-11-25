# Technical Debt

**Last Updated**: 2025-11-06 | **Total Issues**: 35 (6 Critical, 14 High, 8 Medium, 7 Low)

Living document tracking outstanding issues. Items removed when fixed.

---

## CRITICAL (Must Fix Immediately) - 6 Issues

### Enum Case Mismatch - SYSTEM BROKEN
- **Files**: `backend/app/models/claim.py:7-11`, `backend/app/models/quote_request.py:7-12`
- **Problem**: Python enums use lowercase (`"pending"`), DB migration uses uppercase (`'PENDING'`)
- **Impact**: All quote/claim submissions fail with constraint violations
- **Fix**: Change enum values to uppercase: `PENDING = "PENDING"` (not `"pending"`)

### Hardcoded Credentials in Git
- **File**: `docker-compose.dev.yml:10-13, 35-36`
- **Problem**: `MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD`, `JWT_SECRET_KEY` hardcoded
- **Impact**: Credential compromise for anyone with repo access
- **Fix**: Move to `.env` file (gitignored), use Docker secrets, generate 256+ bit JWT secret

### XSS Vulnerability - Unescaped JSON
- **File**: `frontend/src/views/QuoteDetailPage.vue:47`
- **Problem**: `<pre>{{ JSON.stringify(quote.quote_data, null, 2) }}</pre>` renders user input directly
- **Impact**: Malicious content executes when admins view quotes
- **Fix**: Sanitize or render specific fields individually

### Missing CSRF Protection
- **Files**: All API endpoints
- **Problem**: No CSRF validation on POST/PUT/DELETE, vulnerable if cookies added
- **Impact**: CSRF attacks possible if auth method changes
- **Fix**: Document bearer-only auth OR add `fastapi-csrf-protect`

### Async/Await Inconsistency
- **Files**: `backend/app/services/quote_service.py:42`, `backend/app/services/auth_service.py:47, 84`
- **Problem**: `AuditLogService.log_user_action()` is async but uses sync DB ops, inconsistently awaited
- **Impact**: Potential deadlocks, silent failures
- **Fix**: Make synchronous OR use SQLAlchemy 2.0 async

### Information Disclosure in Errors
- **File**: `backend/app/middleware/exception_handler.py:48-59`
- **Problem**: Error handler leaks DB errors, file paths, internal logic via fragile string matching
- **Impact**: Sensitive data exposed to users
- **Fix**: Generic messages in production, detailed logs server-side only

---

## HIGH SEVERITY (Fix Before Shipping) - 14 Issues

### Missing Input Validation - Quote Data
- **File**: `backend/app/schemas/quote_schemas.py:11`
- **Problem**: `quote_data: Dict[str, Any]` accepts any JSON without validation
- **Impact**: DoS via large payloads, malicious content storage, no required field enforcement
- **Fix**: Create typed schemas per insurance category (`AutoQuoteData`, `HomeQuoteData`)

### No Rate Limiting
- **Files**: All API endpoints
- **Problem**: No rate limits on auth or quote submission
- **Impact**: Brute force, spam submissions, DoS
- **Fix**: Use `slowapi`: `@limiter.limit("5/minute")`

### Weak Password Policy
- **File**: `backend/app/schemas/auth.py:12`
- **Problem**: Only 8 chars minimum, no complexity requirements
- **Impact**: Users can use "password" or "12345678"
- **Fix**: Require 12+ chars, uppercase, digit, special char via `@field_validator`

### JWT Token Not Invalidated on Logout
- **File**: `frontend/src/stores/auth.ts:22-27`
- **Problem**: Logout clears client token only, JWT valid 24h
- **Impact**: Stolen tokens work for 24h post-logout
- **Fix**: Token blacklist or refresh token pattern

### Missing Database Indexes
- **File**: `backend/alembic/versions/3d9ff851fab5_initial_schema_with_category_subcategory.py`
- **Problem**: No indexes on `attachments.entity_id:26`, `audit_logs.entity_id:91`
- **Impact**: Poor query performance on joins/filters
- **Fix**: Add `op.create_index()` for FKs

### Sensitive Data in localStorage
- **File**: `frontend/src/stores/auth.ts:17-19`
- **Problem**: Full profile (email, phone) in unencrypted localStorage
- **Impact**: PII accessible to any script (XSS exposure)
- **Fix**: Store only username/id, fetch profile from API

### Wrong Exception Types
- **File**: `backend/app/services/quote_service.py:89-98`
- **Problem**: Raises `ValueError` (not 404), `PermissionError` (not 403)
- **Impact**: Returns 500 instead of correct status codes
- **Fix**: Use `HTTPException` with proper status codes

### No Input Sanitization on Text Fields
- **Files**: `frontend/src/components/quote-forms/VehicleInfoFields.vue` (multiple)
- **Problem**: VIN lacks checksum validation, addresses accept unlimited special chars
- **Impact**: Rendering issues, potential injection
- **Fix**: Add validation regex in backend schemas

### Missing Transaction Management
- **File**: `backend/app/services/quote_service.py:24-49`
- **Problem**: Quote creation and audit log separate commits
- **Impact**: Data inconsistency if audit fails
- **Fix**: Single transaction or make audit optional

### Potential N+1 Query Problem
- **File**: `backend/app/services/quote_service.py:67-69`
- **Problem**: Gets all quotes without eager loading
- **Impact**: N+1 queries when relationships added
- **Fix**: Use `joinedload()` preemptively

### Overly Permissive CORS
- **File**: `backend/app/main.py:14-21`
- **Problem**: `allow_headers=["*"]`, `allow_methods=["*"]`
- **Impact**: Security risk
- **Fix**: Explicit lists: `["GET", "POST", "PUT", "DELETE", "OPTIONS"]`, `["Content-Type", "Authorization"]`

### No Pagination on Quote List
- **File**: `backend/app/routers/quotes.py:31-40`
- **Problem**: Returns all user quotes
- **Impact**: Performance degrades over time
- **Fix**: Add `skip` and `limit` params

### Client-Side Only Auth Check
- **File**: `frontend/src/router/index.ts:92-104`
- **Problem**: No token expiration check in route guard
- **Impact**: Poor UX with expired tokens
- **Fix**: Check expiration before routing

### Deprecated DateTime Usage
- **File**: `backend/app/core/security.py:25-27`
- **Problem**: `datetime.utcnow()` deprecated in Python 3.12+
- **Impact**: Future compatibility, timezone bugs
- **Fix**: Use `datetime.now(timezone.utc)`

---

## MEDIUM PRIORITY - 8 Issues

### Code Duplication - Insurance Name Mapping
- **Files**: `frontend/src/views/DashboardPage.vue:168-209`, `frontend/src/views/QuoteDetailPage.vue:105-146`
- **Problem**: `getInsuranceName()` duplicated
- **Fix**: Extract to `src/utils/insuranceHelpers.ts`

### Magic Numbers in Frontend
- **Files**: Multiple Vue components
- **Problem**: Hardcoded countdown (10s at `QuoteRequestPage.vue:137`), char limits (1000)
- **Fix**: Constants file, sync frontend/backend

### No Frontend Service Logging
- **File**: `frontend/src/services/quotes.ts`
- **Problem**: API calls have no logging/monitoring
- **Fix**: Add structured logging

### Phone Number Validation Mismatch
- **Files**: `backend/app/schemas/auth.py:11` (12 chars), `frontend/src/utils/formatters.ts:14-30` (adds dots)
- **Problem**: Backend allows 12 chars, frontend formats with dots
- **Fix**: Backend allow 20 chars for international

### Missing Disposable Email Check
- **File**: `backend/app/schemas/auth.py:9`
- **Problem**: Uses `EmailStr` but allows disposable domains
- **Fix**: Custom validator to block disposable emails

### console.log in Production
- **File**: `frontend/src/views/QuoteRequestPage.vue:304`
- **Problem**: Debug log left in code
- **Fix**: Remove or use configurable logging

### Inconsistent Error Handling
- **Files**: Multiple Vue components
- **Problem**: Mix of inline errors, modals, console.log
- **Fix**: Standardize on toast notifications

### Missing Email Verification
- **File**: `backend/app/services/auth_service.py`
- **Problem**: Registration doesn't verify email
- **Impact**: Fake emails, no recovery, spam accounts
- **Fix**: Implement verification flow (Slice 7 placeholder exists)

---

## LOW PRIORITY / SUGGESTIONS - 7 Issues

### Type Safety - Quote Data Interface
- **File**: `frontend/src/services/quotes.ts:3-4`
- **Problem**: `[key: string]: any` defeats TypeScript
- **Fix**: Discriminated union of specific quote types

### Missing API Documentation
- **File**: `backend/app/main.py`
- **Problem**: FastAPI auto-docs lack descriptions/examples
- **Fix**: Add OpenAPI metadata, examples, response schemas

### No Database Health Check
- **File**: `backend/app/main.py:41-43`
- **Problem**: Health endpoint doesn't ping DB
- **Fix**: Add DB connectivity check

### Incomplete VIN Validation
- **File**: `frontend/src/utils/formatters.ts:71-77`
- **Problem**: Removes invalid chars but no checksum validation
- **Fix**: Add check digit algorithm

### No Request ID Tracking
- **Files**: Middleware
- **Problem**: No correlation ID for log tracing
- **Fix**: Add request ID middleware

### Missing DB Connection Pool Config
- **File**: Infrastructure config
- **Problem**: No explicit pool settings
- **Fix**: Add SQLAlchemy pool size, timeout, overflow

### No Component Testing
- **Files**: Frontend components
- **Problem**: Complex validation with no tests
- **Fix**: Add Vitest for forms, formatters, submission

---

## TESTING GAPS

- **Backend**: No tests for services, routers, models
- **Frontend**: No component/integration tests
- **E2E**: No automated user flow tests
- **Load**: Quote submission not tested under load
- **Security**: No penetration testing or scans

**Target**: 80%+ service coverage, all endpoints, validation edge cases, auth flows, all insurance types

---

## DOCUMENTATION GAPS

- **API**: Minimal endpoint descriptions
- **Setup**: No environment setup guide
- **Architecture**: No ADRs (Architecture Decision Records)
- **Security**: No documented practices
- **Deployment**: No production guide

---

## IMMEDIATE ACTIONS

**System Broken**: Enum case mismatch
**Security**: Hardcoded credentials, XSS vulnerability
**Stability**: Async/await inconsistency
