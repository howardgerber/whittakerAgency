# Slice 2: Core Pages & Navigation

**Estimated Time:** 10-15 hours
**Dependencies:** Slice 1 (Foundation & Infrastructure) must be complete
**Status:** ✅ Complete (2025-10-28)

---

## Overview

This slice focuses on building out the public-facing pages and navigation system. Users should be able to browse the site, learn about services, meet the team, and understand the agency's Oregon connection - all without needing to log in.

---

## Goals

- [x] Create comprehensive navigation system (header/nav bar)
- [x] Build detailed Services page with all 8 insurance types
- [x] Create full Team page with team member profiles
- [x] Enhance About/Oregon Connection content
- [x] Ensure mobile-responsive design
- [x] Add smooth navigation between pages
- [x] Polish the overall user experience

---

## Features to Implement

### 1. Navigation Component

**Header/Navigation Bar**
- [ ] Company logo/branding
- [ ] Main navigation links:
  - Home
  - Services
  - About Us / Oregon Connection
  - Meet the Team
  - Get a Quote (protected - requires login)
  - Contact
- [ ] User menu (when authenticated):
  - Welcome message with user name
  - Dashboard link
  - My Quotes
  - My Claims
  - Logout button
- [ ] Sign In / Register buttons (when not authenticated)
- [ ] Mobile hamburger menu
- [ ] Sticky header (stays at top on scroll)
- [ ] Active page highlighting

**Footer (enhance existing)**
- [ ] Social media links (optional)
- [ ] Privacy policy link
- [ ] Terms of service link
- [ ] Accessibility statement

### 2. Services Page

**Route:** `/services`

**Content Structure:**
- [ ] Hero section: "Comprehensive Insurance Coverage for Oregon"
- [ ] Grid of 8 insurance types (cards with icons)
- [ ] Detailed section for each insurance type:
  - **Auto Insurance**
    - Coverage types (liability, collision, comprehensive)
    - Oregon-specific requirements
    - Discounts available
  - **Home Insurance**
    - Property coverage
    - Liability protection
    - Additional living expenses
    - Oregon weather considerations (rain, earthquakes)
  - **Life Insurance**
    - Term vs whole life
    - Coverage amounts
    - Beneficiary information
  - **Business Insurance**
    - General liability
    - Property coverage
    - Workers compensation
    - Professional liability
  - **Health Insurance**
    - Individual plans
    - Family coverage
    - Network providers
    - Prescription coverage
  - **Umbrella Insurance**
    - Additional liability protection
    - Coverage limits
    - What it covers beyond standard policies
  - **Motorcycle Insurance**
    - Required coverage in Oregon
    - Optional coverages
    - Seasonal riders
  - **RV Insurance**
    - Full-time vs recreational use
    - Coverage for personal belongings
    - Roadside assistance
- [ ] CTA buttons: "Get a Quote" for each service
- [ ] Comparison table (optional)

### 3. About Us / Oregon Connection Page

**Route:** `/about`

**Content Structure:**
- [ ] Hero section with Oregon landscape
- [ ] Company story
  - Founded in Oregon
  - Years of experience
  - Mission statement
  - Values
- [ ] Why Choose Whittaker Agency
  - Local expertise
  - Personalized service
  - Trusted advisors
  - 24/7 support
  - Oregon-specific knowledge
- [ ] Oregon connection expanded
  - Understanding Oregon weather/natural disasters
  - Knowledge of local regulations
  - Community involvement
  - Supporting Oregon families and businesses
- [ ] Statistics/achievements (optional)
  - Years in business
  - Families served
  - Client satisfaction rate
- [ ] Portland Oregon stag sign image (prominent)
- [ ] Call to action: "Ready to get started?"

### 4. Team Page

**Route:** `/team`

**Content Structure:**
- [ ] Hero section: "Meet Our Expert Team"
- [ ] Team member grid (6 members)
  - Photo (circular avatar or professional headshot)
  - Full name
  - Title/role
  - Bio/background
  - Specialties
  - Contact email (optional)
  - LinkedIn profile (optional)

**Team Member Profiles to Create:**
1. **Kyle Whittaker** - Founder & Lead Agent
2. **Michael Chen** - Commercial Insurance Specialist
3. **Jennifer Martinez** - Personal Lines Agent
4. **David Thompson** - Claims Specialist
5. **Emily Rodriguez** - Life Insurance Advisor
6. **James Anderson** - Customer Service Manager

**Note:** Use placeholder photos initially (initials in circles), can add real photos later

### 5. Enhanced Home Page

