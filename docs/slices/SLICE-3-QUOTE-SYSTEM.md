# Slice 3: Quote Request System

**Estimated Time:** 6-8 hours
**Dependencies:** Slice 1 & 2 must be complete
**Status:** Ready to implement

---

## Overview

This slice implements the quote request system, allowing authenticated users to request insurance quotes for various coverage types. Users can submit detailed information about their insurance needs, and agents can review and respond to these requests.

---

## Goals

- [ ] Create quote request form with dynamic fields based on insurance type
- [ ] Implement backend API endpoints for quote management
- [ ] Add quote history to user dashboard
- [ ] Enable users to view their submitted quotes
- [ ] Add quote status tracking (Pending, In Review, Quoted, Declined)
- [ ] Implement email notifications for new quote requests
- [ ] Add form validation and error handling

---

## Features to Implement

### 1. Quote Request Form

**Route:** `/quote` (protected - requires authentication)

**Form Structure:**
- [ ] Insurance type selector (dropdown)
- [ ] Dynamic form fields based on selected insurance type
- [ ] Contact preference (Email, Phone, Both)
- [ ] Additional notes/comments field
- [ ] Submit button with loading state

**Insurance Types to Support:**
1. Auto Insurance
2. Home Insurance
3. Life Insurance
4. Business Insurance
5. Motorcycle Insurance
6. RV Insurance
7. Boat Insurance
8. Umbrella Insurance

**Dynamic Fields by Type:**

#### Auto Insurance
- Year, Make, Model
- VIN (optional)
- Current insurance provider
- Coverage level desired (Liability only, Full coverage, etc.)
- Number of drivers
- Primary use (Commute, Personal, Business)

#### Home Insurance
- Property address
- Home type (Single family, Condo, Townhouse, Mobile home)
- Year built
- Square footage
- Current insurance provider
- Coverage amount desired

#### Life Insurance
- Coverage amount desired
- Type (Term, Whole, Universal)
- Term length (if applicable)
- Beneficiary information
- Health information (basic)

#### Business Insurance
- Business name
- Business type/industry
- Number of employees
- Annual revenue
- Property value
- Coverage types needed (General liability, Property, Workers comp, etc.)

#### Motorcycle Insurance
- Year, Make, Model
- VIN (optional)
- Primary use (Recreation, Commute)
- Storage location
- Current insurance provider

#### RV Insurance
- Year, Make, Model
- RV type (Class A, B, C, Travel trailer, Fifth wheel)
- VIN (optional)
- Usage (Full-time, Vacation)
- Current insurance provider

#### Boat Insurance
- Year, Make, Model
- Boat type (Power, Sail, Personal watercraft)
- Length
- Storage location
- Usage frequency

#### Umbrella Insurance
- Current auto insurance limits
- Current home insurance limits
- Desired umbrella coverage amount
- Number of properties owned
- Number of vehicles owned

### 2. Backend API Endpoints

**Quote Management:**

```
POST /api/v1/quotes/request
- Create new quote request
- Requires authentication
- Validates form data
- Sends email notification to admin
- Returns quote ID

GET /api/v1/quotes/my-quotes
- Get all quotes for authenticated user
- Returns list with status, date, insurance type
- Supports pagination

GET /api/v1/quotes/{quote_id}
- Get specific quote details
- Must be owner or admin
- Returns full quote information

PUT /api/v1/quotes/{quote_id}
- Update quote (user can add notes)
- Admin can update status and add response

DELETE /api/v1/quotes/{quote_id}
- Cancel/delete quote
- Only owner can delete
```

**Quote Status Flow:**
1. `pending` - Just submitted, awaiting review
2. `in_review` - Agent is reviewing
3. `quoted` - Quote provided to customer
4. `accepted` - Customer accepted quote
5. `declined` - Customer declined or agent cannot quote

### 3. Database Schema Updates

**quotes table** (already exists from Slice 1):
```sql
- id (primary key)
- user_id (foreign key to users)
- insurance_type (varchar)
- status (enum: pending, in_review, quoted, accepted, declined)
- quote_data (JSON) - stores dynamic form data
- agent_notes (text) - internal notes
- customer_notes (text) - customer comments
- quote_amount (decimal, nullable) - quoted price
- quoted_at (timestamp, nullable)
- created_at (timestamp)
- updated_at (timestamp)
```

