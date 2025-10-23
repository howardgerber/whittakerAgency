# Project Structure

**Project:** Whittaker Agency
**Created:** 2025-10-23

---

## Directory Layout

```
KylesWebsite/
├── backend/                          # FastAPI Python backend
│   ├── app/
│   │   ├── routers/                  # API route handlers (thin controllers)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # POST /auth/register, /auth/login
│   │   │   ├── quotes.py            # Quote request endpoints
│   │   │   ├── claims.py            # Claim request endpoints
│   │   │   ├── contact.py           # Contact form endpoints
│   │   │   ├── team.py              # Team members (public)
│   │   │   └── users.py             # User profile endpoints
│   │   │
│   │   ├── services/                 # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py      # Registration, login, JWT
│   │   │   ├── quote_service.py     # Quote request logic
│   │   │   ├── claim_service.py     # Claim request logic
│   │   │   ├── contact_service.py   # Contact message logic
│   │   │   ├── team_service.py      # Team member CRUD
│   │   │   ├── user_service.py      # User profile management
│   │   │   ├── system_log_service.py # System logging
│   │   │   ├── audit_log_service.py  # Audit logging
│   │   │   └── email_service.py     # Brevo email integration
│   │   │
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User table
│   │   │   ├── quote_request.py     # Quote requests table
│   │   │   ├── claim_request.py     # Claim requests table
│   │   │   ├── contact_message.py   # Contact messages table
│   │   │   ├── team_member.py       # Team members table
│   │   │   ├── system_log.py        # System logs table
│   │   │   └── audit_log.py         # Audit logs table
│   │   │
│   │   ├── schemas/                  # Pydantic validation schemas
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # UserRegister, UserLogin, Token
│   │   │   ├── quote.py             # QuoteRequestCreate, QuoteRequestResponse
│   │   │   ├── claim.py             # ClaimRequestCreate, ClaimRequestResponse
│   │   │   ├── contact.py           # ContactMessageCreate
│   │   │   ├── team.py              # TeamMemberResponse
│   │   │   └── user.py              # UserProfile, UserUpdate
│   │   │
│   │   ├── middleware/               # Custom middleware
│   │   │   ├── __init__.py
│   │   │   ├── exception_handler.py # GlobalExceptionMiddleware
│   │   │   └── logging_middleware.py # Request/response logging
│   │   │
│   │   ├── core/                     # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # Environment settings
│   │   │   ├── database.py          # DB connection, sessions
│   │   │   ├── security.py          # JWT, password hashing
│   │   │   └── logging_config.py    # Logging setup
│   │   │
│   │   ├── utils/                    # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── email.py             # Email helpers
│   │   │   └── validators.py        # Custom validators
│   │   │
│   │   └── main.py                   # FastAPI app entry point
│   │
│   ├── alembic/                      # Database migrations
│   │   ├── versions/                # Migration files
│   │   ├── env.py                   # Alembic environment
│   │   └── alembic.ini              # Alembic config
│   │
│   ├── tests/                        # Backend tests
│   │   ├── unit/                    # Unit tests (services)
│   │   ├── integration/             # Integration tests (full stack)
│   │   └── conftest.py              # Pytest configuration
│   │
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Example environment variables
│   └── Dockerfile                    # Backend Docker image
│
├── frontend/                         # Vue 3 frontend
│   ├── src/
│   │   ├── components/              # Reusable Vue components
│   │   │   ├── common/              # Shared components
│   │   │   │   ├── AppHeader.vue
│   │   │   │   ├── AppFooter.vue
│   │   │   │   ├── TopNav.vue       # Top navigation option
│   │   │   │   ├── LeftNav.vue      # Left navigation option
│   │   │   │   ├── LoadingSpinner.vue
│   │   │   │   └── ErrorMessage.vue
│   │   │   │
│   │   │   ├── forms/               # Form components
│   │   │   │   ├── QuoteRequestForm.vue
│   │   │   │   ├── ClaimRequestForm.vue
│   │   │   │   ├── ContactForm.vue
│   │   │   │   └── LoginForm.vue
│   │   │   │
│   │   │   └── cards/               # Card components
│   │   │       ├── ServiceCard.vue
│   │   │       ├── TeamMemberCard.vue
│   │   │       └── RequestStatusCard.vue
│   │   │
│   │   ├── views/                   # Page components (routes)
│   │   │   ├── HomePage.vue
│   │   │   ├── ServicesPage.vue
│   │   │   ├── TeamPage.vue
│   │   │   ├── QuoteRequestPage.vue
│   │   │   ├── ClaimsProcessPage.vue
│   │   │   ├── OpenClaimPage.vue
│   │   │   ├── ContactPage.vue
│   │   │   ├── LoginPage.vue
│   │   │   ├── RegisterPage.vue
│   │   │   └── DashboardPage.vue
│   │   │
│   │   ├── router/                  # Vue Router configuration
│   │   │   └── index.ts
│   │   │
│   │   ├── stores/                  # Pinia state management
│   │   │   ├── auth.ts              # Authentication state
│   │   │   ├── quotes.ts            # Quote requests state
│   │   │   ├── claims.ts            # Claim requests state
│   │   │   └── user.ts              # User profile state
│   │   │
│   │   ├── services/                # API client services
│   │   │   ├── api.ts               # Axios instance
│   │   │   ├── authService.ts       # Auth API calls
│   │   │   ├── quoteService.ts      # Quote API calls
│   │   │   ├── claimService.ts      # Claim API calls
│   │   │   ├── contactService.ts    # Contact API calls
│   │   │   └── teamService.ts       # Team API calls
│   │   │
│   │   ├── assets/                  # Static assets
│   │   │   ├── images/              # Images
│   │   │   │   ├── mt-hood.jpg      # Hero image
│   │   │   │   ├── oregon-stag.jpg  # Stag sign
│   │   │   │   └── placeholder.jpg
│   │   │   │
│   │   │   └── styles/              # Global styles
│   │   │       ├── main.css         # Global CSS
│   │   │       ├── variables.css    # CSS variables (colors)
│   │   │       └── reset.css        # CSS reset
│   │   │
│   │   ├── types/                   # TypeScript type definitions
│   │   │   ├── auth.ts
│   │   │   ├── quote.ts
│   │   │   ├── claim.ts
│   │   │   └── user.ts
│   │   │
│   │   ├── App.vue                  # Root Vue component
│   │   └── main.ts                  # Vue app entry point
│   │
│   ├── public/                      # Public static files
│   │   ├── favicon.ico
│   │   └── robots.txt
│   │
│   ├── index.html                   # HTML template
│   ├── package.json                 # NPM dependencies
│   ├── vite.config.ts               # Vite configuration
│   ├── tsconfig.json                # TypeScript configuration
│   └── Dockerfile                   # Frontend Docker image
│
├── docker/                          # Docker configuration files
│   ├── nginx.conf                   # Production nginx config (HTTPS, SSL)
│   ├── nginx.dev.conf               # Development nginx config (HTTP only)
│   └── init.sql                     # Database initialization SQL
│
├── docs/                            # Project documentation
│   ├── api/                         # API endpoint documentation
│   │   ├── auth-endpoints.md
│   │   ├── quote-endpoints.md
│   │   └── ...
│   │
│   ├── sessions/                    # Session notes
│   │   ├── 2025-10-23-session.md
│   │   └── ...
│   │
│   ├── architecture/                # Architecture documentation
│   │   ├── BACKEND-PATTERNS.md
│   │   ├── PROJECT-STRUCTURE.md
│   │   └── DATABASE-DESIGN.md
│   │
│   ├── templates/                   # Documentation templates
│   │   ├── api-endpoint-template.md
│   │   └── session-notes-template.md
│   │
│   └── DESIGN.md                    # Main design document
│
├── docker-compose.yml               # Production Docker Compose (default)
├── docker-compose.dev.yml           # Development Docker Compose
├── .gitignore                       # Git ignore rules
├── .env.example                     # Example production environment file
├── .env.dev.example                 # Example development environment file
└── README.md                        # Project README
```

