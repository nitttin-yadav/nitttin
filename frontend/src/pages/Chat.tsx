import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { Send, Plus, MessageSquare, Cpu, Trash2 } from "lucide-react";
import GlassCard from "../components/GlassCard";
import { api } from "../api/client";

interface Conversation {
  id: string;
  title: string;
  created_at: string;
}

interface Message {
  id: string;
  role: string;
  content: string;
  created_at: string;
}

export default function Chat() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.get<Conversation[]>("/conversations/").then((c) => {
      setConversations(c);
      if (c.length > 0 && !activeId) setActiveId(c[0].id);
    });
  }, []);

  useEffect(() => {
    if (activeId) {
      api
        .get<{ messages: Message[] }>(`/conversations/${activeId}`)
        .then((d) => setMessages(d.messages));
    }
  }, [activeId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const createConversation = async () => {
    const c = await api.post<Conversation>("/conversations/", {
      title: "New Chat",
    });
    setConversations((prev) => [c, ...prev]);
    setActiveId(c.id);
    setMessages([]);
  };

  const sendMessage = async () => {
    if (!input.trim() || !activeId || sending) return;
    setSending(true);
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: input,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    try {
      const aiMsg = await api.post<Message>(
        `/conversations/${activeId}/messages`,
        { content: input }
      );
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
    } finally {
      setSending(false);
    }
  };

  const deleteConversation = async (id: string) => {
    await api.delete(`/conversations/${id}`);
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeId === id) {
      setActiveId(null);
      setMessages([]);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex gap-4 h-[calc(100vh-120px)] lg:h-[calc(100vh-80px)]"
    >
      {/* Sidebar */}
      <div className="hidden md:flex flex-col w-64 glass rounded-2xl">
        <div className="p-4 border-b border-ni-border">
          <button
            onClick={createConversation}
            className="w-full flex items-center justify-center gap-2 py-2 rounded-xl bg-ni-accent/20 text-ni-accent-light hover:bg-ni-accent/30 transition text-sm font-medium"
          >
            <Plus className="w-4 h-4" /> New Chat
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {conversations.map((c) => (
            <div
              key={c.id}
              onClick={() => setActiveId(c.id)}
              className={`flex items-center justify-between px-3 py-2 rounded-xl cursor-pointer text-sm group transition ${
                activeId === c.id
                  ? "bg-ni-accent/15 text-ni-accent-light"
                  : "text-ni-muted hover:bg-white/5"
              }`}
            >
              <div className="flex items-center gap-2 min-w-0">
                <MessageSquare className="w-4 h-4 flex-shrink-0" />
                <span className="truncate">{c.title}</span>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  deleteConversation(c.id);
                }}
                className="opacity-0 group-hover:opacity-100 text-ni-muted hover:text-ni-rose transition"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Chat area */}
      <div className="flex-1 flex flex-col glass rounded-2xl">
        {!activeId ? (
          <div className="flex-1 flex flex-col items-center justify-center text-ni-muted gap-4">
            <Cpu className="w-16 h-16 text-ni-accent/30" />
            <p className="text-lg font-medium">Start a conversation with Ni</p>
            <button
              onClick={createConversation}
              className="px-6 py-2 rounded-xl bg-ni-accent/20 text-ni-accent-light hover:bg-ni-accent/30 transition text-sm"
            >
              New Chat
            </button>
          </div>
        ) : (
          <>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((m) => (
                <div
                  key={m.id}
                  className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm ${
                      m.role === "user"
                        ? "bg-ni-accent/20 text-white rounded-br-md"
                        : "glass rounded-bl-md"
                    }`}
                  >
                    {m.role === "assistant" && (
                      <div className="flex items-center gap-1.5 mb-1.5">
                        <Cpu className="w-3.5 h-3.5 text-ni-cyan" />
                        <span className="text-xs font-medium text-ni-cyan">Ni</span>
                      </div>
                    )}
                    <p className="whitespace-pre-wrap">{m.content}</p>
                  </div>
                </div>
              ))}
              {sending && (
                <div className="flex justify-start">
                  <div className="glass rounded-2xl rounded-bl-md px-4 py-3">
                    <div className="flex items-center gap-1.5 mb-1.5">
                      <Cpu className="w-3.5 h-3.5 text-ni-cyan" />
                      <span className="text-xs font-medium text-ni-cyan">Ni</span>
                    </div>
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-ni-muted rounded-full animate-bounce" />
                      <span className="w-2 h-2 bg-ni-muted rounded-full animate-bounce [animation-delay:0.15s]" />
                      <span className="w-2 h-2 bg-ni-muted rounded-full animate-bounce [animation-delay:0.3s]" />
                    </div>
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>

            <div className="p-4 border-t border-ni-border">
              <div className="flex gap-2">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
                  placeholder="Message Ni..."
                  className="flex-1"
                />
                <button
                  onClick={sendMessage}
                  disabled={!input.trim() || sending}
                  className="px-4 py-2 rounded-xl bg-gradient-to-r from-ni-accent to-ni-accent-light text-white hover:opacity-90 disabled:opacity-50 transition"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </motion.div>
  );
}
