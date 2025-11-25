# Slice 4: Claims System

**Estimated Time:** 4-6 hours
**Dependencies:** Slice 1, 2, and 3 must be complete
**Status:** ✅ Complete

---

## Overview

Lightweight claims reporting system where customers give the agent a heads-up about an incident they plan to discuss. Provides basic incident information so agents are prepared when customers arrive in person or call.

**Note:** This is a lightweight claims reporting system where customers provide basic incident information to help agents prepare for their visit. This is NOT a full claim processing system - no sensitive PII or policy numbers are collected, no financial tracking, and no claim status workflows.

**Key Concept:** "Planning to file a claim? Let us know when you'll stop by."

---

## Goals

- [x] Create public page explaining claim filing process and optional reporting
- [x] Create claim form with basic incident fields by insurance type
- [x] Implement backend API for claim submission and viewing
- [x] Add claim history to user dashboard
- [x] Enable simple contact preference and appointment requests

**Not Goals:**
- ❌ No claim status tracking (submitted/under review/approved/denied)
- ❌ No adjuster assignment or notes
- ❌ No claim amounts or financial processing
- ❌ No document uploads or photo submission
- ❌ No approval/denial workflow

**Note:** Email notifications moved to Slice 7 (Email & Notifications)

---

## Features to Implement

### 1. Claim Information Page

**Route:** `/claims` (public)

**Content:**
- [ ] Hero: "Planning to File a Claim? We're Here to Help"
- [ ] 3-step process:
  1. **Optional Heads-Up** - Give us a heads-up online (optional)
  2. **Come In or Call** - Visit office or call to file claim
  3. **We Handle the Rest** - Agent processes claim with your insurance carrier
- [ ] What to bring when filing:
  - Policy number
  - Incident details and photos (if applicable)
  - Police/incident report (if applicable)
  - Contact info for other parties (if applicable)
- [ ] Contact information:
  - Phone: (541) 555-0123
  - Business hours: Mon-Fri 8am-5pm PST
  - Address: [Office address]
- [ ] CTAs:
  - "Submit Claim" button (optional, requires login)
  - "Call Us Now" button (tel: link)
  - "Walk-In Welcome" message

**Tone:** Reassuring, low-pressure, emphasizing this is OPTIONAL and helpful, not required.

### 2. Claim Submission Form

**Route:** `/claims/submit` (protected - requires authentication)

**Core Fields (All Types):**
- [ ] Insurance category selector (dropdown) - see [CATEGORIES.md](../architecture/CATEGORIES.md)
- [ ] Insurance subcategory selector (dropdown, dependent on category)
- [ ] Incident date (required, date picker, max = today)
- [ ] Brief incident summary (required, textarea, 250 chars max, character counter)
- [ ] Preferred appointment date/time (optional, datetime picker)
- [ ] Contact preference (dropdown: Email, Phone, Both)
- [ ] Preferred contact time (optional, dropdown: Morning, Afternoon, Evening, Anytime)
- [ ] Additional notes (optional, textarea, 250 chars max, character counter)
- [ ] Submit button with loading state

**Form Behavior:**
- Category selection shows subcategory dropdown (if applicable)
- Subcategory selection loads basic incident fields
- Character counters on textareas (red when over limit)
- Submit button disabled until required fields valid
- Success message: "Thanks! We received your claim information. Stop by anytime or we'll contact you soon."

**No Collection:**
- ❌ No policy numbers
- ❌ No SSN, driver's license, or other govt IDs
- ❌ No detailed financial information
- ❌ No claim amounts or repair estimates
- ❌ No full addresses (location descriptions only)

---

## Dynamic Fields by Category/Subcategory

**Validation Pattern:** Use shared utilities from `@/utils/validation` and `@/utils/formatters`

### Vehicle - Auto

**Fields:**
- [ ] Incident type (dropdown, required): Collision with vehicle, Collision with object, Hit and run, Vandalism, Theft, Glass damage, Weather damage, Animal collision, Other
- [ ] Incident location (text, required, max 250 chars)
- [ ] Other party involved? (yes/no, required)
  - If yes:
    - [ ] Other party name (text, required, use full name validation)
    - [ ] Other party insurance company (text, optional, max 100 chars)
    - [ ] Other party phone (tel, optional, format: (xxx) xxx-xxxx)
- [ ] Police report filed? (yes/no, required)
  - If yes:
    - [ ] Report number (text, required, max 50 chars)
    - [ ] Police department (text, required, max 100 chars)
