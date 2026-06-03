import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Wallet, Plus, PieChart, PiggyBank } from "lucide-react";
import GlassCard from "../components/GlassCard";
import { api } from "../api/client";

interface Expense {
  id: string;
  amount: number;
  category: string;
  description: string;
  expense_date: string;
}

interface Budget {
  id: string;
  category: string;
  monthly_limit: number;
}

interface SavingsGoal {
  id: string;
  title: string;
  target_amount: number;
  current_amount: number;
}

interface Report {
  total_spent: number;
  breakdown: Record<string, number>;
  budget_status: { category: string; limit: number; spent: number; remaining: number }[];
}

export default function Finance() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [report, setReport] = useState<Report | null>(null);
  const [savings, setSavings] = useState<SavingsGoal[]>([]);
  const [showAdd, setShowAdd] = useState(false);
  const [form, setForm] = useState({ amount: 0, category: "food", description: "", expense_date: new Date().toISOString().split("T")[0] });

  useEffect(() => {
    api.get<Expense[]>("/finance/expenses").then(setExpenses);
    api.get<Report>("/finance/report").then(setReport);
    api.get<SavingsGoal[]>("/finance/savings").then(setSavings);
  }, []);

  const addExpense = async () => {
    if (!form.amount) return;
    const exp = await api.post<Expense>("/finance/expenses", form);
    setExpenses((prev) => [exp, ...prev]);
    setForm({ amount: 0, category: "food", description: "", expense_date: new Date().toISOString().split("T")[0] });
    setShowAdd(false);
    api.get<Report>("/finance/report").then(setReport);
  };

  const categories = ["food", "transport", "shopping", "entertainment", "bills", "health", "education", "other"];
  const catColors: Record<string, string> = {
    food: "bg-ni-amber/20 text-ni-amber",
    transport: "bg-ni-cyan/20 text-ni-cyan",
    shopping: "bg-ni-rose/20 text-ni-rose",
    entertainment: "bg-ni-accent/20 text-ni-accent-light",
    bills: "bg-red-500/20 text-red-400",
    health: "bg-ni-emerald/20 text-ni-emerald",
    education: "bg-blue-500/20 text-blue-400",
    other: "bg-white/10 text-ni-muted",
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Wallet className="w-6 h-6 text-ni-amber" /> Finance Dashboard
        </h1>
        <button
          onClick={() => setShowAdd(!showAdd)}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-ni-amber/20 text-ni-amber hover:bg-ni-amber/30 transition text-sm"
        >
          <Plus className="w-4 h-4" /> Add Expense
        </button>
      </div>

      {/* Add expense form */}
      {showAdd && (
        <GlassCard>
          <div className="grid md:grid-cols-4 gap-3">
            <input
              type="number"
              placeholder="Amount (₹)"
              value={form.amount || ""}
              onChange={(e) => setForm({ ...form, amount: Number(e.target.value) })}
              className="text-sm"
            />
            <select
              value={form.category}
              onChange={(e) => setForm({ ...form, category: e.target.value })}
              className="text-sm"
            >
              {categories.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
            <input
              placeholder="Description"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              className="text-sm"
            />
            <button
              onClick={addExpense}
              className="px-4 py-2 rounded-xl bg-ni-amber/20 text-ni-amber text-sm hover:bg-ni-amber/30 transition"
            >
              Save
            </button>
          </div>
        </GlassCard>
      )}

      <div className="grid md:grid-cols-3 gap-6">
        {/* Monthly Summary */}
        <GlassCard glow="amber" className="md:col-span-2">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <PieChart className="w-5 h-5 text-ni-amber" /> Monthly Overview
          </h2>
          {report && (
            <>
              <p className="text-3xl font-bold text-ni-amber mb-4">
                ₹{report.total_spent.toLocaleString()}
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                {Object.entries(report.breakdown).map(([cat, amt]) => (
                  <div key={cat} className={`p-3 rounded-xl ${catColors[cat] || catColors.other}`}>
                    <p className="text-xs font-medium capitalize">{cat}</p>
                    <p className="text-lg font-bold">₹{amt.toLocaleString()}</p>
                  </div>
                ))}
              </div>
              {report.budget_status.length > 0 && (
                <div className="mt-4 space-y-2">
                  <h3 className="text-sm font-medium text-ni-muted">Budget Status</h3>
                  {report.budget_status.map((b) => (
                    <div key={b.category}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="capitalize">{b.category}</span>
                        <span>₹{b.spent} / ₹{b.limit}</span>
                      </div>
                      <div className="w-full bg-white/5 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all ${
                            b.remaining < 0 ? "bg-ni-rose" : "bg-ni-emerald"
                          }`}
                          style={{ width: `${Math.min(100, (b.spent / b.limit) * 100)}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </GlassCard>

        {/* Savings Goals */}
        <GlassCard glow="emerald">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <PiggyBank className="w-5 h-5 text-ni-emerald" /> Savings Goals
          </h2>
          <div className="space-y-4">
            {savings.map((s) => {
              const pct = Math.min(100, Math.round((s.current_amount / s.target_amount) * 100));
              return (
                <div key={s.id}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium">{s.title}</span>
                    <span className="text-ni-emerald">{pct}%</span>
                  </div>
                  <div className="w-full bg-white/5 rounded-full h-2 mb-1">
                    <div
                      className="h-2 rounded-full bg-gradient-to-r from-ni-emerald to-ni-cyan transition-all"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                  <p className="text-xs text-ni-muted">
                    ₹{s.current_amount.toLocaleString()} / ₹{s.target_amount.toLocaleString()}
                  </p>
                </div>
              );
            })}
            {savings.length === 0 && (
              <p className="text-sm text-ni-muted text-center py-4">No savings goals yet</p>
            )}
          </div>
        </GlassCard>
      </div>

      {/* Recent Expenses */}
      <GlassCard>
        <h2 className="font-semibold mb-4">Recent Expenses</h2>
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {expenses.map((e) => (
            <div key={e.id} className="flex items-center justify-between p-3 rounded-xl bg-white/5 text-sm">
              <div>
                <span className={`inline-block px-2 py-0.5 rounded-md text-xs mr-2 ${catColors[e.category] || catColors.other}`}>
                  {e.category}
                </span>
                <span>{e.description || "Expense"}</span>
              </div>
              <div className="text-right">
                <p className="font-medium">₹{e.amount}</p>
                <p className="text-xs text-ni-muted">{e.expense_date}</p>
              </div>
            </div>
          ))}
          {expenses.length === 0 && (
            <p className="text-sm text-ni-muted text-center py-4">No expenses this month</p>
          )}
        </div>
      </GlassCard>
    </motion.div>
  );
}
