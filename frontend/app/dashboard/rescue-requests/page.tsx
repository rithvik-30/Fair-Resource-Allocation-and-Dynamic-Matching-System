'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/dashboard/Header';
import { rescueRequestsApi, RescueRequest } from '@/lib/api/rescueRequests';
import { Clock, GitPullRequest, Plus } from 'lucide-react';

export default function RescueRequestsPage() {
  const [requests, setRequests] = useState<RescueRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadData(); }, []);

  async function loadData() {
    setLoading(true);
    try { setRequests(await rescueRequestsApi.list().catch(() => [])); }
    catch (err) { console.error(err); }
    finally { setLoading(false); }
  }

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <Header title="Rescue Requests Management" subtitle="Open Food Rescue Tasks & Fulfillment Status" />

      <main className="p-8 space-y-6 flex-1">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-white">Active Rescue Requests</h2>
            <p className="text-xs text-slate-400 mt-0.5">Rescue requests requiring volunteer dispatch matching</p>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase">
                  <th className="py-3 px-4">Request ID</th>
                  <th className="py-3 px-4">Donation ID</th>
                  <th className="py-3 px-4">Agency ID</th>
                  <th className="py-3 px-4">Quantity (kg)</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Created At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {requests.length === 0 ? (
                  <tr><td colSpan={6} className="py-6 text-center text-slate-500">No rescue requests found</td></tr>
                ) : (
                  requests.map((r) => (
                    <tr key={r.id} className="hover:bg-slate-800/40">
                      <td className="py-3.5 px-4 font-mono text-slate-300 flex items-center space-x-2">
                        <GitPullRequest className="w-3.5 h-3.5 text-amber-400" />
                        <span>{r.id.substring(0, 8)}...</span>
                      </td>
                      <td className="py-3.5 px-4 font-mono text-slate-400">{r.donation_id.substring(0, 8)}...</td>
                      <td className="py-3.5 px-4 font-mono text-slate-400">{r.agency_id.substring(0, 8)}...</td>
                      <td className="py-3.5 px-4 text-emerald-400 font-mono font-bold">{r.requested_quantity_kg} kg</td>
                      <td className="py-3.5 px-4">
                        <span className={`px-2.5 py-0.5 rounded text-[10px] font-mono uppercase border ${
                          r.status === 'completed' ? 'bg-emerald-950 text-emerald-400 border-emerald-800' :
                          r.status === 'assigned' ? 'bg-cyan-950 text-cyan-400 border-cyan-800' :
                          'bg-amber-950 text-amber-400 border-amber-800'
                        }`}>
                          {r.status}
                        </span>
                      </td>
                      <td className="py-3.5 px-4 font-mono text-slate-500">{new Date(r.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
