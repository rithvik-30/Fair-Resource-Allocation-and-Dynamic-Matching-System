'use client';

import React, { useEffect, useRef } from 'react';

export function CursorRingField() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = canvas.parentElement?.clientWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.clientHeight || 400);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = canvas.parentElement?.clientWidth || window.innerWidth;
      height = canvas.height = canvas.parentElement?.clientHeight || 400;
    };
    window.addEventListener('resize', handleResize);

    const mouse = { x: width / 2, y: height / 2, targetX: width / 2, targetY: height / 2 };

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouse.targetX = e.clientX - rect.left;
      mouse.targetY = e.clientY - rect.top;
    };
    window.addEventListener('mousemove', handleMouseMove);

    // Create node field
    const numParticles = 35;
    const particles = Array.from({ length: numParticles }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.8,
      vy: (Math.random() - 0.5) * 0.8,
      radius: Math.random() * 2 + 1.5,
      angle: Math.random() * Math.PI * 2,
    }));

    let ringAngle = 0;

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Smooth mouse easing
      mouse.x += (mouse.targetX - mouse.x) * 0.1;
      mouse.y += (mouse.targetY - mouse.y) * 0.1;

      ringAngle += 0.02;

      // Draw Cursor Glowing Ring
      const ringRadius = 60;
      ctx.save();
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, ringRadius, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(16, 185, 129, 0.4)';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([8, 8]);
      ctx.stroke();
      ctx.restore();

      // Outer Pulsing Glow Ring
      const outerRadius = ringRadius + Math.sin(ringAngle * 2) * 8;
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, outerRadius, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(6, 182, 212, 0.2)';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Draw particles & cursor connections
      particles.forEach((p, i) => {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        // Distance to cursor
        const dx = mouse.x - p.x;
        const dy = mouse.y - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        // Pull towards cursor if inside field
        if (dist < 180) {
          const force = (180 - dist) / 180;
          p.x += (dx / dist) * force * 0.6;
          p.y += (dy / dist) * force * 0.6;

          // Draw line to cursor
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = `rgba(16, 185, 129, ${0.3 * force})`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }

        // Draw particle node
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = dist < 180 ? '#10b981' : '#334155';
        ctx.shadowColor = '#10b981';
        ctx.shadowBlur = dist < 180 ? 10 : 0;
        ctx.fill();

        // Connect nearby particles
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const pdx = p2.x - p.x;
          const pdy = p2.y - p.y;
          const pdist = Math.sqrt(pdx * pdx + pdy * pdy);
          if (pdist < 100) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(51, 65, 85, ${0.2 * (1 - pdist / 100)})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div className="relative w-full h-72 md:h-80 rounded-2xl overflow-hidden border border-slate-800 bg-slate-950/80 backdrop-blur-md shadow-2xl my-8">
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full cursor-crosshair" />
      <div className="absolute top-4 left-4 pointer-events-none flex items-center space-x-2 bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-full text-xs font-mono text-emerald-400">
        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
        <span>CURSOR RING FIELD INTERACTIVE ENGINE</span>
      </div>
      <div className="absolute bottom-4 right-4 pointer-events-none text-right">
        <p className="text-xs text-slate-400 font-mono">Move cursor over field to interact</p>
        <p className="text-[10px] text-slate-500 font-mono">Dynamic node attraction & field response</p>
      </div>
    </div>
  );
}