- [ ] Vehicle drivable? (yes/no, required)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

**Removed:** Policy numbers, estimated damage cost

### Vehicle - Motorcycle

**Fields:**
- [ ] Incident type (dropdown, required): Collision with vehicle, Collision with object, Dropped bike, Theft, Vandalism, Weather damage, Other
- [ ] Incident location (text, required, max 250 chars)
- [ ] Protective gear worn (checkboxes, optional): Helmet, Jacket, Gloves, Boots, Pants, None
- [ ] Other party involved? (yes/no, required)
  - If yes: Same fields as Auto (name, insurance company, phone)
- [ ] Police report filed? (yes/no, required)
  - If yes: Same fields as Auto (report number, department)
- [ ] Motorcycle drivable? (yes/no, required)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

### Vehicle - ATV/Off-road

**Fields:**
- [ ] Incident type (dropdown, required): Rollover, Collision, Mechanical failure, Theft, Vandalism, Other
- [ ] Incident location (text, required, max 250 chars)
- [ ] Terrain type (dropdown, required): Trail, Desert, Mountain, Private property, Other
- [ ] Other party involved? (yes/no, required)
  - If yes: Same fields as Auto (name, insurance company, phone)
- [ ] Injuries sustained? (yes/no, required)
  - If yes:
    - [ ] Medical attention received? (yes/no, required)
- [ ] Vehicle operational? (yes/no, required)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

### Vehicle - Roadside

**Fields:**
- [ ] Service type (dropdown, required): Flat tire, Dead battery, Lockout, Out of fuel, Tow needed, Other
- [ ] Service location (text, required, max 250 chars)
- [ ] Service date/time (datetime, required, max = now)
- [ ] Service provider (text, optional, max 100 chars)
- [ ] Service description (textarea, required, 50-250 chars, character counter)

**Removed:** Service cost, receipt tracking

### Vehicle - Snowmobile

**Fields:**
- [ ] Incident type (dropdown, required): Collision, Rollover, Avalanche, Theft, Vandalism, Mechanical failure, Other
- [ ] Incident location (text, required, max 250 chars)
- [ ] Weather conditions (dropdown, required): Clear, Snowing, Icy, Blizzard, Poor visibility
- [ ] Other party involved? (yes/no, required)
  - If yes: Same fields as Auto
- [ ] Injuries sustained? (yes/no, required)
  - If yes: Medical attention received? (yes/no)
- [ ] Snowmobile operational? (yes/no, required)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

### Vehicle - Boat

**Fields:**
- [ ] Incident type (dropdown, required): Collision with vessel, Collision with object, Sinking, Fire, Theft, Vandalism, Weather damage, Grounding, Other
- [ ] Incident location (dropdown, required): Lake, River, Ocean, Marina, Storage facility, Trailer
- [ ] Water conditions (dropdown, required): Calm, Moderate, Rough, Storm
- [ ] Other vessel involved? (yes/no, required)
  - If yes:
    - [ ] Other vessel operator name (text, required, use full name validation)
    - [ ] Other vessel registration (text, optional, max 50 chars)
- [ ] Coast Guard report filed? (yes/no, required)
  - If yes:
    - [ ] Report number (text, required, max 50 chars)
- [ ] Boat operational? (yes/no, required)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

**Removed:** Other vessel insurance details

### Vehicle - RV

**Fields:**
- [ ] Incident type (dropdown, required): Collision, Fire, Theft, Vandalism, Weather damage, Water damage, Appliance failure, Other
- [ ] Incident location (text, required, max 250 chars)
- [ ] RV in motion when incident occurred? (yes/no, required)
- [ ] Other party involved? (yes/no, required)
  - If yes: Same fields as Auto
- [ ] Police report filed? (yes/no, required)
  - If yes: Same fields as Auto
- [ ] RV drivable? (yes/no, required)
- [ ] Living quarters affected? (yes/no, required)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

### Vehicle - Vehicle Protection

**Fields:**
- [ ] Issue type (dropdown, required): Mechanical breakdown, Engine failure, Transmission failure, Electrical issue, Other
- [ ] Current mileage (number, required, min 0)
- [ ] Warning signs before failure (textarea, optional, max 250 chars)
- [ ] Vehicle currently operable? (yes/no, required)
- [ ] Issue description (textarea, required, 50-250 chars, character counter)