**Improvements to existing HomePage.vue:**
- [ ] Add CTA buttons that link to Services and Team pages
- [ ] Make service cards clickable (link to Services page with anchor)
- [ ] Add testimonials section (optional)
- [ ] Add "How It Works" process section (optional)
- [ ] Ensure all sections flow smoothly

---

## Technical Implementation

### Frontend Components to Create

```
frontend/src/
├── components/
│   ├── layout/
│   │   ├── Header.vue           # Main navigation
│   │   ├── Footer.vue           # Move footer from HomePage
│   │   └── Layout.vue           # Wrapper with header + router-view + footer
│   ├── navigation/
│   │   ├── NavBar.vue           # Desktop navigation
│   │   ├── MobileMenu.vue       # Mobile hamburger menu
│   │   └── UserMenu.vue         # Authenticated user dropdown
│   └── shared/
│       ├── ServiceCard.vue      # Reusable service card
│       ├── TeamMemberCard.vue   # Team member profile card
│       └── PageHero.vue         # Reusable page hero section
├── views/
│   ├── HomePage.vue             # Already created (enhance)
│   ├── ServicesPage.vue         # NEW
│   ├── AboutPage.vue            # NEW
│   └── TeamPage.vue             # NEW
└── router/
    └── index.ts                 # Add new routes
```

### Routes to Add

```typescript
{
  path: '/services',
  name: 'services',
  component: ServicesPage
},
{
  path: '/about',
  name: 'about',
  component: AboutPage
},
{
  path: '/team',
  name: 'team',
  component: TeamPage
}
```

### Navigation Guard Updates

```typescript
// No navigation guards needed yet - all pages are public
// Will add protected routes in Slice 3 (Quote Request System)
```

---

## Design Specifications

### Color Palette
- **Primary:** `#2f4f4f` (Dark Slate Gray - professional, trustworthy)
- **Secondary:** `#4682b4` (Steel Blue - Oregon sky)
- **Accent:** `#228b22` (Forest Green - Oregon nature)
- **Text:** `#333333` (Dark Gray)
- **Background:** `#ffffff` (White)
- **Light Gray:** `#f8f9fa` (Section backgrounds)

### Typography
- **Headings:** System font stack (can upgrade to custom font later)
- **Body:** System font stack
- **Line height:** 1.6-1.8 for readability

### Responsive Breakpoints
```css
/* Mobile */
@media (max-width: 768px) { }

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) { }

/* Desktop */
@media (min-width: 1025px) { }
```

### Component Styling Patterns
- Use scoped styles in Vue components
- CSS variables for theming
- Box shadows for depth: `0 2px 4px rgba(0, 0, 0, 0.1)`
- Border radius: `8px` for cards and buttons
- Transitions: `0.3s ease` for hover effects

---

## Content Requirements

### Services Page Content

#### Auto Insurance
```
Protect your vehicle with comprehensive auto insurance coverage.

Coverage Options:
• Liability Coverage - Required in Oregon
• Collision Coverage - Repairs to your vehicle
• Comprehensive Coverage - Non-collision damage
• Uninsured/Underinsured Motorist - Protection from others
• Medical Payments - Healthcare costs after accident

Oregon Requirements:
• Minimum liability: $25,000/$50,000/$20,000
• Proof of insurance required
• SR-22 for high-risk drivers

Get competitive rates and personalized service.
```

#### Home Insurance
```
Safeguard your home and belongings with tailored coverage.

Coverage Options:
• Dwelling Coverage - Structure of your home
• Personal Property - Belongings inside
• Liability Protection - Legal claims against you
• Additional Living Expenses - Temporary housing
• Other Structures - Detached garages, sheds

Oregon Considerations:
• Earthquake coverage (optional but recommended)
• Flood insurance (required in some areas)
• Water damage from heavy Pacific Northwest rain
• Wildfire protection

Protect what matters most to you.
```

#### Life Insurance
```
Secure your family's financial future.

Coverage Types:
• Term Life Insurance - Affordable, temporary coverage
• Whole Life Insurance - Permanent protection with cash value
• Universal Life - Flexible premiums and benefits

Coverage Amounts:
• Income replacement calculation
• Debt coverage (mortgage, loans)
• Education funding for children
• Final expenses

No medical exam options available for qualifying applicants.
```

