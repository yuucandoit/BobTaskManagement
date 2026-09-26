import React from 'react';
import EvidenceLink from './EvidenceLink';
import AlarmBadge from './AlarmBadge';
import { Tag, Clock, User2, Layers } from 'lucide-react';

export default function TaskCard({ card, onClick }) {
  const priorityColors = {
    Critical: 'bg-red-500/10 text-red-400 border-red-500/30',
    High: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
    Medium: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    Low: 'bg-slate-500/10 text-slate-400 border-slate-500/30',
  };

  const typeColors = {
    feature: 'text-emerald-400 bg-emerald-950/40 border-emerald-800/40',
    bugfix: 'text-rose-400 bg-rose-950/40 border-rose-800/40',
    refactor: 'text-indigo-400 bg-indigo-950/40 border-indigo-800/40',
    chore: 'text-amber-400 bg-amber-950/40 border-amber-800/40',
    docs: 'text-teal-400 bg-teal-950/40 border-teal-800/40',
  };

  return (
    <div
      onClick={() => onClick && onClick(card)}
      className="group relative bg-[#161b22] hover:bg-[#1c2128] border border-[#30363d] hover:border-slate-500 rounded-xl p-4 transition-all duration-200 cursor-pointer shadow-md hover:shadow-xl flex flex-col gap-3"
    >
      {/* Top row: Badges & Alarms */}
      <div className="flex items-center justify-between gap-2 flex-wrap">
        <div className="flex items-center gap-1.5 flex-wrap">
          <span
            className={`px-2 py-0.5 rounded text-[11px] font-medium uppercase tracking-wider border ${
              typeColors[card.task_type] || typeColors.feature
            }`}
          >
            {card.task_type}
          </span>
          <span
            className={`px-2 py-0.5 rounded text-[11px] font-medium border ${
              priorityColors[card.priority] || priorityColors.Medium
            }`}
          >
            {card.priority}
          </span>
          {card.repo_name && (
            <span
              className="px-1.5 py-0.5 rounded text-[10px] font-mono text-slate-400 bg-[#0d1117] border border-[#30363d] truncate max-w-[130px]"
              title={`Repository: ${card.repo_name}`}
            >
              {card.repo_name.split('/')[1] || card.repo_name}
            </span>
          )}
        </div>

        {/* Story points */}
        {card.story_points && (
          <span className="inline-flex items-center gap-1 text-[11px] font-mono text-slate-400 bg-[#0d1117] px-2 py-0.5 rounded border border-[#30363d]">
            <Layers className="w-3 h-3 text-slate-500" />
            {card.story_points} SP
          </span>
        )}
      </div>

      {/* Alarms row if triggered */}
      {(card.is_stale_pr || card.is_scope_creep) && (
        <div className="flex items-center gap-1.5 flex-wrap pt-0.5">
          {card.is_stale_pr && (
            <AlarmBadge type="stale" days={card.days_inactive} />
          )}
          {card.is_scope_creep && (
            <AlarmBadge type="scope_creep" ratio={card.scope_creep_ratio} />
          )}
        </div>
      )}

      {/* Title & Description */}
      <div>
        <h4 className="text-sm font-semibold text-slate-100 group-hover:text-blue-400 transition-colors line-clamp-2">
          {card.title}
        </h4>
        {card.description && (
          <p className="text-xs text-slate-400 mt-1 line-clamp-2 leading-relaxed">
            {card.description}
          </p>
        )}
      </div>

      {/* Evidence Link Section (Fitur Wajib #3) */}
      {card.evidences && card.evidences.length > 0 && (
        <div className="pt-2 border-t border-[#21262d] flex items-center gap-2 flex-wrap">
          <span className="text-[11px] uppercase tracking-wider text-slate-500 font-semibold">
            Bukti:
          </span>
          {card.evidences.slice(0, 2).map((ev) => (
            <EvidenceLink key={ev.id} evidence={ev} isMini={true} />
          ))}
          {card.evidences.length > 2 && (
            <span className="text-[11px] text-slate-400">+{card.evidences.length - 2} lagi</span>
          )}
        </div>
      )}

      {/* Footer: Assignee & Estimation */}
      <div className="flex items-center justify-between pt-2 border-t border-[#21262d] text-xs text-slate-400 mt-auto">
        <div className="flex items-center gap-1.5 min-w-0">
          {card.assignee_avatar ? (
            <img
              src={card.assignee_avatar}
              alt={card.assignee_name || 'Assignee'}
              className="w-5 h-5 rounded-full ring-1 ring-slate-700 shrink-0"
            />
          ) : (
            <div className="w-5 h-5 rounded-full bg-[#21262d] flex items-center justify-center shrink-0">
              <User2 className="w-3 h-3 text-slate-400" />
            </div>
          )}
          <span className="truncate max-w-[110px] text-slate-300 font-medium">
            {card.assignee_name || 'Unassigned'}
          </span>
        </div>

        {card.estimation_hours && (
          <div className="flex items-center gap-1 font-mono text-[11px] text-slate-400">
            <Clock className="w-3 h-3 text-slate-500" />
            <span>{card.estimation_hours}h</span>
          </div>
        )}
      </div>
    </div>
  );
}
