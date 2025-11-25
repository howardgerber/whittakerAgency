# Slice 6: Admin Dashboard & Management UI

**Estimated Time:** 10-12 hours
**Dependencies:** Slice 1, 2, 3, 4, and 5 must be complete
**Status:** Not Started

---

## Overview

Admin/staff management dashboard for viewing and responding to user submissions. Agency staff can manage quote requests, claims, and contact messages—filtering, reviewing, and updating status while adding notes and responses.

**Key Concept:** "Central hub for staff to manage customer interactions and provide responses."

---

## Goals

- [ ] Implement admin authentication and role-based authorization
- [ ] Create admin dashboard with overview stats and recent activity
- [ ] Build quote management interface (view, filter, respond, add amounts, update status)
- [ ] Build claims management interface (view, filter, respond, update status)
- [ ] Build contact message management interface (view, filter, respond, update status)
- [ ] Add admin-only fields to database schema
- [ ] Implement admin response endpoints and business logic
- [ ] Audit all admin actions to system logs
- [ ] Enable users to see admin responses in their dashboards

**Not Goals:**
- ❌ Full claim processing system (no approval workflow, no payments)
- ❌ Real-time messaging or chat
- ❌ Document management or uploads
- ❌ Complex permission/role hierarchy (simple admin/staff vs. regular user)

---

## Features to Implement

### 1. Admin Authentication & Authorization

**Authentication:**
- Reuse existing JWT-based auth from Slice 1
- No separate admin login - same user table with `is_admin` flag
- User model needs `is_admin` boolean field (default: false)

**Authorization Strategy:**
- Add `is_admin` column to users table
- Create `@requires_admin` decorator for protected admin endpoints
- Check `user.is_admin` in middleware/decorator before allowing access
- All admin routes require authentication + admin flag
- Non-admin users attempting admin routes receive 403 Forbidden

**Database Changes:**
```sql
ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE
```

**Admin Route Protection Pattern:**
```python
# In router (thin controller)
@router.get("/admin/dashboard")
async def get_admin_dashboard(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise PermissionError("Admin access required")
    return await admin_service.get_dashboard_stats(current_user.id)

# In service (business logic + validation)
async def get_dashboard_stats(admin_user_id: int):
    # Calculate stats for dashboard
    pending_quotes = await get_pending_quotes_count()
    pending_claims = await get_pending_claims_count()
    new_messages = await get_new_messages_count()
    return {
        "quotes": pending_quotes,
        "claims": pending_claims,
        "messages": new_messages
    }
```

---

### 2. Admin Dashboard Overview

**Route:** `/admin/dashboard` (protected - admin only)

**Dashboard Sections:**

#### Summary Stats Cards
- Total pending quotes (count)
- Total pending claims (count)
- New contact messages (count)
- Quick stat: Avg response time (optional)

#### Recent Activity Feed
- Last 10 submissions (quotes, claims, messages combined)
- Type indicator (quote, claim, message)
- Customer name
- Date submitted
- Current status
- Click to open detail view

#### Quick Actions
- "Review Pending Quotes" button → quotes list filtered to pending
- "Review Pending Claims" button → claims list filtered to pending
- "New Messages" button → contact messages filtered to new

#### Status Breakdown (Optional)
- Pie chart: Quote status distribution
- Pie chart: Claim status distribution
- Pie chart: Message status distribution

---

### 3. Quote Management Interface

**Route:** `/admin/quotes` (protected - admin only)

**Features:**

#### Quote List View
**Columns:**
- Customer Name (linked to customer detail)
- Insurance Type (category + subcategory)
- Submitted Date
- Current Status (colored badge)
- Quote Amount (if set, in currency format)
- Actions (View, Edit)

**Filters/Search:**
- Category dropdown (vehicle, property, life, business, other)
- Subcategory dropdown (dependent on category)
- Status dropdown (pending, in_review, quoted, accepted, declined)
- Date range picker (submitted between X and Y)
- Search by customer name or email
- Pagination (20 per page)

