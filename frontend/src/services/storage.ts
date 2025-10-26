/**
 * LocalStorage wrapper for token persistence.
 *
 * Provides type-safe methods for storing and retrieving authentication tokens.
 */

const TOKEN_KEY = 'optimeal_access_token';
const USER_KEY = 'optimeal_user';

/**
 * User data interface for storage.
 */
export interface StoredUser {
  id: string;
  email: string;
  full_name?: string;
}

/**
 * Save JWT access token to localStorage.
 *
 * @param token - JWT access token
 */
export const setToken = (token: string): void => {
  try {
    localStorage.setItem(TOKEN_KEY, token);
  } catch (error) {
    console.error('Error saving token to localStorage:', error);
  }
};

/**
 * Get JWT access token from localStorage.
 *
 * @returns JWT token or null if not found
 */
export const getToken = (): string | null => {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch (error) {
    console.error('Error reading token from localStorage:', error);
    return null;
  }
};

/**
 * Remove JWT access token from localStorage.
 */
export const removeToken = (): void => {
  try {
    localStorage.removeItem(TOKEN_KEY);
  } catch (error) {
    console.error('Error removing token from localStorage:', error);
  }
};

/**
 * Check if user is authenticated (has valid token).
 *
 * @returns true if token exists, false otherwise
 */
export const isAuthenticated = (): boolean => {
  return getToken() !== null;
};

/**
 * Save user data to localStorage.
 *
 * @param user - User data to store
 */
export const setUser = (user: StoredUser): void => {
  try {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  } catch (error) {
    console.error('Error saving user to localStorage:', error);
  }
};

/**
 * Get user data from localStorage.
 *
 * @returns User data or null if not found
 */
export const getUser = (): StoredUser | null => {
  try {
    const userJson = localStorage.getItem(USER_KEY);
    return userJson ? JSON.parse(userJson) : null;
  } catch (error) {
    console.error('Error reading user from localStorage:', error);
    return null;
  }
};

/**
 * Remove user data from localStorage.
 */
export const removeUser = (): void => {
  try {
    localStorage.removeItem(USER_KEY);
  } catch (error) {
    console.error('Error removing user from localStorage:', error);
  }
};

/**
 * Clear all authentication data from localStorage.
 */
export const clearAuthData = (): void => {
  removeToken();
  removeUser();
};
