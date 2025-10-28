# Whittaker Agency - Insurance Website

**Tagline:** Your Family, Your Business, Our Priority

Insurance agency website serving the Portland, Oregon area. Built with Vue 3, FastAPI (Python), and MariaDB.

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Development Environment

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up

# Access the application
# Frontend: http://localhost:8082
# API Docs: http://localhost:5102/docs
# Database: localhost:3310
```

### Optional: Vite Dev Server (for UI-heavy work)

```bash
cd frontend
npm install
npm run dev
# Access: http://localhost:3003
```

---

## Technology Stack

### Frontend
- **Framework:** Vue 3 (Composition API)
- **Language:** TypeScript
- **Build Tool:** Vite
- **State Management:** Pinia
- **Routing:** Vue Router

### Backend
- **Framework:** FastAPI (Python)
- **ORM:** SQLAlchemy
- **Auth:** JWT (JSON Web Tokens)
- **Email:** Brevo API
- **Migrations:** Alembic

### Database
- **DBMS:** MariaDB 10.11

### Infrastructure
- **Containers:** Docker + Docker Compose
- **Reverse Proxy:** nginx
- **SSL:** Let's Encrypt (production)

---

## Features

### Public Features
- View insurance services (Auto, Home, Business, Life, Health, Motorcycle, Boat, Rental)
- Meet the team
- Claims process walkthrough
- Contact form

### Authenticated Features
- Request insurance quotes
- Open claim requests
- User dashboard (view all requests)
- Message history

### Security
- JWT authentication
- No sensitive PII collected (by design)
- HTTPS in production
- Global exception handling
- Comprehensive audit logging

---

## Project Structure

```
├── backend/          # FastAPI Python backend
│   ├── app/
│   │   ├── routers/  # API endpoints (thin controllers)
│   │   ├── services/ # Business logic
│   │   ├── models/   # SQLAlchemy ORM
│   │   ├── schemas/  # Pydantic validation
│   │   └── middleware/
│   └── alembic/      # Database migrations
│
├── frontend/         # Vue 3 frontend
│   └── src/
│       ├── views/    # Page components
│       ├── components/
│       ├── stores/   # Pinia state
│       ├── router/
│       └── services/ # API clients
│
├── docs/             # Documentation
│   ├── api/          # API endpoint docs
│   ├── sessions/     # Session notes
│   ├── architecture/ # Design docs
│   └── templates/    # Doc templates
│
└── docker/           # Docker configs
```

See [docs/architecture/PROJECT-STRUCTURE.md](docs/architecture/PROJECT-STRUCTURE.md) for detailed structure.

---

## Port Allocation

### Development
- **MariaDB:** `localhost:3310`
- **FastAPI:** `localhost:5102` (internal)
- **nginx:** `localhost:8082` (main access point)
- **Vite (optional):** `localhost:3003`

### Production
- **MariaDB:** Internal only (SSH tunnel for admin)
- **FastAPI:** Internal `5000`
- **nginx:** `80` → `443` (HTTPS)

See [C:\Users\Howard\SynologyDrive\Drive\Projects\Claude\PORT-ALLOCATION.md](../PORT-ALLOCATION.md) for all projects.

---

## Documentation

### Key Documents

- **[DESIGN.md](docs/DESIGN.md)** - Complete design specification with implementation slices
- **[BACKEND-PATTERNS.md](docs/architecture/BACKEND-PATTERNS.md)** - Backend architecture patterns (thin controllers, exception handling, logging)
- **[PROJECT-STRUCTURE.md](docs/architecture/PROJECT-STRUCTURE.md)** - Detailed directory layout
- **[PORT-ALLOCATION.md](../PORT-ALLOCATION.md)** - Port allocations across all projects

### Templates

- **[api-endpoint-template.md](docs/templates/api-endpoint-template.md)** - For documenting new API endpoints
- **[session-notes-template.md](docs/templates/session-notes-template.md)** - For documenting work sessions

---

## Architecture Principles

### Thin Controllers
- Controllers (routers) only handle HTTP routing
- All business logic in service layer
- No try-catch blocks (handled by global middleware)

### Service Layer
- All business logic and validation
- Throws meaningful exceptions
- Database operations
- Returns domain models

### Global Exception Handling
- GlobalExceptionMiddleware catches all exceptions
- Automatic HTTP status code mapping
- Comprehensive logging to SystemLog
- User context tracking

### Dual Logging System
- **SystemLog:** All exceptions, errors, system events
- **AuditLog:** User actions, successful operations, data modifications

See [docs/architecture/BACKEND-PATTERNS.md](docs/architecture/BACKEND-PATTERNS.md) for details.

---

## Development Workflow

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run locally (without Docker)
uvicorn app.main:app --reload --port 5102

# Create database migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Run tests
pytest
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Run tests
npm run test:unit
```

