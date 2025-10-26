/**
 * API client methods for Recipes
 */
import apiClient from '../api';

export interface RecipeCreateFromMealLog {
  name: string;
  description?: string;
  meal_log_id: string;
}

export interface RecipeIngredientResponse {
  id: string;
  recipe_id: string;
  food_item_id: string;
  servings: number;
  food_item_name: string;
  food_item_brand?: string | null;
  food_item_serving_unit: string;
  total_calories?: number | null;
  total_protein_g?: number | null;
  total_carbs_g?: number | null;
  total_fat_g?: number | null;
  total_cost?: number | null;
  created_at: string;
}

export interface RecipeNutritionTotals {
  total_calories?: number | null;
  total_protein_g?: number | null;
  total_carbs_g?: number | null;
  total_fat_g?: number | null;
  total_cost?: number | null;
}

export interface RecipeResponse {
  id: string;
  user_id: string;
  name: string;
  description?: string | null;
  created_from_meal_log_id?: string | null;
  ingredients: RecipeIngredientResponse[];
  nutrition_totals: RecipeNutritionTotals;
  created_at: string;
  updated_at: string;
}

export interface RecipeListItem {
  id: string;
  user_id: string;
  name: string;
  description?: string | null;
  ingredient_count: number;
  nutrition_totals: RecipeNutritionTotals;
  created_at: string;
  updated_at: string;
}

export interface RecipeListResponse {
  recipes: RecipeListItem[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

export const recipesApi = {
  createFromMeal: async (data: RecipeCreateFromMealLog): Promise<RecipeResponse> => {
    const res = await apiClient.post<RecipeResponse>('/recipes', data);
    return res.data;
  },
  list: async (params?: { page?: number; per_page?: number; search?: string }): Promise<RecipeListResponse> => {
    const res = await apiClient.get<RecipeListResponse>('/recipes', { params });
    return res.data;
  },
  getById: async (id: string): Promise<RecipeResponse> => {
    const res = await apiClient.get<RecipeResponse>(`/recipes/${id}`);
    return res.data;
  },
};