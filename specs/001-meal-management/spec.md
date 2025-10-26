# Feature Specification: Meal Management

**Feature Branch**: `001-meal-management`
**Created**: 2025-10-25
**Status**: Draft
**Input**: "I want to build a new feature focused on 1) pantry inventory, 2) meal logging, 3) simple meal planning (not optimized) with shopping list updating (not including stores). This should purely be an organizational tool for the user. They should be able to keep track of the foods that they have available in their pantry/fridge/etc., and meal plans should be generated with the help of large language models according to certain specifications (specific days and meals to plan for, accounting for preexisting user plans, incorporating the foods they currently have, and suggesting new foods/ingredients to buy). The foods they eat should be logged on a meal-by-meal level, tracking macros such as calories, carbs, fats, proteins, with the option to be more specific about other nutrients as well (sodium, sugar, fiber, types of fats, cholestorol, vitamins) as well as the cost of the food they eat. The user should also be able to view insights, where they can see and create charts visualizing the trends in all of the factors of their eating. Each time they eat/record a meal, they should be prompted with an optional survey asking them to rate 1-5 how they liked that meal. If they change the plan, they should be optionally be prompted to give feedback on why they changed from the plan. Also, as they share nutrition details for certain types of foods, that information should be stored so as they eat that food more later, they don't need to enter the information in repeatedly."

## Clarifications

### Session 2025-10-25
- Q: How should the system behave when a user logs a meal that consumes more of an item than the pantry shows is available? → A: Allow, Warn, and Zero: Allow the meal to be logged, set the pantry quantity to zero, and show a non-blocking warning (e.g., "You've logged more eggs than were in your pantry. We've updated your pantry count to 0.")
- Q: For the initial version (MVP), should the system rely exclusively on user-entered nutritional data, or should it attempt to fetch this data from an external database? → A: User-Entry Only: The user is fully responsible for inputting all nutritional and cost data for new foods. The system's only role is to save it for reuse.
- Q: How should the system allow users to log and reuse their own multi-ingredient recipes (e.g., "Mom's Lasagna")? → A: Save Meal as Recipe: After logging a meal, provide a "Save as Recipe" button. This lets the user name the combination of ingredients (e.g., "Morning Smoothie"), which they can then select as a single item in the future.
- Q: What methods should be available for entering nutritional information? → A: Users can input data manually via a UI that mimics a nutrition label, or by uploading a picture of a nutrition label for automated parsing.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Pantry Inventory Management (Priority: P1)

As a user, I want to digitally manage my pantry, fridge, and freezer so that I know what food I have at all times. I want to be able to add, edit, and remove food items, specifying their quantities and, optionally, their expiration dates.

**Why this priority**: This is a foundational feature. The meal planner and logger depend on knowing what food is available.
**Independent Test**: A user can successfully add a list of grocery items to their pantry, see the correct quantities, and then remove an item.

**Acceptance Scenarios**:

1.  **Given** I am on the pantry screen, **When** I add a new food item with a name and quantity, **Then** the item appears in my pantry list with the correct details.
2.  **Given** an item exists in my pantry, **When** I update its quantity, **Then** the pantry list reflects the new quantity.
3.  **Given** an item exists in my pantry, **When** I delete it, **Then** the item is removed from my pantry list.

---

### User Story 2 - Meal Logging & Nutrient Tracking (Priority: P1)

As a user, I want to log the meals I eat to track my nutritional intake and food costs. When I log a meal, the items I use from my pantry should be automatically deducted.

**Why this priority**: Core feature for users focused on health and budget tracking. It provides the data for the insights feature.
**Independent Test**: A user can log a breakfast consisting of two eggs and a slice of toast, see the correct total calories and macros, and see their pantry's egg and bread count decrease.

**Acceptance Scenarios**:

1.  **Given** I am on the meal logging screen, **When** I create a new meal and add food items with quantities, **Then** the meal is saved with the correct date, time, and items.
2.  **Given** I have logged a meal with items from my pantry, **When** I check my pantry, **Then** the quantities of the consumed items are correctly reduced.
3.  **Given** I enter nutritional and cost information for a new food for the first time by uploading a nutrition label, **When** I go to log that same food again later, **Then** the system retrieves the saved nutritional and cost information.
4.  **Given** I have previously logged a meal, **When** I choose to "Save as Recipe", **Then** I can name it and it becomes available for future logging as a single item.

---

### User Story 3 - LLM-Powered Meal Planning (Priority: P2)

As a user, I want to generate a simple meal plan for a specific period. The planner should use my current pantry inventory and saved recipes to suggest meals and create a shopping list for any missing ingredients.

**Why this priority**: This provides significant user value by automating the difficult task of meal planning.
**Independent Test**: A user with chicken and rice in their pantry can request a 3-day dinner plan and receive a plan that includes a chicken and rice dish, plus a shopping list for the other two meals.

**Acceptance Scenarios**:

1.  **Given** I have items in my pantry, **When** I request a meal plan for the next 3 days of dinners, **Then** I receive a plausible 3-day dinner plan that incorporates some of my pantry items.
2.  **Given** a meal plan has been generated, **When** I view the corresponding shopping list, **Then** it only contains items needed for the plan that are not already in my pantry.
3.  **Given** I already have a lunch meeting scheduled on one day, **When** I generate a plan for that week, **Then** the generated plan does not create a lunch for that specific day.

