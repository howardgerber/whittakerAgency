# Development Scripts

Batch scripts for managing the Whittaker Agency development environment on Windows.

## First Time Setup

**Run this once to set up your development environment:**
```
FIRST-TIME-SETUP.bat
```

This will:
1. Install Python dependencies
2. Install Node dependencies
3. Run database migrations (requires Docker running)
4. Build frontend

---

## Daily Development Scripts

### Starting/Stopping Services

**Start all services (Docker Compose):**
```
start-all-dev.bat
```
Starts: MariaDB, FastAPI, nginx

**Stop all services:**
```
stop-all-dev.bat
```

### Frontend Development

**Build frontend for nginx:**
```
build-frontend-dev.bat
```
Builds frontend into `frontend/dist/` for nginx to serve

**Run Vite dev server (hot-reload):**
```
run-frontend-dev.bat
```
Starts Vite on http://localhost:3003 (faster for UI development)

**Setup frontend (install + build):**
```
setup-frontend-dev.bat
```

### Backend Development

**Setup backend (install dependencies + migrate):**
```
setup-backend-dev.bat
```

**Run database migrations:**
```
migrate-database-dev.bat
```

**Create new migration:**
```
create-migration-dev.bat "your migration message"
```
Example: `create-migration-dev.bat "add user_preferences table"`

### Logs

**View API logs:**
```
logs-api-dev.bat
```

**View database logs:**
```
logs-db-dev.bat
```

**View all logs:**
```
logs-all-dev.bat
```

---

## Typical Workflow

### First Time
1. Run `FIRST-TIME-SETUP.bat`
2. Run `start-all-dev.bat`
3. Open http://localhost:8082

### Daily Development
1. Run `start-all-dev.bat`
2. Make code changes
3. For frontend changes: Run `build-frontend-dev.bat` OR use `run-frontend-dev.bat` for hot-reload
4. For backend changes: Code reloads automatically (thanks to uvicorn --reload)
5. For database changes: Run `create-migration-dev.bat "message"` then `migrate-database-dev.bat`

### End of Day
1. Run `stop-all-dev.bat`

---

## Access Points

- **Frontend:** http://localhost:8082
- **API Docs (Swagger):** http://localhost:5102/docs
- **API Docs (ReDoc):** http://localhost:5102/redoc
- **Database:** localhost:3310 (HeidiSQL/MySQL Workbench)
  - User: `whittaker_user`
  - Password: `SecureW@Pa55!2025`
  - Database: `whittaker`

---

## Production Scripts

(To be added in Slice 6)
