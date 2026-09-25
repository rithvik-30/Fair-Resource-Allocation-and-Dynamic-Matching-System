'use client';

import React from 'react';
import { Box, HeartHandshake, Truck, Users } from 'lucide-react';

export function HowItWorks() {
  const steps = [
    {
      icon: Box,
      title: '1. Food Donation',
      desc: 'Donors submit food surplus details including volume, perishable status, refrigeration, and pickup availability window.',
      color: 'from-amber-500/20 to-orange-500/10 text-amber-400 border-amber-500/30',
    },
    {
      icon: HeartHandshake,
      title: '2. Fair Allocation',
      desc: 'Fairness-Aware Max-Min allocator evaluates agency demands, capacity bounds, and priority scores to maximize Jain Index.',
      color: 'from-emerald-500/20 to-teal-500/10 text-emerald-400 border-emerald-500/30',
    },
    {
      icon: Users,
      title: '3. Volunteer Matching',
      desc: 'Bipartite matching & multi-criteria scoring algorithm pairs pending rescue tasks with feasible nearby volunteers.',
      color: 'from-cyan-500/20 to-blue-500/10 text-cyan-400 border-cyan-500/30',
    },
    {
      icon: Truck,
      title: '4. Rescue Execution',
      desc: 'Volunteers pick up food allocations and deliver directly to recipient agencies, balancing workload equity & distance.',
      color: 'from-purple-500/20 to-indigo-500/10 text-purple-400 border-purple-500/30',
    },
  ];

  return (
    <section id="how-it-works" className="py-20 px-6 max-w-7xl mx-auto">
      <div className="text-center max-w-2xl mx-auto mb-16">
        <h2 className="text-xs font-mono text-emerald-400 uppercase tracking-widest mb-2">System Pipeline</h2>
        <h3 className="text-3xl font-bold text-white">How FRADMS Computational Flow Works</h3>
        <p className="text-slate-400 mt-3 text-sm">A four-stage operational pipeline transforming surplus food donations into equitable rescue executions.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          return (
            <div
              key={idx}
              className={`p-6 rounded-2xl bg-gradient-to-b ${step.color} border backdrop-blur-md relative group hover:-translate-y-1 transition-transform`}
            >
              <div className="w-12 h-12 rounded-xl bg-slate-950/80 flex items-center justify-center mb-5 border border-slate-800">
                <Icon className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-white mb-2">{step.title}</h4>
              <p className="text-slate-400 text-xs leading-relaxed">{step.desc}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}
