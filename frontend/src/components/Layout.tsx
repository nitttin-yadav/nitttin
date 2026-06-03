import { useState, type ReactNode } from "react";
import { Menu } from "lucide-react";
import Sidebar from "./Sidebar";

export default function Layout({ children }: { children: ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-ni-bg bg-mesh flex">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <main className="flex-1 min-h-screen lg:ml-0">
        {/* Mobile header */}
        <div className="lg:hidden flex items-center p-4 border-b border-ni-border">
          <button
            onClick={() => setSidebarOpen(true)}
            className="text-ni-muted hover:text-white"
          >
            <Menu className="w-6 h-6" />
          </button>
          <span className="ml-3 text-lg font-bold bg-gradient-to-r from-ni-accent-light to-ni-cyan bg-clip-text text-transparent">
            Ni
          </span>
        </div>

        <div className="p-4 md:p-6 lg:p-8 max-w-7xl mx-auto">{children}</div>
      </main>
    </div>
  );
}
