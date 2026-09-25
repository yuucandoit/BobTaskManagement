import React from 'react';
import KanbanColumn from './KanbanColumn';
import { AlertCircle, TrendingUp, Users, CheckCircle2, ShieldCheck, RefreshCw } from 'lucide-react';

export default function KanbanBoard({ board, onCardClick, onAddCard, onRefresh, isRefreshing = false }) {
  if (!board) return null;

  const { columns, stats, total_cards } = board;

  return (
    <div className="flex flex-col gap-6 w-full">
      {/* Metrics Banner */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-3 flex items-center justify-between">
          <div>
            <span className="text-xs text-slate-400 font-medium">Total Kartu</span>
            <p className="text-xl font-bold text-slate-100 font-mono mt-0.5">{total_cards}</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center">
            <CheckCircle2 className="w-4 h-4" />
          </div>
        </div>

        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-3 flex items-center justify-between">
          <div>
            <span className="text-xs text-slate-400 font-medium">Bukti Terverifikasi</span>
            <p className="text-xl font-bold text-emerald-400 font-mono mt-0.5">{stats?.total_evidences || 0}</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <ShieldCheck className="w-4 h-4" />
          </div>
        </div>

        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-3 flex items-center justify-between">
          <div>
            <span className="text-xs text-slate-400 font-medium">Alarm PR Diam</span>
            <p className="text-xl font-bold text-red-400 font-mono mt-0.5">{stats?.stale_pr_alerts || 0}</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-red-500/10 text-red-400 flex items-center justify-center">
            <AlertCircle className="w-4 h-4" />
          </div>
        </div>

        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-3 flex items-center justify-between">
          <div>
            <span className="text-xs text-slate-400 font-medium">Scope Creep</span>
            <p className="text-xl font-bold text-amber-400 font-mono mt-0.5">{stats?.scope_creep_alerts || 0}</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center">
            <TrendingUp className="w-4 h-4" />
          </div>
        </div>

        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-3 flex items-center justify-between col-span-2 md:col-span-1">
          <div>
            <span className="text-xs text-slate-400 font-medium">Developer Aktif</span>
            <p className="text-xl font-bold text-purple-400 font-mono mt-0.5">{stats?.active_devs || 0}</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center">
            <Users className="w-4 h-4" />
          </div>
        </div>
      </div>

      {/* 3 Columns Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <KanbanColumn
          columnId="to_do"
          title={columns?.to_do?.title || 'To Do'}
          count={columns?.to_do?.count || 0}
          cards={columns?.to_do?.cards || []}
          onCardClick={onCardClick}
          onAddCard={onAddCard}
        />

        <KanbanColumn
          columnId="in_progress"
          title={columns?.in_progress?.title || 'In Progress'}
          count={columns?.in_progress?.count || 0}
          cards={columns?.in_progress?.cards || []}
          onCardClick={onCardClick}
        />

        <KanbanColumn
          columnId="done"
          title={columns?.done?.title || 'Done'}
          count={columns?.done?.count || 0}
          cards={columns?.done?.cards || []}
          onCardClick={onCardClick}
        />
      </div>
    </div>
  );
}