**Removed:** Repair shop info, diagnosis, estimated repair cost

### Property - Homeowners

**Fields:**
- [ ] Incident type (dropdown, required): Fire, Water damage, Wind damage, Hail damage, Theft, Vandalism, Liability claim, Tree damage, Other
- [ ] Area affected (checkboxes, required at least one): Roof, Exterior walls, Interior, Kitchen, Bathroom, Bedrooms, Basement, Garage, Yard, Other
- [ ] Damage extent (dropdown, required): Minor, Moderate, Severe, Catastrophic
- [ ] Emergency repairs needed? (yes/no, required)
- [ ] Currently living in home? (yes/no, required)
- [ ] Police report filed? (yes/no, required)
  - If yes: Same fields as Auto (report number, department)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

**Removed:** Contractor names, emergency repair costs, other party policy numbers

### Property - Renters

**Fields:**
- [ ] Incident type (dropdown, required): Theft, Fire, Water damage, Vandalism, Liability claim, Other
- [ ] Items affected (checkboxes, required at least one): Electronics, Furniture, Clothing, Jewelry, Appliances, Other personal property
- [ ] Police report filed? (yes/no, required)
  - If yes: Same fields as Auto
- [ ] Landlord notified? (yes/no, required)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

**Removed:** Number of items, approximate total value

### Property - Condo

**Fields:**
- [ ] Incident type (dropdown, required): Fire, Water damage, Wind damage, Theft, Vandalism, Liability claim, Other
- [ ] Area affected (checkboxes, required at least one): Unit interior, Balcony/Patio, Personal property, Common area, Other
- [ ] Damage extent (dropdown, required): Minor, Moderate, Severe, Catastrophic
- [ ] HOA notified? (yes/no, required)
- [ ] Common area issue? (yes/no, required)
- [ ] Currently living in unit? (yes/no, required)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

**Removed:** Emergency repair costs, contractor info

### Property - Landlord

**Fields:**
- [ ] Incident type (dropdown, required): Fire, Water damage, Wind damage, Tenant damage, Vandalism, Liability claim, Other
- [ ] Tenant involved? (yes/no, required)
  - If yes:
    - [ ] Tenant name (text, required, use full name validation)
    - [ ] Tenant caused damage? (yes/no, required)
- [ ] Property currently occupied? (yes/no, required)
- [ ] Rent interruption expected? (yes/no, required)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

**Removed:** Property address (kept general location only), repair costs

### Property - Mobile Home

**Fields:**
- [ ] Incident type (dropdown, required): Fire, Water damage, Wind damage, Structural damage, Theft, Vandalism, Other
- [ ] Area affected (checkboxes, required at least one): Roof, Exterior, Interior, Skirting, Deck/Steps, Shed, Other
- [ ] Damage extent (dropdown, required): Minor, Moderate, Severe, Catastrophic
- [ ] Mobile home movable? (yes/no, required)
- [ ] Currently living in mobile home? (yes/no, required)
- [ ] Damage description (textarea, required, 50-250 chars, character counter)

### Life

**Fields:**
- [ ] Claim type (dropdown, required): Death of insured, Terminal illness diagnosis, Critical illness diagnosis, Other
- [ ] Date of death/diagnosis (date, required, max = today)
- [ ] Physician name (text, optional, max 100 chars)
- [ ] Medical facility (text, optional, max 100 chars)
- [ ] Brief description (textarea, required, 50-250 chars, character counter)

**Note:** Life claims require compassionate messaging. Removed beneficiary contact details (collected during in-person filing).

**Removed:** Beneficiary PII, death certificate status, cause of death details

### Business

**Fields:**
- [ ] Incident type (dropdown, required): Property damage, Liability claim, Business interruption, Employee injury, Data breach, Theft, Vandalism, Other
- [ ] Business operational status (dropdown, required): Fully operational, Partially operational, Temporarily closed
- [ ] Employees affected? (yes/no, required)
- [ ] Third parties involved? (yes/no, required)
  - If yes:
    - [ ] Third party type (dropdown): Customer, Vendor, Contractor, Other business, Other
- [ ] Police report filed? (yes/no, required)
  - If yes: Same fields as Auto
- [ ] Incident description (textarea, required, 50-250 chars, character counter)

**Removed:** Revenue impact, daily loss estimates, third party names

### Identity Protection

