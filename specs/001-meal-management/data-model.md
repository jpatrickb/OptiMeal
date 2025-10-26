# Data Model: Meal Management Feature

**Feature**: 001-meal-management
**Date**: 2025-10-25
**Purpose**: Define database schema, entities, and relationships for the meal management system

---

## Entity-Relationship Overview

```
User (1) ──────< (M) PantryItem (M) >────── (1) FoodItem
  │                                              │
  │                                              │
  ├────< (M) MealLog                             │
  │           │                                  │
  │           └────< (M) LoggedItem >────────────┘
  │                                              │
  ├────< (M) Recipe                              │
  │           │                                  │
  │           └────< (M) RecipeIngredient >──────┘
  │
  ├────< (M) MealPlan
  │           │
  │           └────< (M) PlannedMeal
  │                       │
  │                       └────< (M) PlannedItem >────> (1) FoodItem or Recipe
  │
  ├────< (M) ShoppingListItem >────── (1) FoodItem
  │
  ├────< (M) Feedback
  │
  └────< (M) Insight
```

---

## Core Entities

### 1. User

Represents an individual using the application.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User email (for authentication) |
| `password_hash` | VARCHAR(255) | NOT NULL | Hashed password |
| `full_name` | VARCHAR(255) | NULL | User's full name |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Validation Rules:**
- Email must be valid format
- Password must be hashed (bcrypt/argon2)

**Indexes:**
- `email` (unique index for fast lookup)

---

### 2. FoodItem

A template for a type of food, containing nutritional information and cost. This is user-defined and reusable.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique food item identifier |
| `user_id` | UUID | FOREIGN KEY (User.id), NOT NULL | Owner of this food item |
| `name` | VARCHAR(255) | NOT NULL | Name of the food (e.g., "Whole Milk") |
| `brand` | VARCHAR(255) | NULL | Brand name (optional) |
| `serving_size` | DECIMAL(10,2) | NOT NULL | Size of one serving |
| `serving_unit` | VARCHAR(50) | NOT NULL | Unit of serving (e.g., "cup", "oz", "g") |
| `calories` | DECIMAL(8,2) | NULL | Calories per serving |
| `protein_g` | DECIMAL(8,2) | NULL | Protein in grams |
| `carbs_g` | DECIMAL(8,2) | NULL | Carbohydrates in grams |
| `fat_g` | DECIMAL(8,2) | NULL | Total fat in grams |
| `saturated_fat_g` | DECIMAL(8,2) | NULL | Saturated fat in grams |
| `trans_fat_g` | DECIMAL(8,2) | NULL | Trans fat in grams |
| `cholesterol_mg` | DECIMAL(8,2) | NULL | Cholesterol in milligrams |
| `sodium_mg` | DECIMAL(8,2) | NULL | Sodium in milligrams |
| `fiber_g` | DECIMAL(8,2) | NULL | Dietary fiber in grams |
| `sugar_g` | DECIMAL(8,2) | NULL | Sugar in grams |
| `vitamin_a_mcg` | DECIMAL(8,2) | NULL | Vitamin A in micrograms |
| `vitamin_c_mg` | DECIMAL(8,2) | NULL | Vitamin C in milligrams |
| `calcium_mg` | DECIMAL(8,2) | NULL | Calcium in milligrams |
| `iron_mg` | DECIMAL(8,2) | NULL | Iron in milligrams |
| `cost_per_serving` | DECIMAL(10,2) | NULL | Cost in USD per serving |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Validation Rules:**
- All numeric nutritional fields ≥ 0
- `serving_size` > 0
- `serving_unit` must be from predefined list (cups, oz, g, ml, etc.)

**Indexes:**
- `user_id, name` (composite index for fast user-specific searches)
- `user_id, created_at` (for recent items)

**State Transitions:**
N/A (immutable once created, or updated in place)

---

### 3. PantryItem

