/**
 * API client methods for Food Items
 *
 * Provides CRUD operations for managing food items with nutritional information.
 */

import apiClient from '../api';

export interface FoodItemCreate {
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
}

export interface FoodItemUpdate {
  name?: string;
  brand?: string | null;
  serving_size?: number;
  serving_unit?: string;
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
}

export interface FoodItemResponse extends FoodItemCreate {
  id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

/**
 * Create a new food item
 */
export const createFoodItem = async (data: FoodItemCreate): Promise<FoodItemResponse> => {
  const response = await apiClient.post<FoodItemResponse>('/food-items', data);
  return response.data;
};

/**
 * Get all food items for the authenticated user
 */
export const listFoodItems = async (params?: {
  skip?: number;
  limit?: number;
  search?: string;
}): Promise<FoodItemResponse[]> => {
  const response = await apiClient.get<FoodItemResponse[]>('/food-items', { params });
  return response.data;
};

/**
 * Get a specific food item by ID
 */
export const getFoodItem = async (id: string): Promise<FoodItemResponse> => {
  const response = await apiClient.get<FoodItemResponse>(`/food-items/${id}`);
  return response.data;
};

/**
 * Update a food item
 */
export const updateFoodItem = async (
  id: string,
  data: FoodItemUpdate
): Promise<FoodItemResponse> => {
  const response = await apiClient.put<FoodItemResponse>(`/food-items/${id}`, data);
  return response.data;
};

/**
 * Delete a food item
 */
export const deleteFoodItem = async (id: string): Promise<{ message: string }> => {
  const response = await apiClient.delete<{ message: string }>(`/food-items/${id}`);
  return response.data;
};

// Export as foodItemsApi object for easier use
export const foodItemsApi = {
  create: createFoodItem,
  list: listFoodItems,
  getById: getFoodItem,
  update: updateFoodItem,
  delete: deleteFoodItem,
};
