# Slice 1: Foundation & Infrastructure

**Project:** Whittaker Agency
**Slice:** 1 of 6
**Estimated Time:** 8-12 hours
**Status:** Ready to implement

---

## Overview

This slice establishes the foundational infrastructure for the entire project:
- Docker containerization (MariaDB, FastAPI, nginx)
- Database schema and migrations
- JWT authentication system
- Basic project structure for frontend and backend
- Development and production configurations

**Goal:** By the end of this slice, you should be able to register a user, log in, and receive a JWT token.

---

## Deliverables Checklist

### Docker & Infrastructure
- [ ] Create `docker-compose.yml` (production configuration)
- [ ] Create `docker-compose.dev.yml` (development configuration)
- [ ] Create `docker/nginx.conf` (production - HTTPS, SSL, rate limiting)
- [ ] Create `docker/nginx.dev.conf` (development - HTTP only)
- [ ] Create `docker/init.sql` (initial database setup)
- [ ] Create `.env.example` (production environment template)
- [ ] Create `.env.dev.example` (development environment template)
- [ ] Test Docker containers start successfully

### Backend Structure
- [ ] Create `backend/requirements.txt` with all Python dependencies
- [ ] Create `backend/Dockerfile` (multi-stage for dev/prod)
- [ ] Create `backend/app/main.py` (FastAPI application entry point)
- [ ] Create `backend/app/core/config.py` (environment settings)
- [ ] Create `backend/app/core/database.py` (database connection, sessions)
- [ ] Create `backend/app/core/security.py` (JWT, password hashing)
- [ ] Create `backend/app/core/logging_config.py` (logging setup)
- [ ] Create `backend/app/middleware/exception_handler.py` (global exception middleware)
- [ ] Create `backend/app/middleware/logging_middleware.py` (request/response logging)

### Database Schema & Migrations
- [ ] Initialize Alembic (`alembic init alembic`)
- [ ] Configure `alembic.ini` and `alembic/env.py`
- [ ] Create `backend/app/models/user.py` (User ORM model)
- [ ] Create `backend/app/models/quote_request.py` (QuoteRequest ORM model)
- [ ] Create `backend/app/models/claim_request.py` (ClaimRequest ORM model)
- [ ] Create `backend/app/models/contact_message.py` (ContactMessage ORM model)
- [ ] Create `backend/app/models/team_member.py` (TeamMember ORM model)
- [ ] Create `backend/app/models/system_log.py` (SystemLog ORM model)
- [ ] Create `backend/app/models/audit_log.py` (AuditLog ORM model)
- [ ] Create `backend/app/models/attachment.py` (Attachment ORM model)
- [ ] Generate initial migration: `alembic revision --autogenerate -m "Initial schema"`
- [ ] Apply migration: `alembic upgrade head`
- [ ] Verify all tables created in database

### Authentication System
- [ ] Create `backend/app/schemas/auth.py` (UserRegister, UserLogin, Token, UserProfile)
- [ ] Create `backend/app/services/auth_service.py` (registration, login, JWT logic)
- [ ] Create `backend/app/services/system_log_service.py` (system logging service)
- [ ] Create `backend/app/services/audit_log_service.py` (audit logging service)
- [ ] Create `backend/app/routers/auth.py` (POST /auth/register, POST /auth/login)
- [ ] Create `backend/app/core/dependencies.py` (`get_current_user` dependency)
- [ ] Test registration endpoint with Postman/curl
- [ ] Test login endpoint returns valid JWT
- [ ] Test protected endpoint requires valid JWT

### Frontend Structure
- [ ] Create `frontend/package.json` with Vue 3, TypeScript, Vite dependencies
- [ ] Create `frontend/vite.config.ts`
- [ ] Create `frontend/tsconfig.json`
- [ ] Create `frontend/index.html`
- [ ] Create `frontend/Dockerfile` (multi-stage build)
- [ ] Create `frontend/src/main.ts` (Vue app entry point)
- [ ] Create `frontend/src/App.vue` (root component)
- [ ] Create `frontend/src/router/index.ts` (Vue Router setup)
- [ ] Create `frontend/src/stores/auth.ts` (Pinia auth store)
- [ ] Create `frontend/src/services/api.ts` (Axios instance with JWT interceptor)
- [ ] Create `frontend/src/services/authService.ts` (register, login API calls)
- [ ] Create `frontend/src/types/auth.ts` (TypeScript interfaces)
- [ ] Create `frontend/src/assets/styles/main.css` (global CSS)
- [ ] Create `frontend/src/assets/styles/variables.css` (CSS color variables)
- [ ] Create `frontend/.env.development` (`VITE_API_BASE_URL=http://localhost:8082/api/v1`)
- [ ] Create `frontend/.env.production` (`VITE_API_BASE_URL=https://whittakeragency.com/api/v1`)

### Basic UI Components
- [ ] Create `frontend/src/views/LoginPage.vue` (basic login form)
- [ ] Create `frontend/src/views/RegisterPage.vue` (basic registration form)
- [ ] Create `frontend/src/components/common/AppHeader.vue` (placeholder header)
- [ ] Create `frontend/src/components/common/AppFooter.vue` (placeholder footer)
- [ ] Configure routes for `/login` and `/register`