An instance of a FoodItem in the user's pantry with quantity and expiration.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique pantry item identifier |
| `user_id` | UUID | FOREIGN KEY (User.id), NOT NULL | Owner of pantry |
| `food_item_id` | UUID | FOREIGN KEY (FoodItem.id), NOT NULL | Reference to food template |
| `quantity` | DECIMAL(10,2) | NOT NULL, CHECK (≥ 0) | Current quantity in pantry |
| `unit` | VARCHAR(50) | NOT NULL | Unit of quantity (matches FoodItem.serving_unit) |
| `expiration_date` | DATE | NULL | Optional expiration date |
| `location` | VARCHAR(100) | NULL | Storage location (e.g., "Pantry", "Fridge", "Freezer") |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When added to pantry |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last quantity update |

**Validation Rules:**
- `quantity` ≥ 0 (enforced by CHECK constraint)
- `unit` must match `food_item_id.serving_unit`
- `expiration_date` can be NULL (user may not know/track)

**Indexes:**
- `user_id, food_item_id` (composite unique index - one pantry entry per food item)
- `user_id, expiration_date` (for "expiring soon" queries)

**State Transitions:**
- Quantity decreases when meal is logged (via LoggedItem)
- Quantity can go to 0 (but item stays in pantry unless user deletes)

---

### 4. MealLog

A record of a meal eaten by the user at a specific date and time.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique meal log identifier |
| `user_id` | UUID | FOREIGN KEY (User.id), NOT NULL | User who logged meal |
| `meal_name` | VARCHAR(255) | NULL | Optional name (e.g., "Breakfast", "Lunch") |
| `meal_type` | VARCHAR(50) | NULL | Type (e.g., "breakfast", "lunch", "dinner", "snack") |
| `logged_at` | TIMESTAMP | NOT NULL | When meal was eaten |
| `notes` | TEXT | NULL | Optional notes about the meal |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When log was created |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update |

**Validation Rules:**
- `logged_at` cannot be in the future
- `meal_type` must be from enum: ["breakfast", "lunch", "dinner", "snack", null]

**Indexes:**
- `user_id, logged_at DESC` (for chronological queries)
- `user_id, meal_type` (for meal type analysis)

**Relationships:**
- Has many `LoggedItem` (the foods consumed in this meal)
- May have one `Feedback` (optional rating)

---

### 5. LoggedItem

A specific quantity of a FoodItem consumed as part of a MealLog.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique logged item identifier |
| `meal_log_id` | UUID | FOREIGN KEY (MealLog.id), NOT NULL, CASCADE DELETE | Parent meal |
| `food_item_id` | UUID | FOREIGN KEY (FoodItem.id), NOT NULL | Food consumed |
| `servings` | DECIMAL(10,2) | NOT NULL, CHECK (> 0) | Number of servings consumed |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When added to meal |

**Validation Rules:**
- `servings` > 0

**Indexes:**
- `meal_log_id` (for fetching all items in a meal)
- `food_item_id` (for "foods eaten" analysis)

**Computed Fields (application layer):**
- Total calories = `food_item.calories * servings`
- Total protein = `food_item.protein_g * servings`
- (etc. for all nutrients)

**Side Effects:**
- On create: Decrement `PantryItem.quantity` by `servings` if pantry item exists
- If pantry quantity < servings: Allow, set to 0, show warning (per spec clarification)

---

### 6. Recipe

A user-defined collection of FoodItems saved from a MealLog for reuse.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique recipe identifier |
| `user_id` | UUID | FOREIGN KEY (User.id), NOT NULL | Recipe creator |
| `name` | VARCHAR(255) | NOT NULL | Recipe name (e.g., "Mom's Lasagna") |
| `description` | TEXT | NULL | Optional description/instructions |
| `created_from_meal_log_id` | UUID | FOREIGN KEY (MealLog.id), NULL | Original meal log (if saved from one) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update |

**Validation Rules:**
- `name` must be unique per user

**Indexes:**
- `user_id, name` (unique composite index)

**Relationships:**
- Has many `RecipeIngredient` (the foods in this recipe)

---

### 7. RecipeIngredient

A specific quantity of a FoodItem that is part of a Recipe.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique ingredient identifier |
| `recipe_id` | UUID | FOREIGN KEY (Recipe.id), NOT NULL, CASCADE DELETE | Parent recipe |
| `food_item_id` | UUID | FOREIGN KEY (FoodItem.id), NOT NULL | Ingredient |
| `servings` | DECIMAL(10,2) | NOT NULL, CHECK (> 0) | Number of servings in recipe |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When added |

**Validation Rules:**
- `servings` > 0