**Sorting:**
- By date (newest first default)
- By status
- By customer name
- By quote amount

#### Quote Detail View
**Sections:**

**Quote Information:**
- Quote ID
- Customer name + email + phone
- Insurance type (category + subcategory)
- Submitted date
- Current status (colored badge)
- Current status history (timeline: pending → in_review → quoted → closed)

**Customer Information (readonly):**
- All submitted form data
- Customer notes (if provided)
- Preferred contact method

**Agent Response Section:**
- [ ] Quote amount field (numeric, editable)
- [ ] Agent notes field (textarea, editable)
- [ ] Status dropdown (change: pending → in_review → quoted → accepted → declined)
- [ ] "Save Changes" button with loading state
- [ ] Show when last updated + who updated

**Actions:**
- Save Changes
- Mark as Reviewed (change to in_review)
- Send Quote to Customer (mark as quoted, trigger email to Slice 7)
- Close Quote (mark as declined)
- Back to List

**Status Flow:**
1. `pending` - Newly submitted
2. `in_review` - Staff is reviewing
3. `quoted` - Quote amount + notes provided to customer
4. `accepted` - Customer accepted quote (system auto-set)
5. `declined` - Staff or customer declined

**Audit Trail:**
- Each update logged with timestamp + admin user + change details

---

### 4. Claims Management Interface

**Route:** `/admin/claims` (protected - admin only)

**Features:**

#### Claims List View
**Columns:**
- Customer Name
- Insurance Type (category + subcategory)
- Incident Date
- Submitted Date
- Current Status (colored badge)
- Actions (View, Update)

**Filters/Search:**
- Category dropdown
- Subcategory dropdown
- Status dropdown (submitted, contacted, closed)
- Date range (submitted between X and Y)
- Incident date range (incident between X and Y)
- Search by customer name or email
- Pagination (20 per page)

**Sorting:**
- By date (newest first default)
- By incident date
- By status
- By customer name

#### Claim Detail View
**Sections:**

**Claim Information:**
- Claim ID
- Customer name + email + phone
- Insurance type (category + subcategory)
- Incident date
- Submitted date
- Current status (colored badge)
- Preferred appointment date (if requested)
- Contact preference

**Incident Details (readonly):**
- All submitted form data
- Incident summary
- Additional notes from customer
- Dynamic fields based on category/subcategory

**Staff Response Section:**
- [ ] Admin notes field (textarea, editable) - internal notes not visible to customer
- [ ] Status dropdown (submitted → contacted → closed)
- [ ] Appointment date field (editable, for scheduling)
- [ ] Customer response field (what agent will send to customer) - optional
- [ ] "Save Changes" button

**Actions:**
- Mark as Contacted (change status, send notification to Slice 7)
- Close Claim
- Back to List

**Status Flow:**
1. `submitted` - Customer submitted claim info
2. `contacted` - Staff reached out to customer
3. `closed` - Claim resolved (customer filed or withdrew)

**Audit Trail:**
- Track all status changes + notes with timestamp + admin user

---

### 5. Contact Message Management Interface

**Route:** `/admin/contact` (protected - admin only)

**Features:**

#### Message List View
**Columns:**
- Sender Name
- Subject (with icon indicator: general, quote, claim, policy, other)
- Submitted Date
- Current Status (colored badge: new, read, responded, closed)
- Has Response (checkmark if admin response exists)
- Actions (View, Respond)

**Filters/Search:**
- Subject dropdown (general, quote, claim, policy, other)
- Status dropdown (new, read, responded, closed)
- Date range (submitted between X and Y)
- Search by sender name or email
- Guest messages toggle (show/hide messages from non-authenticated users)
- Pagination (20 per page)

**Sorting:**
- By date (newest first default)
- By status
- By sender name
- By subject

#### Message Detail View
**Sections:**

