import { useState } from "react";
import { motion } from "framer-motion";
import { Settings as SettingsIcon, User, Globe, Sparkles } from "lucide-react";
import GlassCard from "../components/GlassCard";
import { useAuth } from "../auth/AuthContext";
import { api } from "../api/client";

export default function Settings() {
  const { user } = useAuth();
  const [fullName, setFullName] = useState(user?.full_name || "");
  const [language, setLanguage] = useState(user?.language_preference || "en");
  const [saved, setSaved] = useState(false);

  const save = async () => {
    await api.patch("/auth/me", { full_name: fullName, language_preference: language });
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6 max-w-2xl">
      <h1 className="text-2xl font-bold flex items-center gap-2">
        <SettingsIcon className="w-6 h-6 text-ni-muted" /> Settings
      </h1>

      <GlassCard>
        <h2 className="font-semibold mb-4 flex items-center gap-2">
          <User className="w-5 h-5 text-ni-accent-light" /> Profile
        </h2>
        <div className="space-y-4">
          <div>
            <label className="text-sm text-ni-muted block mb-1">Full Name</label>
            <input value={fullName} onChange={(e) => setFullName(e.target.value)} className="w-full" />
          </div>
          <div>
            <label className="text-sm text-ni-muted block mb-1">Email</label>
            <input value={user?.email || ""} disabled className="w-full opacity-50" />
          </div>
          <div>
            <label className="text-sm text-ni-muted block mb-1">Username</label>
            <input value={user?.username || ""} disabled className="w-full opacity-50" />
          </div>
        </div>
      </GlassCard>

      <GlassCard>
        <h2 className="font-semibold mb-4 flex items-center gap-2">
          <Globe className="w-5 h-5 text-ni-cyan" /> Language
        </h2>
        <select value={language} onChange={(e) => setLanguage(e.target.value)} className="w-full">
          <option value="en">English</option>
          <option value="hi">Hindi (हिन्दी)</option>
        </select>
      </GlassCard>

      <GlassCard>
        <h2 className="font-semibold mb-4 flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-ni-amber" /> AI Personality
        </h2>
        <p className="text-sm text-ni-muted mb-3">
          Configure how Ni interacts with you. Personality customization coming soon.
        </p>
        <div className="flex gap-2">
          {["Professional", "Friendly", "Casual", "Motivational"].map((p) => (
            <button key={p} className="px-3 py-1.5 rounded-lg bg-white/5 text-sm text-ni-muted hover:bg-ni-accent/20 hover:text-ni-accent-light transition">
              {p}
            </button>
          ))}
        </div>
      </GlassCard>

      <button
        onClick={save}
        className="px-6 py-3 rounded-xl bg-gradient-to-r from-ni-accent to-ni-accent-light text-white font-semibold hover:opacity-90 transition"
      >
        {saved ? "Saved!" : "Save Changes"}
      </button>
    </motion.div>
  );
}
