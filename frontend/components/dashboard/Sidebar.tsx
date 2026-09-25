'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Activity,
  BarChart3,
  Box,
  Building2,
  Cpu,
  GitPullRequest,
  Home,
  Layers,
  Scale,
  Sliders,
  Truck,
  Users,
} from 'lucide-react';

export function Sidebar() {
  const pathname = usePathname();

  const groups = [
    {
      title: 'Main',
      items: [
        { name: 'Overview', href: '/dashboard', icon: Home },
      ],
    },
    {
      title: 'Operations Engine',
      items: [
        { name: 'Food Allocation', href: '/dashboard/allocation', icon: Scale },
        { name: 'Volunteer Dispatch', href: '/dashboard/dispatch', icon: Truck },
        { name: 'Donations', href: '/dashboard/donations', icon: Box },
        { name: 'Agencies', href: '/dashboard/agencies', icon: Building2 },
        { name: 'Volunteers', href: '/dashboard/volunteers', icon: Users },
        { name: 'Rescue Requests', href: '/dashboard/rescue-requests', icon: GitPullRequest },
      ],
    },
    {
      title: 'Analysis & Benchmarking',
      items: [
        { name: 'Simulation', href: '/dashboard/simulation', icon: Sliders },
        { name: 'Benchmarks', href: '/dashboard/benchmarks', icon: BarChart3 },
        { name: 'Analytics', href: '/dashboard/analytics', icon: Activity },
        { name: 'Algorithm Explorer', href: '/dashboard/algorithm-explorer', icon: Cpu },
      ],
    },
  ];

  return (
    <aside className="w-64 bg-slate-950/90 border-r border-slate-800/80 flex flex-col justify-between shrink-0 h-screen sticky top-0 z-40 backdrop-blur-md">
      <div>
        {/* Brand Header */}
        <div className="p-5 border-b border-slate-800/80 flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-cyan-500 p-0.5 shadow-md shadow-emerald-500/20">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Cpu className="w-5 h-5 text-emerald-400" />
            </div>
          </div>
          <div>
            <h1 className="font-bold text-white text-base leading-none">FRADMS</h1>
            <p className="text-[11px] font-mono text-slate-400 mt-1">Platform v1.0</p>
          </div>
        </div>

        {/* Navigation Links */}
        <div className="p-4 space-y-6 overflow-y-auto max-h-[calc(100vh-140px)]">
          {groups.map((group, idx) => (
            <div key={idx}>
              <h2 className="px-3 text-[11px] font-mono uppercase tracking-wider text-slate-500 mb-2 font-semibold">
                {group.title}
              </h2>
              <div className="space-y-1">
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`flex items-center space-x-3 px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                        isActive
                          ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 shadow-inner font-semibold'
                          : 'text-slate-400 hover:text-white hover:bg-slate-900/80'
                      }`}
                    >
                      <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-400' : 'text-slate-500'}`} />
                      <span>{item.name}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Database Health Pill */}
      <div className="p-4 border-t border-slate-800/80">
        <div className="p-3 rounded-xl bg-slate-900/90 border border-slate-800 flex items-center justify-between text-xs">
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-slate-300 font-mono text-[11px]">PostgreSQL DB</span>
          </div>
          <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-900">
            ONLINE
          </span>
        </div>
      </div>
    </aside>
  );
}
