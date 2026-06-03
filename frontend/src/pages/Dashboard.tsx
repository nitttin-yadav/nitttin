import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  CheckSquare,
  Target,
  BookOpen,
  Dumbbell,
  Droplets,
  Wallet,
  StickyNote,
  Wifi,
  Calendar,
} from "lucide-react";
import StatCard from "../components/StatCard";
import GlassCard from "../components/GlassCard";
import { api } from "../api/client";

interface DashboardData {
  greeting: string;
  tasks: { pending: number; due_today: number };
  goals: { active: number };
  study: { hours_this_week: number; active_plans: number };
  fitness: { workouts_this_week: number; water_today_ml: number; water_goal_ml: number };
  finance: { month_spent: number };
  notes: { total: number };
  upcoming_events: { title: string; start: string; location: string }[];
  devices: { online: number; total: number };
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    api.get<DashboardData>("/dashboard/").then(setData).catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-ni-accent border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const waterPercent = Math.min(
    100,
    Math.round((data.fitness.water_today_ml / data.fitness.water_goal_ml) * 100)
  );

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold">{data.greeting}</h1>
        <p className="text-ni-muted mt-1">Here's your life at a glance.</p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          icon={<CheckSquare className="w-5 h-5" />}
          label="Pending Tasks"
          value={data.tasks.pending}
          sub={`${data.tasks.due_today} due today`}
          glow="accent"
        />
        <StatCard
          icon={<Target className="w-5 h-5" />}
          label="Active Goals"
          value={data.goals.active}
          glow="cyan"
        />
        <StatCard
          icon={<BookOpen className="w-5 h-5" />}
          label="Study Hours"
          value={`${data.study.hours_this_week}h`}
          sub="this week"
          glow="emerald"
        />
        <StatCard
          icon={<Dumbbell className="w-5 h-5" />}
          label="Workouts"
          value={data.fitness.workouts_this_week}
          sub="this week"
          glow="rose"
        />
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        {/* Water Progress */}
        <GlassCard glow="cyan">
          <div className="flex items-center gap-2 mb-3">
            <Droplets className="w-5 h-5 text-ni-cyan" />
            <h3 className="font-semibold">Water Intake</h3>
          </div>
          <div className="w-full bg-white/5 rounded-full h-3 mb-2">
            <div
              className="h-3 rounded-full bg-gradient-to-r from-ni-cyan to-ni-accent transition-all"
              style={{ width: `${waterPercent}%` }}
            />
          </div>
          <p className="text-sm text-ni-muted">
            {data.fitness.water_today_ml}ml / {data.fitness.water_goal_ml}ml
          </p>
        </GlassCard>

        {/* Finance */}
        <GlassCard glow="amber">
          <div className="flex items-center gap-2 mb-3">
            <Wallet className="w-5 h-5 text-ni-amber" />
            <h3 className="font-semibold">Month Spending</h3>
          </div>
          <p className="text-3xl font-bold text-ni-amber">
            ₹{data.finance.month_spent.toLocaleString()}
          </p>
        </GlassCard>

        {/* Quick Stats */}
        <GlassCard>
          <div className="flex items-center gap-2 mb-3">
            <StickyNote className="w-5 h-5 text-ni-muted" />
            <h3 className="font-semibold">Quick Stats</h3>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-ni-muted">Notes</span>
              <span>{data.notes.total}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-ni-muted">Study Plans</span>
              <span>{data.study.active_plans}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-ni-muted">Devices</span>
              <span>
                {data.devices.online}/{data.devices.total} online
              </span>
            </div>
          </div>
        </GlassCard>
      </div>

      {/* Upcoming Events */}
      <GlassCard>
        <div className="flex items-center gap-2 mb-4">
          <Calendar className="w-5 h-5 text-ni-accent-light" />
          <h3 className="font-semibold">Upcoming Events</h3>
        </div>
        {data.upcoming_events.length === 0 ? (
          <p className="text-ni-muted text-sm">No upcoming events</p>
        ) : (
          <div className="space-y-3">
            {data.upcoming_events.map((ev, i) => (
              <div key={i} className="flex items-center gap-3 text-sm">
                <div className="w-2 h-2 rounded-full bg-ni-accent flex-shrink-0" />
                <div className="flex-1">
                  <p className="font-medium">{ev.title}</p>
                  <p className="text-ni-muted text-xs">
                    {new Date(ev.start).toLocaleString()} {ev.location && `• ${ev.location}`}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </GlassCard>
    </motion.div>
  );
}
