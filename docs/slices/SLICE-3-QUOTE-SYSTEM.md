# Slice 3: Quote Request System

**Estimated Time:** 6-8 hours
**Dependencies:** Slice 1 & 2 must be complete
**Status:** ✅ Complete

---

## Overview

This slice implements the quote request system, allowing authenticated users to request insurance quotes for various coverage types. Users can submit detailed information about their insurance needs, and agents can review and respond to these requests.

---

## Goals

- [x] Create quote request form with dynamic fields based on insurance type
- [x] Implement backend API endpoints for quote management
- [x] Add quote history to user dashboard
- [x] Enable users to view their submitted quotes
- [x] Add quote status tracking (Pending, In Review, Quoted, Declined)
- [x] Add form validation and error handling

**Note:** Email notifications moved to Slice 7 (Email & Notifications)

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

**Insurance Categories to Support:**

See [docs/architecture/CATEGORIES.md](../architecture/CATEGORIES.md) for the complete category and subcategory structure.

**Summary:**
1. 🚗 Vehicle (Auto, Motorcycle, ATV/off-road, Roadside, Snowmobile, Boat, RV, Vehicle Protection)
2. 🏠 Property (Homeowners, Renters, Condo, Landlord, Mobile home)
3. ❤️ Life
4. 💼 Business
5. 🔒 Identity Protection
6. 📱 Phone Protection
7. ☂️ Other (Personal umbrella policy, Retirement, Individual/Group Health, Pet, Event, Travel, Jewelry, Collectibles, My Offers)

**Dynamic Fields by Subcategory:**

*Note: These are examples for common subcategories. Full list in [CATEGORIES.md](../architecture/CATEGORIES.md)*

#### Vehicle - Auto
- Year, Make, Model
- VIN (optional)
- Current insurance provider
- Coverage level desired (Liability only, Full coverage, etc.)
- Number of drivers
- Primary use (Commute, Personal, Business)

#### Property - Homeowners
- Property address
- Home type (Single family, Condo, Townhouse, Mobile home)
- Year built
- Square footage
- Current insurance provider
- Coverage amount desired

#### Life
- Coverage amount desired
- Type (Term, Whole, Universal)
- Term length (if applicable)
- Beneficiary information
- Health information (basic)

#### Business
- Business name
- Business type/industry
- Number of employees
- Annual revenue
- Property value
- Coverage types needed (General liability, Property, Workers comp, etc.)

#### Vehicle - Motorcycle
- Year, Make, Model
- VIN (optional)
- Primary use (Recreation, Commute)
- Storage location
- Current insurance provider

#### Vehicle - RV
- Year, Make, Model
- RV type (Class A, B, C, Travel trailer, Fifth wheel)
- VIN (optional)
- Usage (Full-time, Vacation)
- Current insurance provider

#### Vehicle - Boat
- Year, Make, Model
- Boat type (Power, Sail, Personal watercraft)
- Length
- Storage location
- Usage frequency

#### Other - Personal Umbrella Policy
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

**Note:** Email notifications (to admin on new quote, to customer on quote response) will be implemented in Slice 7.

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
│   ├── quote-forms/
│   │   ├── QuoteFormWrapper.vue     # Main form wrapper with category/subcategory selection
│   │   ├── VehicleAutoFields.vue    # Vehicle - Auto specific fields
│   │   ├── PropertyHomeFields.vue   # Property - Homeowners specific fields
│   │   ├── LifeFields.vue           # Life insurance fields
│   │   ├── BusinessFields.vue       # Business insurance fields
│   │   └── ... (additional subcategory field components as needed)
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

### Vehicle - Auto
- Year: Required, 1900-current year+1
- Make: Required, max 50 chars
- Model: Required, max 50 chars
- VIN: Optional, exactly 17 chars if provided
- Coverage level: Required

### Property - Homeowners
- Address: Required
- Home type: Required
- Year built: Required, 1800-current year
- Square footage: Required, min 1

### Life
- Coverage amount: Required, min $10,000
- Type: Required
- Health information: Required

### Business
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
- [x] Submit quote for each insurance type
- [x] View all quotes in dashboard
- [x] View individual quote details
- [ ] Update quote with additional notes (deferred to admin features)
- [ ] Cancel/delete quote (deferred to admin features)
- [x] Navigation guard redirects to login when not authenticated

### Form Validation
- [x] Required fields show errors
- [x] Invalid data rejected (e.g., year out of range)
- [x] Character limits enforced
- [x] Dynamic fields show/hide correctly

### Backend Testing
- [x] API creates quote correctly
- [x] Quote data stored as JSON
- [x] User can only see their own quotes
- [ ] Admin can see all quotes (deferred to admin features)
- [ ] Status updates work (deferred to admin features)
- [ ] Pagination works for quote list (deferred - not many quotes yet)

### Responsive Design
- [x] Dashboard works on mobile
- [x] Quote form works on mobile
- [x] Tables scroll horizontally on small screens
- [x] Form inputs are touch-friendly

### Error Handling
- [x] Network errors show user-friendly message
- [x] Invalid data returns clear error
- [x] 404 for non-existent quote
- [x] 403 for accessing another user's quote

---

## Success Criteria

- ✅ Authenticated users can submit quote requests for all insurance categories and subcategories
- ✅ Dynamic form fields show based on selected category and subcategory
- ✅ All quote data saved correctly to database
- ✅ Users can view their quote history
- ✅ Quote status visible with colored badges
- ✅ Dashboard shows quick overview of user's quotes
- ✅ Form validation prevents invalid submissions
- ✅ Mobile-friendly interface
- ✅ No console errors

**Note:** Email notifications moved to Slice 7 (Email & Notifications)

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

**Backend Development:** 2-3 hours ✅
- Quote endpoints
- Quote service logic
- Data validation

**Frontend - Quote Form:** 2-3 hours ✅
- Main form component
- Dynamic field components (17 forms total)
- Form validation
- API integration

**Frontend - Dashboard:** 1-2 hours ✅
- Dashboard layout
- Stats cards
- Quotes table
- Quote detail view

**Testing & Polish:** 1-2 hours ✅
- Form testing
- API testing
- Responsive design
- Bug fixes

**Total:** 6-10 hours (Actual: ~8 hours)

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

## Completion Summary

**Completed:** 2025-11-04

**What Was Built:**
- 17 quote forms covering all insurance categories and subcategories
- Dynamic form selection based on category and subcategory
- Full backend API with quote endpoints
- User dashboard with quote history and filtering
- Quote detail view page
- Form validation with shared validation utilities
- Character limits on description fields
- Currency formatting and full name validation
- Protected routes requiring authentication
- Database schema refactored to use category + subcategory structure

**Deferred to Other Slices:**
- Email notifications → Slice 7 (Email & Notifications)
- Admin quote management → Slice 6 (Admin Dashboard)
- Quote status updates by admin → Slice 6 (Admin Dashboard)

---

**Document Version:** 1.1
**Created:** 2025-10-28
**Last Updated:** 2025-11-04