**Message Information:**
- Message ID
- Sender name + email + phone
- Subject (with icon)
- Submitted date
- Current status (colored badge)
- Is guest message indicator (if applicable)

**Customer Message (readonly):**
- Full message text
- Formatted with timestamp

**Admin Response Section:**
- [ ] Admin response field (textarea, editable)
- [ ] Mark as Read checkbox (auto-checked on open)
- [ ] "Send Response" button (changes status to responded)
- [ ] Show current response (if exists) with timestamp

**Status Workflow:**
- Open message → auto-mark as read
- Edit response + click Send → status = responded, timestamp recorded
- Close message → status = closed

**Actions:**
- Mark as Read (if not already)
- Send Response (change to responded)
- Close Message
- Delete Message (optional, soft delete)
- Back to List

**Audit Trail:**
- Track response creation + edits with timestamp + admin user

---

### 6. User Management (Optional - Lower Priority)

**Route:** `/admin/users` (protected - admin only)

**Features:**

#### User List View
**Columns:**
- Username
- Full Name
- Email
- Registered Date
- Status (active, inactive)
- Quotes (count)
- Claims (count)
- Messages (count)
- Actions (View, Deactivate)

**Filters/Search:**
- Status dropdown (active, inactive)
- Search by username, email, or name
- Date range (registered between X and Y)
- Pagination (20 per page)

**Sorting:**
- By date (newest first)
- By name
- By status

#### User Detail View
**Sections:**

**User Information:**
- User ID
- Username + email
- Full name + phone
- Account status (active/inactive)
- Created date
- Last login date

**User Activity:**
- Quotes submitted (count + table)
- Claims submitted (count + table)
- Messages sent (count + table)
- Recent activity feed

**Actions:**
- Deactivate Account
- Back to List

---

## Backend Database Schema Updates

### Approach: Drop and Recreate All Tables

**Strategy:**
- Drop all existing tables
- Create a single new migration file with complete schema
- Include all admin fields from the start
- No ALTER TABLE statements needed

### Implementation Steps

1. **Create new migration file:** `backend/alembic/versions/002_complete_schema_with_admin.py`
2. **Drop all existing tables** (in correct order to handle foreign keys)
3. **Recreate all tables** with complete schema including admin fields

### Required Admin Fields

**users table:**
- Add `is_admin` BOOLEAN DEFAULT FALSE
- Add index on `is_admin`

**quote_requests table:**
- Add `quote_amount` DECIMAL(10,2) NULLABLE
- Add `quoted_at` TIMESTAMP NULLABLE
- Add `agent_notes` TEXT NULLABLE

**claims table:**
- Add `admin_notes` TEXT NULLABLE
- Add `contacted_at` TIMESTAMP NULLABLE

**contact_messages table:**
- Add `admin_response` TEXT NULLABLE
- Add `responded_at` TIMESTAMP NULLABLE

### Audit Logging

All admin actions logged to existing `audit_logs` table:
- Admin user ID
- Action (create, update, delete)
- Entity type (quote, claim, message)
- Entity ID
- Changes (JSON: before/after values)
- Timestamp

### Migration File Location

`backend/alembic/versions/002_complete_schema_with_admin.py`

This single migration file will contain ALL table definitions with all fields needed for the complete application including admin functionality.

---

## Backend API Endpoints

### Quote Management

```
GET    /api/v1/admin/quotes                    - List all quotes (paginated, filtered)
GET    /api/v1/admin/quotes/{quote_id}         - Get quote details
PUT    /api/v1/admin/quotes/{quote_id}         - Update quote (amount, notes, status)
GET    /api/v1/admin/quotes/stats/summary      - Dashboard stats
```

**PUT /api/v1/admin/quotes/{quote_id}**
```json
// Request body
{
  "status": "quoted",              // pending, in_review, quoted, accepted, declined
  "quote_amount": 1500.00,
  "agent_notes": "Based on their coverage needs, recommended full coverage..."
}

// Response
{
  "id": 123,
  "status": "quoted",
  "quote_amount": 1500.00,
  "agent_notes": "...",
  "updated_at": "2025-11-22T10:30:00",
  "updated_by": 5
}
```

