'use client';

import React from 'react';
import { Cpu, GitMerge, Scale, ShieldAlert, Zap } from 'lucide-react';

export function AlgorithmsSection() {
  const allocationAlgos = [
    {
      name: 'Priority Greedy Allocator',
      type: 'Baseline',
      desc: 'Myopically satisfies highest-priority agencies first until food supply or storage capacity is exhausted.',
      metrics: 'Fast O(N log N) runtime, lower fairness index under constrained supply.',
      icon: Zap,
    },
    {
      name: 'Fairness-Aware Max-Min',
      type: 'Optimization',
      desc: 'Iteratively equalizes fulfillment ratios across all recipient agencies to maximize Jain\'s Fairness Index.',
      metrics: 'Maximizes fairness metric J >= 0.90, minimizes allocation disparity.',
      icon: Scale,
    },
  ];

  const dispatchAlgos = [
    {
      name: 'Nearest Volunteer Greedy',
      type: 'Spatial Baseline',
      desc: 'Sequentially pairs each rescue request with the closest available feasible volunteer using Haversine distance.',
      metrics: 'Low individual distance, potential high workload variance.',
      icon: ShieldAlert,
    },
    {
      name: 'Multi-Criteria Scored Dispatch',
      type: 'Utility Tradeoff',
      desc: 'Evaluates weighted utility balancing pickup distance, deadline urgency, workload equity, and vehicle capacity.',
      metrics: 'Balanced performance across travel distance and workload variance.',
      icon: GitMerge,
    },
    {
      name: 'Batch Bipartite Matching',
      type: 'Global Optimal',
      desc: 'Constructs complete bipartite graph between requests and volunteers, solved via Hungarian algorithm linear sum assignment.',
      metrics: 'Global minimum travel distance across batch execution.',
      icon: Cpu,
    },
  ];

  return (
    <section id="algorithms" className="py-20 px-6 max-w-7xl mx-auto border-t border-slate-800/80">
      <div className="text-center max-w-2xl mx-auto mb-16">
        <h2 className="text-xs font-mono text-cyan-400 uppercase tracking-widest mb-2">Algorithmic Suite</h2>
        <h3 className="text-3xl font-bold text-white">Resource Allocation & Dispatch Engines</h3>
        <p className="text-slate-400 mt-3 text-sm">Formal mathematical algorithms comparing baseline heuristics against optimization engines.</p>
      </div>

      <div className="space-y-12">
        <div>
          <h4 className="text-lg font-bold text-emerald-400 flex items-center space-x-2 mb-6">
            <Scale className="w-5 h-5" />
            <span>1. Food Resource Allocation Algorithms</span>
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {allocationAlgos.map((algo, i) => {
              const Icon = algo.icon;
              return (
                <div key={i} className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-emerald-500/40 transition-all">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        <Icon className="w-5 h-5" />
                      </div>
                      <h5 className="font-bold text-white">{algo.name}</h5>
                    </div>
                    <span className="text-xs font-mono px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">{algo.type}</span>
                  </div>
                  <p className="text-slate-400 text-xs leading-relaxed mb-4">{algo.desc}</p>
                  <div className="text-[11px] font-mono text-emerald-400/90 bg-emerald-950/40 border border-emerald-900/50 p-2.5 rounded-lg">
                    {algo.metrics}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div>
          <h4 className="text-lg font-bold text-cyan-400 flex items-center space-x-2 mb-6">
            <Cpu className="w-5 h-5" />
            <span>2. Dynamic Volunteer Dispatch Algorithms</span>
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {dispatchAlgos.map((algo, i) => {
              const Icon = algo.icon;
              return (
                <div key={i} className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-cyan-500/40 transition-all">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-2.5 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="text-xs font-mono px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">{algo.type}</span>
                  </div>
                  <h5 className="font-bold text-white mb-2">{algo.name}</h5>
                  <p className="text-slate-400 text-xs leading-relaxed mb-4">{algo.desc}</p>
                  <div className="text-[11px] font-mono text-cyan-400/90 bg-cyan-950/40 border border-cyan-900/50 p-2.5 rounded-lg">
                    {algo.metrics}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
