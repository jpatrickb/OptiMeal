/**
 * API client methods for Pantry Management
 *
 * Provides CRUD operations for managing pantry inventory.
 */

import apiClient from '../api';
import type { FoodItemResponse } from './foodItems';

export interface PantryItemCreate {
  food_item_id: string;
  quantity: number;
  unit: string;
  expiration_date?: string | null;
  location?: string | null;
}

export interface PantryItemUpdate {
  quantity?: number;
  unit?: string;
  expiration_date?: string | null;
  location?: string | null;
}

export interface PantryItemResponse {
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

export interface PantryItemWithFoodResponse extends PantryItemResponse {
  food_item: FoodItemResponse;
}

/**
 * Add a food item to the pantry
 */
export const addToPantry = async (data: PantryItemCreate): Promise<PantryItemWithFoodResponse> => {
  const response = await apiClient.post<PantryItemWithFoodResponse>('/pantry', data);
  return response.data;
};

/**
 * Get all pantry items for the authenticated user
 */
export const getPantry = async (): Promise<PantryItemWithFoodResponse[]> => {
  const response = await apiClient.get<PantryItemWithFoodResponse[]>('/pantry');
  return response.data;
};

/**
 * Get pantry items expiring soon
 */
export const getExpiringSoon = async (days: number = 3): Promise<PantryItemWithFoodResponse[]> => {
  const response = await apiClient.get<PantryItemWithFoodResponse[]>('/pantry/expiring-soon', {
    params: { days },
  });
  return response.data;
};

/**
 * Get a specific pantry item by ID
 */
export const getPantryItem = async (id: string): Promise<PantryItemWithFoodResponse> => {
  const response = await apiClient.get<PantryItemWithFoodResponse>(`/pantry/${id}`);
  return response.data;
};

/**
 * Update a pantry item
 */
export const updatePantryItem = async (
  id: string,
  data: PantryItemUpdate
): Promise<PantryItemWithFoodResponse> => {
  const response = await apiClient.patch<PantryItemWithFoodResponse>(`/pantry/${id}`, data);
  return response.data;
};

/**
 * Remove an item from the pantry
 */
export const removeFromPantry = async (id: string): Promise<{ message: string }> => {
  const response = await apiClient.delete<{ message: string }>(`/pantry/${id}`);
  return response.data;
};

// Export as pantryApi object for easier use
export const pantryApi = {
  add: addToPantry,
  list: getPantry,
  getExpiringSoon,
  getById: getPantryItem,
  update: updatePantryItem,
  delete: removeFromPantry,
};