---

### Claims Management

```
GET    /api/v1/admin/claims                    - List all claims (paginated, filtered)
GET    /api/v1/admin/claims/{claim_id}         - Get claim details
PUT    /api/v1/admin/claims/{claim_id}         - Update claim (notes, status, appointment)
GET    /api/v1/admin/claims/stats/summary      - Dashboard stats
```

**PUT /api/v1/admin/claims/{claim_id}**
```json
// Request body
{
  "status": "contacted",           // submitted, contacted, closed
  "admin_notes": "Customer called, scheduled visit for Nov 25...",
  "appointment_date": "2025-11-25T14:00:00"
}

// Response
{
  "id": 456,
  "status": "contacted",
  "admin_notes": "...",
  "contacted_at": "2025-11-22T11:00:00",
  "updated_at": "2025-11-22T11:00:00",
  "updated_by": 5
}
```

---

### Contact Message Management

```
GET    /api/v1/admin/contact                   - List all messages (paginated, filtered)
GET    /api/v1/admin/contact/{message_id}      - Get message details
PUT    /api/v1/admin/contact/{message_id}      - Add response, update status
GET    /api/v1/admin/contact/stats/summary     - Dashboard stats
```

**PUT /api/v1/admin/contact/{message_id}**
```json
// Request body
{
  "status": "responded",           // new, read, responded, closed
  "admin_response": "Thanks for your message! Here's the information..."
}

// Response
{
  "id": 789,
  "status": "responded",
  "admin_response": "...",
  "responded_at": "2025-11-22T11:30:00",
  "updated_at": "2025-11-22T11:30:00",
  "updated_by": 5
}
```

---

### User Management (Optional)

```
GET    /api/v1/admin/users                     - List all users
GET    /api/v1/admin/users/{user_id}           - Get user details
PUT    /api/v1/admin/users/{user_id}           - Deactivate/reactivate user
```

---

### Dashboard Stats

```
GET    /api/v1/admin/dashboard/stats           - Summary stats

// Response
{
  "quotes": {
    "pending": 5,
    "in_review": 3,
    "quoted": 12,
    "total": 20
  },
  "claims": {
    "submitted": 8,
    "contacted": 4,
    "closed": 2,
    "total": 14
  },
  "messages": {
    "new": 3,
    "read": 7,
    "responded": 10,
    "closed": 4,
    "total": 24
  },
  "recent_activity": [
    {
      "type": "quote",
      "customer": "John Smith",
      "action": "submitted",
      "date": "2025-11-22T10:15:00"
    },
    ...
  ]
}
```

---

## Frontend File Structure

```
frontend/src/
├── views/
│   ├── admin/
│   │   ├── AdminDashboardPage.vue              # Dashboard overview
│   │   ├── AdminQuotesPage.vue                 # Quotes list + filters
│   │   ├── AdminQuoteDetailPage.vue            # Quote detail + edit
│   │   ├── AdminClaimsPage.vue                 # Claims list + filters
│   │   ├── AdminClaimDetailPage.vue            # Claim detail + edit
│   │   ├── AdminContactPage.vue                # Messages list + filters
│   │   ├── AdminContactDetailPage.vue          # Message detail + response
│   │   └── AdminUsersPage.vue                  # Users list (optional)
├── components/
│   └── admin/
│       ├── AdminNav.vue                        # Admin-only navigation
│       ├── DashboardStats.vue                  # Stats cards component
│       ├── ActivityFeed.vue                    # Recent activity
│       ├── QuotesList.vue                      # Table component
│       ├── ClaimsList.vue                      # Table component
│       ├── MessagesList.vue                    # Table component
│       └── FilterPanel.vue                     # Reusable filter component
└── services/
    └── admin.ts                                # Admin API client
```

---

## Frontend Routes to Add

