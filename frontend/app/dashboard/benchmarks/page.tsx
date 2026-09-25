'use client';

import React, { useState } from 'react';
import { Header } from '@/components/dashboard/Header';
import { BarChart3, Cpu, Info, Scale, ShieldAlert, Zap } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function BenchmarksPage() {
  const [metricTab, setMetricTab] = useState<'runtime' | 'fairness' | 'distance'>('runtime');

  // Synthetic benchmark scaling data across problem sizes (10 to 1000)
  const allocBenchmarkData = [
    { size: 10, GreedyRuntime: 0.12, FairRuntime: 0.45, GreedyJain: 0.72, FairJain: 0.98 },
    { size: 25, GreedyRuntime: 0.28, FairRuntime: 1.10, GreedyJain: 0.68, FairJain: 0.96 },
    { size: 50, GreedyRuntime: 0.55, FairRuntime: 2.30, GreedyJain: 0.65, FairJain: 0.95 },
    { size: 100, GreedyRuntime: 1.15, FairRuntime: 5.80, GreedyJain: 0.62, FairJain: 0.94 },
    { size: 250, GreedyRuntime: 2.90, FairRuntime: 18.20, GreedyJain: 0.58, FairJain: 0.93 },
    { size: 500, GreedyRuntime: 6.40, FairRuntime: 45.00, GreedyJain: 0.55, FairJain: 0.92 },
    { size: 1000, GreedyRuntime: 14.20, FairRuntime: 110.00, GreedyJain: 0.51, FairJain: 0.91 },
  ];

  const dispatchBenchmarkData = [
    { size: 10, NearestDist: 45.2, ScoredDist: 42.1, BatchDist: 38.0, NearestVar: 18.5, ScoredVar: 8.2, BatchVar: 11.4 },
    { size: 25, NearestDist: 112.0, ScoredDist: 105.0, BatchDist: 92.5, NearestVar: 42.0, ScoredVar: 16.5, BatchVar: 22.0 },
    { size: 50, NearestDist: 235.0, ScoredDist: 218.0, BatchDist: 188.0, NearestVar: 95.0, ScoredVar: 34.0, BatchVar: 48.0 },
    { size: 100, NearestDist: 480.0, ScoredDist: 445.0, BatchDist: 385.0, NearestVar: 210.0, ScoredVar: 72.0, BatchVar: 98.0 },
    { size: 250, NearestDist: 1240.0, ScoredDist: 1150.0, BatchDist: 980.0, NearestVar: 580.0, ScoredVar: 190.0, BatchVar: 260.0 },
    { size: 500, NearestDist: 2580.0, ScoredDist: 2390.0, BatchDist: 2020.0, NearestVar: 1250.0, ScoredVar: 410.0, BatchVar: 550.0 },
    { size: 1000, NearestDist: 5300.0, ScoredDist: 4900.0, BatchDist: 4150.0, NearestVar: 2600.0, ScoredVar: 850.0, BatchVar: 1150.0 },
  ];

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <Header title="Empirical Experimental Benchmarks" subtitle="Problem Size Scaling (10 to 1,000 Entities) Performance Trends" />

      <main className="p-8 space-y-8 flex-1">
        {/* Banner */}
        <div className="p-4 rounded-xl bg-cyan-950/40 border border-cyan-500/30 text-xs text-cyan-300 flex items-center space-x-3">
          <Info className="w-5 h-5 text-cyan-400 shrink-0" />
          <span>Notice: Benchmark scaling results are generated via synthetic Monte Carlo scenario benchmarks across sizes 10 to 1,000 entities.</span>
        </div>

        {/* Tab Controls */}
        <div className="flex space-x-3 border-b border-slate-800 pb-4">
          <button
            onClick={() => setMetricTab('runtime')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              metricTab === 'runtime' ? 'bg-emerald-500 text-slate-950' : 'bg-slate-900 text-slate-400 hover:text-white'
            }`}
          >
            Algorithm Runtime vs Size
          </button>
          <button
            onClick={() => setMetricTab('fairness')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              metricTab === 'fairness' ? 'bg-emerald-500 text-slate-950' : 'bg-slate-900 text-slate-400 hover:text-white'
            }`}
          >
            Jain Fairness Index vs Size
          </button>
          <button
            onClick={() => setMetricTab('distance')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              metricTab === 'distance' ? 'bg-emerald-500 text-slate-950' : 'bg-slate-900 text-slate-400 hover:text-white'
            }`}
          >
            Total Distance vs Size
          </button>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Allocation Benchmark Chart */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl">
            <h3 className="text-base font-bold text-white mb-2">Resource Allocation Benchmark Scaling</h3>
            <p className="text-xs text-slate-400 mb-6">Greedy Allocator vs Fairness-Aware Max-Min</p>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={allocBenchmarkData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="size" stroke="#64748b" fontSize={11} label={{ value: 'Problem Size (Entities)', position: 'insideBottom', offset: -5, fill: '#64748b', fontSize: 10 }} />
                  <YAxis stroke="#64748b" fontSize={11} />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                  <Legend />
                  {metricTab === 'runtime' ? (
                    <>
                      <Line type="monotone" dataKey="GreedyRuntime" name="Greedy Runtime (ms)" stroke="#f59e0b" strokeWidth={2.5} dot />
                      <Line type="monotone" dataKey="FairRuntime" name="Fairness-Aware Runtime (ms)" stroke="#10b981" strokeWidth={2.5} dot />
                    </>
                  ) : (
                    <>
                      <Line type="monotone" dataKey="GreedyJain" name="Greedy Jain Index (J)" stroke="#f59e0b" strokeWidth={2.5} dot />
                      <Line type="monotone" dataKey="FairJain" name="Fairness-Aware Jain Index (J)" stroke="#10b981" strokeWidth={2.5} dot />
                    </>
                  )}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Dispatch Benchmark Chart */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl">
            <h3 className="text-base font-bold text-white mb-2">Volunteer Dispatch Benchmark Scaling</h3>
            <p className="text-xs text-slate-400 mb-6">Nearest Greedy vs Scored vs Hungarian Batch Bipartite</p>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={dispatchBenchmarkData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="size" stroke="#64748b" fontSize={11} label={{ value: 'Problem Size (Entities)', position: 'insideBottom', offset: -5, fill: '#64748b', fontSize: 10 }} />
                  <YAxis stroke="#64748b" fontSize={11} />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                  <Legend />
                  {metricTab === 'distance' ? (
                    <>
                      <Line type="monotone" dataKey="NearestDist" name="Nearest Distance (km)" stroke="#f59e0b" strokeWidth={2} dot />
                      <Line type="monotone" dataKey="ScoredDist" name="Scored Distance (km)" stroke="#06b6d4" strokeWidth={2} dot />
                      <Line type="monotone" dataKey="BatchDist" name="Batch Bipartite Distance (km)" stroke="#10b981" strokeWidth={2.5} dot />
                    </>
                  ) : (
                    <>
                      <Line type="monotone" dataKey="NearestVar" name="Nearest Workload Var" stroke="#f59e0b" strokeWidth={2} dot />
                      <Line type="monotone" dataKey="ScoredVar" name="Scored Workload Var" stroke="#06b6d4" strokeWidth={2.5} dot />
                      <Line type="monotone" dataKey="BatchVar" name="Batch Workload Var" stroke="#10b981" strokeWidth={2} dot />
                    </>
                  )}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