---

## Key Directories Explained

### Backend Structure

**`app/routers/`** - Thin controllers that handle HTTP routing
- Define API endpoints
- Call service layer methods
- Return responses
- No business logic

**`app/services/`** - Business logic layer
- All business rules
- Data validation
- Database operations
- Exception throwing

**`app/models/`** - SQLAlchemy ORM models
- Database table definitions
- Relationships
- Constraints

**`app/schemas/`** - Pydantic validation models
- Request validation
- Response serialization
- Type safety

**`app/middleware/`** - Custom middleware
- Global exception handling
- Request/response logging
- CORS configuration

**`app/core/`** - Core configuration
- Settings management
- Database connection
- Security (JWT, password hashing)

### Frontend Structure

**`src/views/`** - Page components (one per route)
- Full page layouts
- Compose smaller components
- Handle route-level logic

**`src/components/`** - Reusable components
- Small, focused components
- Presentational logic
- Shared across views

**`src/stores/`** - Pinia state management
- Global application state
- Authentication state
- User data caching

**`src/services/`** - API client services
- HTTP requests to backend
- Error handling
- Response transformation

**`src/router/`** - Vue Router configuration
- Route definitions
- Navigation guards
- Route meta (auth required)

---

## File Naming Conventions

### Backend (Python)

