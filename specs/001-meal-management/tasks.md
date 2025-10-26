# Tasks: Meal Management

**Feature**: 001-meal-management
**Input**: Design documents from `/specs/001-meal-management/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: This specification does NOT explicitly request tests, so test tasks are OMITTED per the template instructions.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md, this project uses:
- **Backend**: `api/src/` (Python/FastAPI)
- **Frontend**: `frontend/src/` (React with Vite/TypeScript)
- **Database**: PostgreSQL with Alembic migrations

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure with api/, frontend/, and shared/ directories
- [X] T002 [P] Initialize Python backend with FastAPI in api/src/main.py
- [X] T003 [P] Initialize React web app with Vite and TypeScript in frontend/ using npm create vite@latest
- [X] T004 [P] Create backend requirements.txt with FastAPI, SQLAlchemy, Alembic, psycopg2, google-generativeai, paddleocr, opencv-python, mediapipe dependencies
- [X] T005 [P] Create frontend package.json with React Router, Material-UI (MUI), axios, recharts, localforage dependencies
- [X] T006 [P] Configure Python code formatting (black, isort) and linting (ruff) in api/pyproject.toml
- [X] T007 [P] Configure TypeScript linting (ESLint) and formatting (Prettier) in frontend/.eslintrc.cjs
- [X] T008 Setup PostgreSQL database instance (Docker setup complete) (optimeal_dev) per quickstart.md
- [X] T009 Create backend environment configuration file api/.env with DATABASE_URL, SECRET_KEY, GEMINI_API_KEY placeholders
- [X] T010 [P] Create frontend environment configuration in frontend/.env with VITE_API_BASE_URL
- [X] T011 [P] Setup backend directory structure: api/src/{models,schemas,services,api,db,utils}/ with __init__.py files
- [X] T012 [P] Setup frontend directory structure: frontend/src/{pages,components,services,routes,types,theme}/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**STATUS**: ✅ **COMPLETE** (25/25 tasks done)
**DATE COMPLETED**: 2025-10-26

### Database & ORM Foundation

- [X] T013 Initialize Alembic migrations in api/alembic/ directory
- [X] T014 Create SQLAlchemy base configuration in api/src/db/base.py with Base, get_db session dependency
- [X] T015 Configure Alembic env.py to use Base.metadata for autogenerate support
- [X] T016 Create User model in api/src/models/user.py with id, email, password_hash, full_name, created_at, updated_at fields per data-model.md
- [X] T017 Create FoodItem model in api/src/models/food_item.py with all nutritional fields per data-model.md
- [X] T018 Generate initial Alembic migration for User and FoodItem models (COMPLETED via Docker)
- [X] T019 Apply Alembic migration to create users and food_items tables (COMPLETED via Docker)

### Authentication & Authorization

- [X] T020 Implement password hashing utilities in api/src/utils/security.py using passlib with bcrypt
- [X] T021 Implement JWT token generation and validation in api/src/utils/auth.py with python-jose
- [X] T022 Create authentication schemas in api/src/schemas/auth.py for UserCreate, UserLogin, Token
- [X] T023 Implement user registration endpoint POST /api/v1/auth/register in api/src/api/auth.py
- [X] T024 Implement user login endpoint POST /api/v1/auth/login in api/src/api/auth.py returning JWT
- [X] T025 Create authentication dependency get_current_user in api/src/api/dependencies.py for protected routes
- [X] T026 Include auth router in api/src/main.py with /api/v1/auth prefix

### API Infrastructure

- [X] T027 [P] Configure CORS middleware in api/src/main.py for React web development
- [X] T028 [P] Create global exception handlers in api/src/utils/exceptions.py for consistent error responses
- [X] T029 [P] Setup request logging middleware in api/src/utils/logging.py
- [X] T030 [P] Create Pydantic base schemas in api/src/schemas/base.py for common response patterns

### Frontend Infrastructure

- [X] T031 Create axios API client in frontend/src/services/api.ts with baseURL, timeout, auth interceptors
- [X] T032 Implement localStorage wrapper in frontend/src/services/storage.ts for token persistence
- [X] T033 Setup React Router in frontend/src/routes/AppRoutes.tsx with protected and public routes
- [X] T034 Create authentication context in frontend/src/contexts/AuthContext.tsx for login/logout state
- [X] T035 Implement Login page in frontend/src/pages/Auth/LoginPage.tsx with Material-UI form
- [X] T036 Implement Register page in frontend/src/pages/Auth/RegisterPage.tsx with Material-UI form
- [X] T037 Create main navigation layout in frontend/src/components/Layout/MainLayout.tsx with MUI Drawer for Pantry, Logger, Planner, Insights

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Pantry Inventory Management (Priority: P1) 🎯 MVP

**Goal**: Users can add, edit, and remove food items from their digital pantry with quantities and expiration dates

**Independent Test**: A user can successfully add a list of grocery items to their pantry, see the correct quantities, and then remove an item

**STATUS**: ✅ **COMPLETE** (28/28 tasks done - Backend + Frontend)
**DATE COMPLETED**: 2025-10-26

### Backend - Models & Database

- [X] T038 [P] [US1] Create PantryItem model in api/src/models/pantry_item.py with user_id, food_item_id, quantity, unit, expiration_date, location per data-model.md
- [X] T039 [US1] Generate Alembic migration for pantry_items table with foreign keys to users and food_items
- [X] T040 [US1] Apply migration to create pantry_items table with indexes on user_id and expiration_date

### Backend - Schemas

- [X] T041 [P] [US1] Create FoodItem schemas in api/src/schemas/food_item.py for FoodItemCreate, FoodItemUpdate, FoodItemResponse
- [X] T042 [P] [US1] Create PantryItem schemas in api/src/schemas/pantry_item.py for PantryItemCreate, PantryItemUpdate, PantryItemResponse with nested FoodItem

### Backend - Services

- [X] T043 [P] [US1] Implement FoodItemService in api/src/services/food_item_service.py with CRUD operations and user-scoped queries
- [X] T044 [US1] Implement PantryService in api/src/services/pantry_service.py with add_item, update_quantity, delete_item, get_pantry methods
- [X] T045 [US1] Add validation in PantryService to ensure quantity >= 0 and unit matches food_item.serving_unit

### Backend - API Endpoints

- [X] T046 [P] [US1] Implement POST /api/v1/food-items endpoint in api/src/api/food_items.py to create food item
- [X] T047 [P] [US1] Implement GET /api/v1/food-items endpoint in api/src/api/food_items.py to list user's food items
- [X] T048 [P] [US1] Implement PUT /api/v1/food-items/{id} endpoint in api/src/api/food_items.py to update food item
- [X] T049 [P] [US1] Implement DELETE /api/v1/food-items/{id} endpoint in api/src/api/food_items.py
- [X] T050 [P] [US1] Implement POST /api/v1/pantry endpoint in api/src/api/pantry.py to add pantry item
- [X] T051 [P] [US1] Implement GET /api/v1/pantry endpoint in api/src/api/pantry.py to get user's pantry with food details
- [X] T052 [P] [US1] Implement PATCH /api/v1/pantry/{id} endpoint in api/src/api/pantry.py to update quantity
- [X] T053 [P] [US1] Implement DELETE /api/v1/pantry/{id} endpoint in api/src/api/pantry.py
- [X] T054 [US1] Include food_items and pantry routers in api/src/main.py with /api/v1 prefix

### Frontend - Components

- [X] T055 [P] [US1] Create FoodItemCard component in frontend/src/components/FoodItemCard/index.tsx for displaying food with nutrition info using MUI Card
- [X] T056 [P] [US1] Create PantryItemCard component in frontend/src/components/PantryItemCard/index.tsx with quantity and expiration display using MUI Card
- [X] T057 [P] [US1] Create NutritionLabelInput component in frontend/src/components/NutritionLabelInput/index.tsx with label-style form fields using MUI TextField

### Frontend - API Integration

- [X] T058 [P] [US1] Create food items API client methods in frontend/src/services/api/foodItems.ts for create, list, update, delete
- [X] T059 [P] [US1] Create pantry API client methods in frontend/src/services/api/pantry.ts for add, list, update, delete

### Frontend - Pages

- [X] T060 [US1] Implement PantryPage in frontend/src/pages/Pantry/PantryPage.tsx with MUI Grid/List of pantry items
- [X] T061 [US1] Implement AddFoodItemPage in frontend/src/pages/Pantry/AddFoodItemPage.tsx with NutritionLabelInput form
- [X] T062 [US1] Implement AddToPantryPage in frontend/src/pages/Pantry/AddToPantryPage.tsx to select food and set quantity
- [X] T063 [US1] Implement EditPantryItemPage in frontend/src/pages/Pantry/EditPantryItemPage.tsx to update quantity/expiration
- [X] T064 [US1] Add routes from PantryPage to Add/Edit pages in frontend/src/routes/AppRoutes.tsx
- [X] T065 [US1] Implement delete pantry item functionality with MUI confirmation dialog in PantryPage

**Checkpoint**: User Story 1 complete - users can manage pantry inventory independently

---

## Phase 4: User Story 2 - Meal Logging & Nutrient Tracking (Priority: P1)

**Goal**: Users can log meals to track nutrition and costs, with automatic pantry deduction and recipe saving

**Independent Test**: A user can log a breakfast consisting of two eggs and a slice of toast, see the correct total calories and macros, and see their pantry's egg and bread count decrease

### Backend - Models & Database

- [ ] T066 [P] [US2] Create MealLog model in api/src/models/meal_log.py with user_id, meal_name, meal_type, logged_at, notes per data-model.md
- [ ] T067 [P] [US2] Create LoggedItem model in api/src/models/logged_item.py with meal_log_id, food_item_id, servings
- [ ] T068 [P] [US2] Create Recipe model in api/src/models/recipe.py with user_id, name, description, created_from_meal_log_id
- [ ] T069 [P] [US2] Create RecipeIngredient model in api/src/models/recipe_ingredient.py with recipe_id, food_item_id, servings
- [ ] T070 [US2] Generate Alembic migration for meal_logs, logged_items, recipes, recipe_ingredients tables
- [ ] T071 [US2] Apply migration to create meal logging tables with appropriate indexes and cascade deletes

### Backend - Schemas

- [ ] T072 [P] [US2] Create MealLog schemas in api/src/schemas/meal_log.py for MealLogCreate, MealLogResponse with computed nutrition totals
- [ ] T073 [P] [US2] Create LoggedItem schemas in api/src/schemas/logged_item.py for LoggedItemCreate with servings validation
- [ ] T074 [P] [US2] Create Recipe schemas in api/src/schemas/recipe.py for RecipeCreate, RecipeResponse with ingredients list

### Backend - Services

- [ ] T075 [US2] Implement MealLogService in api/src/services/meal_log_service.py with create_meal_log method including transaction for logged items
- [ ] T076 [US2] Implement pantry deduction logic in MealLogService.create_meal_log to decrement PantryItem.quantity for each LoggedItem
- [ ] T077 [US2] Add pantry overflow handling in MealLogService to set quantity to 0 and return warning when servings > available
- [ ] T078 [US2] Implement nutrition aggregation in MealLogService.get_meal_log to sum calories, protein, carbs, fat from all logged items
- [ ] T079 [P] [US2] Implement RecipeService in api/src/services/recipe_service.py with create_from_meal_log method to copy logged items
- [ ] T080 [P] [US2] Implement RecipeService.list_recipes and get_recipe_details with ingredient details

### Backend - API Endpoints

- [ ] T081 [P] [US2] Implement POST /api/v1/meals endpoint in api/src/api/meals.py to create meal log with items array
- [ ] T082 [P] [US2] Implement GET /api/v1/meals endpoint in api/src/api/meals.py to list user's meal history with date filtering
- [ ] T083 [P] [US2] Implement GET /api/v1/meals/{id} endpoint in api/src/api/meals.py to get meal details with nutrition totals
- [ ] T084 [P] [US2] Implement POST /api/v1/recipes endpoint in api/src/api/recipes.py to save meal as recipe
- [ ] T085 [P] [US2] Implement GET /api/v1/recipes endpoint in api/src/api/recipes.py to list user's saved recipes
- [ ] T086 [P] [US2] Implement GET /api/v1/recipes/{id} endpoint in api/src/api/recipes.py to get recipe with ingredients
- [ ] T087 [US2] Include meals and recipes routers in api/src/main.py

### Backend - OCR Integration

- [ ] T088 [US2] Install PaddleOCR, MediaPipe, OpenCV dependencies in api/requirements.txt per research.md
- [ ] T089 [US2] Implement image preprocessing utilities in api/src/utils/image_processing.py using MediaPipe for orientation and OpenCV for enhancement
- [ ] T090 [US2] Implement nutrition label OCR service in api/src/services/nutrition_ocr_service.py using PaddleOCR for text extraction
- [ ] T091 [US2] Implement nutrition label parsing logic in api/src/services/nutrition_ocr_service.py with regex patterns for calories, protein, carbs, fat fields
- [ ] T092 [US2] Add confidence scoring to OCR service and return parsed fields with confidence values
- [ ] T093 [US2] Implement POST /api/v1/food-items/parse-label endpoint in api/src/api/food_items.py to accept image upload and return parsed nutrition data

### Frontend - Components

- [ ] T094 [P] [US2] Create MealCard component in frontend/src/components/MealCard/index.tsx to display meal with nutrition summary using MUI Card
- [ ] T095 [P] [US2] Create FoodItemSelector component in frontend/src/components/FoodItemSelector/index.tsx with MUI Autocomplete for search and quantity input
- [ ] T096 [P] [US2] Create RecipeCard component in frontend/src/components/RecipeCard/index.tsx for recipe selection using MUI Card
- [ ] T097 [US2] Create ImageUploadButton component in frontend/src/components/ImageUploadButton/index.tsx using HTML file input with drag-and-drop

### Frontend - API Integration

- [ ] T098 [P] [US2] Create meals API client methods in frontend/src/services/api/meals.ts for create, list, get
- [ ] T099 [P] [US2] Create recipes API client methods in frontend/src/services/api/recipes.ts for create, list, get
- [ ] T100 [US2] Create OCR API client method in frontend/src/services/api/foodItems.ts for uploadNutritionLabel

### Frontend - Pages

- [ ] T101 [US2] Implement MealLoggerPage in frontend/src/pages/MealLogger/MealLoggerPage.tsx with meal history list using MUI Table/Cards
- [ ] T102 [US2] Implement CreateMealPage in frontend/src/pages/MealLogger/CreateMealPage.tsx with FoodItemSelector for adding items
- [ ] T103 [US2] Add meal type select (breakfast/lunch/dinner/snack) and date/time picker to CreateMealPage using MUI components
- [ ] T104 [US2] Display real-time nutrition totals (calories, protein, carbs, fat) as items are added in CreateMealPage
- [ ] T105 [US2] Add Save as Recipe button to MealLoggerPage after meal is logged
- [ ] T106 [US2] Implement file upload with preview in AddFoodItemPage for nutrition label upload
- [ ] T107 [US2] Display parsed OCR results in NutritionLabelInput with editable fields for user confirmation
- [ ] T108 [US2] Add recipe selection option in CreateMealPage to log entire recipe as single item
- [ ] T109 [US2] Display pantry warnings with MUI Alert when logged quantity exceeds available inventory

**Checkpoint**: User Story 2 complete - users can log meals, track nutrition, save recipes, and use OCR independently

---

## Phase 5: User Story 3 - LLM-Powered Meal Planning (Priority: P2)

**Goal**: Users can generate meal plans for specific periods using their pantry and recipes, with automatic shopping list generation

**Independent Test**: A user with chicken and rice in their pantry can request a 3-day dinner plan and receive a plan that includes a chicken and rice dish, plus a shopping list for the other two meals

### Backend - Models & Database

- [ ] T110 [P] [US3] Create MealPlan model in api/src/models/meal_plan.py with user_id, name, start_date, end_date
- [ ] T111 [P] [US3] Create PlannedMeal model in api/src/models/planned_meal.py with meal_plan_id, date, meal_type, recipe_id, notes
- [ ] T112 [P] [US3] Create PlannedItem model in api/src/models/planned_item.py with planned_meal_id, food_item_id, servings
- [ ] T113 [P] [US3] Create ShoppingListItem model in api/src/models/shopping_list_item.py with meal_plan_id, food_item_id, quantity_needed, is_purchased
- [ ] T114 [US3] Generate Alembic migration for meal_plans, planned_meals, planned_items, shopping_list_items tables
- [ ] T115 [US3] Apply migration with unique constraints on planned_meals (meal_plan_id, date, meal_type) per data-model.md

### Backend - Schemas

- [ ] T116 [P] [US3] Create MealPlan schemas in api/src/schemas/meal_plan.py for MealPlanCreate, MealPlanResponse with planned meals
- [ ] T117 [P] [US3] Create PlannedMeal schemas in api/src/schemas/planned_meal.py for PlannedMealResponse with items or recipe
- [ ] T118 [P] [US3] Create ShoppingListItem schemas in api/src/schemas/shopping_list.py for ShoppingListItemResponse
- [ ] T119 [US3] Create MealPlanGenerateRequest schema in api/src/schemas/meal_plan.py with start_date, end_date, meal_types array, dietary_preferences

### Backend - LLM Integration

- [ ] T120 [US3] Install google-generativeai package in api/requirements.txt per research.md
- [ ] T121 [US3] Create Gemini API client wrapper in api/src/utils/gemini_client.py with API key configuration and error handling
- [ ] T122 [US3] Implement rate limiting decorator in api/src/utils/rate_limit.py for user-level (2 plans/week) and system-level (15 req/min) limits per research.md
- [ ] T123 [US3] Create meal plan prompt builder in api/src/services/planning_service.py to format pantry inventory, recipes, and user constraints for Gemini
- [ ] T124 [US3] Define MealPlanSchema for Gemini structured JSON output with days, meals, ingredients arrays
- [ ] T125 [US3] Implement generate_meal_plan method in planning_service.py to call Gemini 2.5 Flash with JSON mode and response_schema
- [ ] T126 [US3] Add retry logic with exponential backoff for Gemini rate limit errors (429) using tenacity library
- [ ] T127 [US3] Parse Gemini JSON response and create MealPlan, PlannedMeal, PlannedItem database records in transaction

### Backend - Shopping List Logic

- [ ] T128 [US3] Implement shopping list generation in api/src/services/shopping_service.py to calculate total servings needed per food item
- [ ] T129 [US3] Implement pantry availability check in shopping_service.py to compare needed vs available quantities
- [ ] T130 [US3] Create ShoppingListItem records for items where (total_needed - pantry_available) > 0
- [ ] T131 [US3] Add shopping list regeneration when MealPlan or PantryItems are updated

### Backend - API Endpoints

- [ ] T132 [P] [US3] Implement POST /api/v1/plans/generate endpoint in api/src/api/plans.py with rate limit decorator to generate meal plan
- [ ] T133 [P] [US3] Implement GET /api/v1/plans endpoint in api/src/api/plans.py to list user's meal plans
- [ ] T134 [P] [US3] Implement GET /api/v1/plans/{id} endpoint in api/src/api/plans.py to get plan details with all planned meals
- [ ] T135 [P] [US3] Implement GET /api/v1/plans/{id}/shopping-list endpoint in api/src/api/plans.py to get shopping list items
- [ ] T136 [P] [US3] Implement PATCH /api/v1/plans/{id}/shopping-list/{item_id} endpoint in api/src/api/plans.py to mark item as purchased
- [ ] T137 [P] [US3] Implement DELETE /api/v1/plans/{id}/meals/{meal_id} endpoint in api/src/api/plans.py to remove planned meal
- [ ] T138 [US3] Include plans router in api/src/main.py

### Frontend - Components

- [ ] T139 [P] [US3] Create PlannedMealCard component in frontend/src/components/PlannedMealCard/index.tsx for calendar-style meal display using MUI Card
- [ ] T140 [P] [US3] Create ShoppingListItem component in frontend/src/components/ShoppingListItem/index.tsx with MUI Checkbox for is_purchased
- [ ] T141 [US3] Create DateRangePicker component in frontend/src/components/DateRangePicker/index.tsx for plan start/end selection using MUI DatePicker

### Frontend - API Integration

- [ ] T142 [P] [US3] Create plans API client methods in frontend/src/services/api/plans.ts for generate, list, get, getShoppingList
- [ ] T143 [US3] Add shopping list update method in plans API client for marking items purchased

### Frontend - Pages

- [ ] T144 [US3] Implement PlannerPage in frontend/src/pages/Planner/PlannerPage.tsx with plan list and Create Plan button
- [ ] T145 [US3] Implement CreatePlanPage in frontend/src/pages/Planner/CreatePlanPage.tsx with DateRangePicker and meal type checkboxes
- [ ] T146 [US3] Add dietary preferences input (vegetarian, vegan, gluten-free, etc.) to CreatePlanPage using MUI Select/Chips
- [ ] T147 [US3] Display MUI CircularProgress with percentage during plan generation (up to 20 seconds) in CreatePlanPage
- [ ] T148 [US3] Implement PlanDetailsPage in frontend/src/pages/Planner/PlanDetailsPage.tsx with calendar view of planned meals
- [ ] T149 [US3] Add shopping list tab to PlanDetailsPage with checkboxes for purchased items using MUI Tabs
- [ ] T150 [US3] Implement edit/delete planned meal functionality in PlanDetailsPage with MUI Dialog
- [ ] T151 [US3] Display rate limit warnings with MUI Snackbar when user reaches weekly plan limit (2 plans/week)

**Checkpoint**: User Story 3 complete - users can generate AI meal plans and shopping lists independently

---

## Phase 6: User Story 4 - User Feedback Collection (Priority: P2)

**Goal**: Users can rate meals and provide feedback on plan modifications for future personalization

**Independent Test**: After logging a meal, a user is presented with a rating prompt, and their rating is successfully saved

### Backend - Models & Database

- [ ] T152 [US4] Create Feedback model in api/src/models/feedback.py with user_id, feedback_type, meal_log_id, meal_plan_id, rating, comment per data-model.md
- [ ] T153 [US4] Generate Alembic migration for feedback table with CHECK constraints for rating (1-5) and feedback_type enum
- [ ] T154 [US4] Apply migration with unique index on meal_log_id to ensure one feedback per meal

### Backend - Schemas

- [ ] T155 [P] [US4] Create Feedback schemas in api/src/schemas/feedback.py for FeedbackCreate, FeedbackResponse
- [ ] T156 [US4] Add validation in FeedbackCreate to require meal_log_id if feedback_type is meal_rating

### Backend - Services

- [ ] T157 [US4] Implement FeedbackService in api/src/services/feedback_service.py with create_meal_rating and create_plan_feedback methods
- [ ] T158 [US4] Add validation in FeedbackService to ensure rating is 1-5 for meal_rating type
- [ ] T159 [US4] Implement get_user_feedback_history in FeedbackService for future analytics

### Backend - API Endpoints

- [ ] T160 [P] [US4] Implement POST /api/v1/feedback endpoint in api/src/api/feedback.py to create meal rating or plan feedback
- [ ] T161 [P] [US4] Implement GET /api/v1/feedback endpoint in api/src/api/feedback.py to list user's feedback history
- [ ] T162 [US4] Include feedback router in api/src/main.py

### Frontend - Components

- [ ] T163 [US4] Create MealRatingDialog component in frontend/src/components/MealRatingDialog/index.tsx with MUI Rating (1-5 stars) and skip option
- [ ] T164 [US4] Create PlanFeedbackDialog component in frontend/src/components/PlanFeedbackDialog/index.tsx with MUI TextField for qualitative feedback

### Frontend - API Integration

- [ ] T165 [US4] Create feedback API client methods in frontend/src/services/api/feedback.ts for submitMealRating and submitPlanFeedback

### Frontend - Integration

- [ ] T166 [US4] Add MealRatingDialog prompt after meal is successfully logged in CreateMealPage
- [ ] T167 [US4] Add PlanFeedbackDialog prompt when user deletes or modifies a planned meal in PlanDetailsPage
- [ ] T168 [US4] Make feedback prompts optional with Skip button to respect user choice

**Checkpoint**: User Story 4 complete - users can provide feedback on meals and plans independently

---

## Phase 7: User Story 5 - Nutritional Insights (Priority: P3)

**Goal**: Users can view pre-built and custom visualizations of their eating habits over time

**Independent Test**: A user who has logged meals for a week can view a line chart of their daily calorie intake and a pie chart showing their average macronutrient breakdown

### Backend - Models & Database

- [ ] T169 [US5] Create Insight model in api/src/models/insight.py with user_id, name, chart_type, metric, aggregation, time_range per data-model.md
- [ ] T170 [US5] Generate Alembic migration for insights table with CHECK constraints for chart_type, aggregation, time_range enums
- [ ] T171 [US5] Apply migration to create insights table

### Backend - Services

- [ ] T172 [US5] Implement InsightsService in api/src/services/insights_service.py with data aggregation queries on MealLog and LoggedItem
- [ ] T173 [US5] Implement get_daily_calories method in InsightsService to sum calories grouped by date for time range
- [ ] T174 [US5] Implement get_macro_breakdown method in InsightsService to calculate percentage of calories from protein, carbs, fat
- [ ] T175 [US5] Implement get_cost_trend method in InsightsService to sum meal costs over time
- [ ] T176 [US5] Implement get_nutrient_trend method in InsightsService with generic metric parameter (sodium, sugar, fiber, etc.)
- [ ] T177 [US5] Add time_range filtering (7_days, 30_days, 90_days, all_time) to all insight queries
- [ ] T178 [US5] Implement create_custom_insight in InsightsService to save user-defined chart configurations

### Backend - Schemas

- [ ] T179 [P] [US5] Create Insight schemas in api/src/schemas/insight.py for InsightCreate, InsightResponse
- [ ] T180 [P] [US5] Create chart data response schemas in api/src/schemas/insight.py for LineChartData, PieChartData, BarChartData
- [ ] T181 [US5] Add validation for metric field to ensure it matches valid nutritional fields or cost

### Backend - API Endpoints

- [ ] T182 [P] [US5] Implement GET /api/v1/insights/calories endpoint in api/src/api/insights.py to get daily calorie trend
- [ ] T183 [P] [US5] Implement GET /api/v1/insights/macros endpoint in api/src/api/insights.py to get macro breakdown pie chart data
- [ ] T184 [P] [US5] Implement GET /api/v1/insights/cost endpoint in api/src/api/insights.py to get cost trend
- [ ] T185 [P] [US5] Implement GET /api/v1/insights/nutrient endpoint in api/src/api/insights.py with query param for metric name
- [ ] T186 [P] [US5] Implement POST /api/v1/insights endpoint in api/src/api/insights.py to create custom insight
- [ ] T187 [P] [US5] Implement GET /api/v1/insights endpoint in api/src/api/insights.py to list user's saved insights
- [ ] T188 [P] [US5] Implement DELETE /api/v1/insights/{id} endpoint in api/src/api/insights.py
- [ ] T189 [US5] Include insights router in api/src/main.py

### Frontend - Components

- [ ] T190 [P] [US5] Create LineChart wrapper component in frontend/src/components/charts/LineChart.tsx using Recharts LineChart
- [ ] T191 [P] [US5] Create PieChart wrapper component in frontend/src/components/charts/PieChart.tsx using Recharts PieChart
- [ ] T192 [P] [US5] Create BarChart wrapper component in frontend/src/components/charts/BarChart.tsx using Recharts BarChart
- [ ] T193 [US5] Create InsightCard component in frontend/src/components/InsightCard/index.tsx to display saved insights with chart preview using MUI Card

### Frontend - API Integration

- [ ] T194 [P] [US5] Create insights API client methods in frontend/src/services/api/insights.ts for getCalories, getMacros, getCost, getNutrient
- [ ] T195 [US5] Add custom insight methods in insights API client for create, list, delete

### Frontend - Pages

- [ ] T196 [US5] Implement InsightsPage in frontend/src/pages/Insights/InsightsPage.tsx with MUI Tabs for pre-built and custom insights
- [ ] T197 [US5] Add Calories tab to InsightsPage displaying LineChart of daily calorie intake for last 7 days
- [ ] T198 [US5] Add Macros tab to InsightsPage displaying PieChart of protein/carbs/fat percentages
- [ ] T199 [US5] Add Cost tab to InsightsPage displaying LineChart of daily spending
- [ ] T200 [US5] Implement CreateInsightPage in frontend/src/pages/Insights/CreateInsightPage.tsx with metric, chart type, and time range selectors using MUI components
- [ ] T201 [US5] Display custom insights in Custom tab with delete option
- [ ] T202 [US5] Add time range selector (7 days, 30 days, 90 days, all time) to all insight views using MUI ToggleButtonGroup
- [ ] T203 [US5] Handle empty state when user has no meal logs with helpful message to start logging using MUI Box with centered text

**Checkpoint**: User Story 5 complete - users can visualize their nutritional data independently

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T204 [P] Add input validation error messages with MUI FormHelperText across all forms
- [ ] T205 [P] Implement loading states with MUI Skeleton and CircularProgress for all API calls
- [ ] T206 [P] Add responsive design breakpoints for mobile, tablet, and desktop views
- [ ] T207 [P] Implement error handling with user-friendly messages using MUI Snackbar for all API failures
- [ ] T208 [P] Add empty states with helpful prompts for empty pantry, no meals, no plans using MUI Box
- [ ] T209 [P] Optimize database queries with proper indexing based on usage patterns
- [ ] T210 [P] Add browser localStorage caching for frequently accessed data (pantry, food items)
- [ ] T211 [P] Implement Progressive Web App (PWA) support with service worker for offline access
- [ ] T212 [P] Implement data pagination for meal history and plan lists (20 items per page) using MUI Pagination
- [ ] T213 [P] Add search functionality to food items and recipes lists with debounced search
- [ ] T214 [P] Implement expiration date warnings in pantry (items expiring within 3 days highlighted with MUI Chip)
- [ ] T215 Run quickstart.md setup validation on fresh environment
- [ ] T216 Create API documentation with OpenAPI/Swagger at /api/docs
- [ ] T217 [P] Add automated database backup script for PostgreSQL
- [ ] T218 [P] Configure production environment variables and deployment settings for frontend (Vite build) and backend
- [ ] T219 Performance optimization: Ensure meal plan generation completes in <20 seconds (SC-003)
- [ ] T220 Performance optimization: Ensure API response time <200ms p95 for CRUD operations
- [ ] T221 [P] Add monitoring and alerting for Gemini API usage (alert at 80% of 1,500 daily limit)
- [ ] T222 Security audit: Ensure all endpoints require authentication except /auth/register and /auth/login
- [ ] T223 Security audit: Validate all user input with Pydantic schemas and prevent SQL injection
- [ ] T224 Accessibility: Add ARIA labels and keyboard navigation to all frontend components
- [ ] T225 [P] Code cleanup: Remove unused imports and dead code across backend and frontend
- [ ] T226 [P] Code cleanup: Ensure consistent code formatting with black and prettier
- [ ] T227 [P] Add MUI theme customization in frontend/src/theme/theme.ts with OptiMeal branding colors
- [ ] T228 [P] Implement responsive mobile navigation with MUI AppBar and Drawer

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Setup (Phase 1)**: No dependencies - can start immediately
2. **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
3. **User Story 1 - Pantry (Phase 3)**: Depends on Foundational completion
4. **User Story 2 - Meal Logging (Phase 4)**: Depends on Foundational + User Story 1 (needs FoodItem and PantryItem models)
5. **User Story 3 - Meal Planning (Phase 5)**: Depends on Foundational + User Story 1 + User Story 2 (needs pantry and recipes)
6. **User Story 4 - Feedback (Phase 6)**: Depends on Foundational + User Story 2 + User Story 3 (needs MealLog and MealPlan)
7. **User Story 5 - Insights (Phase 7)**: Depends on Foundational + User Story 2 (needs MealLog data)
8. **Polish (Phase 8)**: Depends on desired user stories being complete

### User Story Dependencies

**Critical Path**:
- Foundational (Phase 2) → User Story 1 → User Story 2 → User Story 3 → User Story 4
- User Story 5 can run in parallel after User Story 2

**Parallel Opportunities**:
- After User Story 2 completes: User Story 3, User Story 4, and User Story 5 can all proceed in parallel
- User Story 4 (Feedback) is lightweight and can be implemented quickly
- User Story 5 (Insights) is independent once meal logging exists

### Within Each User Story

1. Models → Database migration → Apply migration (sequential)
2. Schemas can be parallel with services
3. Services before API endpoints
4. Mobile components can be parallel with backend API
5. Mobile screens depend on components and API client methods

### Task-Level Dependencies

**User Story 1 (Pantry)**:
- T038-T040 (models/migrations) must complete before T044 (service)
- T041-T042 (schemas) can run parallel
- T046-T053 (API endpoints) depend on T044 (service)
- T055-T057 (components) can run parallel with backend
- T058-T059 (API client) can start once endpoints exist
- T060-T065 (screens) depend on components and API client

**User Story 2 (Meal Logging)**:
- T066-T071 (models/migrations) must complete first
- T072-T074 (schemas) parallel
- T075-T078 (meal service) depend on models
- T079-T080 (recipe service) parallel with meal service
- T088-T093 (OCR) can run parallel with meal logging implementation
- Mobile components (T094-T097) can run parallel with backend

**User Story 3 (Meal Planning)**:
- T110-T115 (models/migrations) must complete first
- T120-T127 (LLM integration) can run parallel with database setup
- T128-T131 (shopping list) depends on models
- API endpoints (T132-T138) depend on services

### Parallel Execution Examples

**Phase 1 (Setup) - All parallel**:
```
T002, T003, T004, T005, T006, T007, T010, T011, T012 can all run in parallel
```

**Phase 2 (Foundational) - Parallel groups**:
```
Group 1 (parallel): T013, T014, T015, T020, T021, T027, T028, T029, T030
Group 2 (after models): T016, T017 parallel, then T018, then T019
Group 3 (after auth): T022, T023, T024, T025, T026 sequential
Group 4 (mobile): T031, T032, T033, T034, T035, T036, T037 some parallel
```

**User Story 1 - Parallel opportunities**:
```
Backend schemas: T041, T042 parallel
Backend services: T043, T044 (T044 after T043)
API endpoints: T046-T053 all parallel (after services done)
Mobile components: T055, T056, T057 parallel
Mobile API: T058, T059 parallel
```

**User Story 2 - Parallel opportunities**:
```
Models: T066, T067, T068, T069 parallel
Schemas: T072, T073, T074 parallel
Services: T079, T080 parallel (meal service T075-T078 sequential)
OCR backend: T088-T093 parallel track
Mobile components: T094-T097 parallel
API clients: T098, T099, T100 parallel
```

---

## Implementation Strategy

### MVP First (Recommended for Initial Release)

**Suggested MVP Scope**: User Story 1 (Pantry) + User Story 2 (Meal Logging) = Core value

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (auth, database, API infrastructure)
3. Complete Phase 3: User Story 1 (Pantry Management)
   - **STOP and VALIDATE**: Test pantry CRUD independently
4. Complete Phase 4: User Story 2 (Meal Logging with OCR)
   - **STOP and VALIDATE**: Test meal logging, nutrition tracking, recipe saving
5. **MVP COMPLETE**: Users can manage pantry and log meals with full nutrition tracking
6. Deploy MVP and gather user feedback

### Incremental Delivery (Recommended for Feature Rollout)

**Phase 1+2 (Foundation)**: ~7-10 days
- T001-T037: Complete foundational infrastructure
- Deliverable: Working auth, database, mobile app shell

**+ User Story 1 (Pantry)**: +5-7 days (Total: ~15 days)
- T038-T065: Pantry management
- Deliverable: Users can manage digital pantry inventory
- **Deploy and demo**

**+ User Story 2 (Meal Logging)**: +8-10 days (Total: ~25 days)
- T066-T109: Meal logging with OCR
- Deliverable: Full nutrition tracking, OCR label parsing, recipe saving
- **Deploy and demo - this is the recommended MVP**

**+ User Story 3 (Meal Planning)**: +7-9 days (Total: ~33 days)
- T110-T151: AI meal planning and shopping lists
- Deliverable: LLM-powered meal plans
- **Deploy and demo**

**+ User Story 4 (Feedback)**: +3-4 days (Total: ~37 days)
- T152-T168: Feedback collection
- Deliverable: User feedback for personalization
- **Deploy and demo**

**+ User Story 5 (Insights)**: +5-7 days (Total: ~43 days)
- T169-T203: Nutritional insights and charts
- Deliverable: Data visualizations
- **Deploy and demo**

**+ Polish**: +3-5 days (Total: ~48 days)
- T204-T226: Performance, security, UX improvements
- **Production-ready release**

### Parallel Team Strategy

With 3 developers after Foundation completes:

**Scenario 1: Maximize speed**
- Developer A: User Story 1 + User Story 4 (lightweight)
- Developer B: User Story 2 (complex OCR work)
- Developer C: User Story 3 (complex LLM work)
- All converge on User Story 5 or split Polish tasks

**Scenario 2: Balanced workload**
- Developer A: User Story 1 → User Story 4
- Developer B: User Story 2 → User Story 5
- Developer C: User Story 3 → Polish

---

## Summary

### Total Task Count: 228 tasks

**By Phase**:
- Phase 1 (Setup): 12 tasks
- Phase 2 (Foundational): 25 tasks
- Phase 3 (User Story 1 - Pantry): 28 tasks
- Phase 4 (User Story 2 - Meal Logging): 44 tasks
- Phase 5 (User Story 3 - Meal Planning): 42 tasks
- Phase 6 (User Story 4 - Feedback): 17 tasks
- Phase 7 (User Story 5 - Insights): 35 tasks
- Phase 8 (Polish): 25 tasks

**By User Story**:
- User Story 1 (P1 - Pantry): 28 tasks
- User Story 2 (P1 - Meal Logging): 44 tasks
- User Story 3 (P2 - Meal Planning): 42 tasks
- User Story 4 (P2 - Feedback): 17 tasks
- User Story 5 (P3 - Insights): 35 tasks

**Parallel Opportunities**: 94 tasks marked [P] can run in parallel with their phase group

**Independent Test Criteria**:
- US1: Add 10 items to pantry, verify quantities, delete one item
- US2: Log meal with 2 items, see nutrition totals, verify pantry deduction
- US3: Request 3-day plan, see pantry items used, get shopping list
- US4: Log meal, receive rating prompt, submit rating successfully
- US5: View calorie chart for 7 days, view macro pie chart

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 + Phase 4 (User Stories 1 & 2)
- Total MVP tasks: ~109 tasks
- Estimated timeline: 20-25 days (solo developer) or 12-15 days (2 developers)
- Core value: Digital pantry + meal logging with nutrition tracking + OCR

**Format Validation**: ✅ All tasks follow checklist format with Task ID, [P] marker where applicable, [Story] label for user story phases, and file paths in descriptions

---

## Notes

- **Architecture Change**: Updated from React Native mobile app to React web app with Vite + Material-UI to avoid app store fees
- Tasks marked [P] can run in parallel within their phase (different files, no dependencies)
- [US1], [US2], [US3], [US4], [US5] labels map tasks to user stories from spec.md
- Each user story is independently completable and testable after Foundational phase
- No test tasks included as tests were not explicitly requested in spec.md
- Commit frequently after completing tasks or logical groups
- Validate each user story checkpoint before proceeding to next
- **Frontend Stack**: React + TypeScript + Vite + Material-UI (MUI) + Recharts for charting
- **Responsive Design**: Mobile-first responsive web app works on all devices
- **PWA Support**: Progressive Web App (Task T211) enables offline access and installability
- OCR uses open-source PaddleOCR (zero cost) per research.md decision
- LLM uses Google Gemini 2.5 Flash FREE tier (1,500 req/day) per research.md decision
