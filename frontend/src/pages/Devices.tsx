import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Wifi, WifiOff, Plus, Cpu, Zap, ToggleLeft, ToggleRight, Trash2 } from "lucide-react";
import GlassCard from "../components/GlassCard";
import { api } from "../api/client";

interface Device {
  id: string;
  name: string;
  device_type: string;
  ip_address: string;
  status: string;
  last_seen: string | null;
}

interface Automation {
  id: string;
  name: string;
  trigger_type: string;
  trigger_value: string;
  action_type: string;
  action_value: string;
  is_active: boolean;
}

export default function Devices() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [automations, setAutomations] = useState<Automation[]>([]);
  const [showAddDevice, setShowAddDevice] = useState(false);
  const [showAddAuto, setShowAddAuto] = useState(false);
  const [deviceForm, setDeviceForm] = useState({ name: "", device_type: "arduino", ip_address: "" });
  const [autoForm, setAutoForm] = useState({ name: "", trigger_type: "time", trigger_value: "", action_type: "command", action_value: "" });

  useEffect(() => {
    api.get<Device[]>("/devices/").then(setDevices);
    api.get<Automation[]>("/devices/automations").then(setAutomations);
  }, []);

  const addDevice = async () => {
    if (!deviceForm.name.trim()) return;
    const d = await api.post<Device>("/devices/", deviceForm);
    setDevices((prev) => [...prev, d]);
    setDeviceForm({ name: "", device_type: "arduino", ip_address: "" });
    setShowAddDevice(false);
  };

  const deleteDevice = async (id: string) => {
    await api.delete(`/devices/${id}`);
    setDevices((prev) => prev.filter((d) => d.id !== id));
  };

  const addAutomation = async () => {
    if (!autoForm.name.trim()) return;
    const a = await api.post<Automation>("/devices/automations", autoForm);
    setAutomations((prev) => [...prev, a]);
    setAutoForm({ name: "", trigger_type: "time", trigger_value: "", action_type: "command", action_value: "" });
    setShowAddAuto(false);
  };

  const toggleAutomation = async (id: string) => {
    const res = await api.patch<{ is_active: boolean }>(`/devices/automations/${id}/toggle`);
    setAutomations((prev) =>
      prev.map((a) => (a.id === id ? { ...a, is_active: res.is_active } : a))
    );
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <h1 className="text-2xl font-bold flex items-center gap-2">
        <Wifi className="w-6 h-6 text-ni-cyan" /> Devices & IoT
      </h1>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Devices */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="font-semibold">Connected Devices</h2>
            <button
              onClick={() => setShowAddDevice(!showAddDevice)}
              className="flex items-center gap-1 px-3 py-1.5 rounded-xl bg-ni-cyan/20 text-ni-cyan text-sm hover:bg-ni-cyan/30 transition"
            >
              <Plus className="w-4 h-4" /> Add
            </button>
          </div>

          {showAddDevice && (
            <GlassCard>
              <div className="space-y-3">
                <input placeholder="Device name" value={deviceForm.name} onChange={(e) => setDeviceForm({ ...deviceForm, name: e.target.value })} className="w-full text-sm" />
                <input placeholder="IP address" value={deviceForm.ip_address} onChange={(e) => setDeviceForm({ ...deviceForm, ip_address: e.target.value })} className="w-full text-sm" />
                <select value={deviceForm.device_type} onChange={(e) => setDeviceForm({ ...deviceForm, device_type: e.target.value })} className="w-full text-sm">
                  <option value="arduino">Arduino</option>
                  <option value="esp32">ESP32</option>
                  <option value="raspberry_pi">Raspberry Pi</option>
                  <option value="sensor">Sensor</option>
                  <option value="smart_device">Smart Device</option>
                </select>
                <button onClick={addDevice} className="px-4 py-2 rounded-xl bg-ni-cyan/20 text-ni-cyan text-sm hover:bg-ni-cyan/30 transition">
                  Register Device
                </button>
              </div>
            </GlassCard>
          )}

          {devices.map((d) => (
            <GlassCard key={d.id} glow={d.status === "online" ? "cyan" : undefined}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${d.status === "online" ? "bg-ni-cyan/20" : "bg-white/5"}`}>
                    <Cpu className={`w-5 h-5 ${d.status === "online" ? "text-ni-cyan" : "text-ni-muted"}`} />
                  </div>
                  <div>
                    <p className="font-medium text-sm">{d.name}</p>
                    <p className="text-xs text-ni-muted">
                      {d.device_type} · {d.ip_address || "no IP"}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1.5">
                    {d.status === "online" ? (
                      <Wifi className="w-4 h-4 text-ni-emerald" />
                    ) : (
                      <WifiOff className="w-4 h-4 text-ni-muted" />
                    )}
                    <span className={`text-xs ${d.status === "online" ? "text-ni-emerald" : "text-ni-muted"}`}>
                      {d.status}
                    </span>
                  </div>
                  <button onClick={() => deleteDevice(d.id)} className="text-ni-muted hover:text-ni-rose">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </GlassCard>
          ))}

          {devices.length === 0 && (
            <GlassCard>
              <p className="text-sm text-ni-muted text-center py-4">No devices registered</p>
            </GlassCard>
          )}
        </div>

        {/* Automations */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="font-semibold flex items-center gap-2">
              <Zap className="w-5 h-5 text-ni-amber" /> Automations
            </h2>
            <button
              onClick={() => setShowAddAuto(!showAddAuto)}
              className="flex items-center gap-1 px-3 py-1.5 rounded-xl bg-ni-amber/20 text-ni-amber text-sm hover:bg-ni-amber/30 transition"
            >
              <Plus className="w-4 h-4" /> Add
            </button>
          </div>

          {showAddAuto && (
            <GlassCard>
              <div className="space-y-3">
                <input placeholder="Automation name" value={autoForm.name} onChange={(e) => setAutoForm({ ...autoForm, name: e.target.value })} className="w-full text-sm" />
                <select value={autoForm.trigger_type} onChange={(e) => setAutoForm({ ...autoForm, trigger_type: e.target.value })} className="w-full text-sm">
                  <option value="time">Time-based</option>
                  <option value="sensor">Sensor-based</option>
                  <option value="event">Event-based</option>
                </select>
                <input placeholder="Trigger value" value={autoForm.trigger_value} onChange={(e) => setAutoForm({ ...autoForm, trigger_value: e.target.value })} className="w-full text-sm" />
                <select value={autoForm.action_type} onChange={(e) => setAutoForm({ ...autoForm, action_type: e.target.value })} className="w-full text-sm">
                  <option value="command">Command</option>
                  <option value="notification">Notification</option>
                  <option value="api_call">API Call</option>
                </select>
                <input placeholder="Action value" value={autoForm.action_value} onChange={(e) => setAutoForm({ ...autoForm, action_value: e.target.value })} className="w-full text-sm" />
                <button onClick={addAutomation} className="px-4 py-2 rounded-xl bg-ni-amber/20 text-ni-amber text-sm hover:bg-ni-amber/30 transition">
                  Create
                </button>
              </div>
            </GlassCard>
          )}

          {automations.map((a) => (
            <GlassCard key={a.id}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-sm">{a.name}</p>
                  <p className="text-xs text-ni-muted">
                    {a.trigger_type}: {a.trigger_value} → {a.action_type}
                  </p>
                </div>
                <button onClick={() => toggleAutomation(a.id)}>
                  {a.is_active ? (
                    <ToggleRight className="w-8 h-8 text-ni-emerald" />
                  ) : (
                    <ToggleLeft className="w-8 h-8 text-ni-muted" />
                  )}
                </button>
              </div>
            </GlassCard>
          ))}

          {automations.length === 0 && (
            <GlassCard>
              <p className="text-sm text-ni-muted text-center py-4">No automations yet</p>
            </GlassCard>
          )}
        </div>
      </div>
    </motion.div>
  );
}
