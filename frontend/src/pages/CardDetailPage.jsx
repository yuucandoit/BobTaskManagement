import React, { useState } from 'react';
import EvidenceLink from '../components/board/EvidenceLink';
import AlarmBadge from '../components/board/AlarmBadge';
import { GitPullRequest, GitCommit, Clock, User, Layers, History, ExternalLink, Trash2, Edit3 } from 'lucide-react';
import { cardsApi } from '../services/api';

export default function CardDetailPage({ card, onClose, onCardUpdated }) {
  if (!card) return null;

  const [status, setStatus] = useState(card.status);
  const [updating, setUpdating] = useState(false);

  const handleStatusChange = async (newStatus) => {
    setStatus(newStatus);
    setUpdating(true);
    try {
      const updated = await cardsApi.update(card.id, { status: newStatus });
      if (onCardUpdated) onCardUpdated(updated);
    } catch (err) {
      console.error('Failed to update status:', err);
    } finally {
      setUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Yakin ingin menghapus kartu ini?')) {
      try {
        await cardsApi.delete(card.id);
        if (onCardUpdated) onCardUpdated(null);
        if (onClose) onClose();
      } catch (err) {
        console.error('Failed to delete card:', err);
      }
    }
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Top Banner / Actions */}
      <div className="flex items-center justify-between gap-4 flex-wrap pb-4 border-b border-[#30363d]">
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400 font-medium">Status:</span>
          <select
            value={status}
            onChange={(e) => handleStatusChange(e.target.value)}
            disabled={updating}
            className="bg-[#0d1117] border border-[#30363d] rounded-lg px-3 py-1 text-xs font-semibold text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="To Do">To Do</option>
            <option value="In Progress">In Progress</option>
            <option value="Done">Done</option>
          </select>
        </div>

        <button
          onClick={handleDelete}
          className="flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium text-rose-400 hover:bg-rose-950/40 border border-transparent hover:border-rose-800/40 transition-colors"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>Hapus Kartu</span>
        </button>
      </div>

      {/* Alarms row */}
      {(card.is_stale_pr || card.is_scope_creep) && (
        <div className="flex items-center gap-2 p-3 bg-red-950/30 border border-red-900/50 rounded-xl">
          {card.is_stale_pr && (
            <AlarmBadge type="stale" days={card.days_inactive} />
          )}
          {card.is_scope_creep && (
            <AlarmBadge type="scope_creep" ratio={card.scope_creep_ratio} />
          )}
        </div>
      )}

      {/* Description */}
      <div>
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
          Deskripsi & Ringkasan AI
        </h4>
        <p className="text-sm text-slate-200 leading-relaxed bg-[#0d1117] p-3.5 rounded-xl border border-[#30363d]">
          {card.description || 'Tidak ada deskripsi detail.'}
        </p>
      </div>

      {/* Attributes Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="p-3 bg-[#0d1117] rounded-xl border border-[#30363d]">
          <span className="text-[11px] text-slate-500 uppercase tracking-wider block">Assignee</span>
          <div className="flex items-center gap-2 mt-1">
            {card.assignee_avatar && (
              <img src={card.assignee_avatar} alt="Avatar" className="w-4 h-4 rounded-full" />
            )}
            <span className="text-xs font-semibold text-slate-200 truncate">
              {card.assignee_name || 'Unassigned'}
            </span>
          </div>
        </div>

        <div className="p-3 bg-[#0d1117] rounded-xl border border-[#30363d]">
          <span className="text-[11px] text-slate-500 uppercase tracking-wider block">Estimasi</span>
          <p className="text-xs font-semibold text-slate-200 mt-1 font-mono">
            {card.estimation_hours} jam ({card.story_points} SP)
          </p>
        </div>

        <div className="p-3 bg-[#0d1117] rounded-xl border border-[#30363d]">
          <span className="text-[11px] text-slate-500 uppercase tracking-wider block">Diff Kode</span>
          <p className="text-xs font-semibold text-slate-200 mt-1 font-mono">
            {card.diff_loc || 0} LOC
          </p>
        </div>

        <div className="p-3 bg-[#0d1117] rounded-xl border border-[#30363d]">
          <span className="text-[11px] text-slate-500 uppercase tracking-wider block">Asal Kartu</span>
          <p className="text-xs font-semibold text-slate-200 mt-1 font-mono uppercase">
            {card.origin || 'github_pr'}
          </p>
        </div>
      </div>

      {/* Evidence Section (Fitur Wajib #3) */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Tautan Bukti ({card.evidences?.length || 0})
          </h4>
        </div>
        <div className="flex flex-col gap-2.5">
          {(!card.evidences || card.evidences.length === 0) ? (
            <p className="text-xs text-slate-500 italic p-3 bg-[#0d1117] rounded-xl border border-[#30363d]">
              Belum ada bukti yang terhubung (PR / commit).
            </p>
          ) : (
            card.evidences.map((ev) => (
              <EvidenceLink key={ev.id} evidence={ev} isMini={false} />
            ))
          )}
        </div>
      </div>

      {/* Activity Timeline */}
      <div>
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
          <History className="w-3.5 h-3.5" />
          <span>Riwayat Aktivitas & Jejak Audit</span>
        </h4>
        <div className="flex flex-col gap-2 bg-[#0d1117] p-3 rounded-xl border border-[#30363d] max-h-48 overflow-y-auto">
          {(!card.activities || card.activities.length === 0) ? (
            <p className="text-xs text-slate-500 italic">Belum ada riwayat aktivitas tercatat.</p>
          ) : (
            card.activities.map((act) => (
              <div key={act.id} className="text-xs flex items-start justify-between gap-3 border-b border-[#21262d] pb-2 last:border-none last:pb-0">
                <div>
                  <span className="font-semibold text-blue-400 font-mono">[{act.action}]</span>{' '}
                  <span className="text-slate-300">{act.details}</span>
                </div>
                <span className="text-[10px] text-slate-500 shrink-0 font-mono">
                  {new Date(act.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
