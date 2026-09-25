'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/dashboard/Header';
import { donationsApi, Donation } from '@/lib/api/donations';
import { donorsApi, Donor } from '@/lib/api/donors';
import { Box, Plus, RefreshCw, Snowflake } from 'lucide-react';

export default function DonationsPage() {
  const [donations, setDonations] = useState<Donation[]>([]);
  const [donors, setDonors] = useState<Donor[]>([]);
  const [loading, setLoading] = useState(true);

  // Form modal
  const [showModal, setShowModal] = useState(false);
  const [donorId, setDonorId] = useState('');
  const [foodType, setFoodType] = useState('Prepared Meals');
  const [quantity, setQuantity] = useState(100);
  const [refrigerated, setRefrigerated] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    setLoading(true);
    try {
      const [donRes, donorRes] = await Promise.all([
        donationsApi.list().catch(() => []),
        donorsApi.list().catch(() => [])
      ]);
      setDonations(donRes);
      setDonors(donorRes);
      if (donorRes.length > 0) setDonorId(donorRes[0].id);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    try {
      await donationsApi.create({
        donor_id: donorId || (donors[0]?.id ?? 'donor_1'),
        food_type: foodType,
        quantity_kg: Number(quantity),
        requires_refrigeration: refrigerated
      });
      setShowModal(false);
      loadData();
    } catch (err: any) {
      alert('Error creating donation: ' + err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <Header title="Donations Management" subtitle="PostgreSQL Food Surplus Inventory Records" />

      <main className="p-8 space-y-6 flex-1">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-white">Active Food Surplus Items</h2>
            <p className="text-xs text-slate-400 mt-0.5">Manage food rescue contributions from registered donors</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold text-xs hover:from-emerald-400 hover:to-teal-400 transition-all flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Add Donation</span>
          </button>
        </div>

        {/* Data Table */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-[11px] font-mono text-slate-400 uppercase">
                  <th className="py-3 px-4">ID</th>
                  <th className="py-3 px-4">Food Type</th>
                  <th className="py-3 px-4">Donor ID</th>
                  <th className="py-3 px-4">Quantity (kg)</th>
                  <th className="py-3 px-4">Cold Chain Required</th>
                  <th className="py-3 px-4">Created At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {donations.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-6 text-center text-slate-500">No donation records found in PostgreSQL</td>
                  </tr>
                ) : (
                  donations.map((d) => (
                    <tr key={d.id} className="hover:bg-slate-800/40">
                      <td className="py-3.5 px-4 font-mono text-slate-400">{d.id.substring(0, 8)}...</td>
                      <td className="py-3.5 px-4 font-bold text-white flex items-center space-x-2">
                        <Box className="w-3.5 h-3.5 text-emerald-400" />
                        <span>{d.food_type}</span>
                      </td>
                      <td className="py-3.5 px-4 font-mono text-slate-300">{d.donor_id.substring(0, 8)}...</td>
                      <td className="py-3.5 px-4 text-emerald-400 font-mono font-bold">{d.quantity_kg} kg</td>
                      <td className="py-3.5 px-4">
                        {d.requires_refrigeration ? (
                          <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 text-[10px]">
                            <Snowflake className="w-3 h-3" />
                            <span>REFRIGERATED</span>
                          </span>
                        ) : (
                          <span className="px-2.5 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">AMBIENT</span>
                        )}
                      </td>
                      <td className="py-3.5 px-4 font-mono text-slate-500">{new Date(d.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Add Modal */}
        {showModal && (
          <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-6 shadow-2xl">
              <h3 className="text-lg font-bold text-white">Create New Donation</h3>
              <form onSubmit={handleSubmit} className="space-y-4 text-xs">
                <div>
                  <label className="block text-slate-400 mb-1">Donor</label>
                  <select
                    value={donorId}
                    onChange={(e) => setDonorId(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                  >
                    {donors.map(d => (
                      <option key={d.id} value={d.id}>{d.name} ({d.id.substring(0, 6)})</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-slate-400 mb-1">Food Type</label>
                  <input
                    type="text"
                    value={foodType}
                    onChange={(e) => setFoodType(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-slate-400 mb-1">Quantity (kg)</label>
                  <input
                    type="number"
                    value={quantity}
                    onChange={(e) => setQuantity(Number(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                    min="1"
                    required
                  />
                </div>

                <div className="flex items-center space-x-2 pt-2">
                  <input
                    type="checkbox"
                    checked={refrigerated}
                    onChange={(e) => setRefrigerated(e.target.checked)}
                    id="refrig"
                    className="rounded bg-slate-950 border-slate-800 text-emerald-500 focus:ring-0"
                  />
                  <label htmlFor="refrig" className="text-slate-300">Requires Refrigeration Cold Chain</label>
                </div>

                <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 font-semibold"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={saving}
                    className="px-5 py-2 rounded-xl bg-emerald-500 text-slate-950 font-bold hover:bg-emerald-400"
                  >
                    {saving ? 'Saving...' : 'Save Donation'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
