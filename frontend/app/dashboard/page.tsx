'use client';

import React, { useEffect, useState } from 'react';
import { Header } from '@/components/dashboard/Header';
import { donationsApi, Donation } from '@/lib/api/donations';
import { agenciesApi, Agency } from '@/lib/api/agencies';
import { volunteersApi, Volunteer } from '@/lib/api/volunteers';
import { rescueRequestsApi, RescueRequest } from '@/lib/api/rescueRequests';
import { allocationApi } from '@/lib/api/allocation';
import { dispatchApi } from '@/lib/api/dispatch';

import {
  Activity,
  AlertTriangle,
  BarChart3,
  Box,
  Building2,
  CheckCircle,
  Clock,
  Layers,
  MapPin,
  Scale,
  Truck,
  Users,
} from 'lucide-react';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';

export default function OverviewDashboard() {
  const [donations, setDonations] = useState<Donation[]>([]);
  const [agencies, setAgencies] = useState<Agency[]>([]);
  const [volunteers, setVolunteers] = useState<Volunteer[]>([]);
  const [requests, setRequests] = useState<RescueRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [donRes, agRes, volRes, reqRes] = await Promise.all([
          donationsApi.list().catch(() => []),
          agenciesApi.list().catch(() => []),
          volunteersApi.list().catch(() => []),
          rescueRequestsApi.list().catch(() => []),
        ]);

        setDonations(donRes);
        setAgencies(agRes);
        setVolunteers(volRes);
        setRequests(reqRes);
      } catch (err: any) {
        setError(err.message || 'Failed to connect to backend database.');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const totalFoodKg = donations.reduce((acc, d) => acc + d.quantity_kg, 0);
  const totalDemandKg = agencies.reduce((acc, a) => acc + a.demand_kg, 0);
  const activeVolunteersCount = volunteers.length;
  const pendingRequestsCount = requests.filter(r => r.status === 'pending').length;

  // Recharts Data Prep
  const agencyChartData = agencies.slice(0, 5).map(a => ({
    name: a.name.length > 12 ? a.name.substring(0, 12) + '...' : a.name,
    Demand: a.demand_kg,
    Capacity: a.storage_capacity_kg,
  }));

  const volunteerWorkloadData = volunteers.slice(0, 5).map(v => ({
    name: v.name,
    Workload: v.current_workload_kg,
    Capacity: v.capacity_kg,
  }));

  const statusPieData = [
    { name: 'Pending', value: requests.filter(r => r.status === 'pending').length || 1, color: '#f59e0b' },
    { name: 'Assigned', value: requests.filter(r => r.status === 'assigned').length || 0, color: '#06b6d4' },
    { name: 'Completed', value: requests.filter(r => r.status === 'completed').length || 0, color: '#10b981' },
  ];

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <Header title="Operations Overview Dashboard" subtitle="Real-Time FRADMS Database & Decision Metrics" />

      <main className="p-8 space-y-8 flex-1">
        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center space-x-3">
            <AlertTriangle className="w-5 h-5 text-rose-400 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Operational Stat Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-lg relative overflow-hidden group">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono text-slate-400 uppercase">Total Food Supply</span>
              <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <Box className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-4">
              <h2 className="text-3xl font-extrabold text-white">{loading ? '...' : `${totalFoodKg} kg`}</h2>
              <p className="text-xs text-slate-500 mt-1">{donations.length} Active Donations</p>
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-lg relative overflow-hidden group">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono text-slate-400 uppercase">Total Agency Demand</span>
              <div className="p-2 rounded-xl bg-teal-500/10 text-teal-400 border border-teal-500/20">
                <Building2 className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-4">
              <h2 className="text-3xl font-extrabold text-white">{loading ? '...' : `${totalDemandKg} kg`}</h2>
              <p className="text-xs text-slate-500 mt-1">{agencies.length} Registered Agencies</p>
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-lg relative overflow-hidden group">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono text-slate-400 uppercase">Active Volunteers</span>
              <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                <Users className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-4">
              <h2 className="text-3xl font-extrabold text-white">{loading ? '...' : activeVolunteersCount}</h2>
              <p className="text-xs text-slate-500 mt-1">Available for Dispatch</p>
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-lg relative overflow-hidden group">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono text-slate-400 uppercase">Pending Requests</span>
              <div className="p-2 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
                <Clock className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-4">
              <h2 className="text-3xl font-extrabold text-white">{loading ? '...' : requests.length}</h2>
              <p className="text-xs text-slate-500 mt-1">{pendingRequestsCount} Pending Matching</p>
            </div>
          </div>
        </div>

        {/* Operational Analytics & Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Agency Demand vs Capacity Chart */}
          <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-base font-bold text-white">Agency Food Demand vs Capacity</h3>
                <p className="text-xs text-slate-400 mt-0.5">Primary recipient agency specifications (kg)</p>
              </div>
              <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-900">
                PostgreSQL Data
              </span>
            </div>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={agencyChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
                  <YAxis stroke="#64748b" fontSize={11} />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                  <Bar dataKey="Demand" fill="#10b981" radius={[6, 6, 0, 0]} />
                  <Bar dataKey="Capacity" fill="#06b6d4" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Rescue Request Status Pie Chart */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl flex flex-col justify-between">
            <div>
              <h3 className="text-base font-bold text-white mb-1">Rescue Task Status</h3>
              <p className="text-xs text-slate-400">Current rescue requests state breakdown</p>
            </div>
            <div className="h-56 w-full flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={statusPieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={75}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {statusPieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                  <Legend wrapperStyle={{ fontSize: '11px', color: '#94a3b8' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Live Data Tables Overview Preview */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Donations Table */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl">
            <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
              <Box className="w-4 h-4 text-emerald-400" />
              <span>Available Food Donations</span>
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase">
                    <th className="py-2.5 px-3">Food Type</th>
                    <th className="py-2.5 px-3">Quantity</th>
                    <th className="py-2.5 px-3">Cold Chain</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-xs">
                  {donations.length === 0 ? (
                    <tr>
                      <td colSpan={3} className="py-4 text-center text-slate-500">No donations available</td>
                    </tr>
                  ) : (
                    donations.slice(0, 4).map((d) => (
                      <tr key={d.id} className="hover:bg-slate-800/40">
                        <td className="py-3 px-3 font-semibold text-white">{d.food_type}</td>
                        <td className="py-3 px-3 text-emerald-400 font-mono font-bold">{d.quantity_kg} kg</td>
                        <td className="py-3 px-3">
                          {d.requires_refrigeration ? (
                            <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 text-[10px]">Refrigerated</span>
                          ) : (
                            <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">Standard</span>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Active Volunteers Preview */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl">
            <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
              <Users className="w-4 h-4 text-cyan-400" />
              <span>Registered Volunteers</span>
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase">
                    <th className="py-2.5 px-3">Name</th>
                    <th className="py-2.5 px-3">Vehicle Capacity</th>
                    <th className="py-2.5 px-3">Max Travel</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-xs">
                  {volunteers.length === 0 ? (
                    <tr>
                      <td colSpan={3} className="py-4 text-center text-slate-500">No volunteers available</td>
                    </tr>
                  ) : (
                    volunteers.slice(0, 4).map((v) => (
                      <tr key={v.id} className="hover:bg-slate-800/40">
                        <td className="py-3 px-3 font-semibold text-white">{v.name}</td>
                        <td className="py-3 px-3 text-cyan-400 font-mono font-bold">{v.capacity_kg} kg</td>
                        <td className="py-3 px-3 text-slate-300 font-mono">{v.max_travel_distance_km} km</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
