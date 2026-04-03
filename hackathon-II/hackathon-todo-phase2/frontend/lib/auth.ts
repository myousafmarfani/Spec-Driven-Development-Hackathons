// frontend/lib/auth.ts
'use client';

import { useState, useEffect } from 'react';

// Types
export interface User {
  id: string;
  email: string;
  name: string;
}

export interface Session {
  user: User;
}

// API URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Cookie helpers
function setCookie(name: string, value: string, days: number = 7) {
  if (typeof window === 'undefined') return;
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function deleteCookie(name: string) {
  if (typeof window === 'undefined') return;
  document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
}

function getCookie(name: string): string | null {
  if (typeof window === 'undefined') return null;
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
  return null;
}

// Get JWT token from storage
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('jwt_token') || getCookie('jwt_token');
  }
  return null;
};

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  return !!getToken();
};

// Sign up user
export const signupUser = async (email: string, password: string, name: string): Promise<{ token: string; user: User }> => {
  const response = await fetch(`${API_URL}/api/auth/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password, name }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Signup failed' }));
    throw new Error(error.detail || 'Signup failed');
  }

  const data = await response.json();
  
  // Store token in both localStorage and cookies
  if (data.token) {
    localStorage.setItem('jwt_token', data.token);
    setCookie('jwt_token', data.token, 7);
  }
  
  // Store user info
  if (data.user) {
    localStorage.setItem('user', JSON.stringify(data.user));
  }

  return data;
};

// Sign in user
export const signinUser = async (email: string, password: string): Promise<{ token: string; user: User }> => {
  const response = await fetch(`${API_URL}/api/auth/signin`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Invalid credentials' }));
    throw new Error(error.detail || 'Invalid email or password');
  }

  const data = await response.json();
  
  // Store token in both localStorage and cookies
  if (data.token) {
    localStorage.setItem('jwt_token', data.token);
    setCookie('jwt_token', data.token, 7);
  }
  
  // Store user info
  if (data.user) {
    localStorage.setItem('user', JSON.stringify(data.user));
  }

  return data;
};

// Sign out user
export const signoutUser = async (): Promise<void> => {
  try {
    // Call backend signout endpoint
    await fetch(`${API_URL}/api/auth/signout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('Signout API error:', error);
  }
  
  // Clear local storage and cookies
  if (typeof window !== 'undefined') {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user');
    deleteCookie('jwt_token');
  }
};

// Custom hook to use auth (replaces better-auth useSession)
export function useSession(): { data: Session | null; isLoading: boolean; isPending: boolean } {
  const [session, setSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load user from localStorage
    const loadSession = () => {
      try {
        const token = getToken();
        const userStr = localStorage.getItem('user');
        
        if (token && userStr) {
          const user = JSON.parse(userStr);
          setSession({ user });
        } else {
          setSession(null);
        }
      } catch (error) {
        console.error('Error loading session:', error);
        setSession(null);
      } finally {
        setIsLoading(false);
      }
    };

    loadSession();

    // Listen for storage changes (e.g., logout in another tab)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'jwt_token' || e.key === 'user') {
        loadSession();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  return { data: session, isLoading, isPending: isLoading };
}

// Function to validate token server-side (for server components)
export const validateTokenOnServer = async (token: string | null): Promise<boolean> => {
  if (!token) {
    return false;
  }

  try {
    const response = await fetch(`${API_URL}/api/auth/verify`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    return response.ok;
  } catch (error) {
    console.error('Token validation error:', error);
    return false;
  }
};

// Re-export for backward compatibility
export const useSignIn = () => signinUser;
export const useSignOut = () => signoutUser;

// Auth client object for compatibility
export const authClient = {
  signIn: signinUser,
  signOut: signoutUser,
  signUp: signupUser,
};