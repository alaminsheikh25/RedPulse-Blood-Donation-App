import { create } from "zustand";
import { api } from "../lib/api";

interface AuthState {
  token: string | null;
  user: { id: string; email: string; full_name: string; role: string } | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, full_name: string, role?: string) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
}

export const useAuth = create<AuthState>((set) => ({
  token: localStorage.getItem("access_token"),
  user: null,
  loading: false,
  login: async (email, password) => {
    set({ loading: true });
    try {
      const { data } = await api.post("/auth/login", { email, password });
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      set({ token: data.access_token });
      const me = await api.get("/auth/me");
      set({ user: me.data });
    } finally {
      set({ loading: false });
    }
  },
  register: async (email, password, full_name, role) => {
    set({ loading: true });
    try {
      await api.post("/auth/register", { email, password, full_name, role: role ?? "donor" });
    } finally {
      set({ loading: false });
    }
  },
  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    set({ token: null, user: null });
  },
  fetchMe: async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return;
    try {
      const { data } = await api.get("/auth/me");
      set({ token, user: data });
    } catch {
      set({ token: null, user: null });
    }
  },
}));
