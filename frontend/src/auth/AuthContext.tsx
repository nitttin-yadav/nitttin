import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { api, setToken, clearToken } from "../api/client";

interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  language_preference: string;
}

interface AuthState {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (
    email: string,
    username: string,
    password: string,
    fullName: string
  ) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchMe = useCallback(async () => {
    try {
      const u = await api.get<User>("/auth/me");
      setUser(u);
    } catch {
      clearToken();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem("ni_token");
    if (token) fetchMe();
    else setLoading(false);
  }, [fetchMe]);

  const login = async (email: string, password: string) => {
    const res = await api.post<{ access_token: string }>("/auth/login", {
      email,
      password,
    });
    setToken(res.access_token);
    await fetchMe();
  };

  const register = async (
    email: string,
    username: string,
    password: string,
    fullName: string
  ) => {
    await api.post("/auth/register", {
      email,
      username,
      password,
      full_name: fullName,
    });
    await login(email, password);
  };

  const logout = () => {
    clearToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
