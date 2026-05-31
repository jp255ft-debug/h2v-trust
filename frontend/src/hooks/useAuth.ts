"use client";

import { useState, useEffect, useCallback } from "react";
import { API_BASE_URL } from "@/lib/constants";

export interface UserContext {
  id: string;
  email: string;
  full_name: string;
  role: "admin" | "operator" | "auditor";
  tenant_id: string | null;
  tenant_name: string | null;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: UserContext;
}

const TOKEN_KEY = "h2v_admin_token";
const USER_KEY = "h2v_admin_user";

export function useAuth() {
  const [user, setUser] = useState<UserContext | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load user from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem(USER_KEY);
    const storedToken = localStorage.getItem(TOKEN_KEY);
    if (storedUser && storedToken) {
      try {
        setUser(JSON.parse(storedUser));
      } catch {
        localStorage.removeItem(USER_KEY);
        localStorage.removeItem(TOKEN_KEY);
      }
    }
    setLoading(false);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    setError(null);
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const body = await response.text().catch(() => "");
        if (response.status === 401) {
          throw new Error("Email ou senha inválidos");
        }
        throw new Error(body || `Erro ${response.status} ao fazer login`);
      }

      const data: LoginResponse = await response.json();
      
      // Store token and user
      localStorage.setItem(TOKEN_KEY, data.access_token);
      localStorage.setItem(USER_KEY, JSON.stringify(data.user));
      setUser(data.user);
      
      // Set cookie for middleware (expires in 24h)
      document.cookie = `${TOKEN_KEY}=${data.access_token}; path=/; max-age=86400; SameSite=Lax`;
      
      return data;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Erro ao conectar ao servidor";
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    // Remove cookie
    document.cookie = `${TOKEN_KEY}=; path=/; max-age=0; SameSite=Lax`;
    setUser(null);
  }, []);

  const getToken = useCallback((): string | null => {
    return localStorage.getItem(TOKEN_KEY);
  }, []);

  const isAuthenticated = user !== null;
  const isAdmin = user?.role === "admin";

  return {
    user,
    loading,
    error,
    login,
    logout,
    getToken,
    isAuthenticated,
    isAdmin,
  };
}
