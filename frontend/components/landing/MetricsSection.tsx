'use client';

import React from 'react';
import { Activity, Award, BarChart3, Clock, MapPin, Scale, Zap } from 'lucide-react';

export function MetricsSection() {
  const metrics = [
    { name: 'Allocation Rate', desc: 'Percentage of total food donation volume successfully allocated to recipient agencies.', icon: BarChart3, color: 'text-emerald-400' },
    { name: "Jain's Fairness Index", desc: "Quantitative fairness metric measuring distribution equity across agencies J in [1/n, 1.0].", icon: Scale, color: 'text-teal-400' },
    { name: 'Unmet Demand', desc: 'Total unsatisfied food quantity (kg) remaining across all recipient agencies.', icon: Activity, color: 'text-amber-400' },
    { name: 'Assignment Rate', desc: 'Percentage of rescue requests successfully matched with feasible volunteers.', icon: Award, color: 'text-cyan-400' },
    { name: 'Total Travel Distance', desc: 'Sum of Haversine distances (km) driven by assigned volunteers for rescue pickups.', icon: MapPin, color: 'text-blue-400' },
    { name: 'Workload Variance', desc: 'Variance of cumulative rescue workload (kg) assigned across active volunteers.', icon: Zap, color: 'text-purple-400' },
    { name: 'Runtime Execution (ms)', desc: 'Algorithm computation execution time per batch request in milliseconds.', icon: Clock, color: 'text-rose-400' },
  ];

  return (
    <section id="metrics" className="py-20 px-6 max-w-7xl mx-auto border-t border-slate-800/80">
      <div className="text-center max-w-2xl mx-auto mb-16">
        <h2 className="text-xs font-mono text-emerald-400 uppercase tracking-widest mb-2">Quantitative Metrics</h2>
        <h3 className="text-3xl font-bold text-white">Rigorous Algorithmic Evaluation</h3>
        <p className="text-slate-400 mt-3 text-sm">Empirical benchmarks evaluating fairness, assignment efficiency, travel reduction, and workload balance.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((m, i) => {
          const Icon = m.icon;
          return (
            <div key={i} className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/90 backdrop-blur-sm hover:border-slate-700 transition-colors">
              <div className="flex items-center space-x-3 mb-3">
                <div className={`p-2 rounded-lg bg-slate-950 border border-slate-800 ${m.color}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <h5 className="font-bold text-white text-sm">{m.name}</h5>
              </div>
              <p className="text-slate-400 text-xs leading-relaxed">{m.desc}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}
