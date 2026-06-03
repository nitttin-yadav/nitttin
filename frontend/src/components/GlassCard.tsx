import { motion } from "framer-motion";
import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
  className?: string;
  glow?: "accent" | "cyan" | "emerald" | "rose" | "amber";
  onClick?: () => void;
}

const glowMap = {
  accent: "hover:shadow-[0_0_20px_rgba(99,102,241,0.15)]",
  cyan: "hover:shadow-[0_0_20px_rgba(34,211,238,0.15)]",
  emerald: "hover:shadow-[0_0_20px_rgba(52,211,153,0.15)]",
  rose: "hover:shadow-[0_0_20px_rgba(251,113,133,0.15)]",
  amber: "hover:shadow-[0_0_20px_rgba(251,191,36,0.15)]",
};

export default function GlassCard({
  children,
  className = "",
  glow,
  onClick,
}: Props) {
  return (
    <motion.div
      whileHover={{ scale: 1.01 }}
      transition={{ type: "spring", stiffness: 400, damping: 30 }}
      onClick={onClick}
      className={`glass glass-hover rounded-2xl p-5 transition-all duration-300 ${glow ? glowMap[glow] : ""} ${onClick ? "cursor-pointer" : ""} ${className}`}
    >
      {children}
    </motion.div>
  );
}
