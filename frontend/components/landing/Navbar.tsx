'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowRight, Cpu, Layers } from 'lucide-react';

export function LandingNavbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800/80 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-cyan-500 p-0.5 shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Cpu className="w-5 h-5 text-emerald-400" />
            </div>
          </div>
          <div>
            <span className="text-lg font-bold bg-gradient-to-r from-white via-slate-200 to-emerald-400 bg-clip-text text-transparent">
              FRADMS
            </span>
            <span className="hidden sm:inline-block text-xs font-mono text-slate-500 ml-2">v1.0 Engine</span>
          </div>
        </Link>

        <div className="hidden md:flex items-center space-x-8 text-sm text-slate-300 font-medium">
          <a href="#how-it-works" className="hover:text-emerald-400 transition-colors">How It Works</a>
          <a href="#algorithms" className="hover:text-emerald-400 transition-colors">Algorithms</a>
          <a href="#metrics" className="hover:text-emerald-400 transition-colors">Evaluation Metrics</a>
        </div>

        <div className="flex items-center space-x-4">
          <Link
            href="/dashboard"
            className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-semibold text-sm transition-all shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40 active:scale-95"
          >
            <span>Enter Platform</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </nav>
  );
}
