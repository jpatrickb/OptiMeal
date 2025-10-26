/**
 * Authentication Context for managing user authentication state.
 *
 * Provides login, logout, and registration functionality across the app.
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import apiClient from '../services/api';
import {
  setToken,
  removeToken,
  getToken,
  setUser,
  removeUser,
  getUser,
  clearAuthData,
  StoredUser,
} from '../services/storage';

interface AuthContextType {
  user: StoredUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUserState] = useState<StoredUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing session on mount
  useEffect(() => {
    const initAuth = async () => {
      const token = getToken();
      const storedUser = getUser();

      if (token && storedUser) {
        // Verify token is still valid by fetching current user
        try {
          const response = await apiClient.get('/auth/me');
          setUserState(response.data);
          setUser(response.data);
        } catch (error) {
          // Token is invalid, clear auth data
          clearAuthData();
          setUserState(null);
        }
      }

      setIsLoading(false);
    };

    initAuth();

    // Listen for auth:logout events from API client
    const handleLogout = () => {
      setUserState(null);
    };

    window.addEventListener('auth:logout', handleLogout);

    return () => {
      window.removeEventListener('auth:logout', handleLogout);
    };
  }, []);

  /**
   * Login user with email and password.
   */
  const login = async (email: string, password: string): Promise<void> => {
    try {
      // Call login endpoint
      const response = await apiClient.post('/auth/login', {
        email,
        password,
      });

      const { access_token } = response.data;

      // Save token
      setToken(access_token);

      // Fetch user data
      const userResponse = await apiClient.get('/auth/me');
      const userData: StoredUser = userResponse.data;

      // Save user data
      setUser(userData);
      setUserState(userData);
    } catch (error) {
      // Clear any existing auth data
      clearAuthData();
      throw error;
    }
  };

  /**
   * Register new user account.
   */
  const register = async (email: string, password: string, fullName?: string): Promise<void> => {
    try {
      // Call register endpoint
      await apiClient.post('/auth/register', {
        email,
        password,
        full_name: fullName,
      });

      // After registration, log the user in
      await login(email, password);
    } catch (error) {
      throw error;
    }
  };

  /**
   * Logout user and clear authentication data.
   */
  const logout = (): void => {
    clearAuthData();
    setUserState(null);
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: user !== null,
    isLoading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * Hook to access authentication context.
 *
 * Must be used within an AuthProvider.
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