**Fields:**
- [ ] Incident type (dropdown, required): Credit card fraud, Bank account fraud, Identity theft, Data breach, Phishing, Tax fraud, Medical identity theft, Other
- [ ] Date discovered (date, required, max = today)
- [ ] Accounts affected (checkboxes, required at least one): Bank account, Credit card, Investment account, Social Security, Medical records, Tax records, Other
- [ ] Police report filed? (yes/no, required)
  - If yes: Same fields as Auto
- [ ] Financial institutions notified? (yes/no, required)
- [ ] Credit bureaus notified? (yes/no, required)
- [ ] Incident description (textarea, required, 50-250 chars, character counter)

**Removed:** Unauthorized charge details, financial impact estimates, specific account numbers

### Other - Personal Umbrella Policy

**Fields:**
- [ ] Underlying incident type (dropdown, required): Auto liability, Home liability, Boat liability, Business liability, Other liability
- [ ] Primary insurance claim filed? (yes/no, required)
  - If yes:
    - [ ] Primary insurance company (text, required, max 100 chars)
- [ ] Third party involved? (yes/no, required)
- [ ] Lawsuit filed? (yes/no, required)
- [ ] Incident description (textarea, required, 50-250 chars, character counter)

**Removed:** Liability amounts, primary claim numbers, third party attorney info

### Other - Individual Health

**Fields:**
- [ ] Service type (dropdown, required): Medical procedure, Hospital stay, Emergency care, Prescription, Medical equipment, Other
- [ ] Service date (date, required, max = today)
- [ ] Healthcare provider (text, required, max 100 chars)
- [ ] Provider type (dropdown, required): Hospital, Clinic, Doctor's office, Urgent care, Emergency room, Pharmacy, Other
- [ ] Service description (textarea, required, 50-250 chars, character counter)

**Removed:** Diagnosis details, treatment specifics, billed amounts, payment amounts

### Other - Pet

**Fields:**
- [ ] Pet name (text, required, max 50 chars)
- [ ] Incident type (dropdown, required): Illness, Injury, Surgery, Emergency care, Other
- [ ] Treatment date (date, required, max = today)
- [ ] Veterinary clinic (text, required, max 100 chars)
- [ ] Treatment description (textarea, required, 50-250 chars, character counter)

**Removed:** Veterinarian name, diagnosis, bill amounts

### Other - Event

**Fields:**
- [ ] Event name (text, required, max 100 chars)
- [ ] Event date (date, required)
- [ ] Incident type (dropdown, required): Cancellation, Postponement, Property damage, Liability claim, Vendor no-show, Weather, Other
- [ ] Cancellation/incident date (date, required, max = today)
- [ ] Reason description (textarea, required, 50-250 chars, character counter)

**Removed:** Non-refundable costs, vendor contract counts, rescheduling details

### Other - Travel

**Fields:**
- [ ] Trip destination (text, required, max 100 chars)
- [ ] Incident type (dropdown, required): Trip cancellation, Trip interruption, Baggage loss, Baggage delay, Medical emergency, Travel delay, Missed connection, Other
- [ ] Scheduled departure date (date, required)
- [ ] Incident date (date, required, max = today)
- [ ] Incident description (textarea, required, 50-250 chars, character counter)

**Removed:** Financial loss amounts, documentation types, refund offers

### Other - Jewelry

**Fields:**
- [ ] Number of items affected (dropdown, required): 1, 2, 3, 4, 5+
- [ ] Incident type (dropdown, required): Theft, Loss, Damage, Other
- [ ] Incident location (text, required, max 250 chars)
- [ ] Police report filed? (yes/no, required)
  - If yes: Same fields as Auto
- [ ] Incident description (textarea, required, 50-250 chars, character counter)

**Removed:** Dynamic item list, item descriptions, values, appraisals

### Other - Collectibles

**Fields:**
- [ ] Number of items affected (dropdown, required): 1, 2-5, 6-10, 11+
- [ ] Item types (checkboxes, required at least one): Art, Coins, Stamps, Sports memorabilia, Antiques, Other
- [ ] Incident type (dropdown, required): Theft, Fire, Water damage, Damage, Other
- [ ] Incident location (text, required, max 250 chars)
- [ ] Police report filed? (yes/no, required)
  - If yes: Same fields as Auto
- [ ] Incident description (textarea, required, 50-250 chars, character counter)

**Removed:** Dynamic item list, specific descriptions, values, appraisals

---