### 4. User Dashboard Integration

**Route:** `/dashboard` (protected)

**Dashboard Sections:**
- [ ] Welcome message with user name
- [ ] Quick stats (Total quotes, Pending quotes, Active policies)
- [ ] Recent quotes table
  - Insurance type
  - Submission date
  - Status badge
  - Action buttons (View, Cancel)
- [ ] Quick action buttons
  - Request New Quote
  - File a Claim
  - Contact Us

**Recent Quotes Table Columns:**
- Insurance Type (icon + name)
- Submitted (date)
- Status (colored badge)
- Actions (View button)

### 5. Quote Detail View

**Route:** `/quotes/{quote_id}` (protected)

**Information Displayed:**
- [ ] Quote ID
- [ ] Insurance type
- [ ] Submission date
- [ ] Current status with timeline
- [ ] All submitted information (readonly)
- [ ] Customer notes
- [ ] Agent response (if quoted)
- [ ] Quote amount (if provided)
- [ ] Next steps / instructions
- [ ] Contact agent button

### 6. Email Notifications

**To Admin (when new quote submitted):**
```
Subject: New Quote Request - [Insurance Type]

A new quote request has been submitted:

Customer: [Name]
Email: [Email]
Insurance Type: [Type]
Submitted: [Date/Time]

View in dashboard: [Link]
```

**To Customer (when quote is provided):**
```
Subject: Your Insurance Quote is Ready

Hello [Name],

We've prepared your quote for [Insurance Type].

Quote Amount: $[Amount]/[period]
Valid Until: [Date]

View your quote: [Link]

Questions? Reply to this email or call us at (503) 555-1234.

Best regards,
Whittaker Agency Team
```

---

## Technical Implementation

### Frontend Components to Create

```
frontend/src/
├── views/
│   ├── QuoteRequestPage.vue       # Main quote form
│   ├── DashboardPage.vue          # User dashboard
│   └── QuoteDetailPage.vue        # Single quote view
├── components/
│   ├── forms/
│   │   ├── QuoteForm.vue          # Main form wrapper
│   │   ├── AutoQuoteFields.vue    # Auto-specific fields
│   │   ├── HomeQuoteFields.vue    # Home-specific fields
│   │   ├── LifeQuoteFields.vue    # Life-specific fields
│   │   ├── BusinessQuoteFields.vue
│   │   ├── MotorcycleQuoteFields.vue
│   │   ├── RVQuoteFields.vue
│   │   ├── BoatQuoteFields.vue
│   │   └── UmbrellaQuoteFields.vue
│   └── dashboard/
│       ├── DashboardStats.vue     # Stats cards
│       ├── QuotesList.vue         # Quotes table
│       └── QuickActions.vue       # Action buttons
└── services/
    └── quotes.ts                  # API client for quotes
```

### Backend Files to Create

```
backend/app/
├── routers/
│   └── quotes.py                  # Quote endpoints
├── services/
│   └── quote_service.py           # Business logic
├── schemas/
│   └── quote_schemas.py           # Pydantic models
└── models/
    # quote_requests model already exists
```

### Routes to Add

```typescript
// Protected routes
{
  path: '/dashboard',
  name: 'dashboard',
  component: DashboardPage,
  meta: { requiresAuth: true }
},
{
  path: '/quote',
  name: 'quote-request',
  component: QuoteRequestPage,
  meta: { requiresAuth: true }
},
{
  path: '/quotes/:id',
  name: 'quote-detail',
  component: QuoteDetailPage,
  meta: { requiresAuth: true }
}
```

### Navigation Guard Implementation

```typescript
// Update router/index.ts
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login, save intended destination
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})
```

---

## Form Validation Rules

### Common Fields (All Types)
- Insurance type: Required
- Contact preference: Required
- Additional notes: Optional, max 1000 characters

### Auto Insurance
- Year: Required, 1900-current year+1
- Make: Required, max 50 chars
- Model: Required, max 50 chars
- VIN: Optional, exactly 17 chars if provided
- Coverage level: Required

### Home Insurance
- Address: Required
- Home type: Required
- Year built: Required, 1800-current year
- Square footage: Required, min 1

