# OptiMeal - Meal Management System

AI-powered meal planning and nutritional tracking application.

## Project Structure

```
OptiMeal/
├── api/                    # Python/FastAPI backend
│   ├── src/
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── api/           # API endpoints
│   │   ├── db/            # Database configuration
│   │   ├── utils/         # Utilities (auth, image processing, LLM client)
│   │   └── main.py        # FastAPI application
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/               # React + TypeScript + Vite
│   ├── src/
│   │   ├── pages/         # Main pages
│   │   ├── components/    # Reusable components
│   │   ├── services/      # API client, storage
│   │   ├── routes/        # React Router configuration
│   │   ├── types/         # TypeScript types
│   │   └── theme/         # MUI theme customization
│   └── package.json
│
├── shared/                 # Shared types/contracts (optional)
└── specs/                  # Feature specifications
```

## Tech Stack

### Backend
- **Python 3.11+** with FastAPI
- **PostgreSQL** for database
- **SQLAlchemy** ORM with Alembic migrations
- **Google Gemini 2.5 Flash** for AI meal planning (FREE tier)
- **PaddleOCR** + MediaPipe for nutrition label OCR (open-source)

### Frontend
- **React 18** with TypeScript
- **Vite** for build tooling
- **Material-UI (MUI)** for components
- **React Router** for navigation
- **Recharts** for data visualization
- **Axios** for API calls
- **Localforage** for offline storage

## Quick Start

### Prerequisites
- **Docker Desktop** ([download here](https://www.docker.com/products/docker-desktop))
- That's it! Docker handles everything else.

### Start the Application (Recommended - Docker)

```bash
# Start all services (database, API, frontend)
docker-compose up

# Or use the Makefile for convenience
make up
```

**That's it!** The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Common Docker Commands

```bash
make help              # Show all available commands
make up                # Start all services
make down              # Stop all services
make logs              # View logs
make migrate           # Run database migrations
make test-api          # Run backend tests
make shell-api         # Open shell in API container
make shell-db          # Access PostgreSQL CLI
make init              # First-time setup (build + migrate)
```

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed Docker documentation.

### Alternative: Local Setup (Without Docker)

<details>
<summary>Click to expand local setup instructions</summary>

#### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

#### Backend Setup

1. Create virtual environment and install dependencies:
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy environment configuration:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and API keys
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the API server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

#### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

</details>

## Development

### Backend Commands

```bash
# Format code
black src/
isort src/

# Lint code
ruff check .

# Run tests
pytest

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

### Frontend Commands

```bash
# Type check
npm run tsc

# Lint
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

## Database

The Docker setup automatically creates and manages a PostgreSQL database. No manual setup required!

If you need to access the database directly:
```bash
make shell-db
# Or: docker-compose exec postgres psql -U optimeal_user -d optimeal_dev
```

For production, update `DATABASE_URL` in your environment to point to your production PostgreSQL instance.

## Features

This is feature **001-meal-management**, implementing:

1. **Pantry Management** - Track food inventory with quantities and expiration dates
2. **Meal Logging** - Log meals with automatic nutritional tracking
3. **Recipe Management** - Save and reuse meal combinations
4. **AI Meal Planning** - Generate meal plans using Google Gemini AI
5. **Shopping Lists** - Auto-generate shopping lists from meal plans
6. **Nutritional Insights** - Visualize eating patterns and nutrition data
7. **OCR Support** - Parse nutrition labels from photos

## Implementation Status

✅ **Phase 1 Complete**: Project setup and infrastructure
- Created project structure (api/, frontend/, shared/)
- Initialized FastAPI backend with hot reload
- Initialized React + TypeScript + Vite frontend
- Configured development tools (ESLint, Prettier, Black, Ruff)
- **Docker setup complete** - database, API, and frontend run in containers

⏳ **Phase 2 Next**: Database models, authentication, and API foundation

See [specs/001-meal-management/tasks.md](specs/001-meal-management/tasks.md) for detailed task breakdown.

## Documentation

- **[Docker Setup Guide](DOCKER_SETUP.md)** - Complete Docker development guide
- [Feature Specification](specs/001-meal-management/spec.md)
- [Implementation Plan](specs/001-meal-management/plan.md)
- [Data Model](specs/001-meal-management/data-model.md)
- [API Contracts](specs/001-meal-management/contracts/openapi.yaml)
- [Quickstart Guide](specs/001-meal-management/quickstart.md)
- [Research Notes](specs/001-meal-management/research.md)

## License

Proprietary - All rights reserved