**Indexes:**
- `recipe_id` (for fetching all ingredients)

---

### 8. MealPlan

A schedule of suggested meals for a user over a defined period.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique plan identifier |
| `user_id` | UUID | FOREIGN KEY (User.id), NOT NULL | Plan owner |
| `name` | VARCHAR(255) | NOT NULL | Plan name (e.g., "Week of Nov 1") |
| `start_date` | DATE | NOT NULL | First day of plan |
| `end_date` | DATE | NOT NULL, CHECK (≥ start_date) | Last day of plan |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When plan was generated |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last modification |

**Validation Rules:**
- `end_date` ≥ `start_date`

**Indexes:**
- `user_id, start_date DESC` (for recent plans)

**Relationships:**
- Has many `PlannedMeal` (the meals in this plan)
- Has one `ShoppingList` (generated from plan)

---

### 9. PlannedMeal

A single meal within a MealPlan for a specific date and meal type.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique planned meal identifier |
| `meal_plan_id` | UUID | FOREIGN KEY (MealPlan.id), NOT NULL, CASCADE DELETE | Parent plan |
| `date` | DATE | NOT NULL | Date of this meal |
| `meal_type` | VARCHAR(50) | NOT NULL | "breakfast", "lunch", "dinner", "snack" |
| `recipe_id` | UUID | FOREIGN KEY (Recipe.id), NULL | If meal is a saved recipe |
| `notes` | TEXT | NULL | Instructions or notes from LLM |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When planned |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update |

**Validation Rules:**
- `meal_type` must be from enum: ["breakfast", "lunch", "dinner", "snack"]
- If `recipe_id` is set, `PlannedItem` entries should match recipe ingredients (or be empty)

**Indexes:**
- `meal_plan_id, date, meal_type` (composite unique index - one meal per type per day)

**Relationships:**
- Has many `PlannedItem` (if not using a recipe, or to add extra items)

---

### 10. PlannedItem

A specific FoodItem included in a PlannedMeal (used when meal is not a recipe, or to supplement).

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique planned item identifier |
| `planned_meal_id` | UUID | FOREIGN KEY (PlannedMeal.id), NOT NULL, CASCADE DELETE | Parent meal |
| `food_item_id` | UUID | FOREIGN KEY (FoodItem.id), NOT NULL | Food to eat |
| `servings` | DECIMAL(10,2) | NOT NULL, CHECK (> 0) | Planned servings |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When added |

**Validation Rules:**
- `servings` > 0

**Indexes:**
- `planned_meal_id` (for fetching meal contents)

---

### 11. ShoppingListItem

An item needed for a MealPlan that is not sufficiently available in the pantry.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique shopping item identifier |
| `meal_plan_id` | UUID | FOREIGN KEY (MealPlan.id), NOT NULL, CASCADE DELETE | Associated plan |
| `food_item_id` | UUID | FOREIGN KEY (FoodItem.id), NOT NULL | Food to buy |
| `quantity_needed` | DECIMAL(10,2) | NOT NULL, CHECK (> 0) | How much to purchase |
| `unit` | VARCHAR(50) | NOT NULL | Unit of quantity |
| `is_purchased` | BOOLEAN | NOT NULL, DEFAULT FALSE | Checked off by user |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When added to list |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update (e.g., checked off) |

**Validation Rules:**
- `quantity_needed` > 0

**Indexes:**
- `meal_plan_id, is_purchased` (for filtering purchased vs unpurchased)

**Computed Logic:**
For each FoodItem in MealPlan:
  - Total servings needed = sum of all PlannedItem.servings for that food
  - Pantry available = PantryItem.quantity (or 0 if not in pantry)
  - If (total needed > pantry available): Create ShoppingListItem with (total needed - pantry available)

---

### 12. Feedback

A record of user rating or qualitative feedback on a meal or plan.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique feedback identifier |
| `user_id` | UUID | FOREIGN KEY (User.id), NOT NULL | User providing feedback |
| `feedback_type` | VARCHAR(50) | NOT NULL | "meal_rating" or "plan_change" |
| `meal_log_id` | UUID | FOREIGN KEY (MealLog.id), NULL | If rating a meal |
| `meal_plan_id` | UUID | FOREIGN KEY (MealPlan.id), NULL | If feedback on plan change |
| `rating` | INTEGER | NULL, CHECK (1 ≤ rating ≤ 5) | 1-5 rating (for meal_rating) |
| `comment` | TEXT | NULL | Qualitative feedback |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When submitted |

