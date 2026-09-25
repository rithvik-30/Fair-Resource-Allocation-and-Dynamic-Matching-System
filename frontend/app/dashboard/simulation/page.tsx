'use client';

import React, { useState } from 'react';
import { Header } from '@/components/dashboard/Header';
import { simulationApi, SimulationResult } from '@/lib/api/simulation';
import { AlertCircle, Play, RefreshCw, Sliders, Zap } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function SimulationWorkspace() {
  const [numDonations, setNumDonations] = useState(10);
  const [numAgencies, setNumAgencies] = useState(15);
  const [numVolunteers, setNumVolunteers] = useState(8);
  const [seed, setSeed] = useState(42);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<SimulationResult | null>(null);

  async function handleRunSimulation() {
    setLoading(true);
    setError(null);
    try {
      const res = await simulationApi.quick({
        num_donations: numDonations,
        num_agencies: numAgencies,
        num_volunteers: numVolunteers,
        seed: seed,
      });
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Error running simulation.');
    } finally {
      setLoading(false);
    }
  }

  // Prep chart data if result exists
  const allocChartData = result ? [
    {
      metric: 'Allocation Rate (%)',
      Greedy: result.allocation_results.greedy.allocation_rate * 100,
      FairnessAware: result.allocation_results.fairness_aware.allocation_rate * 100,
    },
    {
      metric: "Jain's Fairness Index (x100)",
      Greedy: result.allocation_results.greedy.jains_fairness_index * 100,
      FairnessAware: result.allocation_results.fairness_aware.jains_fairness_index * 100,
    }
  ] : [];

  const dispatchChartData = result ? [
    {
      metric: 'Assignment Rate (%)',
      Nearest: result.dispatch_results.nearest.assignment_rate * 100,
      Scored: result.dispatch_results.scored.assignment_rate * 100,
      BatchBipartite: result.dispatch_results.batch_bipartite.assignment_rate * 100,
    },
    {
      metric: 'Total Distance (km)',
      Nearest: result.dispatch_results.nearest.total_distance_km,
      Scored: result.dispatch_results.scored.total_distance_km,
      BatchBipartite: result.dispatch_results.batch_bipartite.total_distance_km,
    }
  ] : [];

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <Header title="Monte Carlo Simulation Workspace" subtitle="FastAPI Quick Simulation Engine API Integration" />

      <main className="p-8 space-y-8 flex-1">
        {/* Simulation Controls */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-base font-bold text-white flex items-center space-x-2">
                <Sliders className="w-5 h-5 text-emerald-400" />
                <span>Simulation Parameters</span>
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">Configure synthetic scenario sizes and random seeds</p>
            </div>
            <button
              onClick={handleRunSimulation}
              disabled={loading}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold text-sm hover:from-emerald-400 hover:to-teal-400 transition-all shadow-lg shadow-emerald-500/20 flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-current" />}
              <span>{loading ? 'Running Simulation...' : 'Run Quick Simulation'}</span>
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-6 text-xs">
            <div>
              <label className="block text-slate-400 mb-2">Number of Donations ({numDonations})</label>
              <input type="range" min="5" max="100" value={numDonations} onChange={(e) => setNumDonations(Number(e.target.value))} className="w-full accent-emerald-500 bg-slate-950" />
            </div>
            <div>
              <label className="block text-slate-400 mb-2">Number of Agencies ({numAgencies})</label>
              <input type="range" min="5" max="100" value={numAgencies} onChange={(e) => setNumAgencies(Number(e.target.value))} className="w-full accent-emerald-500 bg-slate-950" />
            </div>
            <div>
              <label className="block text-slate-400 mb-2">Number of Volunteers ({numVolunteers})</label>
              <input type="range" min="3" max="50" value={numVolunteers} onChange={(e) => setNumVolunteers(Number(e.target.value))} className="w-full accent-cyan-500 bg-slate-950" />
            </div>
            <div>
              <label className="block text-slate-400 mb-2">Random Seed</label>
              <input type="number" value={seed} onChange={(e) => setSeed(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white font-mono" />
            </div>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Simulation Output Dashboard */}
        {result && (
          <div className="space-y-6">
            <div className="p-4 rounded-xl bg-emerald-950/40 border border-emerald-500/30 flex items-center justify-between text-xs font-mono">
              <span className="text-emerald-400">Simulation Execution Completed</span>
              <span className="text-slate-300">Total Runtime: {result.execution_time_ms.toFixed(2)} ms</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Allocation Simulation Chart */}
              <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl">
                <h3 className="text-base font-bold text-white mb-4">Allocation Simulation Metrics</h3>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={allocChartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                      <XAxis dataKey="metric" stroke="#64748b" fontSize={11} />
                      <YAxis stroke="#64748b" fontSize={11} />
                      <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                      <Legend />
                      <Bar dataKey="Greedy" fill="#f59e0b" radius={[6, 6, 0, 0]} />
                      <Bar dataKey="FairnessAware" fill="#10b981" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Dispatch Simulation Chart */}
              <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl">
                <h3 className="text-base font-bold text-white mb-4">Dispatch Simulation Metrics</h3>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={dispatchChartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                      <XAxis dataKey="metric" stroke="#64748b" fontSize={11} />
                      <YAxis stroke="#64748b" fontSize={11} />
                      <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                      <Legend />
                      <Bar dataKey="Nearest" fill="#f59e0b" radius={[6, 6, 0, 0]} />
                      <Bar dataKey="Scored" fill="#06b6d4" radius={[6, 6, 0, 0]} />
                      <Bar dataKey="BatchBipartite" fill="#10b981" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
