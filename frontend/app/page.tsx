import React from 'react';
import { LandingNavbar } from '@/components/landing/Navbar';
import { LandingHero } from '@/components/landing/Hero';
import { HowItWorks } from '@/components/landing/HowItWorks';
import { AlgorithmsSection } from '@/components/landing/AlgorithmsSection';
import { MetricsSection } from '@/components/landing/MetricsSection';
import { LandingFooter } from '@/components/landing/Footer';

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-[#090d16] text-slate-100 overflow-x-hidden selection:bg-emerald-500/30">
      <LandingNavbar />
      <LandingHero />
      <HowItWorks />
      <AlgorithmsSection />
      <MetricsSection />
      <LandingFooter />
    </main>
  );
}
