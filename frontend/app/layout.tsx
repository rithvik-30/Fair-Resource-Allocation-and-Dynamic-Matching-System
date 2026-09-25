import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'FRADMS - Fair Resource Allocation & Dynamic Matching System',
  description: 'An algorithmic decision-support platform for food rescue logistics.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark scroll-smooth">
      <body className="bg-[#090d16] text-slate-100 font-sans antialiased min-h-screen selection:bg-emerald-500/30 selection:text-emerald-300">
        {children}
      </body>
    </html>
  );
}
