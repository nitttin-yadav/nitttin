import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Brain, Plus, Search, Tag, StickyNote, Trash2 } from "lucide-react";
import GlassCard from "../components/GlassCard";
import { api } from "../api/client";

interface MemoryItem {
  id: string;
  category: string;
  title: string;
  content: string;
  tags: string[] | null;
  importance: number;
  created_at: string;
}

interface NoteItem {
  id: string;
  title: string;
  content: string;
  tags: string[] | null;
  created_at: string;
}

export default function Memory() {
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [notes, setNotes] = useState<NoteItem[]>([]);
  const [search, setSearch] = useState("");
  const [tab, setTab] = useState<"memories" | "notes">("memories");
  const [showAdd, setShowAdd] = useState(false);
  const [form, setForm] = useState({ title: "", content: "", category: "general", tags: "" });

  useEffect(() => {
    loadData();
  }, [search]);

  const loadData = () => {
    const params = search ? `?search=${encodeURIComponent(search)}` : "";
    api.get<MemoryItem[]>(`/memory/${params}`).then(setMemories);
    api.get<NoteItem[]>("/memory/notes").then(setNotes);
  };

  const addMemory = async () => {
    if (!form.title.trim()) return;
    await api.post("/memory/", {
      ...form,
      tags: form.tags
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean),
    });
    setForm({ title: "", content: "", category: "general", tags: "" });
    setShowAdd(false);
    loadData();
  };

  const addNote = async () => {
    if (!form.title.trim()) return;
    await api.post("/memory/notes", {
      title: form.title,
      content: form.content,
      tags: form.tags
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean),
    });
    setForm({ title: "", content: "", category: "general", tags: "" });
    setShowAdd(false);
    loadData();
  };

  const deleteMemory = async (id: string) => {
    await api.delete(`/memory/${id}`);
    setMemories((prev) => prev.filter((m) => m.id !== id));
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Brain className="w-6 h-6 text-ni-accent-light" /> Memory System
        </h1>
        <button
          onClick={() => setShowAdd(!showAdd)}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-ni-accent/20 text-ni-accent-light hover:bg-ni-accent/30 transition text-sm"
        >
          <Plus className="w-4 h-4" /> Add {tab === "memories" ? "Memory" : "Note"}
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ni-muted" />
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search memories..."
          className="w-full pl-10"
        />
      </div>

      {/* Tabs */}
      <div className="flex gap-2">
        <button
          onClick={() => setTab("memories")}
          className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
            tab === "memories" ? "bg-ni-accent/20 text-ni-accent-light" : "text-ni-muted hover:bg-white/5"
          }`}
        >
          <Brain className="w-4 h-4 inline mr-1" /> Memories ({memories.length})
        </button>
        <button
          onClick={() => setTab("notes")}
          className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
            tab === "notes" ? "bg-ni-accent/20 text-ni-accent-light" : "text-ni-muted hover:bg-white/5"
          }`}
        >
          <StickyNote className="w-4 h-4 inline mr-1" /> Notes ({notes.length})
        </button>
      </div>

      {/* Add form */}
      {showAdd && (
        <GlassCard>
          <div className="space-y-3">
            <input
              placeholder="Title"
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              className="w-full text-sm"
            />
            <textarea
              placeholder="Content"
              value={form.content}
              onChange={(e) => setForm({ ...form, content: e.target.value })}
              className="w-full text-sm h-24 resize-none"
            />
            <input
              placeholder="Tags (comma separated)"
              value={form.tags}
              onChange={(e) => setForm({ ...form, tags: e.target.value })}
              className="w-full text-sm"
            />
            <button
              onClick={tab === "memories" ? addMemory : addNote}
              className="px-4 py-2 rounded-xl bg-ni-accent/20 text-ni-accent-light text-sm hover:bg-ni-accent/30 transition"
            >
              Save
            </button>
          </div>
        </GlassCard>
      )}

      {/* List */}
      <div className="grid md:grid-cols-2 gap-4">
        {tab === "memories"
          ? memories.map((m) => (
              <GlassCard key={m.id}>
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-medium text-sm">{m.title}</h3>
                  <button onClick={() => deleteMemory(m.id)} className="text-ni-muted hover:text-ni-rose">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
                <p className="text-sm text-ni-muted line-clamp-3">{m.content}</p>
                {m.tags && m.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-3">
                    {m.tags.map((t) => (
                      <span
                        key={t}
                        className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-ni-accent/10 text-ni-accent-light text-xs"
                      >
                        <Tag className="w-3 h-3" /> {t}
                      </span>
                    ))}
                  </div>
                )}
                <p className="text-xs text-ni-muted mt-2">{m.category} · importance: {m.importance}/10</p>
              </GlassCard>
            ))
          : notes.map((n) => (
              <GlassCard key={n.id}>
                <h3 className="font-medium text-sm mb-2">{n.title}</h3>
                <p className="text-sm text-ni-muted line-clamp-3">{n.content}</p>
                {n.tags && n.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-3">
                    {n.tags.map((t) => (
                      <span
                        key={t}
                        className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-ni-accent/10 text-ni-accent-light text-xs"
                      >
                        <Tag className="w-3 h-3" /> {t}
                      </span>
                    ))}
                  </div>
                )}
              </GlassCard>
            ))}
      </div>
    </motion.div>
  );
}