**Validation Rules:**
- `rating` must be 1-5 (if provided)
- If `feedback_type` = "meal_rating", `meal_log_id` must be set
- If `feedback_type` = "plan_change", `meal_plan_id` must be set

**Indexes:**
- `user_id, created_at DESC` (for feedback history)
- `meal_log_id` (unique - one feedback per meal)

---

### 13. Insight

A user-configured visualization of logged data.

**Attributes:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique insight identifier |
| `user_id` | UUID | FOREIGN KEY (User.id), NOT NULL | Insight owner |
| `name` | VARCHAR(255) | NOT NULL | User-given name (e.g., "Calorie Trend") |
| `chart_type` | VARCHAR(50) | NOT NULL | "line", "bar", "pie", etc. |
| `metric` | VARCHAR(100) | NOT NULL | What to measure (e.g., "calories", "protein_g", "cost") |
| `aggregation` | VARCHAR(50) | NOT NULL | "sum", "average", "count" |
| `time_range` | VARCHAR(50) | NOT NULL | "7_days", "30_days", "all_time" |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When created |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update |

**Validation Rules:**
- `chart_type` must be from enum: ["line", "bar", "pie", "scatter"]
- `metric` must be valid nutritional field or "cost"
- `aggregation` must be from enum: ["sum", "average", "count"]
- `time_range` must be from enum: ["7_days", "30_days", "90_days", "all_time"]

**Indexes:**
- `user_id` (for fetching user's insights)

**Computed Data:**
Insights do not store data; they define a query to run on MealLog/LoggedItem data.

---

## Database Schema (PostgreSQL)

### DDL Summary

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);

-- Food Items
CREATE TABLE food_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255),
    serving_size DECIMAL(10,2) NOT NULL CHECK (serving_size > 0),
    serving_unit VARCHAR(50) NOT NULL,
    calories DECIMAL(8,2) CHECK (calories >= 0),
    protein_g DECIMAL(8,2) CHECK (protein_g >= 0),
    carbs_g DECIMAL(8,2) CHECK (carbs_g >= 0),
    fat_g DECIMAL(8,2) CHECK (fat_g >= 0),
    saturated_fat_g DECIMAL(8,2) CHECK (saturated_fat_g >= 0),
    trans_fat_g DECIMAL(8,2) CHECK (trans_fat_g >= 0),
    cholesterol_mg DECIMAL(8,2) CHECK (cholesterol_mg >= 0),
    sodium_mg DECIMAL(8,2) CHECK (sodium_mg >= 0),
    fiber_g DECIMAL(8,2) CHECK (fiber_g >= 0),
    sugar_g DECIMAL(8,2) CHECK (sugar_g >= 0),
    vitamin_a_mcg DECIMAL(8,2) CHECK (vitamin_a_mcg >= 0),
    vitamin_c_mg DECIMAL(8,2) CHECK (vitamin_c_mg >= 0),
    calcium_mg DECIMAL(8,2) CHECK (calcium_mg >= 0),
    iron_mg DECIMAL(8,2) CHECK (iron_mg >= 0),
    cost_per_serving DECIMAL(10,2) CHECK (cost_per_serving >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_food_items_user_name ON food_items(user_id, name);
CREATE INDEX idx_food_items_user_created ON food_items(user_id, created_at DESC);

-- Pantry Items
CREATE TABLE pantry_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    food_item_id UUID NOT NULL REFERENCES food_items(id) ON DELETE CASCADE,
    quantity DECIMAL(10,2) NOT NULL CHECK (quantity >= 0),
    unit VARCHAR(50) NOT NULL,
    expiration_date DATE,
    location VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, food_item_id)
);
CREATE INDEX idx_pantry_items_user_expiration ON pantry_items(user_id, expiration_date);

-- Meal Logs
CREATE TABLE meal_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    meal_name VARCHAR(255),
    meal_type VARCHAR(50) CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    logged_at TIMESTAMP NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_meal_logs_user_logged ON meal_logs(user_id, logged_at DESC);
