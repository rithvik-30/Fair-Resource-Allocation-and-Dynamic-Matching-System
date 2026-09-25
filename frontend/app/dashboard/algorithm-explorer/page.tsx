'use client';

import React, { useState } from 'react';
import { Header } from '@/components/dashboard/Header';
import { Cpu } from 'lucide-react';

export default function AlgorithmExplorerPage() {
  const [selectedTopic, setSelectedTopic] = useState<'greedy' | 'fair' | 'nearest' | 'scored' | 'batch'>('fair');

  const algos = {
    greedy: {
      name: 'Priority Greedy Allocation',
      category: 'Resource Allocation',
      problem: 'Allocate food donation supply among multiple recipient agencies with different needs and priority levels.',
      inputs: 'Donation volume (kg), Agency demands (kg), Storage capacities (kg), Priority scores (1-5), Perishable/Refrigeration flags.',
      coreIdea: 'Sort recipient agencies by priority descending, then myopically fulfill 100% of each agency demand until supply or capacity is exhausted.',
      constraints: 'Agency storage capacity limit, non-negative allocation, total supply bound.',
      objective: 'Maximize total priority-weighted volume allocated.',
      complexity: 'O(N log N) sorting time.',
      keyMetrics: 'Allocation Rate, Priority Fulfillment Ratio.',
    },
    fair: {
      name: 'Fairness-Aware Max-Min Allocation',
      category: 'Resource Allocation',
      problem: 'Distribute food supply equitably across agencies to avoid starvation of lower-priority or smaller agencies.',
      inputs: 'Donation volume (kg), Agency demands (kg), Storage capacities (kg), Priority scores, Cold storage capability.',
      coreIdea: 'Iteratively equalize the fulfillment ratio (allocated / demand) across all eligible agencies via max-min fairness optimization.',
      constraints: 'Strict storage capacity caps, cold-chain compatibility, total donation supply constraint.',
      objective: 'Maximize Jain\'s Fairness Index J = (sum x_i)^2 / (n * sum x_i^2).',
      complexity: 'O(K * N log N) iterative allocation rounds.',
      keyMetrics: 'Jain\'s Fairness Index (J), Allocation Disparity (kg), Equalized Fulfillment Ratio.',
    },
    nearest: {
      name: 'Nearest Volunteer Greedy Dispatch',
      category: 'Volunteer Dispatch',
      problem: 'Match incoming rescue requests to available volunteers operating in a geographic area.',
      inputs: 'Rescue request locations, Volunteer locations, Vehicle capacities (kg), Max travel distance caps (km).',
      coreIdea: 'Sequentially process incoming requests and assign each to the closest feasible volunteer using Haversine distance.',
      constraints: 'Vehicle load capacity <= volunteer capacity, refrigeration compatibility, distance <= max_travel_distance.',
      objective: 'Minimize individual pickup travel distance for each task.',
      complexity: 'O(R * V) distance matrix evaluation.',
      keyMetrics: 'Individual travel distance, Assignment Rate.',
    },
    scored: {
      name: 'Multi-Criteria Score-Based Dispatch',
      category: 'Volunteer Dispatch',
      problem: 'Balance pickup distance, deadline urgency, workload equity, and vehicle capacity utilization.',
      inputs: 'Pickup/delivery locations, Pickup deadlines, Volunteer workloads (kg), Vehicle capacities, Max travel limits.',
      coreIdea: 'Evaluate a multi-criteria utility score U = w1*Dist + w2*Urgency + w3*Workload + w4*Capacity for all pairs and assign highest score.',
      constraints: 'Vehicle capacity limit, refrigeration compatibility, maximum travel distance.',
      objective: 'Maximize multi-criteria utility balancing urgency and equity.',
      complexity: 'O(R * V) utility computation.',
      keyMetrics: 'Workload Variance, Deadline Satisfaction Rate, Travel Distance.',
    },
    batch: {
      name: 'Batch Minimum-Weight Bipartite Matching',
      category: 'Volunteer Dispatch',
      problem: 'Globally optimize matching for a batch of rescue requests to minimize total fleet travel distance.',
      inputs: 'Complete bipartite graph matrix C where C[i][j] represents travel cost between Request i and Volunteer j.',
      coreIdea: 'Formulate as Linear Sum Assignment Problem (LSAP) and solve globally using the Hungarian Algorithm (scipy.optimize.linear_sum_assignment).',
      constraints: 'Feasibility constraints (capacity, refrigeration, max range), 1-to-1 matching bounds.',
      objective: 'Minimize sum of travel distances across all batch assignments.',
      complexity: 'O(N^3) polynomial time optimal matching.',
      keyMetrics: 'Global Minimum Total Travel Distance (km), Assignment Rate.',
    },
  };

  const active = algos[selectedTopic];

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <Header title="Educational Algorithm Explorer" subtitle="Viva & Technical Demonstration Documentation for Computational Engines" />

      <main className="p-8 space-y-8 flex-1">
        {/* Navigation Selector */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          {Object.entries(algos).map(([key, item]) => (
            <button
              key={key}
              onClick={() => setSelectedTopic(key as any)}
              className={`p-3 rounded-xl border text-left text-xs transition-all ${
                selectedTopic === key
                  ? 'bg-emerald-950/40 border-emerald-500 text-white font-bold shadow-inner'
                  : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              <span className="block font-semibold text-white">{item.name}</span>
              <span className="text-[10px] text-slate-500 font-mono mt-0.5">{item.category}</span>
            </button>
          ))}
        </div>

        {/* Algorithm Detail Sheet */}
        <div className="p-8 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-2xl space-y-6">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div>
              <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-900 uppercase">
                {active.category}
              </span>
              <h2 className="text-2xl font-bold text-white mt-2">{active.name}</h2>
            </div>
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-400">
              <Cpu className="w-6 h-6 text-emerald-400" />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs leading-relaxed">
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <h3 className="font-bold text-slate-300 uppercase font-mono text-[11px] mb-1">Problem Formulation</h3>
                <p className="text-slate-400">{active.problem}</p>
              </div>

              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <h3 className="font-bold text-slate-300 uppercase font-mono text-[11px] mb-1">Core Algorithm Idea</h3>
                <p className="text-slate-400">{active.coreIdea}</p>
              </div>

              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <h3 className="font-bold text-slate-300 uppercase font-mono text-[11px] mb-1">Input Parameters</h3>
                <p className="text-slate-400">{active.inputs}</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <h3 className="font-bold text-slate-300 uppercase font-mono text-[11px] mb-1">Constraints & Feasibility</h3>
                <p className="text-slate-400">{active.constraints}</p>
              </div>

              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <h3 className="font-bold text-slate-300 uppercase font-mono text-[11px] mb-1">Computational Complexity</h3>
                <p className="text-emerald-400 font-mono font-bold">{active.complexity}</p>
              </div>

              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <h3 className="font-bold text-slate-300 uppercase font-mono text-[11px] mb-1">Key Evaluation Metrics</h3>
                <p className="text-cyan-400 font-mono">{active.keyMetrics}</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
