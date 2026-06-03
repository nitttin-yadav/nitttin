import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  MessageSquare,
  CheckSquare,
  Brain,
  Dumbbell,
  Wallet,
  BookOpen,
  Wifi,
  Settings,
  LogOut,
  Cpu,
  X,
} from "lucide-react";
import { useAuth } from "../auth/AuthContext";

const links = [
  { to: "/", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/chat", icon: MessageSquare, label: "Ni Chat" },
  { to: "/tasks", icon: CheckSquare, label: "Tasks & Goals" },
  { to: "/memory", icon: Brain, label: "Memory" },
  { to: "/fitness", icon: Dumbbell, label: "Fitness" },
  { to: "/finance", icon: Wallet, label: "Finance" },
  { to: "/study", icon: BookOpen, label: "Study" },
  { to: "/devices", icon: Wifi, label: "Devices" },
  { to: "/settings", icon: Settings, label: "Settings" },
];

interface Props {
  open: boolean;
  onClose: () => void;
}

export default function Sidebar({ open, onClose }: Props) {
  const { logout, user } = useAuth();

  return (
    <>
      {/* Overlay for mobile */}
      {open && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <motion.aside
        initial={false}
        animate={{ x: open ? 0 : -280 }}
        className={`fixed top-0 left-0 z-50 h-screen w-[260px] glass border-r border-ni-border flex flex-col lg:translate-x-0 lg:static lg:z-auto`}
      >
        {/* Logo */}
        <div className="flex items-center justify-between p-5 border-b border-ni-border">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-ni-accent to-ni-cyan flex items-center justify-center">
              <Cpu className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-ni-accent-light to-ni-cyan bg-clip-text text-transparent">
              Ni
            </span>
          </div>
          <button onClick={onClose} className="lg:hidden text-ni-muted hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Nav */}
        <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
          {links.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/"}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? "bg-ni-accent/15 text-ni-accent-light"
                    : "text-ni-muted hover:text-white hover:bg-white/5"
                }`
              }
            >
              <Icon className="w-[18px] h-[18px]" />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* User */}
        <div className="p-4 border-t border-ni-border">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-ni-accent to-ni-emerald flex items-center justify-center text-sm font-bold">
              {user?.full_name?.[0]?.toUpperCase() || user?.username?.[0]?.toUpperCase() || "N"}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{user?.full_name || user?.username}</p>
              <p className="text-xs text-ni-muted truncate">{user?.email}</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-2 text-sm text-ni-muted hover:text-ni-rose transition-colors w-full px-2"
          >
            <LogOut className="w-4 h-4" />
            Sign Out
          </button>
        </div>
      </motion.aside>
    </>
  );
}