#### Business Insurance
```
Protect your Oregon business from unexpected risks.

Coverage Options:
• General Liability - Third-party injuries/property damage
• Property Insurance - Buildings and equipment
• Business Interruption - Lost income coverage
• Workers Compensation - Required for employees in Oregon
• Professional Liability - Errors and omissions
• Cyber Liability - Data breach protection

Industry-Specific Solutions:
• Retail stores
• Restaurants
• Professional services
• Contractors
• Technology companies

Custom packages for businesses of all sizes.
```

#### Health Insurance
```
Quality healthcare coverage for you and your family.

Plan Types:
• Individual Plans - Coverage for one person
• Family Plans - Coverage for your household
• HSA-Compatible Plans - Tax-advantaged savings
• Marketplace Plans - Affordable Care Act options

Coverage Includes:
• Doctor visits and preventive care
• Hospital stays and surgeries
• Prescription medications
• Mental health services
• Maternity and newborn care

Network providers throughout Oregon.
```

#### Umbrella Insurance
```
Extra liability protection beyond your standard policies.

What It Covers:
• Liability claims exceeding auto/home limits
• Legal defense costs
• Libel, slander, and defamation
• False arrest and wrongful eviction
• Liability from rental properties

Coverage Limits:
• $1 million to $5 million additional protection
• Affordable annual premiums
• Peace of mind for your assets

Recommended for homeowners and high-net-worth individuals.
```

#### Motorcycle Insurance
```
Hit the road with confidence.

Coverage Options:
• Liability Coverage - Required in Oregon
• Collision - Repairs after accident
• Comprehensive - Theft and non-collision damage
• Accessory Coverage - Custom parts and equipment
• Roadside Assistance - Towing and emergency service

Oregon Requirements:
• Same minimum liability as auto insurance
• Proof of insurance required
• Seasonal storage discounts available

Specialized coverage for riders.
```

#### RV Insurance
```
Protect your home on wheels.

Coverage Types:
• Full-Time RV Coverage - If RV is primary residence
• Vacation Use Coverage - Recreational travel only
• Personal Belongings - Contents inside RV
• Attached Accessories - Awnings, satellite dishes
• Emergency Expense Coverage - Lodging if RV unusable
• Roadside Assistance - Towing and emergency repairs

Custom Coverage:
• Class A, B, C motorhomes
• Travel trailers
• Fifth wheels
• Pop-up campers

Hit the open road worry-free.
```

### About Page Content

```markdown
# Proudly Serving Oregon Since [Year]

At Whittaker Agency, we're more than just an insurance provider—we're your neighbors, committed to protecting Oregon families and businesses.

## Our Story

Founded in Portland, Oregon, Whittaker Agency was built on a simple principle: insurance should be personal, transparent, and tailored to the unique needs of our community. With deep roots in the Pacific Northwest, we understand the challenges and opportunities that come with living in Oregon.

## Our Mission

To provide comprehensive, affordable insurance solutions with exceptional service that makes our clients feel valued, protected, and confident about their future.

## Why Choose Us

**Local Expertise**
We know Oregon inside and out—from coastal communities to mountain towns, we understand the specific risks and requirements of insuring in the Pacific Northwest.

**Personalized Service**
No two families or businesses are alike. We take the time to understand your unique situation and craft coverage that fits your needs and budget.

**Trusted Advisors**
With years of experience in the insurance industry, our team provides expert guidance you can trust.

**Always Available**
When you need us, we're here. 24/7 claims support and responsive customer service.

## Our Values

• **Integrity** - We do the right thing, even when no one is watching
• **Community** - We invest in and support Oregon communities
• **Excellence** - We strive for the highest standards in everything we do
• **Transparency** - Clear communication, no hidden fees or surprises

## The Oregon Connection

Living in Oregon means understanding rain, earthquakes, wildfires, and the unique beauty of the Pacific Northwest. Our policies are designed with Oregon in mind:

• Earthquake coverage recommendations
• Flood insurance expertise
• Wildfire protection strategies
• Understanding of Oregon insurance regulations
• Local claims adjusters who know the area

We're proud to call Oregon home, and we're committed to protecting the people and places that make it special.
```

### Team Page Content

Use the 3 team members already on the home page, plus add 3 more:

**David Thompson** - Claims Specialist
"With 10 years of experience in claims management, David ensures our clients receive fast, fair settlements when they need it most."

**Emily Rodriguez** - Life Insurance Advisor
"Emily specializes in helping families plan for the future with comprehensive life insurance solutions tailored to their goals."

**James Anderson** - Customer Service Manager
"James leads our customer service team with a focus on responsiveness, empathy, and going above and beyond for every client."

---

## Images Needed