### Testing & Verification
- [ ] Start development environment: `docker-compose -f docker-compose.dev.yml up`
- [ ] Verify MariaDB accessible on `localhost:3310`
- [ ] Verify FastAPI docs accessible at `http://localhost:5102/docs`
- [ ] Verify frontend accessible at `http://localhost:8082`
- [ ] Test full registration flow (frontend → backend → database)
- [ ] Test full login flow (frontend → backend → JWT → auth store)
- [ ] Verify JWT stored in auth store and used in API requests
- [ ] Check SystemLog table for any errors
- [ ] Check AuditLog table for user registration/login events

---

## Docker Compose Configuration

### Production (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  db:
    image: mariadb:10.11
    container_name: whittaker-db
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: whittaker
      MYSQL_USER: whittaker_user
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - whittaker_mariadb_data:/var/lib/mysql
    networks:
      - whittaker-network
    restart: unless-stopped

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: production
    container_name: whittaker-api
    environment:
      DATABASE_URL: mysql+pymysql://whittaker_user:${MYSQL_PASSWORD}@db:3306/whittaker
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      BREVO_API_KEY: ${BREVO_API_KEY}
      ENVIRONMENT: production
    volumes:
      - whittaker_uploads:/app/uploads
    depends_on:
      - db
    networks:
      - whittaker-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: whittaker-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
    depends_on:
      - api
    networks:
      - whittaker-network
    restart: unless-stopped

  certbot:
    image: certbot/certbot
    container_name: whittaker-certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

volumes:
  whittaker_mariadb_data:
  whittaker_uploads:

networks:
  whittaker-network:
    driver: bridge
```

---

### Development (`docker-compose.dev.yml`)

```yaml
version: '3.8'

services:
  db:
    image: mariadb:10.11
    container_name: whittaker-db
    ports:
      - "3310:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: whittaker
      MYSQL_USER: whittaker_user
      MYSQL_PASSWORD: SecureW@Pa55!2025
    volumes:
      - whittaker_mariadb_data:/var/lib/mysql
      - ./docker/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - whittaker-network

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: development
    container_name: whittaker-api
    ports:
      - "5102:5102"
    environment:
      DATABASE_URL: mysql+pymysql://whittaker_user:SecureW@Pa55!2025@db:3306/whittaker
      JWT_SECRET_KEY: dev-secret-key-change-in-production
      BREVO_API_KEY: stub
      ENVIRONMENT: development
    volumes:
      - ./backend/app:/app/app
      - whittaker_uploads:/app/uploads
    depends_on:
      - db
    networks:
      - whittaker-network
    command: uvicorn app.main:app --host 0.0.0.0 --port 5102 --reload

  nginx:
    image: nginx:alpine
    container_name: whittaker-nginx
    ports:
      - "8082:80"
    volumes:
      - ./docker/nginx.dev.conf:/etc/nginx/nginx.conf:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - api
    networks:
      - whittaker-network

volumes:
  whittaker_mariadb_data:
  whittaker_uploads:

networks:
  whittaker-network:
    driver: bridge
```

---

## Database Schema (Initial Migration)

### Users Table

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;
```

### Quote Requests Table

```sql
CREATE TABLE quote_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    insurance_type ENUM('auto', 'home', 'business', 'life', 'health', 'motorcycle', 'boat', 'rental') NOT NULL,
    coverage_details TEXT,
    status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
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
    insurance_type ENUM('auto', 'home', 'business', 'life', 'health', 'motorcycle', 'boat', 'rental') NOT NULL,
    incident_description TEXT NOT NULL,
    incident_date DATE NOT NULL,
    status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
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
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status ENUM('new', 'read', 'responded') DEFAULT 'new',
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
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    bio TEXT,
    photo_url VARCHAR(500),
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_display_order (display_order),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB;
```

### System Log Table

```sql
CREATE TABLE system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') NOT NULL,
    message TEXT NOT NULL,
    exception_type VARCHAR(255),
    exception_message TEXT,
    stack_trace TEXT,
    request_method VARCHAR(10),
    request_path VARCHAR(500),
    request_ip VARCHAR(45),
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_level (level),
    INDEX idx_created_at (created_at),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

### Audit Log Table

```sql
CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INT,
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_created_at (created_at)
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

---

## Backend Key Files

### `backend/requirements.txt`

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pymysql==1.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
httpx==0.25.2
```

---

### `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware.exception_handler import GlobalExceptionMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.routers import auth

