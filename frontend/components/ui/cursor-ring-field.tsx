'use client';

import React, { useEffect, useRef } from 'react';

export interface CursorRingFieldProps {
  className?: string;
  ringRadius?: number;
  particleCount?: number;
  accentColor?: string;
  glowColor?: string;
}

/**
 * Originkit Cursor Ring Field Component
 * Official component providing dynamic mouse cursor tracking, radial particle attraction,
 * and ambient canvas glows for landing page hero sections.
 */
export function CursorRingField({
  className = '',
  ringRadius = 60,
  particleCount = 40,
  accentColor = '#10b981',
  glowColor = 'rgba(6, 182, 212, 0.25)',
}: CursorRingFieldProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;
    let width = (canvas.width = canvas.parentElement?.clientWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.clientHeight || 360);

    const onResize = () => {
      if (!canvas) return;
      width = canvas.width = canvas.parentElement?.clientWidth || window.innerWidth;
      height = canvas.height = canvas.parentElement?.clientHeight || 360;
    };
    window.addEventListener('resize', onResize);

    const mouse = {
      x: width / 2,
      y: height / 2,
      targetX: width / 2,
      targetY: height / 2,
    };

    const onMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouse.targetX = e.clientX - rect.left;
      mouse.targetY = e.clientY - rect.top;
    };
    window.addEventListener('mousemove', onMouseMove);

    // Initialize Originkit particle node array
    const particles = Array.from({ length: particleCount }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.7,
      vy: (Math.random() - 0.5) * 0.7,
      size: Math.random() * 2 + 1,
    }));

    let pulse = 0;

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Smooth cursor lerp
      mouse.x += (mouse.targetX - mouse.x) * 0.12;
      mouse.y += (mouse.targetY - mouse.y) * 0.12;
      pulse += 0.025;

      // Draw Outer Glow Ring
      const currentRadius = ringRadius + Math.sin(pulse * 2) * 6;
      ctx.save();
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, currentRadius, 0, Math.PI * 2);
      ctx.strokeStyle = glowColor;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Draw Inner Cursor Ring
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, ringRadius * 0.7, 0, Math.PI * 2);
      ctx.strokeStyle = accentColor;
      ctx.lineWidth = 2;
      ctx.setLineDash([6, 6]);
      ctx.stroke();
      ctx.restore();

      // Render nodes & dynamic spring forces
      particles.forEach((p, idx) => {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        const dx = mouse.x - p.x;
        const dy = mouse.y - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 160) {
          const factor = (160 - dist) / 160;
          p.x += (dx / dist) * factor * 0.5;
          p.y += (dy / dist) * factor * 0.5;

          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = `rgba(16, 185, 129, ${0.35 * factor})`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = dist < 160 ? accentColor : '#475569';
        ctx.shadowColor = accentColor;
        ctx.shadowBlur = dist < 160 ? 8 : 0;
        ctx.fill();

        // Connect adjacent node web
        for (let j = idx + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const pdx = p2.x - p.x;
          const pdy = p2.y - p.y;
          const pdist = Math.sqrt(pdx * pdx + pdy * pdy);
          if (pdist < 90) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(51, 65, 85, ${0.25 * (1 - pdist / 90)})`;
            ctx.lineWidth = 0.7;
            ctx.stroke();
          }
        }
      });

      animId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', onResize);
      window.removeEventListener('mousemove', onMouseMove);
      cancelAnimationFrame(animId);
    };
  }, [ringRadius, particleCount, accentColor, glowColor]);

  return (
    <div
      className={`relative w-full h-72 sm:h-80 rounded-2xl overflow-hidden border border-slate-800/90 bg-slate-950/80 backdrop-blur-md shadow-2xl my-8 ${className}`}
    >
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full cursor-crosshair" />
      <div className="absolute top-4 left-4 pointer-events-none flex items-center space-x-2 bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-full text-xs font-mono text-emerald-400">
        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
        <span>ORIGINKIT CURSOR RING FIELD</span>
      </div>
      <div className="absolute bottom-4 right-4 pointer-events-none text-right">
        <p className="text-xs text-slate-400 font-mono">Move cursor over field to interact</p>
        <p className="text-[10px] text-slate-500 font-mono">Official Originkit React Component</p>
      </div>
    </div>
  );
}

export default CursorRingField;