### Life Insurance
- Coverage amount: Required, min $10,000
- Type: Required
- Health information: Required

### Business Insurance
- Business name: Required
- Industry: Required
- Number of employees: Required, min 1
- Coverage types: At least one required

---

## Design Specifications

### Dashboard Layout
- Header with user greeting
- 3-column stats cards (Total Quotes, Pending, Active Policies)
- Full-width quotes table
- Sidebar with quick actions (optional)

### Quote Form
- Clean, single-column layout
- Step indicator (optional)
- Insurance type selector at top
- Dynamic fields appear below
- Submit button at bottom
- Loading state during submission
- Success message with quote ID

### Status Badges
```css
pending: Yellow/Gold background
in_review: Blue background
quoted: Green background
accepted: Dark green background
declined: Red background
```

---

## Testing Checklist

### Functionality Testing
- [ ] Submit quote for each insurance type
- [ ] View all quotes in dashboard
- [ ] View individual quote details
- [ ] Update quote with additional notes
- [ ] Cancel/delete quote
- [ ] Navigation guard redirects to login when not authenticated
- [ ] Email notifications sent correctly

### Form Validation
- [ ] Required fields show errors
- [ ] Invalid data rejected (e.g., year out of range)
- [ ] Character limits enforced
- [ ] Dynamic fields show/hide correctly

### Backend Testing
- [ ] API creates quote correctly
- [ ] Quote data stored as JSON
- [ ] User can only see their own quotes
- [ ] Admin can see all quotes (future feature)
- [ ] Status updates work
- [ ] Pagination works for quote list

### Responsive Design
- [ ] Dashboard works on mobile
- [ ] Quote form works on mobile
- [ ] Tables scroll horizontally on small screens
- [ ] Form inputs are touch-friendly

### Error Handling
- [ ] Network errors show user-friendly message
- [ ] Invalid data returns clear error
- [ ] 404 for non-existent quote
- [ ] 403 for accessing another user's quote

---

## Success Criteria

- Authenticated users can submit quote requests for all 8 insurance types
- Dynamic form fields show based on selected insurance type
- All quote data saved correctly to database
- Users can view their quote history
- Quote status visible with colored badges
- Email notifications sent to admin on new quotes
- Dashboard shows quick overview of user's quotes
- Form validation prevents invalid submissions
- Mobile-friendly interface
- No console errors

---

## Security Considerations

- [ ] All quote routes require authentication
- [ ] Users can only access their own quotes
- [ ] Quote data sanitized before storage
- [ ] SQL injection prevention (using ORM)
- [ ] XSS prevention in form inputs
- [ ] CSRF protection (handled by FastAPI)
- [ ] Rate limiting on quote submission (prevent spam)

---

## Future Enhancements (Not in this slice)

- Admin dashboard to manage quotes
- Quote comparison feature
- Document upload (insurance cards, photos)
- Real-time chat with agents
- Quote expiration dates
- Multi-step form with progress indicator
- Save draft quotes

---

## Estimated Breakdown

**Backend Development:** 2-3 hours
- Quote endpoints
- Quote service logic
- Email notifications
- Data validation

**Frontend - Quote Form:** 2-3 hours
- Main form component
- Dynamic field components
- Form validation
- API integration

**Frontend - Dashboard:** 1-2 hours
- Dashboard layout
- Stats cards
- Quotes table
- Quote detail view

**Testing & Polish:** 1-2 hours
- Form testing
- API testing
- Responsive design
- Bug fixes

**Total:** 6-10 hours

---

## Dependencies for Future Slices

**Slice 4 (Claims System):**
- Similar form structure can be reused
- Dashboard integration pattern established

**Slice 5 (Contact System):**
- Contact form similar to quote form
- Dashboard can show contact messages

---

## Notes for Implementation

- Start with backend API first (easier to test with Swagger)
- Build one insurance type form completely, then replicate pattern
- Use TypeScript interfaces for quote data structure
- Consider using a form library like VeeValidate (optional)
- Reuse existing components (buttons, cards, etc.)
- Follow established patterns from Slice 2

---

**Document Version:** 1.0
**Created:** 2025-10-28
**Last Updated:** 2025-10-28
