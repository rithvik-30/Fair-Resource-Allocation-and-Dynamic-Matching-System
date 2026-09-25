'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/dashboard/Header';
import { allocationApi, AllocationResult, AllocationCompareResult } from '@/lib/api/allocation';
import { donationsApi, Donation } from '@/lib/api/donations';
import { agenciesApi, Agency } from '@/lib/api/agencies';
import { AlertCircle, BarChart2, CheckCircle2, Play, RefreshCw, Scale, Zap } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function AllocationWorkspace() {
  const [selectedAlgo, setSelectedAlgo] = useState<'greedy' | 'fair' | 'compare'>('compare');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AllocationResult | null>(null);
  const [compareResult, setCompareResult] = useState<AllocationCompareResult | null>(null);

  const [donations, setDonations] = useState<Donation[]>([]);
  const [agencies, setAgencies] = useState<Agency[]>([]);

  useEffect(() => {
    async function init() {
      try {
        const [d, a] = await Promise.all([donationsApi.list(), agenciesApi.list()]);
        setDonations(d);
        setAgencies(a);
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
      // Build request body from real database objects if available
      const payloadDonations = donations.length > 0 ? donations.map(d => ({
        id: d.id,
        food_type: d.food_type,
        quantity_kg: d.quantity_kg,
        requires_refrigeration: d.requires_refrigeration
      })) : [{ id: 'don_1', food_type: 'Perishables', quantity_kg: 250, requires_refrigeration: false }];

      const payloadAgencies = agencies.length > 0 ? agencies.map(a => ({
        id: a.id,
        name: a.name,
        demand_kg: a.demand_kg,
        storage_capacity_kg: a.storage_capacity_kg,
        requires_refrigeration: a.requires_refrigeration,
        priority: a.priority
      })) : [
        { id: 'ag_1', name: 'Agency A', demand_kg: 100, storage_capacity_kg: 150, priority: 3 },
        { id: 'ag_2', name: 'Agency B', demand_kg: 120, storage_capacity_kg: 150, priority: 2 },
        { id: 'ag_3', name: 'Agency C', demand_kg: 80, storage_capacity_kg: 100, priority: 1 },
      ];

      const body = {
        donation: payloadDonations[0],
        agencies: payloadAgencies
      };

      if (selectedAlgo === 'greedy') {
        const res = await allocationApi.greedy(body);
        setResult(res);
        setCompareResult(null);
      } else if (selectedAlgo === 'fair') {
        const res = await allocationApi.fair(body);
        setResult(res);
        setCompareResult(null);
      } else {
        const res = await allocationApi.compare(body);
        setCompareResult(res);
        setResult(null);
      }
    } catch (err: any) {
      setError(err.message || 'Error executing allocation algorithm.');
    } finally {
      setLoading(false);
    }
  }

  // Chart data prep
  const chartData = compareResult ? (
    Object.keys(compareResult.greedy.fulfillment_ratios || {}).map(agId => {
      const agName = agencies.find(a => a.id === agId)?.name || agId;
      return {
        agency: agName,
        GreedyRatio: (compareResult.greedy.fulfillment_ratios[agId] || 0) * 100,
        FairnessAwareRatio: (compareResult.fairness_aware.fulfillment_ratios[agId] || 0) * 100,
      };
    })
  ) : [];

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <Header title="Food Resource Allocation Workspace" subtitle="Priority Greedy vs Fairness-Aware Max-Min Decision Engine" />

      <main className="p-8 space-y-8 flex-1">
        {/* Execution Controls */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-base font-bold text-white">Select Allocation Algorithm</h2>
              <p className="text-xs text-slate-400 mt-0.5">Run individual engine algorithms or compare performance side-by-side</p>
            </div>
            <button
              onClick={handleRun}
              disabled={loading}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold text-sm hover:from-emerald-400 hover:to-teal-400 transition-all shadow-lg shadow-emerald-500/20 flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-current" />}
              <span>{loading ? 'Executing Engine...' : 'Run Allocation'}</span>
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <button
              onClick={() => setSelectedAlgo('greedy')}
              className={`p-4 rounded-xl border text-left transition-all ${
                selectedAlgo === 'greedy'
                  ? 'bg-emerald-950/40 border-emerald-500 text-white shadow-inner'
                  : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-white">Priority Greedy</span>
                <Zap className="w-4 h-4 text-amber-400" />
              </div>
              <p className="text-xs text-slate-400">Myopic priority-first allocation baseline</p>
            </button>

            <button
              onClick={() => setSelectedAlgo('fair')}
              className={`p-4 rounded-xl border text-left transition-all ${
                selectedAlgo === 'fair'
                  ? 'bg-emerald-950/40 border-emerald-500 text-white shadow-inner'
                  : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-white">Fairness-Aware Max-Min</span>
                <Scale className="w-4 h-4 text-emerald-400" />
              </div>
              <p className="text-xs text-slate-400">Maximizes Jain Index & equalizes fulfillment</p>
            </button>

            <button
              onClick={() => setSelectedAlgo('compare')}
              className={`p-4 rounded-xl border text-left transition-all ${
                selectedAlgo === 'compare'
                  ? 'bg-emerald-950/40 border-emerald-500 text-white shadow-inner'
                  : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-white">Algorithm Comparison</span>
                <BarChart2 className="w-4 h-4 text-cyan-400" />
              </div>
              <p className="text-xs text-slate-400">Side-by-side metric & fairness evaluation</p>
            </button>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Algorithm Comparison Results */}
        {compareResult && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Greedy Metrics Card */}
              <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <h3 className="font-bold text-white text-base">Priority Greedy</h3>
                  <span className="text-xs font-mono text-amber-400 bg-amber-950/60 px-2.5 py-0.5 rounded border border-amber-900">Baseline</span>
                </div>
                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                    <span className="text-slate-400">Allocated</span>
                    <p className="text-lg font-bold text-emerald-400 mt-1">{compareResult.greedy.total_allocated_kg} kg</p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                    <span className="text-slate-400">Jain Fairness (J)</span>
                    <p className="text-lg font-bold text-white mt-1">{compareResult.greedy.jains_fairness_index.toFixed(3)}</p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                    <span className="text-slate-400">Allocation Rate</span>
                    <p className="text-lg font-bold text-cyan-400 mt-1">{(compareResult.greedy.allocation_rate * 100).toFixed(1)}%</p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                    <span className="text-slate-400">Execution Time</span>
                    <p className="text-lg font-bold text-slate-300 mt-1">{compareResult.greedy.execution_time_ms.toFixed(2)} ms</p>
                  </div>
                </div>
              </div>

              {/* Fairness-Aware Metrics Card */}
              <div className="p-6 rounded-2xl bg-slate-900/80 border border-emerald-500/30 space-y-4 shadow-xl shadow-emerald-500/5">
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <h3 className="font-bold text-emerald-400 text-base">Fairness-Aware Max-Min</h3>
                  <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2.5 py-0.5 rounded border border-emerald-900">Optimization</span>
                </div>
                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                    <span className="text-slate-400">Allocated</span>
                    <p className="text-lg font-bold text-emerald-400 mt-1">{compareResult.fairness_aware.total_allocated_kg} kg</p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                    <span className="text-slate-400">Jain Fairness (J)</span>
                    <p className="text-lg font-bold text-emerald-300 mt-1">{compareResult.fairness_aware.jains_fairness_index.toFixed(3)}</p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                    <span className="text-slate-400">Allocation Rate</span>
                    <p className="text-lg font-bold text-cyan-400 mt-1">{(compareResult.fairness_aware.allocation_rate * 100).toFixed(1)}%</p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                    <span className="text-slate-400">Execution Time</span>
                    <p className="text-lg font-bold text-slate-300 mt-1">{compareResult.fairness_aware.execution_time_ms.toFixed(2)} ms</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Side-by-Side Chart */}
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800">
              <h3 className="text-base font-bold text-white mb-4">Agency Fulfillment Ratio Comparison (%)</h3>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="agency" stroke="#64748b" fontSize={11} />
                    <YAxis stroke="#64748b" fontSize={11} unit="%" />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                    <Legend />
                    <Bar dataKey="GreedyRatio" name="Greedy Fulfillment %" fill="#f59e0b" radius={[6, 6, 0, 0]} />
                    <Bar dataKey="FairnessAwareRatio" name="Fairness-Aware Fulfillment %" fill="#10b981" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* Single Algorithm Result */}
        {result && (
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-6">
            <h3 className="text-base font-bold text-white">Execution Result: {result.algorithm}</h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <span className="text-slate-400">Total Allocated</span>
                <p className="text-xl font-bold text-emerald-400 mt-1">{result.total_allocated_kg} kg</p>
              </div>
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <span className="text-slate-400">Jain Fairness Index</span>
                <p className="text-xl font-bold text-white mt-1">{result.jains_fairness_index.toFixed(3)}</p>
              </div>
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <span className="text-slate-400">Unmet Demand</span>
                <p className="text-xl font-bold text-amber-400 mt-1">{result.unmet_demand_kg} kg</p>
              </div>
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <span className="text-slate-400">Runtime</span>
                <p className="text-xl font-bold text-slate-300 mt-1">{result.execution_time_ms.toFixed(2)} ms</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
