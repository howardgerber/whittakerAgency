# Whittaker Agency - Design Document

**Project Name:** Whittaker Agency Insurance Website
**Client:** Kyle (friend)
**Location:** Portland, Oregon area
**Tagline:** Your Family, Your Business, Our Priority
**Created:** 2025-10-23
**Status:** Planning Phase

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Business Requirements](#business-requirements)
3. [Technology Stack](#technology-stack)
4. [Architecture Overview](#architecture-overview)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Pages & Features](#pages--features)
8. [Design & Branding](#design--branding)
9. [Implementation Slices](#implementation-slices)
10. [Deployment Strategy](#deployment-strategy)
11. [Future Enhancements](#future-enhancements)

---

## Executive Summary

Professional website for Whittaker Agency (Allstate) serving Portland, Oregon.

**Core features:**
- Request insurance quotes
- File claims
- Contact agency
- Meet the team

**Security:** No sensitive PII collected (SSN, license numbers, etc.)

**Target:** Portland-area families and businesses needing insurance coverage

---

## Business Requirements

### Insurance Categories
See [docs/architecture/CATEGORIES.md](architecture/CATEGORIES.md) for complete structure.

**Main categories:** Vehicle, Property, Life, Business, Identity Protection, Other

### Features

**Public:**
- Browse services
- View team
- Claims walkthrough
- Contact form

**Authenticated:**
- Request quotes
- File claims
- View dashboard

**Security constraint:** No SSN, license numbers, or bank info collected. Quotes/claims are "intent to start" only.

---

## Technology Stack

### Frontend
- **Framework:** Vue 3 (Composition API)
- **Language:** TypeScript
- **Build Tool:** Vite
- **State Management:** Pinia
- **Routing:** Vue Router
- **UI Components:** Custom components with Allstate-inspired styling
- **CSS:** Scoped CSS / CSS Modules

### Backend
- **Framework:** FastAPI (Python)
- **Language:** Python 3.11+
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)
- **Validation:** Pydantic models
- **Email:** Brevo API (stubbed for now)

### Database
- **DBMS:** MariaDB 10.11
- **Schema Management:** Alembic migrations

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Reverse Proxy:** nginx
- **SSL/TLS:** Let's Encrypt (production)

### Development Tools
- **Version Control:** Git
- **API Documentation:** FastAPI automatic OpenAPI docs
- **Database Client:** HeidiSQL / MySQL Workbench

---

## Architecture Overview

### Three-Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         nginx (Port 8082/80)                │
│  - Serves Vue static files                                  │
│  - Reverse proxy for /api/ → FastAPI                        │
│  - SSL termination (prod)                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴────────────────┐
        │                              │
┌───────▼──────────┐          ┌────────▼─────────┐
│   FastAPI        │          │   Vue Frontend   │
│   (Port 5102)    │          │   (served by     │
│                  │          │    nginx)        │
│  - REST API      │          │                  │
│  - JWT Auth      │          │  - User UI       │
│  - Business      │          │  - Forms         │
│    Logic         │          │  - Dashboard     │
│  - Email stub    │          │                  │
└────────┬─────────┘          └──────────────────┘
         │
         │
┌────────▼──────────┐
│   MariaDB         │
│   (Port 3310)     │
│                   │
│  - User accounts  │
│  - Quote requests │
│  - Claim requests │
│  - Contact msgs   │
└───────────────────┘
```

### Port Allocation

**Development:**
- MariaDB: `localhost:3310` → container `3306`
- FastAPI: `localhost:5102` (internal)
- nginx: `localhost:8082` (access point)
- Vite (optional): `localhost:3003`

**Production:**
- MariaDB: Internal only (SSH tunnel for admin)
- FastAPI: Internal `5000` (proxied via nginx)
- nginx: `80` → `443` (HTTPS redirect)

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email)
) ENGINE=InnoDB;
```

### Quote Requests Table
```sql
CREATE TABLE quote_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    insurance_type ENUM('Auto', 'Home', 'Business', 'Life', 'Health', 'Motorcycle', 'Boat', 'Rental') NOT NULL,
    preferred_contact_method ENUM('Email', 'Phone', 'Either') DEFAULT 'Either',
    message TEXT,
    status ENUM('Pending', 'Contacted', 'Quoted', 'Converted', 'Declined') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;
```

### Claim Requests Table
```sql
CREATE TABLE claim_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    insurance_type ENUM('Auto', 'Home', 'Business', 'Life', 'Health', 'Motorcycle', 'Boat', 'Rental') NOT NULL,
    incident_date DATE NOT NULL,
    brief_description TEXT NOT NULL,
    preferred_contact_method ENUM('Email', 'Phone', 'Either') DEFAULT 'Either',
    status ENUM('Pending', 'Under Review', 'Approved', 'Denied', 'Closed') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;
```

### Contact Messages Table
```sql
CREATE TABLE contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    status ENUM('New', 'Read', 'Responded', 'Archived') DEFAULT 'New',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;
```

### Team Members Table
```sql
CREATE TABLE team_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    title VARCHAR(100) NOT NULL,
    bio TEXT,
    photo_url VARCHAR(255),
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_display_order (display_order)
) ENGINE=InnoDB;
```

### Attachments Table
```sql
CREATE TABLE attachments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entity_type ENUM('claim', 'contact') NOT NULL,
    entity_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_uploaded_at (uploaded_at)
) ENGINE=InnoDB;
```

**Attachments Table Notes:**
- **entity_type**: 'claim' or 'contact' - indicates what the file is attached to
- **entity_id**: ID of the claim_request or contact_message
- **filename**: Unique generated filename (e.g., `claim_123_20251023_143022.jpg`)
- **original_filename**: Original filename from user upload
- **file_path**: Full path in Docker volume (e.g., `/app/uploads/claims/claim_123_20251023_143022.jpg`)
- **Validation**:
  - Allowed types: JPEG, PNG, GIF images
  - Max file size: 5MB
  - Max 3 attachments per claim/contact message

---

## API Endpoints

### Authentication Endpoints

**POST /api/v1/auth/register**
- Register new user account
- Request: `{ email, password, first_name, last_name, phone }`
- Response: `{ user, access_token, token_type }`

**POST /api/v1/auth/login**
- User login
- Request: `{ email, password }`
- Response: `{ access_token, token_type, user }`

**POST /api/v1/auth/logout**
- Logout (optional - JWT is stateless)
- Headers: `Authorization: Bearer <token>`
- Response: `{ message }`

**GET /api/v1/auth/me**
- Get current user profile
- Headers: `Authorization: Bearer <token>`
- Response: `{ user }`

### Quote Requests Endpoints

**POST /api/v1/quotes** (Protected)
- Submit a quote request
- Headers: `Authorization: Bearer <token>`
- Request: `{ insurance_type, preferred_contact_method, message }`
- Response: `{ quote_request }`

**GET /api/v1/quotes** (Protected)
- Get current user's quote requests
- Headers: `Authorization: Bearer <token>`
- Response: `{ quote_requests: [] }`

**GET /api/v1/quotes/{id}** (Protected)
- Get specific quote request
- Headers: `Authorization: Bearer <token>`
- Response: `{ quote_request }`

### Claim Requests Endpoints

**POST /api/v1/claims** (Protected)
- Submit a claim request
- Headers: `Authorization: Bearer <token>`
- Request: `{ insurance_type, incident_date, brief_description, preferred_contact_method }`
- Response: `{ claim_request }`

**GET /api/v1/claims** (Protected)
- Get current user's claim requests
- Headers: `Authorization: Bearer <token>`
- Response: `{ claim_requests: [] }`

**GET /api/v1/claims/{id}** (Protected)
- Get specific claim request
- Headers: `Authorization: Bearer <token>`
- Response: `{ claim_request }`

### Contact Messages Endpoints

**POST /api/v1/contact** (Public/Protected)
- Submit contact form
- Optional Headers: `Authorization: Bearer <token>`
- Request: `{ name, email, phone, subject, message }`
- Response: `{ contact_message }`

**GET /api/v1/contact** (Protected)
- Get current user's contact messages
- Headers: `Authorization: Bearer <token>`
- Response: `{ messages: [] }`

### Team Members Endpoints

**GET /api/v1/team** (Public)
- Get all active team members
- Response: `{ team_members: [] }`

### Services Endpoints

**GET /api/v1/services** (Public)
- Get list of insurance types
- Response: `{ services: [] }`

### File Upload Endpoints

**POST /api/v1/attachments/upload** (Protected)
- Upload file attachment for claim or contact message
- Headers: `Authorization: Bearer <token>`
- Request: `multipart/form-data`
  - `file`: File object (image only)
  - `entity_type`: 'claim' or 'contact'
  - `entity_id`: ID of claim_request or contact_message
- Response: `{ attachment }`
- Validation:
  - File types: JPEG, PNG, GIF only
  - Max size: 5MB
  - Max 3 files per entity

**GET /api/v1/attachments/{entity_type}/{entity_id}** (Protected)
- Get all attachments for a claim or contact message
- Headers: `Authorization: Bearer <token>`
- Response: `{ attachments: [] }`

**DELETE /api/v1/attachments/{id}** (Protected)
- Delete an attachment
- Headers: `Authorization: Bearer <token>`
- Response: `{ message }`

---

## Pages & Features

### 1. Home Page (`/`)
**Route:** `/`
**Access:** Public

**Sections:**
- Hero section with Oregon imagery (Mt. Hood)
  - Headline: "Insurance That Protects What Matters Most"
  - Subtext: "Serving Portland and surrounding communities with personalized insurance solutions"
  - CTA buttons: "Get a Quote" | "Contact Us"
- Services overview (8 insurance types with icons)
- Why Choose Us section
- Meet the Team preview (3 team members)
- Oregon connection section (Stag sign image)
- Footer with contact info

### 2. Services Page (`/services`)
**Route:** `/services`
**Access:** Public

**Content:**
- Header with tagline
- Grid of 8 insurance types:
  - Auto Insurance
  - Home Insurance
  - Business Insurance
  - Life Insurance
  - Health Insurance
  - Motorcycle Insurance
  - Boat Insurance
  - Rental Property Insurance
- Each card shows:
  - Icon
  - Title
  - Brief description
  - "Learn More" / "Get a Quote" button

### 3. Meet the Team Page (`/team`)
**Route:** `/team`
**Access:** Public

**Content:**
- Page header
- Grid of 6 team members (placeholder data):
  - Photo
  - Name
  - Title/Role
  - Short bio
- Call to action: "Ready to work with us?"

### 4. Request a Quote Page (`/quote`)
**Route:** `/quote`
**Access:** Protected (requires login)

**Form Fields:**
- Insurance type (dropdown)
- Preferred contact method (radio: Email, Phone, Either)
- Message/Details (textarea)
- Submit button

**Behavior:**
- Redirects to login if not authenticated
- On submit: creates quote request in DB
- Shows success message
- Optionally sends email notification to agency (Brevo)

### 5. Claims Process Walkthrough (`/claims-process`)
**Route:** `/claims-process`
**Access:** Public

**Content:**
- Educational page explaining how to file a claim
- Step-by-step guide:
  1. Contact your agent immediately
  2. Document the incident (photos, police report, etc.)
  3. Gather necessary information
  4. Submit claim through agent or online
  5. Work with claims adjuster
  6. Receive resolution
- CTA: "Ready to start a claim?" → links to `/claims/new`

### 6. Open a Claim Page (`/claims/new`)
**Route:** `/claims/new`
**Access:** Protected (requires login)

**Form Fields:**
- Insurance type (dropdown)
- Date of incident (date picker)
- Brief description (textarea)
- Preferred contact method (radio)
- Submit button

**Behavior:**
- Redirects to login if not authenticated
- On submit: creates claim request in DB
- Shows success message with next steps
- Optionally sends email notification to agency

### 7. Contact Us Page (`/contact`)
**Route:** `/contact`
**Access:** Public (enhanced if logged in)

**Form Fields:**
- Name (auto-filled if logged in)
- Email (auto-filled if logged in)
- Phone (optional, auto-filled if logged in)
- Subject (text)
- Message (textarea)
- Submit button

**Additional Content:**
- Agency contact information
- Office hours
- Map/address
- Phone number
- Email address

**Behavior:**
- If logged in: associates message with user account
- If not logged in: stores as anonymous message
- Shows success message
- Optionally sends email notification

### 8. Login Page (`/login`)
**Route:** `/login`
**Access:** Public

**Form Fields:**
- Email
- Password
- "Remember me" checkbox (optional)
- Submit button

**Links:**
- "Don't have an account? Register"
- "Forgot password?" (future enhancement)

**Behavior:**
- On success: stores JWT token, redirects to dashboard or return URL
- On failure: shows error message

### 9. Register Page (`/register`)
**Route:** `/register`
**Access:** Public

**Form Fields:**
- First name
- Last name
- Email
- Phone
- Password
- Confirm password
- Terms & conditions checkbox
- Submit button

**Links:**
- "Already have an account? Login"

**Behavior:**
- Validates all fields
- Checks password strength
- On success: creates account, logs in, redirects to dashboard
- On failure: shows validation errors

### 10. User Dashboard (`/dashboard`)
**Route:** `/dashboard`
**Access:** Protected (requires login)

**Sections:**
- Welcome message with user name
- Quick stats cards:
  - Pending quote requests
  - Open claims
  - Recent messages
- Tabs:
  - **Quote Requests:** table of all quote requests with status
  - **Claim Requests:** table of all claim requests with status
  - **Messages:** table of all contact messages
- Account settings link

**Features:**
- View all submitted requests
- Filter by status
- Sort by date
- Click to view details

---

## Design & Branding

### Color Scheme (Allstate-Inspired)

**Primary Colors:**
- **Blue Primary:** `#003DA5` (Allstate blue)
- **Blue Dark:** `#002B73`
- **Blue Light:** `#0057C8`

**Secondary Colors:**
- **Gray Dark:** `#333333`
- **Gray Medium:** `#666666`
- **Gray Light:** `#F5F5F5`
- **White:** `#FFFFFF`

**Accent Colors:**
- **Success Green:** `#28A745`
- **Warning Orange:** `#FFA500`
- **Error Red:** `#DC3545`
- **Info Blue:** `#17A2B8`

### Typography

**Headings:**
- Font Family: `'Montserrat', sans-serif` or similar modern sans-serif
- Font Weights: 600 (semi-bold), 700 (bold)

**Body:**
- Font Family: `'Open Sans', sans-serif` or similar readable sans-serif
- Font Size: 16px base
- Line Height: 1.6

### Oregon Imagery

**Mt. Hood Image:**
- Location: Homepage hero section
- Style: Full-width background image with overlay
- Source: Unsplash or free stock photo

**Portland Stag Sign (Made in Oregon):**
- Location: About section or footer area
- Style: Integrated as design element
- Source: Public domain or licensed image

### Layout

**Navigation (Two Options to Choose From):**

**Option A - Top Navigation:**
```
┌────────────────────────────────────────────────┐
│ [Logo] Whittaker Agency    [Nav Links] [Login] │
└────────────────────────────────────────────────┘
```

**Option B - Left Navigation:**
```
┌──────┬────────────────────────────────────────┐
│ Logo │                                        │
│ Nav  │         Main Content Area              │
│ Nav  │                                        │
│ Nav  │                                        │
│ Nav  │                                        │
└──────┴────────────────────────────────────────┘
```

**Footer:**
- Contact information
- Quick links
- Social media (optional)
- Copyright & disclaimer

### Responsive Design

**Breakpoints:**
- Mobile: `< 768px`
- Tablet: `768px - 1024px`
- Desktop: `> 1024px`

**Mobile Considerations:**
- Hamburger menu for navigation
- Stacked layout for cards
- Touch-friendly buttons (min 44px height)

---

## Implementation Slices

### Slice 1: Foundation & Infrastructure
**Goal:** Set up project structure, Docker containers, and basic authentication

**Tasks:**
1. Initialize project directories (frontend, backend)
2. Create Docker Compose configuration
   - MariaDB container
   - FastAPI container
   - nginx container
3. Set up FastAPI with basic structure
   - Main app file
   - Database connection (SQLAlchemy)
   - Environment variables
4. Set up Vue 3 with Vite
   - Basic routing (Vue Router)
   - State management (Pinia)
   - TypeScript configuration
5. Create database schema
   - Users table
   - Create Alembic migrations
6. Implement JWT authentication
   - Register endpoint
   - Login endpoint
   - Auth middleware
7. Create Login/Register pages (frontend)
8. Test authentication flow end-to-end

**Deliverables:**
- ✅ Docker containers running
- ✅ Database connected
- ✅ User can register and login
- ✅ JWT token stored in frontend

**Estimated Effort:** 8-12 hours

---

### Slice 2: Core Pages & Navigation
**Goal:** Build public-facing pages and navigation structure

**Tasks:**
1. Choose navigation style (top vs left)
2. Build navigation component
   - Desktop version
   - Mobile responsive version
3. Create Homepage
   - Hero section with Mt. Hood image
   - Services overview section
   - Team preview section
   - Oregon Stag sign section
4. Create Services page
   - 8 insurance type cards
   - Descriptions
5. Create Meet the Team page
   - Team member cards (6 placeholders)
   - Fetch from backend
6. Add team members to database (seed data)
7. Implement team members API endpoint
8. Style all pages with Allstate color scheme
9. Make pages responsive

**Deliverables:**
- ✅ Navigation working on all pages
- ✅ Homepage fully styled
- ✅ Services page complete
- ✅ Meet the Team page with placeholder data
- ✅ Mobile responsive

**Estimated Effort:** 10-15 hours

---

### Slice 3: Quote Request System
**Goal:** Allow authenticated users to request insurance quotes

**Tasks:**
1. Create quote_requests table
2. Implement backend API endpoints
   - POST /api/v1/quotes (create request)
   - GET /api/v1/quotes (list user's requests)
   - GET /api/v1/quotes/{id} (get single request)
3. Create Request a Quote page (frontend)
   - Form with validation
   - Success/error messages
   - Protected route (requires login)
4. Add quote requests section to user dashboard
   - Table showing all requests
   - Status badges
   - Filter/sort functionality
5. Test quote request flow
6. Stub Brevo email notification

**Deliverables:**
- ✅ Users can submit quote requests
- ✅ Requests saved to database
- ✅ Users can view their quote requests in dashboard
- ✅ Email stub in place (ready for Brevo API key)

**Estimated Effort:** 6-8 hours

---

### Slice 4: Claims System
**Goal:** Implement claims process walkthrough and claim request submission with file uploads

**Tasks:**
1. Create claim_requests table
2. Create attachments table
3. Implement backend file upload service
   - Shared FileUploadService for attachments
   - File validation (type, size, count)
   - Save to Docker volume
   - Store metadata in database
4. Implement backend API endpoints
   - POST /api/v1/claims (create request)
   - GET /api/v1/claims (list user's requests)
   - GET /api/v1/claims/{id} (get single request)
   - POST /api/v1/attachments/upload (upload files)
   - GET /api/v1/attachments/claim/{id} (get claim attachments)
5. Create Claims Process Walkthrough page
   - Educational content
   - Step-by-step guide
   - CTA to open claim
6. Create Open a Claim page (frontend)
   - Form with validation
   - Date picker for incident
   - File upload component (drag & drop or click)
   - Image preview before upload
   - Max 3 images per claim
   - Protected route
7. Add claims section to user dashboard
   - Table showing all claims
   - Status badges
   - View attached images
   - Filter/sort functionality
8. Test claim request flow with file uploads
9. Stub Brevo email notification

**Deliverables:**
- ✅ Claims process walkthrough page (public)
- ✅ Users can submit claim requests with up to 3 photos
- ✅ Claims and attachments saved to database
- ✅ Files stored in Docker volume
- ✅ Users can view their claims and photos in dashboard
- ✅ Email stub in place

**Estimated Effort:** 8-10 hours

---

### Slice 5: Contact System & Dashboard
**Goal:** Complete contact form with file uploads and user dashboard

**Tasks:**
1. Create contact_messages table
2. Implement backend API endpoints
   - POST /api/v1/contact (submit message)
   - GET /api/v1/contact (get user's messages)
   - POST /api/v1/attachments/upload (reuse from Slice 4)
   - GET /api/v1/attachments/contact/{id} (get contact attachments)
3. Create Contact Us page
   - Form (works for logged in and guest users)
   - File upload component (reuse from Slice 4)
   - Max 3 images per message
   - Image preview before upload
   - Agency contact information
   - Map/address section
4. Build User Dashboard
   - Summary stats cards
   - Tabs for quotes, claims, messages
   - Filters and sorting
   - Profile section
   - View attached images in messages tab
5. Add messages section to dashboard
6. Test contact form flow (logged in and guest) with file uploads
7. Stub Brevo email notification

**Deliverables:**
- ✅ Contact form functional with optional image attachments
- ✅ Logged-in and guest users can attach photos to questions
- ✅ User dashboard complete
- ✅ All user requests visible in dashboard with attachments
- ✅ Email stub in place

**Estimated Effort:** 6-8 hours

---

### Slice 6: Polish & Production Prep
**Goal:** Finalize design, add Oregon imagery, prepare for deployment

**Tasks:**
1. Add Oregon imagery
   - Mt. Hood hero image (high quality)
   - Portland Stag sign image
2. Refine color scheme
   - Ensure Allstate blues used consistently
   - Add hover states
   - Improve contrast for accessibility
3. Improve responsive design
   - Test on mobile devices
   - Fix any layout issues
4. Add loading states and error handling
   - Skeleton loaders
   - Error boundaries
   - Toast notifications
5. Create production Docker Compose file
   - nginx with SSL configuration
   - Environment variable management
   - Volume management
6. Write deployment documentation
7. Create README.md
8. Test entire application end-to-end
9. Performance optimization
   - Image optimization
   - Code splitting
   - Lazy loading

**Deliverables:**
- ✅ Oregon imagery integrated
- ✅ All pages polished and responsive
- ✅ Production-ready Docker setup
- ✅ Documentation complete
- ✅ Application tested and optimized

**Estimated Effort:** 8-10 hours

---

## Deployment Strategy

### Development Environment

**Setup:**
```bash
cd C:\Users\Howard\SynologyDrive\Drive\Projects\Claude\KylesWebsite
docker-compose -f docker-compose.dev.yml up
```

**Access:**
- Website: http://localhost:8082
- API: http://localhost:5102
- API Docs: http://localhost:5102/docs
- Database: localhost:3310

### Production Environment

**Requirements:**
- Linux server (Ubuntu 20.04+)
- Docker & Docker Compose installed
- Domain name (e.g., whittakeragency.com)
- SSL certificate (Let's Encrypt)

**Setup:**
```bash
# Clone repository
git clone <repository-url>
cd whittaker-agency

# Configure environment
cp .env.example .env
# Edit .env with production values

# Deploy (docker-compose.yml is default for production)
docker-compose up -d
```

**Access:**
- Website: https://whittakeragency.com
- Database: Internal only (SSH tunnel for admin access)

### Environment Variables

**Backend (.env):**
```
# Database
DATABASE_URL=mysql+pymysql://whittaker_user:SecureW@Pa55!2025@db:3306/whittaker

# JWT
JWT_SECRET_KEY=<generate-secure-random-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Email (Brevo)
BREVO_API_KEY=<to-be-configured>
BREVO_SENDER_EMAIL=noreply@whittakeragency.com
BREVO_ADMIN_EMAIL=admin@whittakeragency.com

# Environment
ENVIRONMENT=production
```

**Frontend (.env):**
```
VITE_API_BASE_URL=https://whittakeragency.com/api/v1
```

---

## Future Enhancements

### Phase 2 Features (Post-Launch)

1. **Admin Panel**
   - View all quote requests
   - Update request status
   - Respond to contact messages
   - Manage team members
   - Analytics dashboard

2. **Enhanced Authentication**
   - Password reset functionality
   - Email verification
   - Two-factor authentication (2FA)

3. **Enhanced File Upload Features**
   - PDF document support (currently images only)
   - Video uploads for complex claims
   - File compression/optimization
   - Image gallery viewer with zoom
   - Download all attachments as ZIP
   - Virus/malware scanning
   - CDN/S3 migration for better performance

4. **Live Chat**
   - Chat widget for real-time support
   - Integration with customer service

5. **Blog / Resources**
   - Insurance tips and articles
   - SEO optimization
   - News updates

6. **Multi-language Support**
   - Spanish translation
   - Language selector

7. **Payment Integration**
   - Pay premiums online
   - Payment history
   - Auto-pay setup

8. **Client Portal Enhancements**
   - View active policies
   - Download policy documents
   - Renewal reminders

9. **Analytics & Tracking**
   - Google Analytics integration
   - Conversion tracking
   - User behavior analysis

10. **Mobile App**
    - Native iOS/Android app
    - Push notifications
    - Digital insurance cards

---

## Security Considerations

### Data Protection
- Passwords hashed with bcrypt
- JWT tokens for authentication
- HTTPS only in production
- SQL injection prevention (parameterized queries)
- XSS protection (Vue escaping)
- CORS configuration

### Privacy
- No sensitive PII collected
- Privacy policy page
- Cookie consent (if using analytics)
- GDPR compliance considerations

### Rate Limiting
- Prevent brute force attacks on login
- Limit API requests per user
- Throttle contact form submissions

### Backup Strategy
- Daily database backups
- Offsite backup storage
- Disaster recovery plan

---

## Testing Strategy

### Unit Tests
- Backend: pytest for FastAPI endpoints
- Frontend: Vitest for Vue components

### Integration Tests
- API endpoint testing
- Database operations
- Authentication flow

### End-to-End Tests
- Cypress or Playwright
- Critical user flows:
  - Registration → Login → Quote Request
  - Login → Dashboard → View Requests
  - Contact Form Submission

### Manual Testing Checklist
- [ ] All pages load correctly
- [ ] Forms validate properly
- [ ] Authentication works
- [ ] Dashboard displays data
- [ ] Responsive on mobile/tablet
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)

---

## Success Metrics

### Key Performance Indicators (KPIs)

**User Engagement:**
- Number of registrations per month
- Quote requests submitted
- Claim requests submitted
- Contact form submissions

**Technical:**
- Page load time < 2 seconds
- API response time < 200ms
- 99.9% uptime
- Zero critical security vulnerabilities

**Business:**
- Quote-to-customer conversion rate
- Time to respond to requests
- Customer satisfaction scores

---

## Project Timeline

**Total Estimated Time:** 46-63 hours

**Slice-by-Slice:**
- Slice 1: 8-12 hours (Foundation & Infrastructure)
- Slice 2: 10-15 hours (Core Pages & Navigation)
- Slice 3: 6-8 hours (Quote Request System)
- Slice 4: 8-10 hours (Claims System + File Uploads)
- Slice 5: 6-8 hours (Contact System & Dashboard + File Uploads)
- Slice 6: 8-10 hours (Polish & Production Prep)

**Note:** Slice 4 and 5 times increased slightly to accommodate file upload feature

**Target Completion:** 4-6 weeks (assuming part-time work)

---

## Appendix

### Insurance Type Descriptions

**Auto Insurance:**
Protection for your vehicle against accidents, theft, and liability.

**Home Insurance:**
Comprehensive coverage for your home, belongings, and liability.

**Business Insurance:**
Protect your business assets, employees, and operations.

**Life Insurance:**
Financial security for your loved ones when you're gone.

**Health Insurance:**
Medical coverage for you and your family.

**Motorcycle Insurance:**
Specialized coverage for motorcycle riders.

**Boat Insurance:**
Protection for your watercraft and marine equipment.

**Rental Property Insurance:**
Coverage for landlords and investment properties.

---

**Document Version:** 1.0
**Last Updated:** 2025-10-23
**Next Review:** After Slice 1 completion

---

**End of Design Document**
