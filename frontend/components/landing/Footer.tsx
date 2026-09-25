'use client';

import React from 'react';
import Link from 'next/link';

export function LandingFooter() {
  return (
    <footer className="border-t border-slate-800/80 bg-slate-950 py-12 px-6">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-slate-400 text-xs">
        <div>
          <span className="font-bold text-white text-sm">FRADMS</span>
          <p className="mt-1 text-slate-500">Fair Resource Allocation & Dynamic Matching System</p>
        </div>
        <div className="flex space-x-6 text-slate-400 font-medium">
          <Link href="/dashboard" className="hover:text-emerald-400 transition-colors">Dashboard</Link>
          <Link href="/dashboard/allocation" className="hover:text-emerald-400 transition-colors">Allocation Engine</Link>
          <Link href="/dashboard/dispatch" className="hover:text-emerald-400 transition-colors">Dispatch Engine</Link>
          <Link href="/dashboard/benchmarks" className="hover:text-emerald-400 transition-colors">Benchmarks</Link>
        </div>
        <p className="text-slate-600">© 2026 FRADMS. Computer Science & Algorithmic Logistics Platform.</p>
      </div>
    </footer>
  );
}
