'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/dashboard/Header';
import { agenciesApi, Agency } from '@/lib/api/agencies';
import { Building2, MapPin, Plus, Snowflake } from 'lucide-react';

export default function AgenciesPage() {
  const [agencies, setAgencies] = useState<Agency[]>([]);
  const [loading, setLoading] = useState(true);

  // Modal
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState('');
  const [lat, setLat] = useState(37.7833);
  const [lng, setLng] = useState(-122.4167);
  const [demand, setDemand] = useState(120);
  const [capacity, setCapacity] = useState(250);
  const [priority, setPriority] = useState(2);
  const [refrigerated, setRefrigerated] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => { loadData(); }, []);

  async function loadData() {
    setLoading(true);
    try {
      setAgencies(await agenciesApi.list().catch(() => []));
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    try {
      await agenciesApi.create({
        name,
        latitude: Number(lat),
        longitude: Number(lng),
        demand_kg: Number(demand),
        storage_capacity_kg: Number(capacity),
        priority: Number(priority),
        requires_refrigeration: refrigerated
      });
      setShowModal(false);
      loadData();
    } catch (err: any) { alert('Error: ' + err.message); }
    finally { setSaving(false); }
  }

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <Header title="Recipient Agencies Management" subtitle="Recipient Agencies, Demand, Storage, Priorities" />

      <main className="p-8 space-y-6 flex-1">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-white">Registered Recipient Agencies</h2>
            <p className="text-xs text-slate-400 mt-0.5">Agencies requesting food allocations with capacity constraints</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-teal-500 to-cyan-500 text-slate-950 font-bold text-xs hover:from-teal-400 hover:to-cyan-400 transition-all flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Add Agency</span>
          </button>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase">
                  <th className="py-3 px-4">Name</th>
                  <th className="py-3 px-4">Location (Lat, Lng)</th>
                  <th className="py-3 px-4">Demand (kg)</th>
                  <th className="py-3 px-4">Storage Capacity</th>
                  <th className="py-3 px-4">Priority Level</th>
                  <th className="py-3 px-4">Cold Storage</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {agencies.length === 0 ? (
                  <tr><td colSpan={6} className="py-6 text-center text-slate-500">No registered agencies found</td></tr>
                ) : (
                  agencies.map((a) => (
                    <tr key={a.id} className="hover:bg-slate-800/40">
                      <td className="py-3.5 px-4 font-bold text-white flex items-center space-x-2">
                        <Building2 className="w-3.5 h-3.5 text-teal-400" />
                        <span>{a.name}</span>
                      </td>
                      <td className="py-3.5 px-4 font-mono text-slate-400 flex items-center space-x-1">
                        <MapPin className="w-3 h-3 text-slate-500" />
                        <span>{a.latitude.toFixed(4)}, {a.longitude.toFixed(4)}</span>
                      </td>
                      <td className="py-3.5 px-4 text-emerald-400 font-mono font-bold">{a.demand_kg} kg</td>
                      <td className="py-3.5 px-4 text-cyan-400 font-mono">{a.storage_capacity_kg} kg</td>
                      <td className="py-3.5 px-4 font-mono">
                        <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-bold">P{a.priority}</span>
                      </td>
                      <td className="py-3.5 px-4">
                        {a.requires_refrigeration ? (
                          <span className="px-2.5 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 text-[10px]">YES</span>
                        ) : (
                          <span className="px-2.5 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">NO</span>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {showModal && (
          <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-6 shadow-2xl">
              <h3 className="text-lg font-bold text-white">Create Recipient Agency</h3>
              <form onSubmit={handleSubmit} className="space-y-4 text-xs">
                <div>
                  <label className="block text-slate-400 mb-1">Agency Name</label>
                  <input type="text" value={name} onChange={(e) => setName(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" required />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-slate-400 mb-1">Demand (kg)</label>
                    <input type="number" value={demand} onChange={(e) => setDemand(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" required />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Storage Capacity (kg)</label>
                    <input type="number" value={capacity} onChange={(e) => setCapacity(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" required />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-slate-400 mb-1">Priority (1-5)</label>
                    <input type="number" min="1" max="5" value={priority} onChange={(e) => setPriority(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" required />
                  </div>
                </div>
                <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
                  <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 font-semibold">Cancel</button>
                  <button type="submit" disabled={saving} className="px-5 py-2 rounded-xl bg-teal-500 text-slate-950 font-bold">{saving ? 'Saving...' : 'Save Agency'}</button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