## Backend API Endpoints

```
POST /api/v1/claims/submit    - Create claim (auth required)
GET  /api/v1/claims/my-list   - List user's claims
GET  /api/v1/claims/{id}      - Get claim details
DELETE /api/v1/claims/{id}    - Cancel claim (optional)
```

**Claim Status (Simple):**
1. `submitted` - Just submitted, awaiting agent contact
2. `contacted` - Agent reached out to customer
3. `closed` - No longer needed (customer filed claim or withdrew)

**User Permissions:**
- Users can submit claims
- Users can view their own claims
- Users can cancel claims (optional feature)
- Admins can view all claims and update status (Slice 6)

---

## Database Schema

**claims table**:

```sql
- id (UUID, primary key)
- user_id (UUID, foreign key to users)
- category (String(30), required, indexed) - e.g., 'vehicle', 'property', 'life'
- subcategory (String(30), nullable, indexed) - e.g., 'auto', 'homeowners', null
- incident_date (Date, required)
- incident_summary (Text, required) - Brief summary from form
- claim_data (JSON, required) - Stores all dynamic fields
- appointment_requested (DateTime, nullable) - Preferred appointment time
- contact_preference (Enum, required) - email, phone, both
- preferred_contact_time (String(20), nullable) - morning, afternoon, evening, anytime
- additional_notes (Text, nullable) - Optional customer notes
- status (Enum, required, default='submitted') - submitted, contacted, closed
- contacted_at (DateTime, nullable) - When agent reached out
- created_at (DateTime, required)
- updated_at (DateTime, required)
```

**Indexes:**
- `user_id + status` (composite) - for dashboard filtering
- `category + subcategory` (composite) - for category filtering
- `incident_date` - for date range filtering
- `created_at` - for recent claims

**Removed from full claim tracking:**
- policy_number (no PII)
- claim_amount (no financial tracking)
- adjuster_notes (no claim processing)
- processed_at (no approval workflow)

---

## User Dashboard Integration

**Route:** `/dashboard` (protected)

**Add Claims Section:**
- [ ] Section header: "Claims"
- [ ] "File a Claim" button (primary action)
- [ ] Simple table:
  - Insurance type (category icon + subcategory name)
  - Incident date
  - Submitted date
  - Status (simple badge: submitted, contacted, closed)
  - Actions (View, Cancel)
- [ ] Pagination (10 per page)
- [ ] Simple filtering:
  - Category dropdown
  - Status dropdown (All, Submitted, Contacted, Closed)

**Table Responsive Design:**
- Desktop: All columns visible
- Mobile: Card layout with key info

---

## Claim Detail View

**Route:** `/claims/{id}` (protected)

**Display Sections:**

### Claim Information
- [ ] Claim ID
- [ ] Insurance type (category + subcategory with icon)
- [ ] Incident date
- [ ] Submitted date
- [ ] Status (simple badge)
- [ ] Preferred appointment time (if provided)
- [ ] Contact preference

### Incident Details
- [ ] All submitted form data (readonly)
- [ ] Incident summary
- [ ] Additional notes

### Next Steps
- [ ] Simple message based on status:
  - **Submitted:** "We received your claim information. Stop by anytime or we'll contact you soon."
  - **Contacted:** "We've reached out to you. Looking forward to helping you file your claim."
  - **Closed:** "This claim is closed."

### Actions
- [ ] "Contact Us" button (opens contact form or shows phone)
- [ ] "Cancel Claim" button (if status = submitted)

**No Status Timeline:** Keep it simple - just show current status.

---

## Technical Implementation

### Frontend Components

