# Implementation Plan: Meal Management

**Branch**: `001-meal-management` | **Date**: 2025-10-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-meal-management/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature implements the foundational organizational tools for OptiMeal: pantry inventory management, meal logging with nutritional tracking, LLM-powered meal planning, user feedback collection, and nutritional insights visualization. This is the first feature (001) and serves as the MVP foundation before implementing the more advanced Economic Utility Model (EUM) optimization engine. The system will be built using React Native for cross-platform mobile apps, Python/FastAPI for the backend, and PostgreSQL for data storage.

## Technical Context

**Language/Version**: Python 3.11+ (backend), JavaScript/TypeScript with React Native (frontend)
**Primary Dependencies**: FastAPI (backend), React Native (mobile UI), SQLAlchemy (ORM), Google Gemini AI (LLM), PaddleOCR + MediaPipe (OCR/CV)
**Storage**: PostgreSQL (relational database for users, food items, meals, recipes, plans, feedback)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: iOS 15+ and Android 8+ (mobile apps), AWS cloud (backend hosting)
**Project Type**: Mobile + API (React Native frontend + Python backend)
**Performance Goals**:
  - Meal plan generation: <20 seconds (per spec SC-003) - Gemini 2.5 Flash typically <5s
  - API response time: <200ms p95 for CRUD operations
  - Nutrition label image parsing: <10 seconds (OCR + parsing)
  - Support 10,000 active users initially (Year 1 goal from business plan)
**Constraints**:
  - User-entry only for nutritional data (no external food database integration in MVP per FR-012)
  - LLM integration: Google Gemini 2.5 Flash free tier (1,500 requests/day limit)
  - Offline capability: Hybrid - meal logging works offline, planning requires internet
  - Image processing: Open-source stack (PaddleOCR, MediaPipe, OpenCV) - zero API costs
  - Cost optimization: FREE tier for both LLM and OCR to minimize MVP operating costs
**Scale/Scope**:
  - Initial target: 10,000 registered users, 40% MoM retention
  - Daily LLM usage: ~1,000 meal plans/day (well under 1,500 free tier limit)
  - Data volume: ~50-100 food items per user, ~3-10 meals/day logged
  - Core screens: Pantry, Meal Logger, Planner, Insights (~15-20 screens total)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Intuitive AI-Powered Frontend
**Status**: ✅ ALIGNED

- **Evidence**: Feature includes LLM-powered meal planning (FR-006, FR-007) to simplify user decision-making
- **Evidence**: Nutrition label image upload (FR-014) uses AI/CV to reduce manual data entry burden
- **Evidence**: Spec emphasizes intuitive UI with nutrition label-like input (FR-015) for familiarity
- **Assessment**: This feature leverages AI to abstract complexity from users, strongly aligned with the principle

### Principle II: Rigorous Mathematical & Economic Modeling
**Status**: ⚠️ PARTIAL ALIGNMENT (by design)

- **Evidence**: This is the MVP organizational layer, NOT the optimization engine
- **Evidence**: The EUM (Economic Utility Model) is planned for future phases
- **Evidence**: Current meal planning uses LLM suggestions, not mathematical optimization
- **Justification**: This is feature 001 - the foundation. Mathematical optimization requires this data infrastructure first. Future features will implement the rigorous EUM modeling referenced in the constitution and business plan.
- **Assessment**: Intentional deviation for MVP; mathematical rigor will be introduced in subsequent features

### Principle III: Modular & Composable Architecture
**Status**: ✅ ALIGNED

- **Evidence**: Clean separation of concerns: React Native frontend, Python/FastAPI backend, PostgreSQL storage
- **Evidence**: Mobile + API structure allows independent development and deployment
- **Evidence**: Feature design supports future integration of optimization engine as a separate module
- **Evidence**: User can toggle between simple LLM planning (this feature) and future optimized planning
- **Assessment**: Architecture is designed for modularity and component independence

**GATE DECISION**: ✅ PASS - Feature aligns with constitution. The partial alignment on Principle II is justified as this is the foundational MVP layer required before implementing the optimization engine.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
api/                              # Python FastAPI backend
├── src/
│   ├── models/                  # SQLAlchemy models (User, FoodItem, PantryItem, MealLog, Recipe, MealPlan, etc.)
│   ├── schemas/                 # Pydantic schemas for API request/response validation
│   ├── services/                # Business logic layer
│   │   ├── pantry_service.py   # Pantry CRUD operations
│   │   ├── meal_service.py     # Meal logging and recipe management
│   │   ├── planning_service.py # LLM integration for meal planning
│   │   ├── nutrition_service.py # Nutrition label OCR/parsing
│   │   └── insights_service.py # Data aggregation for visualizations
│   ├── api/                     # FastAPI route handlers
│   │   ├── pantry.py
│   │   ├── meals.py
│   │   ├── plans.py
│   │   ├── feedback.py
│   │   └── insights.py
│   ├── db/                      # Database configuration and migrations
│   └── utils/                   # Shared utilities (LLM client, image processing, etc.)
└── tests/
    ├── unit/                    # Unit tests for services
    ├── integration/             # API integration tests
    └── fixtures/                # Test data and fixtures