CREATE INDEX idx_meal_logs_user_type ON meal_logs(user_id, meal_type);

-- Logged Items
CREATE TABLE logged_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meal_log_id UUID NOT NULL REFERENCES meal_logs(id) ON DELETE CASCADE,
    food_item_id UUID NOT NULL REFERENCES food_items(id),
    servings DECIMAL(10,2) NOT NULL CHECK (servings > 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_logged_items_meal_log ON logged_items(meal_log_id);
CREATE INDEX idx_logged_items_food_item ON logged_items(food_item_id);

-- Recipes
CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_from_meal_log_id UUID REFERENCES meal_logs(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, name)
);
CREATE UNIQUE INDEX idx_recipes_user_name ON recipes(user_id, name);

-- Recipe Ingredients
CREATE TABLE recipe_ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    food_item_id UUID NOT NULL REFERENCES food_items(id),
    servings DECIMAL(10,2) NOT NULL CHECK (servings > 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);

-- Meal Plans
CREATE TABLE meal_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL CHECK (end_date >= start_date),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_meal_plans_user_start ON meal_plans(user_id, start_date DESC);

-- Planned Meals
CREATE TABLE planned_meals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meal_plan_id UUID NOT NULL REFERENCES meal_plans(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    meal_type VARCHAR(50) NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    recipe_id UUID REFERENCES recipes(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(meal_plan_id, date, meal_type)
);
CREATE UNIQUE INDEX idx_planned_meals_unique ON planned_meals(meal_plan_id, date, meal_type);

-- Planned Items
CREATE TABLE planned_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    planned_meal_id UUID NOT NULL REFERENCES planned_meals(id) ON DELETE CASCADE,
    food_item_id UUID NOT NULL REFERENCES food_items(id),
    servings DECIMAL(10,2) NOT NULL CHECK (servings > 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_planned_items_meal ON planned_items(planned_meal_id);

-- Shopping List Items
CREATE TABLE shopping_list_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meal_plan_id UUID NOT NULL REFERENCES meal_plans(id) ON DELETE CASCADE,
    food_item_id UUID NOT NULL REFERENCES food_items(id),
    quantity_needed DECIMAL(10,2) NOT NULL CHECK (quantity_needed > 0),
    unit VARCHAR(50) NOT NULL,
    is_purchased BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_shopping_list_plan_purchased ON shopping_list_items(meal_plan_id, is_purchased);

-- Feedback
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    feedback_type VARCHAR(50) NOT NULL CHECK (feedback_type IN ('meal_rating', 'plan_change')),
    meal_log_id UUID REFERENCES meal_logs(id) ON DELETE CASCADE,
    meal_plan_id UUID REFERENCES meal_plans(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_feedback_user_created ON feedback(user_id, created_at DESC);
CREATE UNIQUE INDEX idx_feedback_meal_log ON feedback(meal_log_id);

-- Insights
CREATE TABLE insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    chart_type VARCHAR(50) NOT NULL CHECK (chart_type IN ('line', 'bar', 'pie', 'scatter')),
    metric VARCHAR(100) NOT NULL,
    aggregation VARCHAR(50) NOT NULL CHECK (aggregation IN ('sum', 'average', 'count')),
    time_range VARCHAR(50) NOT NULL CHECK (time_range IN ('7_days', '30_days', '90_days', 'all_time')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_insights_user ON insights(user_id);
```

---

## Migration Strategy

### Alembic Migrations

1. **Initial migration** (create all tables)
2. **Seed data**: Common serving units (enum-like reference table - optional)
3. **Future migrations**:
   - Add columns for new nutritional fields
   - Add indexes for query optimization as usage patterns emerge
   - Add materialized views for insights if performance degrades

---

## Data Integrity Rules

### Referential Integrity
- All foreign keys use `ON DELETE CASCADE` where child data is meaningless without parent
  - Example: LoggedItems cascade delete with MealLog
- Use `ON DELETE SET NULL` where child should survive parent deletion
  - Example: Recipe can survive deletion of the MealLog it was created from

### Application-Level Constraints
- **Pantry deduction logic**: When LoggedItem is created, decrement PantryItem.quantity atomically in a transaction
- **Shopping list generation**: Recalculate shopping list whenever MealPlan or PantryItems change
- **Duplicate prevention**: Ensure one PantryItem per (user_id, food_item_id) via unique index

---

## Scalability Considerations

### Partitioning (Future)
- Partition `meal_logs` and `logged_items` by `logged_at` (monthly or yearly) for time-series queries
- Partition `feedback` by `created_at` similarly

### Archiving
- Archive MealLogs older than 2 years to separate "historical" tables
- Keep aggregated insights data, purge raw logs

### Denormalization (If Needed)
- Add `total_calories`, `total_protein`, etc. columns to `meal_logs` table to avoid join-heavy queries
- Trade-off: Storage cost vs query performance

---

## Sample Data Flows

### Flow 1: Log a Meal
1. User selects FoodItems and quantities
2. Frontend sends POST `/api/meals` with:
   ```json
   {
     "meal_type": "breakfast",
     "logged_at": "2025-10-25T08:00:00Z",
     "items": [
       {"food_item_id": "uuid-1", "servings": 2.0},
       {"food_item_id": "uuid-2", "servings": 1.0}
     ]
   }
   ```
3. Backend transaction:
   - Create `MealLog` record
   - For each item: Create `LoggedItem`, decrement `PantryItem.quantity`
   - If pantry quantity < servings: Set to 0, return warning in response
4. Optional: Prompt user for Feedback (1-5 rating)

### Flow 2: Generate Meal Plan
1. User requests plan for 7 days, 3 meals/day
2. Frontend sends POST `/api/plans/generate` with date range, meal types
3. Backend:
   - Fetch user's PantryItems and Recipes
   - Build LLM prompt with constraints
   - Call OpenAI GPT-4o-mini
   - Parse JSON response into `MealPlan`, `PlannedMeal`, `PlannedItem` records
   - Generate `ShoppingListItem` for missing ingredients
4. Return plan ID to frontend

### Flow 3: Save Meal as Recipe
1. User clicks "Save as Recipe" on a MealLog
2. Frontend sends POST `/api/recipes` with:
   ```json
   {
     "name": "Morning Smoothie",
     "meal_log_id": "uuid-xyz"
   }
   ```
3. Backend:
   - Create `Recipe` record
   - Copy all `LoggedItem` entries as `RecipeIngredient` entries
4. Return recipe ID

---

## Validation Summary

| Entity | Key Validations |
|--------|-----------------|
| `User` | Email format, password strength (app layer) |
| `FoodItem` | All numeric ≥ 0, serving_size > 0 |
| `PantryItem` | Quantity ≥ 0, unique per user+food |
| `MealLog` | logged_at not in future |
| `LoggedItem` | Servings > 0 |
| `Recipe` | Unique name per user |
| `MealPlan` | end_date ≥ start_date |
| `PlannedMeal` | Unique per plan+date+meal_type |
| `Feedback` | Rating 1-5, correct foreign key based on type |
| `Insight` | Valid enum values for chart_type, metric, etc. |

---

## Appendix: Sample Queries

### Get user's pantry with food details
```sql
SELECT
    pi.id, pi.quantity, pi.unit, pi.expiration_date,
    fi.name, fi.brand, fi.calories, fi.protein_g
FROM pantry_items pi
JOIN food_items fi ON pi.food_item_id = fi.id
WHERE pi.user_id = :user_id
ORDER BY pi.expiration_date ASC NULLS LAST;
```

### Get total calories for a date range
```sql
SELECT
    DATE(ml.logged_at) as date,
    SUM(fi.calories * li.servings) as total_calories
FROM meal_logs ml
JOIN logged_items li ON ml.id = li.meal_log_id
JOIN food_items fi ON li.food_item_id = fi.id
WHERE ml.user_id = :user_id
  AND ml.logged_at BETWEEN :start_date AND :end_date
GROUP BY DATE(ml.logged_at)
ORDER BY date;
```

### Get shopping list for a meal plan
```sql
SELECT
    fi.name, fi.brand, sl.quantity_needed, sl.unit, sl.is_purchased
FROM shopping_list_items sl
JOIN food_items fi ON sl.food_item_id = fi.id
WHERE sl.meal_plan_id = :plan_id
ORDER BY sl.is_purchased ASC, fi.name ASC;
```