### Services Page
- [ ] Auto icon/image
- [ ] Home icon/image
- [ ] Life icon/image
- [ ] Business icon/image
- [ ] Health icon/image
- [ ] Umbrella icon/image
- [ ] Motorcycle icon/image
- [ ] RV icon/image

**Note:** Use icons from existing home page (car, house, heart, briefcase, hospital, umbrella, motorcycle, RV emojis)

### About Page
- [ ] Oregon landscape (Mt. Hood or coast) - hero section
- [ ] Portland Oregon stag sign (already have)
- [ ] Team photo (optional - group photo)

### Team Page
- [ ] 6 team member photos (or initial placeholders)

---

## Testing Checklist

### Functionality Testing
- [ ] All navigation links work correctly
- [ ] Mobile menu opens/closes properly
- [ ] Active page highlighting works
- [ ] Service cards are clickable
- [ ] All images load correctly
- [ ] User menu appears when authenticated
- [ ] Sign In/Register buttons show when not authenticated
- [ ] Logout functionality works

### Responsive Design Testing
- [ ] Test on mobile (375px width)
- [ ] Test on tablet (768px width)
- [ ] Test on desktop (1440px width)
- [ ] Mobile menu works on small screens
- [ ] Navigation collapses appropriately
- [ ] Images scale correctly
- [ ] Text remains readable at all sizes
- [ ] Cards stack properly on mobile

### Browser Testing
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Accessibility Testing
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Alt text on all images
- [ ] Semantic HTML structure
- [ ] Color contrast meets WCAG AA standards

### Performance Testing
- [ ] Page load time < 3 seconds
- [ ] Images optimized
- [ ] No console errors
- [ ] Smooth scrolling
- [ ] No layout shifts

---

## Success Criteria

- Users can navigate between all pages seamlessly
- All 8 insurance types have detailed information
- Team page shows all 6 team members with bios
- About page communicates the agency's Oregon connection
- Mobile experience is smooth and intuitive
- Design is professional and trustworthy
- All pages load quickly with no errors
- User menu shows correctly for authenticated users

---

## Notes for Implementation

### Reusable Components
- Create generic `PageHero.vue` component for consistent hero sections across pages
- Use `ServiceCard.vue` for both home page and services page
- Footer should be extracted to its own component and shared

### State Management
- Navigation state (which page is active) handled by Vue Router
- User authentication state already managed by Pinia auth store
- No new state management needed for these pages

### Code Organization
- Keep components small and focused
- Use TypeScript interfaces for props
- Add JSDoc comments for complex components
- Follow existing naming conventions

### Performance Optimization
- Lazy load images below the fold
- Use `v-once` for static content
- Consider route-level code splitting (can add later)

---

## Estimated Breakdown

**Navigation System:** 3-4 hours
- Header component
- Mobile menu
- User menu
- Footer extraction

**Services Page:** 3-4 hours
- Page structure
- 8 service sections
- Content writing/formatting
- Responsive design

**About Page:** 2-3 hours
- Page structure
- Content sections
- Image integration

**Team Page:** 2-3 hours
- Team member grid
- Card components
- Content for 6 members

**Testing & Polish:** 2-3 hours
- Responsive testing
- Cross-browser testing
- Bug fixes
- Performance optimization

**Total:** 10-15 hours

---

## Dependencies for Future Slices

**Slice 3 (Quote Request System):**
- Navigation will need "Get a Quote" button to link to protected quote form
- Services page CTAs will link to quote form with pre-selected insurance type

**Slice 4 (Claims System):**
- Navigation may add "File a Claim" link
- Footer may add claims FAQ link

**Slice 5 (Contact System):**
- Navigation already has contact page
- Contact form will be new protected page

---

## Git Commit Strategy

Commit after each major component is complete:

1. `feat: Add navigation header and mobile menu`
2. `feat: Create Services page with 8 insurance types`
3. `feat: Build About Us page with Oregon connection`
4. `feat: Add Team page with member profiles`
5. `refactor: Extract footer to shared component`
6. `style: Add responsive design for all new pages`
7. `test: Complete cross-browser and mobile testing`
8. `docs: Update session notes for Slice 2 completion`

Final commit:
```
feat: Complete Slice 2 - Core Pages & Navigation

- Add comprehensive navigation system (desktop + mobile)
- Create Services page with detailed coverage for 8 insurance types
- Build About Us page highlighting Oregon connection
- Add Team page with 6 team member profiles
- Extract footer to shared component
- Implement fully responsive design
- Test across browsers and devices
```

---

**Document Version:** 1.0
**Created:** 2025-10-24
**Last Updated:** 2025-10-24