**File Structure:**
```
frontend/src/
├── views/
│   ├── ClaimsPage.vue                    # Public info page
│   ├── ClaimSubmitPage.vue               # Claim form
│   └── ClaimDetailPage.vue               # Individual claim view
├── components/
│   ├── claim-forms/
│   │   ├── ClaimFormWrapper.vue          # Main form with category/subcategory
│   │   ├── VehicleAutoFields.vue         # Vehicle - Auto claim fields
│   │   ├── VehicleMotorcycleFields.vue   # Vehicle - Motorcycle fields
│   │   ├── VehicleAtvFields.vue          # Vehicle - ATV/off-road fields
│   │   ├── VehicleRoadsideFields.vue     # Vehicle - Roadside fields
│   │   ├── VehicleSnowmobileFields.vue   # Vehicle - Snowmobile fields
│   │   ├── VehicleBoatFields.vue         # Vehicle - Boat fields
│   │   ├── VehicleRvFields.vue           # Vehicle - RV fields
│   │   ├── VehicleProtectionFields.vue   # Vehicle - Vehicle Protection fields
│   │   ├── PropertyHomeFields.vue        # Property - Homeowners fields
│   │   ├── PropertyRentersFields.vue     # Property - Renters fields
│   │   ├── PropertyCondoFields.vue       # Property - Condo fields
│   │   ├── PropertyLandlordFields.vue    # Property - Landlord fields
│   │   ├── PropertyMobileFields.vue      # Property - Mobile home fields
│   │   ├── LifeFields.vue                # Life insurance fields
│   │   ├── BusinessFields.vue            # Business insurance fields
│   │   ├── IdentityFields.vue            # Identity Protection fields
│   │   ├── OtherUmbrellaFields.vue       # Other - Personal Umbrella fields
│   │   ├── OtherHealthFields.vue         # Other - Individual Health fields
│   │   ├── OtherPetFields.vue            # Other - Pet fields
│   │   ├── OtherEventFields.vue          # Other - Event fields
│   │   ├── OtherTravelFields.vue         # Other - Travel fields
│   │   ├── OtherJewelryFields.vue        # Other - Jewelry fields
│   │   └── OtherCollectiblesFields.vue   # Other - Collectibles fields
│   └── dashboard/
│       └── ClaimsList.vue                # Claims table
└── services/
    └── claims.ts                         # API client
```

**Total Forms:** 24 claim forms (one per category/subcategory combination)

### Backend Files

```
backend/app/
├── routers/
│   └── claims.py                         # Claim endpoints
├── services/
│   └── claim_service.py                  # Business logic
├── schemas/
│   └── claim_schemas.py                  # Pydantic models
└── models/
    └── claim.py                          # Claim model
```

### Routes to Add

```typescript
// Public route
{
  path: '/claims',
  name: 'claims',
  component: ClaimsPage
},

// Protected routes
{
  path: '/claims/submit',
  name: 'claim-submit',
  component: ClaimSubmitPage,
  meta: { requiresAuth: true }
},
{
  path: '/claims/:id',
  name: 'claim-detail',
  component: ClaimDetailPage,
  meta: { requiresAuth: true }
}
```

---

## Form Validation

### Shared Utilities (from Slice 3)
- **Full name validation:** `@/utils/validation` - validates "First Last" format
- **Character counters:** Red border when over limit, no error text

### Common Fields (All Claims)
- Incident date: Required, not future, not more than 2 years past
- Incident summary: Required, 250 chars max, character counter
- Contact preference: Required, dropdown selection
- Additional notes: Optional, 250 chars max, character counter

### Field-Specific Validation
- **Text inputs:** Max length enforced, trimmed
- **Textareas:** Character counter, red border when over limit
- **Dates:** Date picker, range validation
- **Phone:** Format (xxx) xxx-xxxx
- **Checkboxes (when required):** At least one selected
- **Yes/No:** Required selection
- **Dropdowns:** Required selection from valid options

### Conditional Validation
- If "Other party involved" = Yes, other party name required
- If "Police report filed" = Yes, report number + department required
- If "Injuries sustained" = Yes, medical attention question required

---

## Design Specifications

### Info Page (Public)
- **Hero:** Blue gradient, white text, "Planning to File a Claim? We're Here to Help"
- **Steps:** Simple 3-step process, vertical on mobile, horizontal on desktop
- **Tone:** Warm, reassuring, low-pressure
- **Emphasis:** Reporting is OPTIONAL - customers can walk in anytime

### Claim Form (Protected)
- **Layout:** Single column, max-width 800px, centered
- **Category/Subcategory:** Dropdowns at top
- **Fields:** Label above input, required asterisk, character counter below textareas
- **Validation:** Red border on invalid (no error text)
- **Submit button:** Blue, full width on mobile, disabled until valid, loading spinner
- **Success:** Green checkmark, simple message, "View Claim" and "Done" buttons

### Dashboard Claims Section
- **Placement:** Below quotes section, same styling
- **Table:** Striped rows, hover highlight
- **Status badges:** Simple colored pills
  - `submitted`: Blue background, white text
  - `contacted`: Green background, white text
  - `closed`: Gray background, white text
- **Mobile:** Card layout, touch-friendly buttons

