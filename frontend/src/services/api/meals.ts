/**
 * API client methods for Meals (meal logs)
 */
import apiClient from '../api';

export interface LoggedItemCreate {
  food_item_id: string;
  servings: number;
}

export interface MealLogCreate {
  meal_name?: string;
  meal_type?: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  logged_at: string; // ISO string
  notes?: string;
  items: LoggedItemCreate[];
}

export interface LoggedItemResponse {
  id: string;
  food_item_id: string;
  servings: number;
  food_item_name: string;
  food_item_brand?: string | null;
  total_calories?: number | null;
  total_protein_g?: number | null;
  total_carbs_g?: number | null;
  total_fat_g?: number | null;
  total_cost?: number | null;
  created_at: string;
}

export interface NutritionTotals {
  total_calories?: number | null;
  total_protein_g?: number | null;
  total_carbs_g?: number | null;
  total_fat_g?: number | null;
  total_cost?: number | null;
}

export interface MealLogResponse {
  id: string;
  user_id: string;
  meal_name?: string | null;
  meal_type?: 'breakfast' | 'lunch' | 'dinner' | 'snack' | null;
  logged_at: string;
  notes?: string | null;
  logged_items: LoggedItemResponse[];
  nutrition_totals: NutritionTotals;
  created_at: string;
  updated_at: string;
}

export interface MealLogListResponse {
  meals: MealLogResponse[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

export interface MealLogWarning {
  food_item_id: string;
  food_item_name: string;
  requested_servings: number;
  available_servings: number;
  message: string;
}

export interface MealLogCreateResponse {
  meal_log: MealLogResponse;
  warnings: MealLogWarning[];
}

export const mealsApi = {
  create: async (data: MealLogCreate): Promise<MealLogCreateResponse> => {
    const res = await apiClient.post<MealLogCreateResponse>('/meals', data);
    return res.data;
  },
  list: async (params?: {
    page?: number;
    per_page?: number;
    start_date?: string;
    end_date?: string;
    meal_type?: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  }): Promise<MealLogListResponse> => {
    const res = await apiClient.get<MealLogListResponse>('/meals', { params });
    return res.data;
  },
  getById: async (id: string): Promise<MealLogResponse> => {
    const res = await apiClient.get<MealLogResponse>(`/meals/${id}`);
    return res.data;
  },
};