### Docker Development

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up

# Rebuild containers
docker-compose -f docker-compose.dev.yml up --build

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop all services
docker-compose -f docker-compose.dev.yml down
```

---

## API Documentation

**FastAPI provides automatic documentation:**

- **Swagger UI:** http://localhost:5102/docs
- **ReDoc:** http://localhost:5102/redoc

**Manual documentation:**
- Store in `docs/api/` using [api-endpoint-template.md](docs/templates/api-endpoint-template.md)

---

## Database

### Connection

**Development:**
```
Host: localhost
Port: 3310
Database: whittaker_agency
User: whittaker_user
Password: SecureW@Pa55!2025
```

**Client:** HeidiSQL, MySQL Workbench, or any MySQL-compatible client

### Migrations

```bash
# Create migration
cd backend
alembic revision --autogenerate -m "Add users table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Environment Variables

### Backend (.env)

```bash
DATABASE_URL=mysql+pymysql://whittaker_user:SecureW@Pa55!2025@db:3306/whittaker_agency
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440
BREVO_API_KEY=your-brevo-api-key
BREVO_SENDER_EMAIL=noreply@whittakeragency.com
BREVO_ADMIN_EMAIL=admin@whittakeragency.com
ENVIRONMENT=development
```

### Frontend (.env)

```bash
VITE_API_BASE_URL=http://localhost:8082/api/v1
```

---

## Implementation Slices

Project is divided into 6 implementation slices:

1. **Foundation & Infrastructure** (8-12 hrs)
   - Docker setup
   - Database schema
   - Authentication

2. **Core Pages & Navigation** (10-15 hrs)
   - Homepage, Services, Team pages
   - Navigation component

3. **Quote Request System** (6-8 hrs)
   - Quote request form
   - Dashboard integration

4. **Claims System** (6-8 hrs)
   - Claims walkthrough page
   - Claim request form

5. **Contact System & Dashboard** (6-8 hrs)
   - Contact form
   - User dashboard completion

6. **Polish & Production Prep** (8-10 hrs)
   - Oregon imagery
   - Responsive design
   - Production deployment

See [docs/DESIGN.md](docs/DESIGN.md) for full slice breakdown.

---

## Testing

### Backend Tests

```bash
cd backend

# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# With coverage
pytest --cov=app tests/
```

### Frontend Tests

```bash
cd frontend

# Unit tests
npm run test:unit

# E2E tests
npm run test:e2e
```

---

## Deployment

### Production Setup

1. Clone repository on server
2. Configure environment variables
3. Run production Docker Compose
4. Set up SSL with Let's Encrypt
5. Configure domain DNS

```bash
# On production server
git clone <repository-url>
cd whittaker-agency

# Configure environment
cp .env.example .env.production
# Edit .env.production

# Deploy (docker-compose.yml is production by default)
docker-compose up -d
```

See [docs/DESIGN.md](docs/DESIGN.md) deployment section for details.

---

## Design & Branding

### Color Scheme (Allstate-Inspired)

- **Primary Blue:** `#003DA5`
- **Dark Blue:** `#002B73`
- **Light Blue:** `#0057C8`
- **Grays:** `#333333`, `#666666`, `#F5F5F5`
- **White:** `#FFFFFF`

### Oregon Imagery

- **Mt. Hood** - Homepage hero section
- **Portland Stag Sign** - About section

### Typography

- **Headings:** Montserrat (semi-bold, bold)
- **Body:** Open Sans (16px base)

---

## Contributing

### Session Notes

After each development session, document your work using the [session-notes-template.md](docs/templates/session-notes-template.md):

```bash
cp docs/templates/session-notes-template.md docs/sessions/2025-10-23-session.md
# Fill in the template
```

### API Documentation

When adding new endpoints, document using [api-endpoint-template.md](docs/templates/api-endpoint-template.md):

```bash
cp docs/templates/api-endpoint-template.md docs/api/new-endpoint.md
# Fill in the template
```

---

## Status

✅ **Slice 2 Complete** - Core pages and navigation fully implemented

**Completed:**
- ✅ Slice 1: Foundation & Infrastructure (2025-10-23)
- ✅ Slice 2: Core Pages & Navigation (2025-10-28)

**Next Steps:**
- Begin Slice 3: Quote Request System
- Implement quote request form
- Create quote management backend
- Add quote history to dashboard

**Progress:** ~35% Complete

---

## License

Proprietary - Whittaker Agency

---

## Contact

**Project Owner:** Kyle (Whittaker Agency)
**Location:** Portland, Oregon area

---

**Last Updated:** 2025-10-23
