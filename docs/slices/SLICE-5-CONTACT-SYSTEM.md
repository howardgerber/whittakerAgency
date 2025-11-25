# Slice 5: Contact System & Dashboard Completion

**Estimated Time:** 4-6 hours
**Dependencies:** Slice 1, 2, 3, and 4 must be complete
**Status:** Not Started

---

## Overview

Public contact form allowing anyone (authenticated or guest) to send messages to the insurance agency. Authenticated users can view their message history and admin responses in their dashboard. Simple, low-stakes communication channel for general questions.

**Key Concept:** "Have a question? Send us a message - we'll get back to you soon."

**Design Pattern:**
- Public form accessible to everyone (auth optional)
- If user is authenticated, link message to user_id for dashboard tracking
- If not authenticated, user_id = null (guest message stored but not shown in user dashboard)
- Admin view of all messages (authenticated + guest) deferred to Slice 6

---

## Goals

- [ ] Create public contact form (no authentication required)
- [ ] Implement backend API for contact message submission and retrieval
- [ ] Add contact messages section to user dashboard
- [ ] Create message detail view with admin response display
- [ ] Enable authenticated users to track their message history

**Not Goals:**
- ❌ No admin message management interface (Slice 6)
- ❌ No email notifications (Slice 7)
- ❌ No real-time chat or messaging
- ❌ No file attachments

---

## Features to Implement

### 1. Public Contact Form

**Route:** `/contact` (public, no auth required)

**Form Fields:**
- [ ] Full name (required, use `ValidationRules.fullName`)
- [ ] Email (required, use `ValidationRules.email`)
- [ ] Phone (optional, format XXX.XXX.XXXX, use `formatPhoneNumber`)
- [ ] Subject (required, dropdown)
  - General Question
  - Quote Question
  - Claim Question
  - Policy Question
  - Other
- [ ] Message (required, textarea, 250 chars max, character counter)
- [ ] Submit button with loading state

**Form Behavior:**
- No authentication required - completely public
- If user IS logged in, capture user_id automatically (link to account)
- If user NOT logged in, user_id = null (guest message)
- Character counter on message field (red border when over limit)
- Submit button disabled until all required fields valid
- Success message: "Thanks for your message! We'll get back to you soon."
- For authenticated users: Add "View in Dashboard" link after submission

**Validation:**
- Full name: Shared validation from `@/utils/validation` (first + last)
- Email: Shared validation from `@/utils/validation`
- Phone: Optional, but if provided must match XXX.XXX.XXXX format
- Subject: Required dropdown selection
- Message: Required, 50-250 characters

---

### 2. Backend API Endpoints

```
POST /api/v1/contact/submit          - Submit contact message (no auth required)
GET  /api/v1/contact/messages        - Get user's messages (auth required)
GET  /api/v1/contact/{id}            - Get message details (auth required, owner only)
```

**API Details:**

**POST /api/v1/contact/submit**
- Public endpoint (no auth required)
- Accepts: full_name, email, phone (optional), subject, message
- If user is authenticated (token provided), capture user_id
- If no token, user_id = null (guest message)
- Returns: message_id, status, created_at

**GET /api/v1/contact/messages**
- Requires authentication
- Returns only messages where user_id matches authenticated user
- Pagination: 10 per page
- Sort: Most recent first (created_at DESC)
- Response includes: id, subject, created_at, status, admin_response (if exists)

**GET /api/v1/contact/{id}**
- Requires authentication
- User can only access their own messages (user_id check)
- Returns full message details + admin response (if exists)
- 403 if trying to access another user's message
- 404 if message not found

**Message Status:**
1. `new` - Just submitted, awaiting admin review
2. `read` - Admin has viewed the message
3. `responded` - Admin has replied
4. `closed` - Message resolved, no further action needed

---

### 3. Database Schema

**contact_messages table:**

