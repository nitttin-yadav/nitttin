import type { ReactNode } from "react";
import GlassCard from "./GlassCard";

interface Props {
  icon: ReactNode;
  label: string;
  value: string | number;
  sub?: string;
  glow?: "accent" | "cyan" | "emerald" | "rose" | "amber";
}

export default function StatCard({ icon, label, value, sub, glow }: Props) {
  return (
    <GlassCard glow={glow}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-ni-muted text-xs font-medium uppercase tracking-wider mb-1">
            {label}
          </p>
          <p className="text-2xl font-bold">{value}</p>
          {sub && <p className="text-ni-muted text-xs mt-1">{sub}</p>}
        </div>
        <div className="text-ni-muted">{icon}</div>
      </div>
    </GlassCard>
  );
}