mobile/                          # React Native cross-platform app
├── src/
│   ├── screens/                 # Main app screens
│   │   ├── PantryScreen/
│   │   ├── MealLoggerScreen/
│   │   ├── PlannerScreen/
│   │   └── InsightsScreen/
│   ├── components/              # Reusable UI components
│   │   ├── NutritionLabelInput/
│   │   ├── FoodItemCard/
│   │   ├── MealCard/
│   │   └── charts/             # Chart components for insights
│   ├── services/                # API client, local storage
│   │   ├── api.ts              # API integration layer
│   │   └── storage.ts          # Local/offline storage
│   ├── navigation/              # React Navigation setup
│   └── types/                   # TypeScript type definitions
└── __tests__/                   # Jest tests for components and logic

shared/                          # Shared types/contracts (optional)
└── types/                       # TypeScript interfaces matching API schemas
```

**Structure Decision**: Mobile + API architecture selected based on React Native frontend + Python/FastAPI backend. The `api/` directory contains the Python backend with a clean layered architecture (models, schemas, services, routes). The `mobile/` directory contains the React Native cross-platform application organized by screens and reusable components. A `shared/` directory may be added for TypeScript type definitions that match the API contracts to ensure type safety across the stack.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No violations requiring justification. The partial alignment on Principle II (Mathematical Modeling) is intentional and documented in the Constitution Check section above.

---

## Post-Design Constitution Re-Evaluation

**Date**: 2025-10-25
**Status**: ✅ CONFIRMED ALIGNED

After completing Phase 0 (Research) and Phase 1 (Design), the implementation plan has been re-evaluated against the constitution:

### Principle I: Intuitive AI-Powered Frontend
**Status**: ✅ STRENGTHENED ALIGNMENT

- **Design Evidence**:
  - LLM integration via Google Gemini 2.5 Flash with structured JSON output ensures reliable meal plan generation
  - Open-source OCR stack (PaddleOCR + MediaPipe) for nutrition label parsing significantly reduces user data entry burden
  - React Native Paper provides Material Design components for familiar, intuitive UI
  - Offline-first meal logging removes connectivity friction (research.md decision)
  - API response times <200ms p95 ensures snappy user experience
  - Cost optimization (FREE LLM and OCR) enables sustainable AI features without budget constraints

- **Assessment**: Design decisions actively enhance AI-powered simplification of the user experience while maintaining zero API costs

### Principle II: Rigorous Mathematical & Economic Modeling
**Status**: ⚠️ PARTIAL ALIGNMENT (unchanged, as expected)

- **Design Evidence**:
  - This remains the foundational MVP layer without optimization
  - Database schema supports future integration of EUM parameters (e.g., user preferences, utility coefficients)
  - Data collection infrastructure (meal logs, feedback, costs) provides the dataset needed for future optimization
  - Modular architecture allows seamless addition of optimization engine

- **Assessment**: Design maintains clear path to future mathematical modeling while serving immediate organizational needs

### Principle III: Modular & Composable Architecture
**Status**: ✅ CONFIRMED ALIGNED

- **Design Evidence**:
  - Clean separation: Mobile (React Native) ↔ API (FastAPI) ↔ Database (PostgreSQL)
  - Service layer in backend isolates business logic from routes and models
  - External services (Gemini AI, PaddleOCR) accessed via utility modules for easy replacement
  - Open-source dependencies reduce vendor lock-in (can swap PaddleOCR ↔ Tesseract, Gemini ↔ other LLMs)
  - Offline storage (AsyncStorage + SQLite) separates mobile persistence from API calls
  - OpenAPI contract ensures frontend-backend independence
  - Project structure allows independent deployment and scaling of mobile vs backend

- **Assessment**: Architecture is highly modular with clear component boundaries, minimal coupling, and flexible dependency management

### Overall Gate Decision
**Status**: ✅ PASS - All constitutional principles are satisfied or intentionally deferred

**Complexity Score**: LOW
- Mobile + API is standard for React Native apps (not complex)
- Service layer follows established patterns (not complex)
- External API integrations are well-documented and standard (not complex)
- No custom optimization algorithms yet (waiting for EUM feature)

**Next Phase**: Ready to proceed to `/speckit.tasks` for implementation task breakdown