### Detail Page
- **Simple layout:** Single column, readonly fields
- **Readonly fields:** Light gray background, no border
- **Status badge:** Top of page, prominent
- **Actions:** "Contact Us" and "Cancel" buttons at bottom

---

## Testing Checklist

### Functionality Testing
- [ ] Public claims info page loads
- [ ] Submit claims for all 24 category/subcategory combinations
- [ ] View claims in dashboard
- [ ] View individual claim details
- [ ] Cancel claim (if implemented)
- [ ] Auth guards redirect to login when not authenticated
- [ ] Users can only access their own claims

### Form Validation Testing
- [ ] Required fields show red border when empty
- [ ] Incident date constraints (not future, not > 2 years past)
- [ ] Character limits enforced on textareas
- [ ] Character counters update correctly
- [ ] Conditional fields show/hide correctly
- [ ] Full name validation on name fields
- [ ] Submit button disabled until form valid

### Backend Testing
- [ ] API creates claims correctly
- [ ] Claim data stored in JSON field
- [ ] Category + subcategory stored in separate columns
- [ ] User access control (users see only their claims)
- [ ] Pagination works
- [ ] Filtering works (category, status)
- [ ] Audit logging captures claim actions

### Responsive Design
- [ ] Claims info page mobile-friendly
- [ ] Claim form works on mobile (touch inputs, date pickers)
- [ ] Dashboard table responsive (cards on mobile)
- [ ] Detail page responsive
- [ ] All touch targets minimum 44x44px

### Error Handling
- [ ] Network errors show user-friendly message
- [ ] Invalid data returns clear error from backend
- [ ] 404 for non-existent claim
- [ ] 403 for accessing another user's claim
- [ ] Form validation errors clear
- [ ] Graceful handling of missing data

---

## Success Criteria

- ✅ Users can submit claims for all categories/subcategories
- ✅ Public claims info page accessible and reassuring
- ✅ Claim data saved to database with category+subcategory structure
- ✅ Dashboard shows claim history with simple status badges
- ✅ Individual claim details accessible
- ✅ Form validation prevents invalid submissions
- ✅ Mobile-friendly, responsive design
- ✅ No PII collected (no policy numbers, SSNs, addresses, etc.)
- ✅ No console errors
- ✅ Audit logging for all claim actions

---

## Security Considerations

- [ ] Authentication required for claim submission and viewing
- [ ] Users can only access their own claims (user_id check)
- [ ] Data sanitization on all inputs (prevent XSS)
- [ ] SQL injection prevention (using SQLAlchemy ORM)
- [ ] CSRF protection (handled by FastAPI)
- [ ] Rate limiting on claim submission (prevent spam)
- [ ] Audit logging for all claim actions
- [ ] No sensitive PII collected - LOW STAKES data

**Security Note:** This is intentionally LOW-STAKES. No policy numbers, no financial data, no government IDs. Basic incident info only.

---

## Future Enhancements (Not in this slice)

**Slice 6 - Admin Dashboard:**
- Admin view all claims
- Update claim status (contacted, closed)
- Add internal notes (not visible to customer)

**Slice 7 - Email Notifications:**
- Email to admin on new claim
- Email to customer confirming receipt

**Future Considerations:**
- SMS notification option
- Appointment scheduling integration
- Direct messaging with agent
- Upload photos during submission (optional)

---

## Estimated Breakdown

**Backend Development:** 1-2 hours
- Claim endpoints (submit, list, get, cancel)
- Service logic (simple validation, no complex business rules)
- Schema validation (24 different field sets)
- Audit logging integration

**Frontend - Info Page:** 30 minutes
- Public info page with 3-step process
- Contact information
- Reassuring messaging

**Frontend - Claim Forms:** 2-3 hours
- Form wrapper with category/subcategory selection
- 24 field components for all category/subcategory combinations
- Reuse validation utilities from Slice 3
- Reuse formatters from Slice 3
- Character counters
- API integration

**Frontend - Dashboard Integration:** 30 minutes
- Claims section in dashboard
- Simple table with filtering
- Status badges

**Frontend - Detail View:** 30 minutes
- Claim detail page
- Readonly fields display
- Simple status and next steps
- Actions (contact, cancel)

**Testing & Polish:** 1 hour
- Test all 24 claim forms
- API testing
- Responsive design testing
- Bug fixes

**Total:** 4-6 hours

---

