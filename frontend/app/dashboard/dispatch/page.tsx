'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/dashboard/Header';
import { dispatchApi, DispatchResult, DispatchCompareResult } from '@/lib/api/dispatch';
import { rescueRequestsApi, RescueRequest } from '@/lib/api/rescueRequests';
import { volunteersApi, Volunteer } from '@/lib/api/volunteers';
import { AlertCircle, CheckCircle2, Cpu, GitMerge, MapPin, Play, RefreshCw, ShieldAlert, Truck, XCircle } from 'lucide-react';

export default function DispatchWorkspace() {
  const [selectedAlgo, setSelectedAlgo] = useState<'nearest' | 'scored' | 'batch' | 'compare'>('compare');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DispatchResult | null>(null);
  const [compareResult, setCompareResult] = useState<DispatchCompareResult | null>(null);

  const [requests, setRequests] = useState<RescueRequest[]>([]);
  const [volunteers, setVolunteers] = useState<Volunteer[]>([]);

  useEffect(() => {
    async function init() {
      try {
        const [r, v] = await Promise.all([rescueRequestsApi.list(), volunteersApi.list()]);
        setRequests(r);
        setVolunteers(v);
      } catch (err: any) {
        console.error(err);
      }
    }
    init();
  }, []);

  async function handleRun() {
    setLoading(true);
    setError(null);
    try {
      const payloadRequests = requests.length > 0 ? requests.map(r => ({
        id: r.id,
        donation_id: r.donation_id,
        agency_id: r.agency_id,
        requested_quantity_kg: r.requested_quantity_kg,
        pickup_location: { latitude: 37.7749, longitude: -122.4194 },
        delivery_location: { latitude: 37.7833, longitude: -122.4167 }
      })) : [
        { id: 'req_1', donation_id: 'don_1', agency_id: 'ag_1', requested_quantity_kg: 50, pickup_location: { latitude: 37.7749, longitude: -122.4194 }, delivery_location: { latitude: 37.7833, longitude: -122.4167 } },
        { id: 'req_2', donation_id: 'don_2', agency_id: 'ag_2', requested_quantity_kg: 80, pickup_location: { latitude: 37.7750, longitude: -122.4180 }, delivery_location: { latitude: 37.7850, longitude: -122.4150 } }
      ];

      const payloadVolunteers = volunteers.length > 0 ? volunteers.map(v => ({
        id: v.id,
        name: v.name,
        capacity_kg: v.capacity_kg,
        has_refrigeration: v.has_refrigeration,
        current_workload_kg: v.current_workload_kg,
        max_travel_distance_km: v.max_travel_distance_km,
        location: { latitude: v.latitude, longitude: v.longitude }
      })) : [
        { id: 'vol_1', name: 'Alex Rivers', capacity_kg: 100, has_refrigeration: true, current_workload_kg: 0, max_travel_distance_km: 15, location: { latitude: 37.7750, longitude: -122.4180 } },
        { id: 'vol_2', name: 'Sam Taylor', capacity_kg: 60, has_refrigeration: false, current_workload_kg: 0, max_travel_distance_km: 10, location: { latitude: 37.7800, longitude: -122.4100 } }
      ];

      const body = {
        requests: payloadRequests,
        volunteers: payloadVolunteers
      };

      if (selectedAlgo === 'nearest') {
        setResult(await dispatchApi.nearest(body));
        setCompareResult(null);
      } else if (selectedAlgo === 'scored') {
        setResult(await dispatchApi.scored(body));
        setCompareResult(null);
      } else if (selectedAlgo === 'batch') {
        setResult(await dispatchApi.batch(body));
        setCompareResult(null);
      } else {
        setCompareResult(await dispatchApi.compare(body));
        setResult(null);
      }
    } catch (err: any) {
      setError(err.message || 'Error executing dispatch algorithm.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <Header title="Dynamic Volunteer Dispatch Workspace" subtitle="Nearest Greedy vs Scored vs Hungarian Batch Bipartite Matching" />

      <main className="p-8 space-y-8 flex-1">
        {/* Controls */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-base font-bold text-white">Select Dispatch Algorithm</h2>
              <p className="text-xs text-slate-400 mt-0.5">Evaluate assignment rates, total travel distance, and workload equity</p>
            </div>
            <button
              onClick={handleRun}
              disabled={loading}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 text-slate-950 font-bold text-sm hover:from-cyan-400 hover:to-blue-400 transition-all shadow-lg shadow-cyan-500/20 flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-current" />}
              <span>{loading ? 'Dispatching...' : 'Run Dispatch'}</span>
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <button
              onClick={() => setSelectedAlgo('nearest')}
              className={`p-4 rounded-xl border text-left transition-all ${
                selectedAlgo === 'nearest'
                  ? 'bg-cyan-950/40 border-cyan-500 text-white shadow-inner'
                  : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-white">Nearest Greedy</span>
                <ShieldAlert className="w-4 h-4 text-amber-400" />
              </div>
              <p className="text-xs text-slate-400">Closest feasible volunteer baseline</p>
            </button>

            <button
              onClick={() => setSelectedAlgo('scored')}
              className={`p-4 rounded-xl border text-left transition-all ${
                selectedAlgo === 'scored'
                  ? 'bg-cyan-950/40 border-cyan-500 text-white shadow-inner'
                  : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-white">Score-Based</span>
                <GitMerge className="w-4 h-4 text-cyan-400" />
              </div>
              <p className="text-xs text-slate-400">Multi-criteria tradeoff heuristic</p>
            </button>

            <button
              onClick={() => setSelectedAlgo('batch')}
              className={`p-4 rounded-xl border text-left transition-all ${
                selectedAlgo === 'batch'
                  ? 'bg-cyan-950/40 border-cyan-500 text-white shadow-inner'
                  : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-white">Batch Bipartite</span>
                <Cpu className="w-4 h-4 text-emerald-400" />
              </div>
              <p className="text-xs text-slate-400">Hungarian global minimum distance</p>
            </button>

            <button
              onClick={() => setSelectedAlgo('compare')}
              className={`p-4 rounded-xl border text-left transition-all ${
                selectedAlgo === 'compare'
                  ? 'bg-cyan-950/40 border-cyan-500 text-white shadow-inner'
                  : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-white">Compare All</span>
                <Truck className="w-4 h-4 text-purple-400" />
              </div>
              <p className="text-xs text-slate-400">Tri-algorithm benchmark comparison</p>
            </button>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Dispatch Comparison View */}
        {compareResult && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {['nearest', 'scored', 'batch_bipartite'].map((key) => {
              const res = (compareResult as any)[key] as DispatchResult;
              if (!res) return null;
              return (
                <div key={key} className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
                  <h3 className="font-bold text-white text-base capitalize">{res.algorithm}</h3>
                  <div className="space-y-3 text-xs">
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <span className="text-slate-400">Assignment Rate</span>
                      <p className="text-lg font-bold text-cyan-400 mt-0.5">{(res.assignment_rate * 100).toFixed(1)}%</p>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <span className="text-slate-400">Total Distance</span>
                      <p className="text-lg font-bold text-emerald-400 mt-0.5">{res.total_distance_km.toFixed(2)} km</p>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <span className="text-slate-400">Workload Variance</span>
                      <p className="text-lg font-bold text-purple-400 mt-0.5">{res.workload_variance.toFixed(2)}</p>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <span className="text-slate-400">Execution Time</span>
                      <p className="text-lg font-bold text-slate-300 mt-0.5">{res.execution_time_ms.toFixed(2)} ms</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Detailed Assignments Table */}
        {result && (
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
            <h3 className="text-base font-bold text-white">Dispatch Assignments: {result.algorithm}</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase">
                    <th className="py-3 px-4">Request ID</th>
                    <th className="py-3 px-4">Assigned Volunteer</th>
                    <th className="py-3 px-4">Distance</th>
                    <th className="py-3 px-4">Feasibility</th>
                    <th className="py-3 px-4">Explanation</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {result.assignments.map((a, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/40">
                      <td className="py-3 px-4 font-mono text-slate-300">{a.rescue_request_id}</td>
                      <td className="py-3 px-4 font-semibold text-white">{a.volunteer_id}</td>
                      <td className="py-3 px-4 text-emerald-400 font-mono font-bold">{a.distance_km.toFixed(2)} km</td>
                      <td className="py-3 px-4">
                        {a.is_feasible ? (
                          <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-mono">
                            <CheckCircle2 className="w-3 h-3" />
                            <span>FEASIBLE</span>
                          </span>
                        ) : (
                          <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full bg-rose-950 text-rose-400 border border-rose-800 text-[10px] font-mono">
                            <XCircle className="w-3 h-3" />
                            <span>INFEASIBLE</span>
                          </span>
                        )}
                      </td>
                      <td className="py-3 px-4 text-slate-400">{a.explanation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
