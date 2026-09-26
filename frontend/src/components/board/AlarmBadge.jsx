import React from 'react';
import { AlertCircle, Clock, TrendingUp } from 'lucide-react';

export default function AlarmBadge({ type, detail, days = null, ratio = null }) {
  if (type === 'stale') {
    return (
      <div
        className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium bg-red-950/60 text-red-400 border border-red-800/80 animate-pulse shadow-sm"
        title={`PR has been inactive for ${days || '>2'} days`}
      >
        <Clock className="w-3 h-3 text-red-400 shrink-0" />
        <span>Inactive {days ? `${days}d` : '>2d'}</span>
      </div>
    );
  }

  if (type === 'scope_creep') {
    return (
      <div
        className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium bg-amber-950/60 text-amber-300 border border-amber-800/80"
        title={`Code diff size is ${ratio ? `${ratio}x` : '>3x'} larger than initial estimate`}
      >
        <TrendingUp className="w-3 h-3 text-amber-400 shrink-0" />
        <span>Scope Creep {ratio ? `(${ratio}x)` : ''}</span>
      </div>
    );
  }

  return (
    <div className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-slate-300">
      <AlertCircle className="w-3 h-3" />
      <span>{detail || 'Warning'}</span>
    </div>
  );
}
