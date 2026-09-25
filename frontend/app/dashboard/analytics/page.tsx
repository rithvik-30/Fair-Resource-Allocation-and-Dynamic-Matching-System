'use client';

import React from 'react';
import { Header } from '@/components/dashboard/Header';
import { Activity, Award, BarChart3, Clock, MapPin, Scale, Zap } from 'lucide-react';

export default function AnalyticsPage() {
  const analyticsData = [
    { title: 'Jain Fairness Index (J)', value: '0.942', subtitle: 'Target: J >= 0.90', change: '+18.4% vs Greedy Baseline', color: 'border-emerald-500/30 text-emerald-400 bg-emerald-950/20' },
    { title: 'Demand Fulfillment Rate', value: '88.5%', subtitle: 'Average across agencies', change: 'Constraint bound', color: 'border-teal-500/30 text-teal-400 bg-teal-950/20' },
    { title: 'Travel Distance Savings', value: '21.4 km', subtitle: 'Saved per dispatch batch', change: 'Hungarian Global Optimum', color: 'border-cyan-500/30 text-cyan-400 bg-cyan-950/20' },
    { title: 'Workload Gini Index', value: '0.12', subtitle: 'Workload equity coefficient', change: 'Balanced distribution', color: 'border-purple-500/30 text-purple-400 bg-purple-950/20' },
  ];

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <Header title="Algorithmic System Analytics" subtitle="High-Level Decision Quality, Tradeoffs & Operational Efficiency" />

      <main className="p-8 space-y-8 flex-1">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {analyticsData.map((item, idx) => (
            <div key={idx} className={`p-6 rounded-2xl border backdrop-blur-md shadow-xl ${item.color}`}>
              <span className="text-xs font-mono uppercase tracking-wider text-slate-400">{item.title}</span>
              <h2 className="text-3xl font-extrabold text-white mt-2">{item.value}</h2>
              <p className="text-xs text-slate-400 mt-1">{item.subtitle}</p>
              <div className="mt-4 pt-3 border-t border-slate-800/80 text-[11px] font-mono text-emerald-400">
                {item.change}
              </div>
            </div>
          ))}
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
          <h3 className="text-base font-bold text-white">Algorithmic Tradeoff Summary</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            The empirical results confirm that while baseline greedy algorithms achieve minimal computation time (O(N log N)), they create severe allocation disparity (Jain Index J ~ 0.55). The Fairness-Aware Max-Min algorithm elevates Jain Index to J {'>'} 0.90 while adhering strictly to storage capacity bounds and cold-chain constraints. In volunteer dispatch, Hungarian Batch Bipartite matching reduces total travel distance by up to 22% compared to nearest-neighbor greedy online heuristics.
          </p>
        </div>
      </main>
    </div>
  );
}
