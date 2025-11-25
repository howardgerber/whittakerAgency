# Insurance Categories & Subcategories

This document defines the **official category structure** for the Whittaker Agency website.

**IMPORTANT:** This is the single source of truth for all insurance categories and subcategories. Always reference this document when working with insurance types.

---

## Categories & Subcategories

### 🚗 Vehicle
- Auto
- Motorcycle
- ATV/off-road
- Roadside
- Snowmobile
- Boat
- RV
- Vehicle Protection

### 🏠 Property
- Homeowners
- Renters
- Condo
- Landlord
- Mobile home

### ❤️ Life
*(No subcategories)*

### 💼 Business
*(No subcategories)*

### 🔒 Identity Protection
*(No subcategories)*

### ☂️ Other
- Personal umbrella policy
- Individual health
- Pet
- Event
- Travel
- Jewelry
- Collectibles

---

## Data Storage Format

In the database, insurance types are stored using **two separate columns**:

**Tables:** `quote_requests`, `claims`

**Columns:**
- `category` (String(30), required, indexed) - Examples: `vehicle`, `property`, `life`, `business`, `identity_protection`, `other`
- `subcategory` (String(30), nullable, indexed) - Examples: `auto`, `motorcycle`, `homeowners`, `renters`, `pet`, `travel`

**Examples:**

| Category | Subcategory | Description |
|----------|-------------|-------------|
| `vehicle` | `auto` | Auto insurance |
| `vehicle` | `motorcycle` | Motorcycle insurance |
| `property` | `homeowners` | Homeowners insurance |
| `property` | `renters` | Renters insurance |
| `life` | `null` | Life insurance (no subcategory) |
| `business` | `null` | Business insurance (no subcategory) |
| `identity_protection` | `null` | Identity protection (no subcategory) |
| `other` | `pet` | Pet insurance |
| `other` | `travel` | Travel insurance |

**Benefits:**
- Easy category-level filtering: `WHERE category = 'vehicle'`
- Better for analytics and reporting
- Cleaner data normalization
- Simpler validation

---

## Implementation Notes

### Frontend Display
- Category cards shown on Services Overview page
- Each category has a dedicated page showing its subcategories
- Quote forms use category + subcategory selection

### Backend Validation
- The `category` and `subcategory` fields in `quote_requests` and `claims` tables store values separately
- Maximum length: 30 characters each
- Format: lowercase with underscores for multi-word categories (e.g., `identity_protection`, `phone_protection`)
- Subcategory can be `null` for categories without subcategories

### Filtering & Dropdowns
- Category dropdown shows only categories the user has quotes/claims for
- Subcategory dropdown is dependent on selected category
- Year dropdown shows only years with data

---

**Document Version:** 1.0
**Created:** 2025-11-01
**Last Updated:** 2025-11-01