```typescript
// Admin routes - protected with isAdmin check
const adminRoutes = [
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: AdminDashboardPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/quotes',
    name: 'admin-quotes',
    component: AdminQuotesPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/quotes/:id',
    name: 'admin-quote-detail',
    component: AdminQuoteDetailPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/claims',
    name: 'admin-claims',
    component: AdminClaimsPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/claims/:id',
    name: 'admin-claim-detail',
    component: AdminClaimDetailPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/contact',
    name: 'admin-contact',
    component: AdminContactPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/contact/:id',
    name: 'admin-contact-detail',
    component: AdminContactDetailPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: AdminUsersPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]
```

---

## Navigation Updates

**AppHeader.vue:**
- Add "Admin" link/dropdown if user is admin
- Shows only for admin users
- Links to `/admin/dashboard`
- Dropdown with quick links to quotes, claims, messages management

**Router Guard:**
```typescript
// Add requiresAdmin check to existing beforeEach guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next({ name: 'dashboard' }) // Redirect non-admins to user dashboard
  } else {
    next()
  }
})
```

**Auth Store Update:**
```typescript
// Add isAdmin computed property
const isAdmin = computed(() => user.value?.is_admin ?? false)
```

---

## Backend Files to Create/Update

```
backend/app/
├── routers/
│   └── admin.py                    # NEW - Admin routes (quotes, claims, contact, users)
├── services/
│   └── admin_service.py            # NEW - Admin business logic
├── schemas/
│   └── admin_schemas.py            # NEW - Admin request/response models
├── middleware/
│   └── admin_auth.py               # NEW - Admin authorization decorator
└── models/
    ├── user.py                     # UPDATE - Add is_admin field
    ├── quote_request.py            # UPDATE - Verify admin fields
    ├── claim.py                    # UPDATE - Add admin_notes, contacted_at
    └── contact_message.py          # UPDATE - Verify admin response fields
```

---

## Design Specifications

### Admin Dashboard Layout
- Header with "Admin Dashboard" title + admin name
- 3 stat cards across top (pending quotes, pending claims, new messages)
- Activity feed section below (recent submissions)
- Quick action buttons (review pending, new messages)
- Responsive on mobile (stats stack vertically)

### List Views (Quotes, Claims, Messages)
- Toolbar at top: search box + filter button + sort dropdown
- Filter panel (collapsible on mobile): category, status, date range, etc.
- Table with sortable columns (click header to sort)
- Pagination controls (showing "1-20 of 150" etc.)
- Hover highlight on table rows
- Action buttons aligned right (View, Edit)
- Mobile: Card layout instead of table

### Detail Views
- Header: Title + status badge
- Two-column layout on desktop (info left, edit form right)
- Single column on mobile
- Readonly sections (white cards, light gray background)
- Edit sections (white cards, input fields)
- Save button at bottom with loading state
- Audit trail: "Last updated Nov 22 at 10:30 AM by John Admin"

### Status Badges
```
Quote Status:
- pending: Yellow/Gold (#F59E0B)
- in_review: Blue (#3B82F6)
- quoted: Green (#10B981)
- accepted: Dark green (#059669)
- declined: Red (#EF4444)

Claim Status:
- submitted: Yellow/Gold (#F59E0B)
- contacted: Blue (#3B82F6)
- closed: Gray (#6B7280)

Message Status:
- new: Red (#EF4444)
- read: Yellow/Gold (#F59E0B)
- responded: Green (#10B981)
- closed: Gray (#6B7280)
```

### Form Fields in Detail Views
- Quote amount: Currency input with $ symbol
- Notes: Textarea with character count (no limit, but visible)
- Status: Dropdown with current status highlighted
- Date pickers: Calendar widget for appointment/contact dates
- Read-only fields: Light gray background, no borders, non-editable

---

## Testing Checklist