## Dependencies for Future Slices

**Slice 5 (Contact System):**
- Contact form reuses form structure
- Dashboard integration pattern established

**Slice 6 (Admin Dashboard):**
- Admin needs to view claims
- Update status (contacted, closed)
- Add internal notes

**Slice 7 (Email & Notifications):**
- Email to admin on new claim
- Email to customer confirming receipt

---

## Implementation Notes

### Reuse from Slice 3 (Quote System)
- Backend structure nearly identical (simpler field definitions)
- Form wrapper with category/subcategory selection pattern
- Dynamic field rendering based on selection
- Shared validation utilities (`@/utils/validation`)
- Shared formatters (`@/utils/formatters`)
- Character counters on textareas (250 char limit)
- Red border validation (no error text)
- Dashboard table layout and styling
- Status badge styling pattern
- Date picker components
- Loading states and success messages

### Key Differences from Quote Forms
**Quote Forms:** "What do you want to insure?" (prospective, detailed)
- Ask for policy details, coverage amounts
- Ask for property/vehicle specifications
- Collect detailed personal information

**Claim Forms:** "Basic incident info for heads-up" (lightweight, simple)
- No policy numbers or coverage details
- Basic incident type and description
- Minimal personal information
- Emphasize this is OPTIONAL

### Key Differences from Full Claim Processing
**Full Claim Processing (NOT this slice):** "Complete claim submission with PII"
- Policy numbers required
- Claim amounts and estimates
- Adjuster notes and status tracking
- Approval/denial workflow
- Document uploads

**Claims System (THIS slice):** "Light reporting for appointment prep"
- No policy numbers
- No financial information
- No claim processing
- Simple status (submitted, contacted, closed)
- No document handling

---

## Development Sequence

**Recommended Order:**
1. Backend API (claims.py, service, schemas, model)
2. Test backend with Swagger/Postman
3. Claims info page (ClaimsPage.vue - static content)
4. Form wrapper (ClaimFormWrapper.vue - category/subcategory selection)
5. Build 2-3 claim forms (e.g., Auto, Homeowners, Pet)
6. Test submission end-to-end
7. Build remaining 21 claim forms (replicate pattern)
8. Dashboard integration (claims section, table)
9. Claim detail view (ClaimDetailPage.vue)
10. Testing, responsive design, bug fixes

**Parallel Work:**
- Backend and public page can be done simultaneously
- Once form wrapper is built, individual forms can be built in any order
- Dashboard and detail view can be built after core submission works

---

## Completion Summary

**Status:** ✅ Complete

**What Was Built:**
- 24 claim forms covering all insurance categories and subcategories
- Public claims information page (ClaimsPage.vue) explaining the process
- Claim submission form (ClaimSubmitPage.vue) with dynamic field selection
- Claim detail view (ClaimDetailPage.vue) showing submitted information
- Full backend API with claim endpoints (POST, GET my-claims, GET by ID)
- Dashboard integration showing claim history with status badges
- Form validation using shared validation utilities
- Character limits on description fields (250 chars)
- Incident date validation (not future, not >2 years past)
- Simple status tracking (submitted, contacted, closed)
- Protected routes requiring authentication
- Database schema with category + subcategory structure

**What Was Deferred:**
- Email notifications → Slice 7 (Email & Notifications)
- Admin claim management → Slice 6 (Admin Dashboard)
- Claim status updates by admin → Slice 6 (Admin Dashboard)

**Forms Implemented (24 total):**

**Vehicle (8 forms):**
- Auto, Motorcycle, ATV/Off-road, Roadside Assistance, Snowmobile, Boat, RV, Vehicle Protection

**Property (5 forms):**
- Homeowners, Renters, Condo, Landlord, Mobile Home

**Other Categories (3 forms):**
- Life Insurance, Business Insurance, Identity Protection

**Other Subcategories (8 forms):**
- Personal Umbrella Policy, Individual Health, Pet, Event, Travel, Jewelry, Collectibles

**Key Features:**
- Lightweight incident reporting (no PII, no policy numbers, no financial data)
- Optional appointment request
- Contact preference selection
- All claims viewable in user dashboard
- Mobile-responsive design
- Shared validation and formatting utilities
- Consistent with Quote System patterns

---

**Document Version:** 3.1
**Created:** 2025-11-04
**Completely Rewritten:** 2025-11-18
**Updated:** 2025-11-21 - Marked as complete