---

### User Story 4 - User Feedback Collection (Priority: P2)

As a user, I want the ability to provide feedback on the meals I eat and the plans I receive, so the system can learn my preferences.

**Why this priority**: This feedback loop is essential for future personalization and optimization features.
**Independent Test**: After logging a meal, a user is presented with a rating prompt, and their rating is successfully saved.

**Acceptance Scenarios**:

1.  **Given** I have just logged a meal, **When** the meal is saved, **Then** I am prompted with an optional 1-5 rating survey.
2.  **Given** I have a meal plan, **When** I modify or delete a planned meal, **Then** I am prompted with an optional form to explain why.

---

### User Story 5 - Nutritional Insights (Priority: P3)

As a user, I want to see visualizations of my eating habits over time, so I can understand my nutritional trends, spending, and make informed decisions.

**Why this priority**: This feature turns raw data into actionable insights, making the app more valuable and "sticky" for the user.
**Independent Test**: A user who has logged meals for a week can view a line chart of their daily calorie intake and a pie chart showing their average macronutrient breakdown.

**Acceptance Scenarios**:

1.  **Given** I have logged meals for at least one week, **When** I navigate to the Insights screen, **Then** I can view a chart of my daily calorie intake over time.
2.  **Given** I am on the Insights screen, **When** I select the "Macros" view, **Then** I can see a pie chart showing the percentage of my calories from protein, carbs, and fats.
3.  **Given** I am on the Insights screen, **When** I choose to create a new chart, **Then** I can select a metric (e.g., cost, sodium) and a time period to visualize.

### Edge Cases

-   What happens when a user tries to log a meal with more of an ingredient than is available in the pantry? The system will allow the meal to be logged, set the pantry quantity to zero, and show a non-blocking warning to the user.
-   How does the system handle a food item with missing or partially parsed nutritional information from an uploaded image?
-   What happens if the LLM meal planner returns an invalid or nonsensical plan?
-   How are custom, multi-ingredient recipes handled? Users can save a logged meal as a reusable 'Recipe', which can then be used in logging and planning.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: System MUST allow users to perform CRUD (Create, Read, Update, Delete) operations on pantry items.
-   **FR-002**: Each pantry item MUST have a name and quantity. Optional fields include expiration date, cost, and a comprehensive set of nutritional data.
-   **FR-003**: System MUST allow users to log meals, specifying the food items and quantities consumed.
-   **FR-004**: The system MUST automatically decrement the quantity of pantry items when a meal containing them is logged.
-   **FR-005**: The system MUST persist nutritional and cost data for food items entered by the user for future use.
-   **FR-006**: System MUST allow users to request a meal plan for a specified date range and meal types (e.g., breakfast, lunch, dinner).
-   **FR-007**: The meal plan generation MUST consider the user's current pantry inventory and saved recipes.
-   **FR-008**: System MUST generate a shopping list of ingredients required for a meal plan that are not sufficiently available in the pantry.
-   **FR-009**: System MUST present an optional 1-5 rating survey after a meal is logged.
-   **FR-010**: System MUST provide visualizations for trends in logged data, including at least calories, macros, and cost.
-   **FR-011**: Users MUST be able to create custom charts to visualize tracked metrics over time.
-   **FR-012**: For the initial version, the system MUST rely exclusively on user-provided data for nutritional and cost information and will not integrate with external food databases.
-   **FR-013**: System MUST allow a user to save a logged meal as a named 'Recipe' for quick logging in the future.
-   **FR-014**: System MUST allow users to upload an image of a nutrition label to automatically populate nutritional data for a FoodItem.
-   **FR-015**: The manual entry interface for nutritional data MUST be designed to resemble a standard nutrition facts label for intuitive input.

### Key Entities *(include if feature involves data)*

-   **User**: The individual using the application.
-   **FoodItem**: A template for a type of food, containing its name, nutritional information (calories, protein, fat, carbs, etc.), and cost per unit. This information is user-defined and saved for reuse.
-   **PantryItem**: An instance of a FoodItem in the user's pantry. It has a quantity and an optional expiration date. It links to a FoodItem.
-   **MealLog**: A record of a meal eaten by the user at a specific date and time. It contains a collection of LoggedItems.
-   **LoggedItem**: A specific quantity of a FoodItem that is part of a MealLog.
-   **Recipe**: A user-defined collection of FoodItems and their quantities, saved from a MealLog for reuse.
-   **MealPlan**: A schedule of suggested meals for a user over a defined period.
-   **ShoppingList**: A list of FoodItems and quantities needed to fulfill a MealPlan.
-   **Feedback**: A record of a user's rating (1-5) for a meal or their qualitative feedback on a plan modification.
-   **Insight**: A user-configured visualization (e.g., chart) of their logged data.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: A new user can add 10 items to their pantry in under 3 minutes.
-   **SC-002**: A user can log a 3-item meal in under 60 seconds if the food items have been logged before.
-   **SC-003**: The system generates a 7-day meal plan in under 20 seconds.
-   **SC-004**: User engagement with the feedback feature reaches an average of 25% of logged meals being rated.
-   **SC-005**: After one month of use, the pantry inventory count for 80% of active users is non-empty, indicating sustained engagement with the inventory feature.
-   **SC-006**: At least 30% of new nutritional data entries are made via the image upload feature within two months of launch.