```sql
- id (UUID, primary key)
- user_id (UUID, nullable, foreign key to users)  -- null for guest messages
- full_name (String(200), required)
- email (String(254), required)
- phone (String(12), nullable)                     -- format: XXX.XXX.XXXX
- subject (Enum, required)                         -- general, quote, claim, policy, other
- message (Text, required)                         -- customer's message
- status (Enum, required, default='new')          -- new, read, responded, closed
- admin_response (Text, nullable)                  -- admin's reply (Slice 6)
- responded_at (DateTime, nullable)                -- when admin replied
- created_at (DateTime, required)
- updated_at (DateTime, required)
```

**Indexes:**
- `user_id` - for user dashboard queries (null for guests)
- `status` - for admin filtering
- `created_at` - for sorting recent messages

**Privacy Note:**
- Regular users can only see their own messages in their dashboard
- Guest messages (user_id = null) have no associated user, so they only appear in admin dashboard
- Admin can view ALL messages - both guest messages and all authenticated user messages (Slice 6)

---

### 4. User Dashboard Integration

**Route:** `/dashboard` (protected)

**Add Contact Messages Section:**

**Section Layout:**
- [ ] Section header: "Contact Messages"
- [ ] "Send New Message" button (links to /contact)
- [ ] Messages table (shows only user's messages)
- [ ] Empty state: "No messages yet. Have a question? Send us a message!"

**Table Columns:**
- Subject (text + icon based on subject type)
- Submitted Date (formatted: "November 20, 2025")
- Status (colored badge)
- Actions (View button)

**Status Badges:**
- `new`: Blue background, "New"
- `read`: Yellow background, "Read"
- `responded`: Green background, "Responded"
- `closed`: Gray background, "Closed"

**Table Features:**
- Pagination (10 per page)
- Sort by date (most recent first)
- Responsive design (cards on mobile)
- Empty state with CTA

---

### 5. Message Detail View

**Route:** `/contact/{id}` (protected)

**Display Sections:**

**Message Information:**
- [ ] Message ID (small, gray text)
- [ ] Subject (large, bold)
- [ ] Status badge (prominent)
- [ ] Submitted date (formatted with time)

**Your Message:**
- [ ] Full name (readonly)
- [ ] Email (readonly)
- [ ] Phone (readonly, if provided)
- [ ] Message content (readonly, styled textarea)

**Our Response:**
- [ ] Show if admin_response exists
- [ ] Admin response text (styled, highlighted background)
- [ ] Responded date (if applicable)
- [ ] Hide section if no response yet ("We'll respond soon!")

**Actions:**
- [ ] "Reply" button (opens new contact form pre-filled with context)
  - Subject: "Re: [Original Subject]"
  - Message: Starts with quote of original message
- [ ] "Back to Dashboard" button

**No Response Yet Message:**
- "We received your message and will respond soon. Check back here or we'll email you when we reply."

---

## Technical Implementation

### Frontend Components

**File Structure:**
```
frontend/src/
├── views/
│   ├── ContactPage.vue           # Public contact form
│   └── ContactDetailPage.vue     # Message detail view (protected)
├── components/
│   └── dashboard/
│       └── ContactMessagesList.vue  # Messages table for dashboard
└── services/
    └── contact.ts                # API client
```

**Component Details:**

**ContactPage.vue** (Public)
- No authentication required
- Check if user is logged in (optional enhancement - pre-fill name/email)
- Form with full name, email, phone, subject, message
- Character counter on message field
- Loading state on submit
- Success message with "View in Dashboard" link (if authenticated)

**ContactDetailPage.vue** (Protected)
- Requires authentication
- Fetch message details on mount
- Display readonly message info
- Show admin response if exists
- "Reply" button opens contact form with context

**ContactMessagesList.vue** (Protected)
- Table of user's messages
- Status badges
- Pagination
- Empty state
- Mobile-responsive cards

### Backend Files

```
backend/app/
├── routers/
│   └── contact.py               # Contact endpoints
├── services/
│   └── contact_service.py       # Business logic
├── schemas/
│   └── contact_schemas.py       # Pydantic models
└── models/
    └── contact_message.py       # ContactMessage model
```

**Backend Implementation Notes:**

**contact.py (Router):**
- Thin controller, no business logic
- POST /submit: Optional authentication (check for token but don't require)
- GET /messages: Require authentication
- GET /{id}: Require authentication + ownership check
- No try-catch blocks (let exceptions bubble to middleware)

**contact_service.py (Service):**
- `create_message(data, user_id=None)`: Create message (user_id optional)
- `get_user_messages(user_id)`: Get all messages for user
- `get_message_by_id(message_id, user_id)`: Get single message (ownership check)
- Throw `PermissionError` if user tries to access another's message
- Throw `ValueError` for invalid input data

**contact_schemas.py (Schemas):**
- `ContactMessageCreate`: full_name, email, phone, subject, message
- `ContactMessageResponse`: id, subject, status, created_at, has_response
- `ContactMessageDetail`: full message + admin_response (if exists)

**contact_message.py (Model):**
- ContactMessage class with all fields
- Relationship to User (nullable)
- Enum for subject and status
- Timestamps (created_at, updated_at)

### Routes to Add

```typescript
// Public route
{
  path: '/contact',
  name: 'contact',
  component: ContactPage
},

// Protected route
{
  path: '/contact/:id',
  name: 'contact-detail',
  component: ContactDetailPage,
  meta: { requiresAuth: true }
}
```

---

## Form Validation

### Shared Utilities
- **Full name:** `ValidationRules.fullName` - validates "First Last" format
- **Email:** `ValidationRules.email` - standard email validation
- **Phone:** `ValidationRules.phone` - optional, XXX.XXX.XXXX format
- **Character counter:** Red border when over 250 chars

### Field Validation Rules

**Full Name:**
- Required
- Min 2 words (first + last)
- Max 200 characters
- Must contain letters

**Email:**
- Required
- Valid email format (RFC 5321)
- Max 254 characters

**Phone:**
- Optional
- If provided, must match XXX.XXX.XXXX exactly
- Use `formatPhoneNumber` formatter

**Subject:**
- Required
- Must select from dropdown options

**Message:**
- Required
- Min 50 characters
- Max 250 characters
- Character counter (gray → orange at 90% → red at 100%)
- Red border when invalid

### Form Submission Validation
- All required fields must be filled
- All fields must pass validation
- Submit button disabled until form valid
- Loading state prevents double-submission

---

## Design Specifications

### Contact Form (Public)

**Layout:**
- Single column, max-width 600px, centered
- Clean, minimal design
- Large, touch-friendly inputs
- Character counter below message field
- Submit button full-width on mobile

**Visual Design:**
- Label above each input
- Required fields marked with red asterisk
- Red border on invalid fields (no error text)
- Character counter: gray → orange → red
- Submit button: Blue, white text, loading spinner

**Success State:**
- Green checkmark icon
- "Thanks for your message! We'll get back to you soon."
- "View in Dashboard" link (if authenticated)
- "Send Another Message" button

### Dashboard Contact Section

**Placement:** After Claims section, same styling

**Table Design:**
- Subject column: Icon + text (based on subject type)
  - General: Question mark icon
  - Quote: Dollar sign icon
  - Claim: File icon
  - Policy: Document icon
  - Other: Ellipsis icon
- Submitted Date: Formatted date (e.g., "November 20, 2025")
- Status: Colored pill badge
- Actions: "View" button (blue, small)

**Status Badge Colors:**
- New: Blue (#3B82F6)
- Read: Yellow (#F59E0B)
- Responded: Green (#10B981)
- Closed: Gray (#6B7280)

**Mobile Design:**
- Cards instead of table rows
- Subject as card title
- Status badge in top-right
- Date and action button below

### Message Detail View

**Layout:**
- Single column, max-width 800px
- Readonly fields with light gray background
- Admin response in highlighted box (light green background)

**Message Info Section:**
- Subject (h2, bold)
- Status badge next to subject
- Message ID (small, gray, "Message #123456")
- Submitted date (gray, "Submitted on November 20, 2025 at 9:31 AM PST")

**Your Message Section:**
- White card with border
- Fields displayed as readonly
- Label + value pairs

**Admin Response Section:**
- Light green background (#ECFDF5)
- Green border (#10B981)
- "Our Response" heading
- Response text (styled)
- Responded date (small, gray)
- Hidden if no response yet

**No Response Message:**
- Light blue background
- Info icon
- "We received your message and will respond soon."

**Actions:**
- "Reply" button (blue, primary)
- "Back to Dashboard" button (gray, secondary)

---

## Testing Checklist

### Functionality Testing
- [ ] Public contact form loads without authentication
- [ ] Submit contact message as guest (user_id = null)
- [ ] Submit contact message as authenticated user (user_id set)
- [ ] View contact messages in dashboard (authenticated only)
- [ ] View individual message details
- [ ] Admin response displays correctly (when present)
- [ ] "Reply" button pre-fills context
- [ ] Auth guard redirects to login for protected routes
- [ ] Users can only access their own messages (403 for others)

### Form Validation Testing
- [ ] Required fields show red border when empty
- [ ] Full name validation (must be "First Last" format)
- [ ] Email validation (must be valid email)
- [ ] Phone validation (optional, but must be XXX.XXX.XXXX if provided)
- [ ] Message character counter updates correctly
- [ ] Red border when message over 250 chars
- [ ] Submit button disabled until form valid
- [ ] Phone number auto-formats as user types

### Backend Testing
- [ ] POST /contact/submit works without authentication
- [ ] POST /contact/submit captures user_id if authenticated
- [ ] GET /messages requires authentication
- [ ] GET /messages returns only user's messages
- [ ] GET /{id} requires authentication
- [ ] GET /{id} throws 403 for another user's message
- [ ] GET /{id} returns 404 for non-existent message
- [ ] Message status defaults to 'new'
- [ ] Timestamps created correctly

### Responsive Design
- [ ] Contact form mobile-friendly (touch inputs)
- [ ] Dashboard table responsive (cards on mobile)
- [ ] Message detail view mobile-friendly
- [ ] All touch targets minimum 44x44px
- [ ] Phone number input works on mobile keyboards

### Error Handling
- [ ] Network errors show user-friendly message
- [ ] Invalid data returns clear error from backend
- [ ] 403 for unauthorized access
- [ ] 404 for non-existent message
- [ ] Form validation errors clear on correction
- [ ] Graceful handling of missing admin response

---

## Success Criteria

- [ ] Anyone can submit contact message (no auth required)
- [ ] Authenticated users see their messages in dashboard
- [ ] Guest messages stored but not shown in user dashboard
- [ ] Message detail view shows admin response (if exists)
- [ ] Form validation prevents invalid submissions
- [ ] Character counter works correctly (250 char limit)
- [ ] Status badges display correctly
- [ ] Mobile-friendly, responsive design
- [ ] Phone number auto-formats as user types
- [ ] No console errors
- [ ] Users cannot access other users' messages

---

## Security Considerations

- [ ] Public endpoint for submission (no auth required)
- [ ] Protected endpoints for viewing messages (auth required)
- [ ] User can only view their own messages (user_id check)
- [ ] Data sanitization on all inputs (prevent XSS)
- [ ] SQL injection prevention (using SQLAlchemy ORM)
- [ ] CSRF protection (handled by FastAPI)
- [ ] Rate limiting on message submission (prevent spam)
- [ ] Audit logging for message actions
- [ ] Admin response creation deferred to Slice 6 (admin only)

**Security Note:** Contact messages are LOW-STAKES. No sensitive PII, no financial data, just basic contact info and a message.

---

## Future Enhancements (Not in this slice)

**Slice 6 - Admin Dashboard:**
- View all contact messages (authenticated + guest)
- Filter by status, subject, date
- Add admin response
- Update message status
- Mark as read

**Slice 7 - Email Notifications:**
- Email to admin on new contact message
- Email to customer when admin responds
- Email copy of submitted message to customer

**Future Considerations:**
- Real-time chat integration
- File attachments
- Internal notes (admin only, not visible to customer)
- Auto-close messages after X days
- Message threading (reply creates new linked message)

---

## Estimated Breakdown

**Backend Development:** 1-2 hours
- Contact endpoints (submit, messages, get by ID)
- Service logic (create, get user messages, ownership check)
- Schema validation
- Model and migration

**Frontend - Contact Form:** 1 hour
- Public contact form page
- Form validation with shared utilities
- Character counter
- Phone number auto-formatting
- API integration
- Success state

**Frontend - Dashboard Integration:** 1 hour
- Contact messages section component
- Messages table with status badges
- Pagination
- Empty state
- Responsive cards for mobile

**Frontend - Detail View:** 1 hour
- Message detail page
- Readonly field display
- Admin response section (conditional)
- Reply button functionality

**Testing & Polish:** 1 hour
- Test message submission (guest + authenticated)
- Test dashboard display
- Test detail view
- Test validation and character counters
- Responsive design testing
- Bug fixes

**Total:** 4-6 hours

---

## Dependencies for Future Slices

**Slice 6 (Admin Dashboard):**
- Admin needs to view all contact messages
- Admin needs to respond to messages
- Admin needs to update message status

**Slice 7 (Email & Notifications):**
- Email to admin on new contact message
- Email to customer when admin responds
- Email copy of message to customer on submission

---

## Implementation Notes

### Reuse from Previous Slices

**From Slice 3 & 4 (Quote & Claims Systems):**
- Form validation pattern with shared utilities
- Character counter on textareas (250 char limit)
- Red border validation (no error text)
- Dashboard table layout and styling
- Status badge styling
- Loading states and success messages
- Mobile-responsive form design

**Shared Utilities:**
- `ValidationRules.fullName` - Full name validation
- `ValidationRules.email` - Email validation
- `ValidationRules.phone` - Phone validation (optional)
- `formatPhoneNumber` - Auto-format phone as XXX.XXX.XXXX
- `formatDateTime` - Display timestamps with timezone
- `getCharacterCountClass` - Character counter styling

### Key Design Decisions

**Why Public Contact Form?**
- Lower barrier to entry - anyone can ask questions
- Not everyone is ready to create an account
- Simple communication channel for general inquiries

**Why Link Messages to user_id?**
- Authenticated users can track their message history
- Dashboard shows all their interactions in one place
- Easier to reference past conversations

**Why Separate Guest Messages?**
- Guest messages (user_id = null) stored for admin view
- Not shown in any user dashboard (no account to link to)
- Admin can respond via email (no dashboard access for guest)

**Why Simple Status Tracking?**
- New: Just received
- Read: Admin has seen it
- Responded: Admin replied
- Closed: Conversation complete
- No complex workflows needed for contact messages

### Authentication Handling

**For Public Form:**
```typescript
// Check if user is logged in (optional)
const authStore = useAuthStore()
const isAuthenticated = authStore.isAuthenticated

// On submit, include token if available
const headers = isAuthenticated
  ? { Authorization: `Bearer ${authStore.token}` }
  : {}

// Backend will capture user_id if token provided, null otherwise
```

**For Protected Routes:**
```typescript
// Standard auth guard
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})
```

---

## Development Sequence

**Recommended Order:**

1. **Backend API** (contact.py, service, schemas, model)
   - Create ContactMessage model
   - Database migration
   - Contact service with business logic
   - Contact router endpoints
   - Test with Swagger/Postman

2. **Public Contact Form** (ContactPage.vue)
   - Form layout with all fields
   - Validation with shared utilities
   - Character counter
   - Phone auto-formatting
   - Submit with optional auth
   - Success state

3. **Dashboard Integration** (ContactMessagesList.vue)
   - Add section to DashboardPage.vue
   - Messages table component
   - Status badges
   - Pagination
   - Empty state

4. **Detail View** (ContactDetailPage.vue)
   - Message info display
   - Readonly fields
   - Admin response section (conditional)
   - Reply button

5. **Testing & Polish**
   - Test guest message submission
   - Test authenticated message submission
   - Test dashboard display
   - Test detail view
   - Test ownership checks (403 errors)
   - Responsive design
   - Bug fixes

**Parallel Work:**
- Frontend and backend can be developed simultaneously
- Contact form can be built while backend is in progress
- Detail view depends on form completion

---

## API Request/Response Examples

### POST /api/v1/contact/submit

**Request (Guest):**
```json
{
  "full_name": "John Smith",
  "email": "john@example.com",
  "phone": "555.555.5555",
  "subject": "general",
  "message": "I have a question about your homeowners insurance policies. Can you tell me more about coverage options?"
}
```

**Request (Authenticated - token in header):**
```
Authorization: Bearer <token>
```
```json
{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "subject": "quote",
  "message": "I submitted a quote request last week. When can I expect to hear back?"
}
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "new",
  "created_at": "2025-11-20 17:31:00",
  "message": "Your message has been received. We'll get back to you soon."
}
```

### GET /api/v1/contact/messages

**Response:**
```json
{
  "messages": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "subject": "Quote Question",
      "status": "responded",
      "created_at": "2025-11-20 17:31:00",
      "has_response": true
    },
    {
      "id": "987e6543-e21b-12d3-a456-426614174000",
      "subject": "General Question",
      "status": "new",
      "created_at": "2025-11-19 14:22:00",
      "has_response": false
    }
  ],
  "total": 2,
  "page": 1,
  "per_page": 10
}
```

### GET /api/v1/contact/{id}

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "555.555.5555",
  "subject": "quote",
  "message": "I submitted a quote request last week. When can I expect to hear back?",
  "status": "responded",
  "admin_response": "Thanks for your patience! We reviewed your quote and sent a detailed proposal to your email. Please check your inbox. Feel free to call us at (541) 555-0123 if you have any questions!",
  "responded_at": "2025-11-20 18:45:00",
  "created_at": "2025-11-20 17:31:00"
}
```

---

## Database Migration

**Alembic Migration:**

```python
"""Add contact_messages table

Revision ID: xxxxx
Revises: previous_migration
Create Date: 2025-11-21

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

def upgrade():
    op.create_table(
        'contact_messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('full_name', sa.String(200), nullable=False),
        sa.Column('email', sa.String(254), nullable=False),
        sa.Column('phone', sa.String(12), nullable=True),
        sa.Column('subject', sa.Enum('general', 'quote', 'claim', 'policy', 'other', name='contact_subject'), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('status', sa.Enum('new', 'read', 'responded', 'closed', name='contact_status'), nullable=False, server_default='new'),
        sa.Column('admin_response', sa.Text, nullable=True),
        sa.Column('responded_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Indexes
    op.create_index('ix_contact_messages_user_id', 'contact_messages', ['user_id'])
    op.create_index('ix_contact_messages_status', 'contact_messages', ['status'])
    op.create_index('ix_contact_messages_created_at', 'contact_messages', ['created_at'])

def downgrade():
    op.drop_table('contact_messages')
    op.execute('DROP TYPE contact_subject')
    op.execute('DROP TYPE contact_status')
```

---

**Document Version:** 1.0
**Created:** 2025-11-21
**Status:** Not Started