### Admin Authentication & Authorization
- [ ] Non-admin users cannot access /admin/* routes (redirected to dashboard)
- [ ] Admin users can access /admin/dashboard
- [ ] Non-admin users accessing /admin/quotes get 403 Forbidden
- [ ] Admin flag set correctly in database
- [ ] Token includes admin status
- [ ] Admin routes require valid JWT token

### Dashboard Functionality
- [ ] Dashboard loads stats correctly
- [ ] Stats numbers accurate (count pending quotes, etc.)
- [ ] Recent activity feed shows last 10 submissions
- [ ] Quick action buttons navigate to filtered lists
- [ ] Responsive design (stats stack on mobile)

### Quote Management
- [ ] List shows all quotes with correct columns
- [ ] Filters work: category, status, date range
- [ ] Search by customer name works
- [ ] Pagination works (20 per page)
- [ ] Sorting works: by date, status, name
- [ ] Detail view loads quote data
- [ ] Can update quote amount
- [ ] Can update agent notes
- [ ] Can change status (pending → in_review → quoted → accepted/declined)
- [ ] Status change updates timestamp + admin user
- [ ] Audit log records all changes

### Claims Management
- [ ] List shows all claims with correct columns
- [ ] Filters work: category, status, date range
- [ ] Search works
- [ ] Detail view loads claim data
- [ ] Can update admin notes
- [ ] Can change status (submitted → contacted → closed)
- [ ] Can set appointment date
- [ ] Status updates logged with timestamp + admin user

### Contact Message Management
- [ ] List shows all messages (auth + guest)
- [ ] Filters work: subject, status, date range
- [ ] Guest messages marked as such
- [ ] Detail view loads message
- [ ] Can add admin response
- [ ] Status changes: new → read → responded → closed
- [ ] Response timestamp recorded
- [ ] Admin response visible in user dashboard

### User Dashboard Integration
- [ ] Users see admin quote responses in their quote details
- [ ] Users see admin claim notes in their claim details
- [ ] Users see admin contact responses in their message details
- [ ] Admin responses don't show admin-only notes

### User Management (Optional)
- [ ] List shows all users with activity counts
- [ ] Can deactivate/reactivate user
- [ ] User detail shows related quotes/claims/messages

### Security & Logging
- [ ] All admin actions logged to audit_logs
- [ ] Audit log shows admin user + timestamp + action
- [ ] Non-admins cannot access audit logs
- [ ] Timestamps are consistent (server-side)
- [ ] CSRF protection on all mutations
- [ ] XSS prevention on all text fields

### Responsive Design
- [ ] Dashboard responsive (mobile-friendly)
- [ ] List views responsive (cards on mobile)
- [ ] Detail views responsive (single column on mobile)
- [ ] Filters collapse on mobile
- [ ] Tables scroll horizontally (if needed)
- [ ] Touch targets minimum 44x44px
- [ ] Form inputs readable on mobile

### Error Handling
- [ ] Network errors show user-friendly message
- [ ] 403 errors for unauthorized access
- [ ] 404 for non-existent resources
- [ ] Graceful handling of missing data
- [ ] Save errors show validation messages

---

## Success Criteria

- ✅ Admin users can log in and access admin dashboard
- ✅ Non-admin users cannot access admin routes (403 Forbidden)
- ✅ Dashboard shows accurate stats for pending items
- ✅ Admin can view all quotes with full details
- ✅ Admin can add quote amounts and notes
- ✅ Admin can change quote status (workflow: pending → in_review → quoted → accepted/declined)
- ✅ Admin can view all claims
- ✅ Admin can add internal notes to claims
- ✅ Admin can change claim status (submitted → contacted → closed)
- ✅ Admin can view all contact messages (including guest messages)
- ✅ Admin can respond to messages
- ✅ Users see admin responses in their dashboards
- ✅ All admin actions logged with timestamp + admin user
- ✅ Responsive design on mobile
- ✅ No console errors
- ✅ All filters and search working correctly

---

## Security Considerations

- [ ] Admin routes require authentication + is_admin flag
- [ ] Router guards prevent non-admin access (beforeEach check)
- [ ] API endpoints verify admin status (controller decorator)
- [ ] Audit logging tracks all admin actions
- [ ] XSS prevention on all text fields (Vue auto-escaping)
- [ ] CSRF protection on all mutations (FastAPI)
- [ ] Rate limiting on API endpoints (prevent abuse)
- [ ] No sensitive data in URLs or query params
- [ ] Soft delete for sensitive operations (don't hard delete)
- [ ] Admin notes not visible to users (separate field from customer_response)

---

## Future Enhancements

**Slice 7 (Email Notifications):**
- Send email to customer when quote status changes to "quoted"
- Send email to customer when claim status changes to "contacted"
- Send email to customer with admin response for contact messages
- Optional: Send internal notifications to other admin users

**Future Considerations:**
- Advanced reporting (quotes by month, claims by type, etc.)
- Bulk actions (mass status updates)
- Admin user roles (super admin, quote manager, claim manager, etc.)
- Audit log visualization/export
- Real-time notifications for new submissions
- Two-factor authentication for admin accounts
- Admin activity feed (who did what and when)
- Quote templates for common insurance types
- Integration with external claim management systems

---

## Estimated Breakdown

**Backend Development:** 4-5 hours
- Admin service with business logic for quotes, claims, messages
- Admin routes/controllers (thin, no business logic)
- Admin schemas (request/response models)
- Database migrations (add is_admin, admin_notes, etc.)
- Authorization decorator/middleware
- Admin API endpoints with filtering, sorting, pagination
- Audit logging integration
- Testing with Swagger

**Frontend - Admin Navigation:** 30 minutes
- Update AppHeader with admin links
- Router guard with requiresAdmin check
- Auth store with isAdmin computed property

**Frontend - Dashboard:** 1-2 hours
- AdminDashboardPage.vue
- DashboardStats component (3 stat cards)
- ActivityFeed component (recent 10)
- Quick action buttons with navigation
- Responsive layout

**Frontend - Quote Management:** 2-2.5 hours
- AdminQuotesPage (list with filters, search, pagination, sorting)
- AdminQuoteDetailPage (display + edit form)
- QuotesList table component (reusable)
- Filter panel component
- Save changes with loading state
- Integration with admin API

**Frontend - Claims Management:** 1.5-2 hours
- AdminClaimsPage (list with filters)
- AdminClaimDetailPage (display + edit)
- ClaimsList table component
- Integration with admin API

**Frontend - Contact Management:** 1.5-2 hours
- AdminContactPage (list with filters)
- AdminContactDetailPage (display + response)
- MessagesList table component
- Response form
- Integration with admin API

**Frontend - User Management (Optional):** 1 hour
- AdminUsersPage (list with activity counts)
- User detail view
- Deactivate/reactivate functionality

**Integration with User Dashboards:** 1 hour
- Update QuoteDetailPage to show admin responses
- Update ClaimDetailPage to show admin notes
- Update ContactDetailPage to show admin response

**Testing & Polish:** 2-3 hours
- Test all admin routes and filters
- Test authorization (admin vs non-admin)
- Test audit logging
- Responsive design testing
- Bug fixes and refinement
- Cross-browser testing

**Total:** 10-12 hours

---

## Dependencies for Future Slices

**Slice 7 (Email & Notifications):**
- Admin quote updates → email to customer
- Admin claim updates → email to customer
- Admin message responses → email to customer
- Internal admin notifications (optional)

---

## Implementation Notes

### Reuse from Previous Slices
- Form validation patterns from Slice 3 & 4
- Dashboard layout from Slice 3, 4, 5 (user dashboard)
- Status badge styling (same colors as user dashboards)
- Character counter logic from previous forms
- Shared utilities for formatting (dates, currency, phone)
- API client pattern from previous slices (admin.ts)

### Admin Field Strategy
- `is_admin` boolean flag on users (simple, scalable to roles later)
- Separate admin_notes field from customer_response field (don't leak internal notes)
- Audit logging via existing audit_logs table
- Soft deletes for sensitive operations (don't hard-delete)

### Authorization Pattern
- Reuse existing JWT auth
- Add is_admin check in router guard
- Add is_admin check in each admin endpoint (defense in depth)
- Use decorator pattern for reusability

### List View Components
- Single FilterPanel component for reuse across lists
- Single sorting mechanism (click header to sort)
- Standard pagination (20 per page)
- Search + filters combined in toolbar
- Mobile: collapse filters, card layout for items

### Detail View Pattern
- Readonly sections (info) on left, editable section on right
- Save button with loading state (prevents double-submit)
- Audit trail at bottom showing last update + admin user
- Immutable history (old values shown, cannot edit past updates)

---

## Development Sequence

**Recommended Order:**

1. **Database & Models** (30 minutes)
   - Add is_admin to users table
   - Verify admin fields in quote_requests, claims, contact_messages
   - Add admin_notes to claims
   - Create migration

2. **Backend - Admin Service** (2-3 hours)
   - Quote service methods (get all, get by id, update status/amount/notes)
   - Claims service methods (get all, get by id, update status/notes)
   - Messages service methods (get all, get by id, add response)
   - Dashboard stats calculation
   - Filtering, sorting, pagination logic

3. **Backend - Routes & Auth** (1-2 hours)
   - Admin router with all endpoints
   - Admin authorization decorator
   - Schemas for request/response
   - Integration with audit logging
   - Test with Swagger

4. **Frontend - Admin Nav & Auth** (30 minutes)
   - Update AppHeader with admin link
   - Update router guard with requiresAdmin check
   - Update auth store with isAdmin property

5. **Frontend - Dashboard** (1-2 hours)
   - AdminDashboardPage layout
   - DashboardStats component
   - ActivityFeed component
   - Stats calculation on frontend
   - Navigation to other admin pages

6. **Frontend - Quote Management** (2-2.5 hours)
   - AdminQuotesPage with list + filters
   - AdminQuoteDetailPage with edit form
   - Reusable QuotesList component
   - Reusable FilterPanel component
   - API integration

7. **Frontend - Claims Management** (1.5-2 hours)
   - AdminClaimsPage with list + filters
   - AdminClaimDetailPage with edit form
   - API integration

8. **Frontend - Contact Management** (1.5-2 hours)
   - AdminContactPage with list + filters
   - AdminContactDetailPage with response form
   - API integration

9. **Frontend - User Dashboards Integration** (1 hour)
   - Show admin quote response in user QuoteDetailPage
   - Show admin notes in user ClaimDetailPage
   - Show admin response in user ContactDetailPage

10. **Frontend - User Management (Optional)** (1 hour)
    - AdminUsersPage
    - User detail view

11. **Testing & Polish** (2-3 hours)
    - Test all routes and filters
    - Test authorization
    - Responsive design
    - Bug fixes

**Parallel Work:**
- Backend and frontend can be developed simultaneously
- Detail pages can be built in any order once list views complete
- Optional user management can be deferred

---

## Success Metrics

**Functionality:**
- All admin routes protected (non-admin = 403)
- Dashboard stats accurate
- All filters/search working
- All status updates persisted
- All responses visible in user dashboards
- No admin data leaks (internal notes hidden from users)

**Performance:**
- List views load in <1s with 100+ items
- Detail pages load in <500ms
- Filter/search response <500ms
- Save operations complete in <1s

**Reliability:**
- Zero unhandled exceptions
- Audit logging 100% coverage for admin actions
- Data consistency (status updates match audit logs)
- No data loss on network failures

**User Experience:**
- Admin workflow intuitive (filters easy to use)
- Mobile interface functional
- Loading states clear
- Error messages helpful
- Responsive design working

---

**Document Version:** 1.0
**Created:** 2025-11-22
**Status:** Not Started