app = FastAPI(
    title="Whittaker Agency API",
    description="Insurance agency management system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(GlobalExceptionMiddleware)
app.add_middleware(LoggingMiddleware)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Whittaker Agency API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

### `backend/app/core/config.py`

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440  # 24 hours

    # Email (Brevo)
    BREVO_API_KEY: str = "stub"
    BREVO_SENDER_EMAIL: str = "noreply@whittakeragency.com"
    BREVO_ADMIN_EMAIL: str = "admin@whittakeragency.com"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3003,http://localhost:8082"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

### `backend/app/core/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### `backend/app/core/security.py`

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
```

---

### `backend/app/routers/auth.py` (Thin Controller Example)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import UserRegister, UserLogin, Token, UserProfile
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user - Thin controller, business logic in service"""
    user = await AuthService.register_user(db, user_data)
    return user

@router.post("/login", response_model=Token)
async def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user and return JWT token - Thin controller"""
    token = await AuthService.login_user(db, credentials)
    return token
```

---

### `backend/app/services/auth_service.py` (Business Logic Example)

```python
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, Token, UserProfile
from app.core.security import hash_password, verify_password, create_access_token
from app.services.audit_log_service import AuditLogService

class AuthService:
    @staticmethod
    async def register_user(db: Session, user_data: UserRegister) -> UserProfile:
        """Register a new user with business logic and validation"""

        # Business rule: Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create user
        hashed_password = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            phone=user_data.phone,
            hashed_password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Audit log
        await AuditLogService.log_user_action(
            db=db,
            user_id=new_user.id,
            action="user_registered",
            entity_type="user",
            entity_id=new_user.id,
            details=f"User registered: {new_user.email}"
        )

        return UserProfile.from_orm(new_user)

    @staticmethod
    async def login_user(db: Session, credentials: UserLogin) -> Token:
        """Authenticate user and return JWT token"""

        # Find user
        user = db.query(User).filter(User.email == credentials.email).first()

        # Verify credentials
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Check if active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )

        # Create JWT token
        access_token = create_access_token(data={"sub": str(user.id)})

        # Audit log
        await AuditLogService.log_user_action(
            db=db,
            user_id=user.id,
            action="user_login",
            entity_type="user",
            entity_id=user.id,
            details=f"User logged in: {user.email}"
        )

        return Token(access_token=access_token, token_type="bearer")
```

---

## Frontend Key Files

### `frontend/package.json`

```json
{
  "name": "whittaker-agency-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "typescript": "^5.3.2",
    "vite": "^5.0.4",
    "vue-tsc": "^1.8.22"
  }
}
```

---

### `frontend/src/stores/auth.ts`

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<any | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function setUser(userData: any) {
    user.value = userData
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    user,
    isAuthenticated,
    setToken,
    setUser,
    logout
  }
})
```

---

### `frontend/src/services/api.ts`

```typescript
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

---

## Testing Checklist

### Manual Testing Steps

1. **Start Development Environment:**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

2. **Verify Database:**
   - Connect to MariaDB on `localhost:3310` using HeidiSQL
   - User: `whittaker_user`, Password: `SecureW@Pa55!2025`
   - Verify all 8 tables exist: users, quote_requests, claim_requests, contact_messages, team_members, system_logs, audit_logs, attachments

3. **Test API Endpoints (FastAPI Docs):**
   - Navigate to `http://localhost:5102/docs`
   - Test POST `/api/v1/auth/register`:
     ```json
     {
       "email": "test@example.com",
       "full_name": "Test User",
       "phone": "555-1234",
       "password": "TestPassword123!"
     }
     ```
   - Verify response returns user profile (no password)
   - Check `audit_logs` table for registration event

   - Test POST `/api/v1/auth/login`:
     ```json
     {
       "email": "test@example.com",
       "password": "TestPassword123!"
     }
     ```
   - Verify response contains `access_token` and `token_type: "bearer"`
   - Check `audit_logs` table for login event

4. **Test Frontend:**
   - Navigate to `http://localhost:8082`
   - Go to `/register` page
   - Register a new user
   - Verify redirected to login
   - Login with new user
   - Verify JWT token stored in localStorage
   - Verify auth store populated

5. **Test Error Handling:**
   - Try registering with existing email (should fail with 400)
   - Try logging in with wrong password (should fail with 401)
   - Check `system_logs` table for error entries

---

## Common Issues & Solutions

### Issue: Database connection refused
**Solution:** Ensure MariaDB container is running and healthy. Wait 10-15 seconds after `docker-compose up` for database initialization.

### Issue: Alembic migration fails
**Solution:** Delete `backend/alembic/versions/*.py` files, drop all tables, run `alembic revision --autogenerate` again.

### Issue: CORS errors in browser
**Solution:** Check `CORS_ORIGINS` in backend `.env` includes frontend URL (e.g., `http://localhost:8082`).

### Issue: JWT token not working
**Solution:** Verify `JWT_SECRET_KEY` is set in backend `.env`. Check browser console for token in localStorage.

### Issue: nginx 502 Bad Gateway
**Solution:** Ensure FastAPI container is running. Check `docker-compose logs api` for errors.

---

## Next Steps

After completing Slice 1, you should have:
- ✅ Working Docker development environment
- ✅ Database schema with all tables
- ✅ User registration and login working
- ✅ JWT authentication protecting routes
- ✅ Basic frontend with login/register pages
- ✅ Exception handling and logging in place

**Ready for Slice 2:** Core Pages & Navigation (Homepage, Services, Team, Navigation components)

---

**Document Version:** 1.0
**Created:** 2025-10-23
**Last Updated:** 2025-10-23
