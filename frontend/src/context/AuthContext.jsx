/**
 * AuthContext — React Context for authentication state management.
 * Checks for existing session on mount via HTTP-only cookie.
 */
import React, { createContext, useState, useEffect, useCallback } from 'react';
import authService from '../services/authService';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check existing session on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await authService.getMe();
      if (response?.success && response.data?.user) {
        setUser(response.data.user);
        setIsAuthenticated(true);
      }
    } catch {
      // Not authenticated — this is expected for new visitors
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const login = useCallback(async (email, password) => {
    const response = await authService.login(email, password);
    if (response?.success && response.data?.user) {
      setUser(response.data.user);
      setIsAuthenticated(true);
      return response.data.user;
    }
    throw new Error(response?.error || 'Login failed');
  }, []);

  const register = useCallback(async (fullName, email, password) => {
    const response = await authService.register(fullName, email, password);
    if (response?.success && response.data?.user) {
      setUser(response.data.user);
      setIsAuthenticated(true);
      return response.data.user;
    }
    throw new Error(response?.error || 'Registration failed');
  }, []);

  const logout = useCallback(async () => {
    try {
      await authService.logout();
    } catch {
      // Even if the API call fails, clear local state
    }
    setUser(null);
    setIsAuthenticated(false);
  }, []);

  const refreshUser = useCallback(async () => {
    try {
      const response = await authService.getMe();
      if (response?.success && response.data?.user) {
        setUser(response.data.user);
        setIsAuthenticated(true);
      }
    } catch {
      setUser(null);
      setIsAuthenticated(false);
    }
  }, []);

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    refreshUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
