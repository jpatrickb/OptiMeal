# Docker Development Setup

This guide explains how to run OptiMeal using Docker for development.

## Prerequisites

- Docker Desktop installed ([download here](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)

## Quick Start

### 1. Start All Services

From the project root directory:

```bash
docker-compose up
```

This will start:
- **PostgreSQL** on port 5432
- **Backend API** on port 8000
- **Frontend** on port 5173

### 2. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432 (username: optimeal_user, password: dev_password_change_in_production)

### 3. Stop All Services

```bash
docker-compose down
```

To also remove volumes (clears database):
```bash
docker-compose down -v
```

## Common Commands

### Build/Rebuild Services

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build api
docker-compose build frontend

# Rebuild without cache
docker-compose build --no-cache
```

### Start/Stop Services

```bash
# Start in detached mode (background)
docker-compose up -d

# Start specific service
docker-compose up postgres
docker-compose up api

# Stop all services
docker-compose stop

# Restart a service
docker-compose restart api
```

### View Logs

```bash
# All services
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f postgres
```

### Execute Commands in Containers

```bash
# Backend shell
docker-compose exec api bash

# Run Alembic migrations
docker-compose exec api alembic upgrade head

# Create new migration
docker-compose exec api alembic revision --autogenerate -m "Description"

# Access PostgreSQL CLI
docker-compose exec postgres psql -U optimeal_user -d optimeal_dev

# Run backend tests
docker-compose exec api pytest

# Frontend shell
docker-compose exec frontend sh

# Run frontend commands
docker-compose exec frontend npm run lint
```

## Database Management

### Reset Database

```bash
# Stop services
docker-compose down

# Remove database volume
docker volume rm optimeal_postgres_data

# Restart (will create fresh database)
docker-compose up postgres
```

### View Database

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U optimeal_user -d optimeal_dev

# Common SQL commands
\dt                    # List tables
\d table_name          # Describe table
SELECT * FROM users;   # Query data
\q                     # Quit
```

### Backup Database

```bash
# Create backup
docker-compose exec postgres pg_dump -U optimeal_user optimeal_dev > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U optimeal_user -d optimeal_dev < backup.sql
```

## Running Migrations

### First-Time Setup

```bash
# Start PostgreSQL
docker-compose up -d postgres

# Wait for database to be ready (about 10 seconds)
sleep 10

# Initialize Alembic (if not already done)
docker-compose exec api alembic init alembic

# Create initial migration
docker-compose exec api alembic revision --autogenerate -m "Initial schema"

# Apply migrations
docker-compose exec api alembic upgrade head
```

### Creating New Migrations

After modifying models:

```bash
# Generate migration
docker-compose exec api alembic revision --autogenerate -m "Add new field"

# Apply migration
docker-compose exec api alembic upgrade head
```

## Development Workflow

### Hot Reload

Both frontend and backend have hot reload enabled:
- Backend: Uvicorn will auto-reload when you edit Python files
- Frontend: Vite will auto-reload when you edit React files

### Environment Variables

**Backend**: Edit `api/.env`
**Frontend**: Edit `frontend/.env`

After changing environment variables:
```bash
docker-compose restart api
docker-compose restart frontend
```

### Installing New Dependencies

**Backend** (Python):
```bash
# Add to requirements.txt, then rebuild
docker-compose build api
docker-compose up api
```

**Frontend** (npm):
```bash
# Add to package.json, then rebuild
docker-compose build frontend
docker-compose up frontend

# Or install directly in running container
docker-compose exec frontend npm install package-name
```

## Troubleshooting

### Port Already in Use

If ports 5432, 8000, or 5173 are already in use:

1. Stop conflicting services
2. Or edit `docker-compose.yml` to use different ports

### Database Connection Errors

```bash
# Check if PostgreSQL is healthy
docker-compose ps

# View PostgreSQL logs
docker-compose logs postgres

# Ensure database is ready
docker-compose exec postgres pg_isready -U optimeal_user
```

### Frontend Can't Connect to API

- Ensure `VITE_API_BASE_URL` in `frontend/.env` is set to `http://localhost:8000/api/v1`
- Check API is running: `curl http://localhost:8000/health`

### Container Won't Start

```bash
# View detailed logs
docker-compose logs -f <service-name>

# Remove all containers and start fresh
docker-compose down
docker-compose up --build
```

### Clear Everything and Start Fresh

```bash
# Stop all containers
docker-compose down -v

# Remove images
docker rmi optimeal-api optimeal-frontend

# Rebuild and start
docker-compose up --build
```

## Production Deployment

**DO NOT use docker-compose.yml for production!**

For production:
1. Use separate environment variables (never commit .env files)
2. Change all passwords and secrets
3. Use proper secret management (AWS Secrets Manager, etc.)
4. Configure proper DATABASE_URL for production PostgreSQL
5. Use production-ready images (multi-stage builds, no --reload)
6. Configure CORS properly in FastAPI
7. Set up HTTPS/SSL
8. Use orchestration (Kubernetes, ECS, etc.)

## Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Frontend  │────────▶│   Backend   │────────▶│  PostgreSQL │
│   (Vite)    │         │  (FastAPI)  │         │             │
│  Port 5173  │         │  Port 8000  │         │  Port 5432  │
└─────────────┘         └─────────────┘         └─────────────┘
      │                        │                        │
      │                        │                        │
      └────────────────────────┴────────────────────────┘
                     optimeal-network (Docker)
```

## Next Steps

1. Verify all services are running: `docker-compose ps`
2. Check API health: `curl http://localhost:8000/health`
3. Open frontend: http://localhost:5173
4. Run migrations (see "Running Migrations" section)
5. Start implementing features!

## Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI in Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Vite Docker Guide](https://vitejs.dev/guide/static-deploy.html)
