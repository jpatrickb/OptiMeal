# Quickstart Guide: Meal Management Feature

**Feature**: 001-meal-management
**Last Updated**: 2025-10-25
**Audience**: Developers implementing this feature

---

## Overview

This guide provides step-by-step instructions to set up and implement the Meal Management feature for OptiMeal. The feature consists of:

1. **Backend API** (Python/FastAPI)
2. **Mobile App** (React Native)
3. **Database** (PostgreSQL)
4. **External Services** (OpenAI GPT-4o-mini, Google Cloud Vision API)

---

## Prerequisites

### Required Software

| Tool | Version | Installation |
|------|---------|--------------|
| **Python** | 3.11+ | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ LTS | [nodejs.org](https://nodejs.org/) |
| **PostgreSQL** | 15+ | [postgresql.org](https://www.postgresql.org/download/) |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) |
| **Docker** (optional) | Latest | [docker.com](https://www.docker.com/) |

### Development Tools

- **Backend**: VS Code with Python extension, or PyCharm
- **Mobile**: VS Code with React Native extension, or Android Studio/Xcode
- **Database**: pgAdmin, DBeaver, or psql CLI
- **API Testing**: Postman, Insomnia, or curl

### External Service Accounts

1. **Google Gemini AI API** (FREE tier):
   - Sign up at [ai.google.dev](https://ai.google.dev/)
   - Create API key (free tier: 1,500 requests/day)
   - No billing required for free tier
   - Rate limits: 15 requests/minute, 1,500/day, 1M/month

**Note**: No cloud OCR service account needed - using open-source PaddleOCR

---

## Project Setup

### 1. Repository Structure

Create the following directory structure:

```bash
mkdir -p OptiMeal/{api,mobile,shared}
cd OptiMeal
git init
```

### 2. Backend Setup (Python/FastAPI)

#### Step 2.1: Create Virtual Environment

```bash
cd api
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 2.2: Install Dependencies

Create `api/requirements.txt`:

```
# Web framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1

# Validation
pydantic==2.5.0
pydantic-settings==2.1.0

# Auth
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# External APIs
google-generativeai==0.3.2

# OCR and Image Processing
paddleocr==2.7.0
opencv-python==4.8.1
mediapipe==0.10.8
Pillow==10.1.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Utilities
python-dotenv==1.0.0
```

Install:
```bash
pip install -r requirements.txt
```

#### Step 2.3: Database Setup

Create PostgreSQL database:

```bash
# Using psql
psql -U postgres
CREATE DATABASE optimeal_dev;
CREATE USER optimeal_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE optimeal_dev TO optimeal_user;
\q
```

Or using Docker:

```bash
docker run --name optimeal-postgres \
  -e POSTGRES_DB=optimeal_dev \
  -e POSTGRES_USER=optimeal_user \
  -e POSTGRES_PASSWORD=secure_password \
  -p 5432:5432 \
  -d postgres:15
```

#### Step 2.4: Environment Configuration

Create `api/.env`:

```env
# Database
DATABASE_URL=postgresql://optimeal_user:secure_password@localhost:5432/optimeal_dev

# JWT Secret (generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key-here

# Rate Limiting
MEAL_PLAN_USER_LIMIT_PER_WEEK=2
GEMINI_REQUESTS_PER_MINUTE=15  # Free tier limit
GEMINI_DAILY_LIMIT=1500  # Free tier limit
GEMINI_DAILY_ALERT_THRESHOLD=1200  # 80% of daily limit

# OCR Settings
OCR_CONFIDENCE_THRESHOLD=0.6  # Skip OCR if below this
PADDLEOCR_LANG=en  # Language for OCR

# Environment
ENVIRONMENT=development
```

#### Step 2.5: Initialize Database Migrations

```bash
cd api
alembic init alembic

# Edit alembic.ini - set:
# sqlalchemy.url = postgresql://optimeal_user:secure_password@localhost:5432/optimeal_dev

# Edit alembic/env.py - add:
from src.models import Base
target_metadata = Base.metadata

# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

#### Step 2.6: Project Structure

Create the backend structure from [plan.md](plan.md):

```bash
mkdir -p src/{models,schemas,services,api,db,utils}
touch src/__init__.py
touch src/models/__init__.py
touch src/schemas/__init__.py
touch src/services/__init__.py
touch src/api/__init__.py
touch src/db/__init__.py
touch src/utils/__init__.py
```

#### Step 2.7: Run Backend

Create `api/src/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OptiMeal API",
    description="Meal Management Feature",
    version="1.0.0"
)

# CORS for React Native development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "OptiMeal API - Meal Management Feature"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Import and include routers here (after implementation)
# from src.api import pantry, meals, plans, feedback, insights
# app.include_router(pantry.router, prefix="/v1/pantry", tags=["pantry"])
# ...
```

Run:
```bash
cd api
uvicorn src.main:app --reload --port 8000
```

Test: `curl http://localhost:8000/health`

---

### 3. Mobile Setup (React Native)

#### Step 3.1: Initialize React Native Project

```bash
cd mobile
npx react-native@latest init OptiMealMobile --template react-native-template-typescript
cd OptiMealMobile
```

#### Step 3.2: Install Dependencies

```bash
# Navigation
npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context
npm install react-native-gesture-handler react-native-reanimated

# UI Components
npm install react-native-paper

# Charts
npm install react-native-chart-kit react-native-svg

# Storage
npm install @react-native-async-storage/async-storage
npm install expo-sqlite

# Image Picker
npm install react-native-image-picker

# HTTP Client
npm install axios

# Dev Dependencies
npm install --save-dev @types/react @types/react-native jest @testing-library/react-native
```

#### Step 3.3: Project Structure

Reorganize `mobile/src/` to match [plan.md](plan.md):

```bash
mkdir -p src/{screens/{PantryScreen,MealLoggerScreen,PlannerScreen,InsightsScreen},components/{NutritionLabelInput,FoodItemCard,MealCard,charts},services,navigation,types}
```

#### Step 3.4: Configure API Client

Create `mobile/src/services/api.ts`:

```typescript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = __DEV__
  ? 'http://localhost:8000/v1'  // Development
  : 'https://api.optimeal.com/v1';  // Production

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await AsyncStorage.removeItem('access_token');
      // Navigate to login screen
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

#### Step 3.5: Run Mobile App

iOS:
```bash
cd mobile/OptiMealMobile
npx react-native run-ios
```

Android:
```bash
cd mobile/OptiMealMobile
npx react-native run-android
```

---

## Development Workflow

### Backend Development

1. **Create Models** (`api/src/models/`)
   - Define SQLAlchemy models for each entity (see [data-model.md](data-model.md))
   - Example: `models/user.py`, `models/food_item.py`, etc.

2. **Create Schemas** (`api/src/schemas/`)
   - Define Pydantic schemas for API validation (see [openapi.yaml](contracts/openapi.yaml))
   - Example: `schemas/food_item.py` with `FoodItemCreate`, `FoodItemUpdate`, `FoodItem`

3. **Implement Services** (`api/src/services/`)
   - Business logic layer
   - Example: `services/pantry_service.py` with CRUD operations

4. **Create API Routes** (`api/src/api/`)
   - FastAPI route handlers
   - Example: `api/pantry.py` with `@router.get("/")`, `@router.post("/")`, etc.

5. **Write Tests** (`api/tests/`)
   - Unit tests for services
   - Integration tests for API endpoints

### Mobile Development

1. **Create Screens** (`mobile/src/screens/`)
   - Main app screens matching user stories
   - Example: `PantryScreen/index.tsx`

2. **Build Components** (`mobile/src/components/`)
   - Reusable UI components
   - Example: `FoodItemCard/index.tsx`

3. **Implement Navigation** (`mobile/src/navigation/`)
   - React Navigation setup
   - Bottom tabs for main screens

4. **Write Tests** (`mobile/__tests__/`)
   - Component tests with Jest and React Testing Library

---

## Implementation Order

Follow this order to build incrementally:

### Phase 1: Authentication & Food Items (Days 1-5)
- [ ] Backend: User model, auth endpoints, JWT
- [ ] Backend: FoodItem model, CRUD endpoints
- [ ] Mobile: Login/Register screens
- [ ] Mobile: Food item creation with manual entry

### Phase 2: Pantry Management (Days 6-10)
- [ ] Backend: PantryItem model, CRUD endpoints
- [ ] Mobile: Pantry screen with list view
- [ ] Mobile: Add/edit/delete pantry items

### Phase 3: Meal Logging (Days 11-15)
- [ ] Backend: MealLog, LoggedItem models
- [ ] Backend: Pantry deduction logic
- [ ] Mobile: Meal logger screen
- [ ] Mobile: Meal history view

### Phase 4: Recipes (Days 16-18)
- [ ] Backend: Recipe, RecipeIngredient models
- [ ] Backend: "Save as Recipe" endpoint
- [ ] Mobile: Recipe list and selection

### Phase 5: Nutrition Label OCR (Days 19-22)
- [ ] Backend: Google Cloud Vision integration
- [ ] Backend: Image upload and parsing endpoint
- [ ] Mobile: Camera/gallery picker
- [ ] Mobile: Parsed data confirmation UI

### Phase 6: Meal Planning (Days 23-30)
- [ ] Backend: MealPlan, PlannedMeal, PlannedItem models
- [ ] Backend: OpenAI integration for plan generation
- [ ] Backend: Shopping list generation
- [ ] Mobile: Plan request screen
- [ ] Mobile: Plan display and shopping list

### Phase 7: Feedback (Days 31-33)
- [ ] Backend: Feedback model and endpoints
- [ ] Mobile: Rating prompts after meal logging
- [ ] Mobile: Plan modification feedback

### Phase 8: Insights (Days 34-40)
- [ ] Backend: Insight model and data aggregation
- [ ] Backend: Chart data endpoints
- [ ] Mobile: Insights screen with pre-built charts
- [ ] Mobile: Custom chart creation

### Phase 9: Testing & Polish (Days 41-45)
- [ ] Backend: Comprehensive test coverage
- [ ] Mobile: Component and integration tests
- [ ] Performance optimization
- [ ] Bug fixes

---

## Testing

### Backend Testing

Run all tests:
```bash
cd api
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

Test specific file:
```bash
pytest tests/unit/test_pantry_service.py
```

### Mobile Testing

Run tests:
```bash
cd mobile/OptiMealMobile
npm test
```

Run specific test:
```bash
npm test -- FoodItemCard
```

---

## API Documentation

Once the backend is running, view interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Common Commands

### Backend

```bash
# Activate virtual environment
cd api && source venv/bin/activate

# Run dev server with auto-reload
uvicorn src.main:app --reload --port 8000

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Run tests
pytest

# Format code
black src/
isort src/

# Type checking
mypy src/
```

### Mobile

```bash
# Start Metro bundler
npx react-native start

# Run on iOS
npx react-native run-ios

# Run on Android
npx react-native run-android

# Clear cache
npx react-native start --reset-cache

# Run tests
npm test

# Type checking
npx tsc --noEmit

# Lint
npm run lint
```

### Database

```bash
# Connect to database
psql -U optimeal_user -d optimeal_dev

# Backup database
pg_dump -U optimeal_user optimeal_dev > backup.sql

# Restore database
psql -U optimeal_user -d optimeal_dev < backup.sql

# Reset database (development only)
dropdb optimeal_dev && createdb optimeal_dev
alembic upgrade head
```

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'src'`
- **Solution**: Ensure you're in the `api/` directory and virtual environment is activated

**Problem**: Database connection error
- **Solution**: Check PostgreSQL is running: `pg_isready`, verify `.env` DATABASE_URL

**Problem**: Alembic migration fails
- **Solution**: Check for circular imports in models, ensure `Base.metadata` is set in `alembic/env.py`

### Mobile Issues

**Problem**: Metro bundler won't start
- **Solution**: `npx react-native start --reset-cache`, delete `node_modules` and reinstall

**Problem**: iOS build fails
- **Solution**: `cd ios && pod install`, clean build folder in Xcode

**Problem**: Android build fails
- **Solution**: `cd android && ./gradlew clean`, check Android SDK is installed

**Problem**: API requests fail with network error
- **Solution**: For iOS simulator use `http://localhost:8000`, for Android emulator use `http://10.0.2.2:8000`

---

## Next Steps

1. Review [data-model.md](data-model.md) for database schema details
2. Review [contracts/openapi.yaml](contracts/openapi.yaml) for API specifications
3. Follow the implementation order above
4. Reference [spec.md](spec.md) for acceptance criteria
5. When ready for task breakdown, run `/speckit.tasks`

---

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [React Navigation](https://reactnavigation.org/docs/getting-started)
- [Google Gemini AI Docs](https://ai.google.dev/docs)
- [PaddleOCR Docs](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/quickstart_en.md)
- [MediaPipe Docs](https://developers.google.com/mediapipe)

### Tutorials
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [React Native Tutorial](https://reactnative.dev/docs/tutorial)
- [Gemini API Quickstart](https://ai.google.dev/tutorials/python_quickstart)
- [PaddleOCR Python](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/quickstart_en.md)

### Tools
- [Postman Collection](https://www.postman.com/) - Import `contracts/openapi.yaml`
- [DB Diagram](https://dbdiagram.io/) - Visualize database schema
- [Figma](https://www.figma.com/) - UI/UX design (if applicable)

---

**Last Updated**: 2025-10-25
**Next Command**: `/speckit.tasks` to generate actionable task breakdown
