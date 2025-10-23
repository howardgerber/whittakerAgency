# Development vs Production Configuration

**Project:** Whittaker Agency
**Created:** 2025-10-23

---

## Overview

This document outlines the differences between development and production configurations. The project uses separate Docker Compose files and nginx configurations to optimize for each environment.

---

## File Structure

```
├── docker-compose.yml          # Production configuration (default)
├── docker-compose.dev.yml      # Development configuration
├── docker/
│   ├── nginx.conf              # Production nginx (HTTPS, ports 80/443)
│   └── nginx.dev.conf          # Development nginx (HTTP only, port 8082)
├── backend/
│   ├── .env.example            # Production environment variables
│   └── .env.dev.example        # Development environment variables
└── frontend/
    ├── .env.production         # Production frontend config
    └── .env.development        # Development frontend config
```

---

## Docker Compose Differences

### Development (`docker-compose.dev.yml`)

**Purpose:** Local development with hot reload, exposed ports, and debugging

**Services:**
```yaml
services:
  db:
    image: mariadb:10.11
    container_name: whittaker-db
    ports:
      - "3310:3306"              # ← EXPOSED for HeidiSQL access
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
    container_name: whittaker-api
    ports:
      - "5102:5102"              # ← EXPOSED for direct API access
    environment:
      DATABASE_URL: mysql+pymysql://whittaker_user:SecureW@Pa55!2025@db:3306/whittaker
      JWT_SECRET_KEY: dev-secret-key-change-in-production
      ENVIRONMENT: development
    volumes:
      - ./backend/app:/app/app   # ← HOT RELOAD: code changes reflected immediately
      - whittaker_uploads:/app/uploads
    depends_on:
      - db
    networks:
      - whittaker-network
    command: uvicorn app.main:app --host 0.0.0.0 --port 5102 --reload  # ← --reload flag

  nginx:
    image: nginx:alpine
    container_name: whittaker-nginx
    ports:
      - "8082:80"                # ← HTTP only on port 8082
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

**Key Features:**
- ✅ Exposed ports for debugging (3310, 5102, 8082)
- ✅ Hot reload enabled (--reload flag, volume mount)
- ✅ Simple passwords (dev only!)
- ✅ HTTP only (no SSL overhead)
- ✅ Can run `npm run dev` on host for Vite hot reload

---

### Production (`docker-compose.yml`)

**Purpose:** Optimized for security, performance, and production deployment

**Services:**
```yaml
services:
  db:
    image: mariadb:10.11
    container_name: whittaker-db
    # NO EXTERNAL PORT EXPOSED  # ← Security: database is internal only
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}  # ← From .env file
      MYSQL_DATABASE: whittaker
      MYSQL_USER: whittaker_user
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}            # ← From .env file
    volumes:
      - whittaker_mariadb_data:/var/lib/mysql
    networks:
      - whittaker-network
    restart: unless-stopped

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: production                           # ← Multi-stage build
    container_name: whittaker-api
    # NO EXTERNAL PORT EXPOSED                     # ← Only accessible via nginx
    environment:
      DATABASE_URL: mysql+pymysql://whittaker_user:${MYSQL_PASSWORD}@db:3306/whittaker
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}            # ← From .env file
      BREVO_API_KEY: ${BREVO_API_KEY}
      ENVIRONMENT: production
    volumes:
      - whittaker_uploads:/app/uploads             # ← NO source code mount
    depends_on:
      - db
    networks:
      - whittaker-network
    restart: unless-stopped
    # NO --reload flag

  nginx:
    image: nginx:alpine
    container_name: whittaker-nginx
    ports:
      - "80:80"                                    # ← HTTP (redirects to HTTPS)
      - "443:443"                                  # ← HTTPS with SSL
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
      - ./certbot/conf:/etc/letsencrypt:ro         # ← SSL certificates
      - ./certbot/www:/var/www/certbot:ro
    depends_on:
      - api
    networks:
      - whittaker-network
    restart: unless-stopped

  certbot:                                         # ← SSL certificate management
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

**Key Features:**
- ✅ No exposed ports (except nginx 80/443)
- ✅ Environment variables from .env file
- ✅ SSL/HTTPS with Let's Encrypt
- ✅ Auto-restart on failure
- ✅ No source code mounts (security)
- ✅ Optimized build (multi-stage Dockerfile)

---

## nginx Configuration Differences

