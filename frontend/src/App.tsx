import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./auth/AuthContext";
import Login from "./auth/Login";
import Register from "./auth/Register";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
import Tasks from "./pages/Tasks";
import Memory from "./pages/Memory";
import Fitness from "./pages/Fitness";
import Finance from "./pages/Finance";
import Study from "./pages/Study";
import Devices from "./pages/Devices";
import Settings from "./pages/Settings";

function ProtectedRoutes() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-ni-bg bg-mesh">
        <div className="w-10 h-10 border-2 border-ni-accent border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!user) return <Navigate to="/login" />;

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/memory" element={<Memory />} />
        <Route path="/fitness" element={<Fitness />} />
        <Route path="/finance" element={<Finance />} />
        <Route path="/study" element={<Study />} />
        <Route path="/devices" element={<Devices />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Layout>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/*" element={<ProtectedRoutes />} />
      </Routes>
    </AuthProvider>
  );
}
