'use client';

import React from 'react';
import Link from 'next/link';
import { CursorRingField } from '@/components/ui/cursor-ring-field';
import { ArrowRight, Sparkles, Zap } from 'lucide-react';

export function LandingHero() {
  return (
    <section className="relative pt-32 pb-16 px-6 max-w-7xl mx-auto">
      {/* Background glow ambient elements */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-emerald-500/10 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute top-1/3 right-1/4 w-[400px] h-[250px] bg-cyan-500/10 blur-[100px] rounded-full pointer-events-none" />

      <div className="relative text-center max-w-3xl mx-auto space-y-6">
        <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-slate-900/90 border border-emerald-500/30 text-emerald-400 text-xs font-mono mb-2 shadow-inner">
          <Sparkles className="w-3.5 h-3.5" />
          <span>ALGORITHMIC DECISION-SUPPORT ENGINE</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
          Smarter Food Rescue.<br />
          <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
            Fairer Allocation. Dynamic Dispatch.
          </span>
        </h1>

        <p className="text-slate-400 text-base sm:text-lg leading-relaxed max-w-2xl mx-auto">
          An offline-runnable, algorithm-first platform optimizing food distribution across recipient agencies with Jain&apos;s Max-Min fairness metrics and matching dynamic volunteers via Minimum-Weight Bipartite graph dispatch.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Link
            href="/dashboard"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold text-base hover:from-emerald-400 hover:to-teal-400 transition-all shadow-xl shadow-emerald-500/30 flex items-center justify-center space-x-2 group"
          >
            <span>Enter Platform</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>

          <a
            href="#algorithms"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-200 font-semibold text-base hover:bg-slate-800 transition-all flex items-center justify-center space-x-2"
          >
            <Zap className="w-5 h-5 text-cyan-400" />
            <span>Explore Algorithms</span>
          </a>
        </div>
      </div>

      {/* Embedded Official Originkit Cursor Ring Field Visualizer */}
      <CursorRingField />
    </section>
  );
}
