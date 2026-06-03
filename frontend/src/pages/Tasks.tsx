import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Plus, CheckCircle2, Circle, Clock, Target, Flame } from "lucide-react";
import GlassCard from "../components/GlassCard";
import { api } from "../api/client";

interface Task {
  id: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  due_date: string | null;
  category: string;
}

interface Goal {
  id: string;
  title: string;
  description: string;
  progress: number;
  status: string;
  target_date: string | null;
}

interface Habit {
  id: string;
  title: string;
  frequency: string;
  streak: number;
  is_active: boolean;
}

const priorityColors: Record<string, string> = {
  urgent: "text-red-400",
  high: "text-ni-rose",
  medium: "text-ni-amber",
  low: "text-ni-emerald",
};

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [habits, setHabits] = useState<Habit[]>([]);
  const [newTask, setNewTask] = useState("");
  const [newGoal, setNewGoal] = useState("");
  const [newHabit, setNewHabit] = useState("");

  useEffect(() => {
    api.get<Task[]>("/tasks/").then(setTasks);
    api.get<Goal[]>("/tasks/goals").then(setGoals);
    api.get<Habit[]>("/tasks/habits").then(setHabits);
  }, []);

  const addTask = async () => {
    if (!newTask.trim()) return;
    const t = await api.post<Task>("/tasks/", { title: newTask });
    setTasks((prev) => [t, ...prev]);
    setNewTask("");
  };

  const toggleTask = async (task: Task) => {
    const newStatus = task.status === "completed" ? "pending" : "completed";
    const updated = await api.patch<Task>(`/tasks/${task.id}`, { status: newStatus });
    setTasks((prev) => prev.map((t) => (t.id === task.id ? updated : t)));
  };

  const addGoal = async () => {
    if (!newGoal.trim()) return;
    const g = await api.post<Goal>("/tasks/goals", { title: newGoal });
    setGoals((prev) => [g, ...prev]);
    setNewGoal("");
  };

  const addHabit = async () => {
    if (!newHabit.trim()) return;
    const h = await api.post<Habit>("/tasks/habits", { title: newHabit });
    setHabits((prev) => [...prev, h]);
    setNewHabit("");
  };

  const logHabit = async (id: string) => {
    await api.post(`/tasks/habits/${id}/log`);
    setHabits((prev) =>
      prev.map((h) => (h.id === id ? { ...h, streak: h.streak + 1 } : h))
    );
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <h1 className="text-2xl font-bold">Tasks & Goals</h1>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Tasks */}
        <div className="lg:col-span-2 space-y-4">
          <GlassCard>
            <h2 className="font-semibold mb-4 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-ni-accent-light" /> Tasks
            </h2>
            <div className="flex gap-2 mb-4">
              <input
                value={newTask}
                onChange={(e) => setNewTask(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addTask()}
                placeholder="Add a task..."
                className="flex-1 text-sm"
              />
              <button
                onClick={addTask}
                className="px-3 py-2 rounded-xl bg-ni-accent/20 text-ni-accent-light hover:bg-ni-accent/30 transition"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {tasks.map((t) => (
                <div
                  key={t.id}
                  onClick={() => toggleTask(t)}
                  className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 cursor-pointer transition group"
                >
                  {t.status === "completed" ? (
                    <CheckCircle2 className="w-5 h-5 text-ni-emerald flex-shrink-0" />
                  ) : (
                    <Circle className="w-5 h-5 text-ni-muted group-hover:text-ni-accent-light flex-shrink-0" />
                  )}
                  <span
                    className={`flex-1 text-sm ${t.status === "completed" ? "line-through text-ni-muted" : ""}`}
                  >
                    {t.title}
                  </span>
                  <span className={`text-xs font-medium ${priorityColors[t.priority] || "text-ni-muted"}`}>
                    {t.priority}
                  </span>
                  {t.due_date && (
                    <span className="text-xs text-ni-muted flex items-center gap-1">
                      <Clock className="w-3 h-3" /> {t.due_date}
                    </span>
                  )}
                </div>
              ))}
              {tasks.length === 0 && (
                <p className="text-sm text-ni-muted py-4 text-center">No tasks yet. Add one above!</p>
              )}
            </div>
          </GlassCard>

          {/* Goals */}
          <GlassCard>
            <h2 className="font-semibold mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-ni-cyan" /> Goals
            </h2>
            <div className="flex gap-2 mb-4">
              <input
                value={newGoal}
                onChange={(e) => setNewGoal(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addGoal()}
                placeholder="Add a goal..."
                className="flex-1 text-sm"
              />
              <button
                onClick={addGoal}
                className="px-3 py-2 rounded-xl bg-ni-cyan/20 text-ni-cyan hover:bg-ni-cyan/30 transition"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
            <div className="space-y-3">
              {goals.map((g) => (
                <div key={g.id} className="p-3 rounded-xl bg-white/5">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium">{g.title}</span>
                    <span className="text-xs text-ni-cyan">{g.progress}%</span>
                  </div>
                  <div className="w-full bg-white/5 rounded-full h-2">
                    <div
                      className="h-2 rounded-full bg-gradient-to-r from-ni-cyan to-ni-accent transition-all"
                      style={{ width: `${g.progress}%` }}
                    />
                  </div>
                </div>
              ))}
              {goals.length === 0 && (
                <p className="text-sm text-ni-muted py-4 text-center">No goals yet</p>
              )}
            </div>
          </GlassCard>
        </div>

        {/* Habits */}
        <div>
          <GlassCard>
            <h2 className="font-semibold mb-4 flex items-center gap-2">
              <Flame className="w-5 h-5 text-ni-rose" /> Habits
            </h2>
            <div className="flex gap-2 mb-4">
              <input
                value={newHabit}
                onChange={(e) => setNewHabit(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addHabit()}
                placeholder="New habit..."
                className="flex-1 text-sm"
              />
              <button
                onClick={addHabit}
                className="px-3 py-2 rounded-xl bg-ni-rose/20 text-ni-rose hover:bg-ni-rose/30 transition"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
            <div className="space-y-2">
              {habits.map((h) => (
                <div
                  key={h.id}
                  className="flex items-center justify-between p-3 rounded-xl bg-white/5"
                >
                  <div>
                    <p className="text-sm font-medium">{h.title}</p>
                    <p className="text-xs text-ni-muted">
                      {h.frequency} · {h.streak} day streak
                    </p>
                  </div>
                  <button
                    onClick={() => logHabit(h.id)}
                    className="px-3 py-1 rounded-lg bg-ni-emerald/20 text-ni-emerald text-xs hover:bg-ni-emerald/30 transition"
                  >
                    Log
                  </button>
                </div>
              ))}
              {habits.length === 0 && (
                <p className="text-sm text-ni-muted py-4 text-center">No habits yet</p>
              )}
            </div>
          </GlassCard>
        </div>
      </div>
    </motion.div>
  );
}
