import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, Plus, Clock, GraduationCap } from "lucide-react";
import GlassCard from "../components/GlassCard";
import StatCard from "../components/StatCard";
import { api } from "../api/client";

interface StudyPlan {
  id: string;
  subject: string;
  goal: string;
  start_date: string;
  end_date: string | null;
  status: string;
}

interface StudySession {
  id: string;
  plan_id: string;
  topic: string;
  duration_minutes: number;
  notes: string;
  completed_at: string;
}

interface StudyDash {
  active_plans: number;
  study_hours_this_week: number;
  sessions_this_week: number;
}

export default function Study() {
  const [dash, setDash] = useState<StudyDash | null>(null);
  const [plans, setPlans] = useState<StudyPlan[]>([]);
  const [sessions, setSessions] = useState<StudySession[]>([]);
  const [showAddPlan, setShowAddPlan] = useState(false);
  const [showAddSession, setShowAddSession] = useState(false);
  const [planForm, setPlanForm] = useState({ subject: "", goal: "", start_date: new Date().toISOString().split("T")[0] });
  const [sessionForm, setSessionForm] = useState({ plan_id: "", topic: "", duration_minutes: 30, notes: "" });

  useEffect(() => {
    api.get<StudyDash>("/study/dashboard").then(setDash);
    api.get<StudyPlan[]>("/study/plans").then(setPlans);
    api.get<StudySession[]>("/study/sessions").then(setSessions);
  }, []);

  const addPlan = async () => {
    if (!planForm.subject.trim()) return;
    const p = await api.post<StudyPlan>("/study/plans", planForm);
    setPlans((prev) => [p, ...prev]);
    setPlanForm({ subject: "", goal: "", start_date: new Date().toISOString().split("T")[0] });
    setShowAddPlan(false);
    api.get<StudyDash>("/study/dashboard").then(setDash);
  };

  const addSession = async () => {
    if (!sessionForm.plan_id || !sessionForm.topic.trim()) return;
    const s = await api.post<StudySession>("/study/sessions", sessionForm);
    setSessions((prev) => [s, ...prev]);
    setSessionForm({ plan_id: "", topic: "", duration_minutes: 30, notes: "" });
    setShowAddSession(false);
    api.get<StudyDash>("/study/dashboard").then(setDash);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <h1 className="text-2xl font-bold flex items-center gap-2">
        <BookOpen className="w-6 h-6 text-ni-emerald" /> Study & Career
      </h1>

      {dash && (
        <div className="grid grid-cols-3 gap-4">
          <StatCard icon={<GraduationCap className="w-5 h-5" />} label="Active Plans" value={dash.active_plans} glow="emerald" />
          <StatCard icon={<Clock className="w-5 h-5" />} label="Hours This Week" value={`${dash.study_hours_this_week}h`} glow="cyan" />
          <StatCard icon={<BookOpen className="w-5 h-5" />} label="Sessions" value={dash.sessions_this_week} sub="this week" glow="accent" />
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        {/* Study Plans */}
        <GlassCard glow="emerald">
          <div className="flex justify-between items-center mb-4">
            <h2 className="font-semibold flex items-center gap-2">
              <GraduationCap className="w-5 h-5 text-ni-emerald" /> Study Plans
            </h2>
            <button onClick={() => setShowAddPlan(!showAddPlan)} className="text-ni-emerald">
              <Plus className="w-5 h-5" />
            </button>
          </div>
          {showAddPlan && (
            <div className="space-y-3 mb-4">
              <input placeholder="Subject" value={planForm.subject} onChange={(e) => setPlanForm({ ...planForm, subject: e.target.value })} className="w-full text-sm" />
              <input placeholder="Goal" value={planForm.goal} onChange={(e) => setPlanForm({ ...planForm, goal: e.target.value })} className="w-full text-sm" />
              <button onClick={addPlan} className="px-4 py-2 rounded-xl bg-ni-emerald/20 text-ni-emerald text-sm hover:bg-ni-emerald/30 transition">
                Create Plan
              </button>
            </div>
          )}
          <div className="space-y-3">
            {plans.map((p) => (
              <div key={p.id} className="p-3 rounded-xl bg-white/5">
                <div className="flex justify-between items-center">
                  <span className="font-medium text-sm">{p.subject}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-md ${p.status === "active" ? "bg-ni-emerald/20 text-ni-emerald" : "bg-white/10 text-ni-muted"}`}>
                    {p.status}
                  </span>
                </div>
                {p.goal && <p className="text-xs text-ni-muted mt-1">{p.goal}</p>}
              </div>
            ))}
            {plans.length === 0 && <p className="text-sm text-ni-muted text-center py-4">No plans yet</p>}
          </div>
        </GlassCard>

        {/* Study Sessions */}
        <GlassCard glow="cyan">
          <div className="flex justify-between items-center mb-4">
            <h2 className="font-semibold flex items-center gap-2">
              <Clock className="w-5 h-5 text-ni-cyan" /> Recent Sessions
            </h2>
            <button onClick={() => setShowAddSession(!showAddSession)} className="text-ni-cyan">
              <Plus className="w-5 h-5" />
            </button>
          </div>
          {showAddSession && (
            <div className="space-y-3 mb-4">
              <select
                value={sessionForm.plan_id}
                onChange={(e) => setSessionForm({ ...sessionForm, plan_id: e.target.value })}
                className="w-full text-sm"
              >
                <option value="">Select plan...</option>
                {plans.filter((p) => p.status === "active").map((p) => (
                  <option key={p.id} value={p.id}>{p.subject}</option>
                ))}
              </select>
              <input placeholder="Topic" value={sessionForm.topic} onChange={(e) => setSessionForm({ ...sessionForm, topic: e.target.value })} className="w-full text-sm" />
              <input type="number" placeholder="Duration (min)" value={sessionForm.duration_minutes} onChange={(e) => setSessionForm({ ...sessionForm, duration_minutes: Number(e.target.value) })} className="w-full text-sm" />
              <button onClick={addSession} className="px-4 py-2 rounded-xl bg-ni-cyan/20 text-ni-cyan text-sm hover:bg-ni-cyan/30 transition">
                Log Session
              </button>
            </div>
          )}
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {sessions.map((s) => (
              <div key={s.id} className="flex justify-between items-center p-2 rounded-lg bg-white/5 text-sm">
                <span className="font-medium">{s.topic}</span>
                <span className="text-ni-muted">{s.duration_minutes}min</span>
              </div>
            ))}
            {sessions.length === 0 && <p className="text-sm text-ni-muted text-center py-4">No sessions logged</p>}
          </div>
        </GlassCard>
      </div>
    </motion.div>
  );
}
