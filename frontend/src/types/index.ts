// Type definitions for OptiMeal application

export interface User {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
  updated_at: string;
}

export interface FoodItem {
  id: string;
  user_id: string;
  name: string;
  brand?: string | null;
  serving_size: number;
  serving_unit: string;
  calories?: number | null;
  protein_g?: number | null;
  carbs_g?: number | null;
  fat_g?: number | null;
  saturated_fat_g?: number | null;
  trans_fat_g?: number | null;
  cholesterol_mg?: number | null;
  sodium_mg?: number | null;
  fiber_g?: number | null;
  sugar_g?: number | null;
  vitamin_a_mcg?: number | null;
  vitamin_c_mg?: number | null;
  calcium_mg?: number | null;
  iron_mg?: number | null;
  cost_per_serving?: number | null;
  created_at: string;
  updated_at: string;
}

export interface FoodItemCreate {
  name: string;
  brand?: string;
  serving_size: number;
  serving_unit: string;
  calories?: number;
  protein_g?: number;
  carbs_g?: number;
  fat_g?: number;
  saturated_fat_g?: number;
  trans_fat_g?: number;
  cholesterol_mg?: number;
  sodium_mg?: number;
  fiber_g?: number;
  sugar_g?: number;
  vitamin_a_mcg?: number;
  vitamin_c_mg?: number;
  calcium_mg?: number;
  iron_mg?: number;
  cost_per_serving?: number;
}

export interface PantryItem {
  id: string;
  user_id: string;
  food_item_id: string;
  quantity: number;
  unit: string;
  expiration_date?: string | null;
  location?: string | null;
  created_at: string;
  updated_at: string;
}

export interface PantryItemWithFood extends PantryItem {
  food_item: FoodItem;
}

export interface PantryItemCreate {
  food_item_id: string;
  quantity: number;
  unit: string;
  expiration_date?: string;
  location?: string;
}

export interface PantryItemUpdate {
  quantity?: number;
  unit?: string;
  expiration_date?: string;
  location?: string;
}
