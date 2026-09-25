'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft, Database, RefreshCw, Zap } from 'lucide-react';

export function Header({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md px-8 py-5 flex items-center justify-between sticky top-0 z-30">
      <div>
        <h1 className="text-xl font-bold text-white tracking-tight">{title}</h1>
        {subtitle && <p className="text-xs text-slate-400 mt-0.5 font-mono">{subtitle}</p>}
      </div>

      <div className="flex items-center space-x-4">
        <div className="hidden sm:flex items-center space-x-2 text-xs font-mono text-slate-400 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg">
          <Database className="w-3.5 h-3.5 text-emerald-400" />
          <span>PostgreSQL Active</span>
        </div>

        <Link
          href="/"
          className="flex items-center space-x-2 text-xs font-semibold text-slate-300 hover:text-white bg-slate-900 hover:bg-slate-800 border border-slate-800 px-3.5 py-2 rounded-lg transition-all"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Landing Page</span>
        </Link>
      </div>
    </header>
  );
}