### Development (`docker/nginx.dev.conf`)

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream fastapi_backend {
        server api:5102;  # ← FastAPI on port 5102
    }

    server {
        listen 80;        # ← HTTP only
        server_name localhost;

        # Serve Vue frontend
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # Proxy API requests
        location /api/ {
            proxy_pass http://fastapi_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Serve uploaded files
        location /uploads/ {
            alias /app/uploads/;
        }
    }
}
```

**Key Features:**
- ✅ HTTP only on port 80
- ✅ Simple configuration
- ✅ No SSL overhead
- ✅ Direct file serving for uploads

---

### Production (`docker/nginx.conf`)

```nginx
events {
    worker_connections 2048;  # ← Higher for production
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;

    upstream fastapi_backend {
        server api:5000;  # ← FastAPI on port 5000
    }

    # HTTP → HTTPS redirect
    server {
        listen 80;
        server_name whittakeragency.com www.whittakeragency.com;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$server_name$request_uri;  # ← Force HTTPS
        }
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name whittakeragency.com www.whittakeragency.com;

        # SSL configuration
        ssl_certificate /etc/letsencrypt/live/whittakeragency.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/whittakeragency.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Serve Vue frontend
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # Proxy API requests with rate limiting
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://fastapi_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Login endpoint with stricter rate limiting
        location /api/v1/auth/login {
            limit_req zone=login_limit burst=3 nodelay;

            proxy_pass http://fastapi_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Serve uploaded files
        location /uploads/ {
            alias /app/uploads/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

**Key Features:**
- ✅ HTTPS with SSL/TLS
- ✅ HTTP → HTTPS redirect
- ✅ Gzip compression
- ✅ Rate limiting (10 req/s general, 5 req/min login)
- ✅ Security headers
- ✅ Cache control for static files
- ✅ Let's Encrypt SSL certificates

---

## Environment Variables

### Development (backend/.env.dev)

```bash
# Database
DATABASE_URL=mysql+pymysql://whittaker_user:SecureW@Pa55!2025@db:3306/whittaker

# JWT
JWT_SECRET_KEY=dev-secret-key-change-in-production-this-is-not-secure
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Email (stubbed)
BREVO_API_KEY=stub
BREVO_SENDER_EMAIL=dev@localhost
BREVO_ADMIN_EMAIL=admin@localhost

# Environment
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG

# CORS (allow Vite dev server)
CORS_ORIGINS=http://localhost:3003,http://localhost:8082
```

---

### Production (backend/.env)

```bash
# Database
DATABASE_URL=mysql+pymysql://whittaker_user:${MYSQL_PASSWORD}@db:3306/whittaker

# JWT (MUST be secure random key)
JWT_SECRET_KEY=${JWT_SECRET_KEY}  # Generate with: openssl rand -hex 32
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Email (actual Brevo API key)
BREVO_API_KEY=${BREVO_API_KEY}
BREVO_SENDER_EMAIL=noreply@whittakeragency.com
BREVO_ADMIN_EMAIL=kyle@whittakeragency.com

# Environment
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO

# CORS (only allow production domain)
CORS_ORIGINS=https://whittakeragency.com,https://www.whittakeragency.com

# Database passwords (from Docker Compose .env)
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
MYSQL_PASSWORD=${MYSQL_PASSWORD}
```

---

## Frontend Environment Variables

### Development (frontend/.env.development)

```bash
VITE_API_BASE_URL=http://localhost:8082/api/v1
```

---

### Production (frontend/.env.production)

```bash
VITE_API_BASE_URL=https://whittakeragency.com/api/v1
```

---

## Port Summary

| Service        | Development | Production |
|----------------|-------------|------------|
| MariaDB        | 3310        | Internal   |
| FastAPI        | 5102        | Internal   |
| nginx          | 8082        | 80/443     |
| Vite (optional)| 3003        | N/A        |

---

## Startup Commands

### Development

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up

# Start in background
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Rebuild after code changes
docker-compose -f docker-compose.dev.yml up --build

# Stop all services
docker-compose -f docker-compose.dev.yml down
```

**Optional Vite Dev Server:**
```bash
cd frontend
npm run dev
# Access at http://localhost:3003
```

---

### Production

```bash
# Initial setup (one-time)
cp .env.example .env
# Edit .env with production values

# Start all services (docker-compose.yml is default)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# SSL certificate renewal (automatic via certbot)
docker-compose exec certbot certbot renew
```

---

## Security Differences

| Feature                    | Development | Production |
|----------------------------|-------------|------------|
| Database external port     | ✅ Exposed  | ❌ Internal only |
| API external port          | ✅ Exposed  | ❌ Internal only |
| HTTPS/SSL                  | ❌ HTTP     | ✅ HTTPS   |
| Source code in container   | ✅ Mounted  | ❌ Copied  |
| Debug mode                 | ✅ On       | ❌ Off     |
| Hot reload                 | ✅ On       | ❌ Off     |
| Rate limiting              | ❌ Off      | ✅ On      |
| Security headers           | ❌ Off      | ✅ On      |
| Gzip compression           | ❌ Off      | ✅ On      |
| Auto-restart               | ❌ Off      | ✅ On      |
| Simple passwords           | ✅ OK       | ❌ Must be strong |

---

## Best Practices

### Development
- ✅ Use simple passwords (easier to type)
- ✅ Enable hot reload for faster iteration
- ✅ Expose ports for debugging
- ✅ Use volume mounts for code changes
- ✅ Keep DEBUG=True for detailed errors

### Production
- ✅ Use strong, random passwords
- ✅ Never expose database/API ports
- ✅ Always use HTTPS
- ✅ Enable rate limiting
- ✅ Set DEBUG=False
- ✅ Use environment variables for secrets
- ✅ Enable auto-restart
- ✅ Regular backups
- ✅ Monitor logs

---

**Document Version:** 1.0
**Last Updated:** 2025-10-23
