import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Dumbbell, Droplets, Moon, Scale, Plus } from "lucide-react";
import GlassCard from "../components/GlassCard";
import StatCard from "../components/StatCard";
import { api } from "../api/client";

interface FitnessDash {
  workouts_this_week: number;
  water_today_ml: number;
  water_goal_ml: number;
  latest_weight_kg: number | null;
  latest_sleep_quality: number | null;
}

interface Workout {
  id: string;
  workout_type: string;
  duration_minutes: number;
  calories_burned: number;
  completed_at: string;
}

export default function Fitness() {
  const [dash, setDash] = useState<FitnessDash | null>(null);
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [showAdd, setShowAdd] = useState(false);
  const [form, setForm] = useState({ workout_type: "", duration_minutes: 30, calories_burned: 0 });
  const [waterAmount, setWaterAmount] = useState(250);

  useEffect(() => {
    api.get<FitnessDash>("/fitness/dashboard").then(setDash);
    api.get<Workout[]>("/fitness/workouts").then(setWorkouts);
  }, []);

  const addWorkout = async () => {
    if (!form.workout_type.trim()) return;
    const w = await api.post<Workout>("/fitness/workouts", form);
    setWorkouts((prev) => [w, ...prev]);
    setForm({ workout_type: "", duration_minutes: 30, calories_burned: 0 });
    setShowAdd(false);
    api.get<FitnessDash>("/fitness/dashboard").then(setDash);
  };

  const logWater = async () => {
    await api.post("/fitness/water", { amount_ml: waterAmount });
    api.get<FitnessDash>("/fitness/dashboard").then(setDash);
  };

  if (!dash) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-ni-accent border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const waterPercent = Math.min(100, Math.round((dash.water_today_ml / dash.water_goal_ml) * 100));

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <h1 className="text-2xl font-bold flex items-center gap-2">
        <Dumbbell className="w-6 h-6 text-ni-rose" /> Fitness & Wellness
      </h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard icon={<Dumbbell className="w-5 h-5" />} label="Workouts" value={dash.workouts_this_week} sub="this week" glow="rose" />
        <StatCard icon={<Droplets className="w-5 h-5" />} label="Water" value={`${dash.water_today_ml}ml`} sub={`of ${dash.water_goal_ml}ml`} glow="cyan" />
        <StatCard icon={<Scale className="w-5 h-5" />} label="Weight" value={dash.latest_weight_kg ? `${dash.latest_weight_kg}kg` : "—"} glow="amber" />
        <StatCard icon={<Moon className="w-5 h-5" />} label="Sleep Quality" value={dash.latest_sleep_quality ? `${dash.latest_sleep_quality}/10` : "—"} glow="accent" />
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Water Tracker */}
        <GlassCard glow="cyan">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <Droplets className="w-5 h-5 text-ni-cyan" /> Quick Water Log
          </h2>
          <div className="w-full bg-white/5 rounded-full h-4 mb-3">
            <div
              className="h-4 rounded-full bg-gradient-to-r from-ni-cyan to-ni-accent transition-all"
              style={{ width: `${waterPercent}%` }}
            />
          </div>
          <p className="text-sm text-ni-muted mb-4">
            {dash.water_today_ml}ml / {dash.water_goal_ml}ml ({waterPercent}%)
          </p>
          <div className="flex gap-2">
            {[150, 250, 500].map((ml) => (
              <button
                key={ml}
                onClick={() => setWaterAmount(ml)}
                className={`px-3 py-1.5 rounded-lg text-sm transition ${waterAmount === ml ? "bg-ni-cyan/20 text-ni-cyan" : "bg-white/5 text-ni-muted hover:bg-white/10"}`}
              >
                {ml}ml
              </button>
            ))}
            <button
              onClick={logWater}
              className="px-4 py-1.5 rounded-lg bg-ni-cyan/20 text-ni-cyan text-sm hover:bg-ni-cyan/30 transition ml-auto"
            >
              + Log
            </button>
          </div>
        </GlassCard>

        {/* Add Workout */}
        <GlassCard glow="rose">
          <div className="flex justify-between items-center mb-4">
            <h2 className="font-semibold flex items-center gap-2">
              <Dumbbell className="w-5 h-5 text-ni-rose" /> Log Workout
            </h2>
            <button onClick={() => setShowAdd(!showAdd)} className="text-ni-rose">
              <Plus className="w-5 h-5" />
            </button>
          </div>
          {showAdd && (
            <div className="space-y-3 mb-4">
              <input
                placeholder="Workout type (e.g., Running)"
                value={form.workout_type}
                onChange={(e) => setForm({ ...form, workout_type: e.target.value })}
                className="w-full text-sm"
              />
              <div className="flex gap-3">
                <input
                  type="number"
                  placeholder="Minutes"
                  value={form.duration_minutes}
                  onChange={(e) => setForm({ ...form, duration_minutes: Number(e.target.value) })}
                  className="flex-1 text-sm"
                />
                <input
                  type="number"
                  placeholder="Calories"
                  value={form.calories_burned}
                  onChange={(e) => setForm({ ...form, calories_burned: Number(e.target.value) })}
                  className="flex-1 text-sm"
                />
              </div>
              <button
                onClick={addWorkout}
                className="px-4 py-2 rounded-xl bg-ni-rose/20 text-ni-rose text-sm hover:bg-ni-rose/30 transition"
              >
                Save Workout
              </button>
            </div>
          )}
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {workouts.slice(0, 5).map((w) => (
              <div key={w.id} className="flex justify-between items-center p-2 rounded-lg bg-white/5 text-sm">
                <span className="font-medium">{w.workout_type}</span>
                <span className="text-ni-muted">{w.duration_minutes}min · {w.calories_burned}cal</span>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </motion.div>
  );
}