- **Files:** `snake_case.py`
- **Classes:** `PascalCase`
- **Functions:** `snake_case()`
- **Variables:** `snake_case`
- **Constants:** `UPPER_SNAKE_CASE`

### Frontend (TypeScript/Vue)

- **Files:** `PascalCase.vue`, `camelCase.ts`
- **Components:** `PascalCase.vue`
- **Composables:** `use*.ts`
- **Services:** `*Service.ts`
- **Stores:** `camelCase.ts`
- **Types:** `PascalCase` interfaces

---

## Environment Configuration

### Development

**Backend** - `.env`:
```
DATABASE_URL=mysql+pymysql://whittaker_user:SecureW@Pa55!2025@db:3306/whittaker_agency
JWT_SECRET_KEY=dev-secret-key-change-in-production
ENVIRONMENT=development
BREVO_API_KEY=stub
```

**Frontend** - `.env`:
```
VITE_API_BASE_URL=http://localhost:8082/api/v1
```

### Production

**Backend** - `.env.production`:
```
DATABASE_URL=mysql+pymysql://whittaker_user:SecureW@Pa55!2025@db:3306/whittaker_agency
JWT_SECRET_KEY=<generate-secure-random-key>
ENVIRONMENT=production
BREVO_API_KEY=<actual-brevo-api-key>
BREVO_SENDER_EMAIL=noreply@whittakeragency.com
BREVO_ADMIN_EMAIL=admin@whittakeragency.com
```

**Frontend** - `.env.production`:
```
VITE_API_BASE_URL=https://whittakeragency.com/api/v1
```

---

## Docker Configuration

### Development Stack

**Services:**
1. **MariaDB** - Port 3310 (external)
2. **FastAPI** - Port 5102 (internal)
3. **nginx** - Port 8082 (serves Vue + proxies API)

**Optional:**
- **Vite** - Port 3003 (hot reload for UI development)

### Production Stack

**Services:**
1. **MariaDB** - Internal only
2. **FastAPI** - Internal port 5000
3. **nginx** - Ports 80/443 (SSL termination)

---

## Database Migrations

**Tool:** Alembic

**Create migration:**
```bash
cd backend
alembic revision --autogenerate -m "Description"
```

**Apply migrations:**
```bash
alembic upgrade head
```

**Rollback:**
```bash
alembic downgrade -1
```

---

## Development Workflow

### Starting Development Environment

```bash
# Start all services
docker-compose up

# Access points:
# - Frontend: http://localhost:8082
# - API: http://localhost:8082/api/v1
# - API Docs: http://localhost:5102/docs
# - Database: localhost:3310
```

### Optional: Vite Dev Server (UI-heavy work)

```bash
cd frontend
npm run dev
# Access: http://localhost:3003
```

---

## API Documentation

**Auto-generated:** FastAPI provides automatic OpenAPI documentation

**Access:**
- **Swagger UI:** http://localhost:5102/docs
- **ReDoc:** http://localhost:5102/redoc

**Manual documentation:** Store in `docs/api/` using template

---

## Testing Strategy

### Backend Tests

**Unit Tests:**
```bash
cd backend
pytest tests/unit/
```

**Integration Tests:**
```bash
pytest tests/integration/
```

### Frontend Tests

**Component Tests:**
```bash
cd frontend
npm run test:unit
```

**E2E Tests:**
```bash
npm run test:e2e
```

---

**Document Version:** 1.0
**Last Updated:** 2025-10-23
