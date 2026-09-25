import React from 'react';
import { GitPullRequest, GitCommit, ExternalLink, CheckCircle2 } from 'lucide-react';

export default function EvidenceLink({ evidence, isMini = false }) {
  if (!evidence) return null;

  const isPR = evidence.evidence_type === 'pr';
  const isMerged = evidence.title?.toLowerCase().includes('merged');

  if (isMini) {
    return (
      <a
        href={evidence.url || '#'}
        target="_blank"
        rel="noopener noreferrer"
        onClick={(e) => !evidence.url && e.preventDefault()}
        className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-mono font-medium transition-all ${
          isMerged
            ? 'bg-purple-950/40 text-purple-300 border border-purple-800/50 hover:bg-purple-900/60'
            : isPR
            ? 'bg-emerald-950/40 text-emerald-300 border border-emerald-800/50 hover:bg-emerald-900/60'
            : 'bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700'
        }`}
        title={`${evidence.title} - ${evidence.description || ''}`}
      >
        {isMerged ? (
          <CheckCircle2 className="w-3 h-3 text-purple-400 shrink-0" />
        ) : isPR ? (
          <GitPullRequest className="w-3 h-3 text-emerald-400 shrink-0" />
        ) : (
          <GitCommit className="w-3 h-3 text-blue-400 shrink-0" />
        )}
        <span className="truncate max-w-[120px]">
          {evidence.reference_id ? `#${evidence.reference_id}` : evidence.title}
        </span>
        <ExternalLink className="w-2.5 h-2.5 opacity-60 shrink-0" />
      </a>
    );
  }

  return (
    <div className="flex items-start justify-between gap-3 p-3 bg-[#0d1117] rounded-lg border border-[#30363d] hover:border-slate-600 transition-colors">
      <div className="flex items-start gap-2.5 min-w-0">
        <div
          className={`p-1.5 rounded-md mt-0.5 shrink-0 ${
            isMerged
              ? 'bg-purple-900/40 text-purple-300'
              : isPR
              ? 'bg-emerald-900/40 text-emerald-300'
              : 'bg-blue-900/40 text-blue-300'
          }`}
        >
          {isMerged ? (
            <CheckCircle2 className="w-4 h-4" />
          ) : isPR ? (
            <GitPullRequest className="w-4 h-4" />
          ) : (
            <GitCommit className="w-4 h-4" />
          )}
        </div>
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              {evidence.evidence_type} bukti
            </span>
            {evidence.reference_id && (
              <span className="px-1.5 py-0.5 bg-[#21262d] rounded text-[11px] font-mono text-slate-300">
                #{evidence.reference_id}
              </span>
            )}
          </div>
          <p className="text-sm font-medium text-slate-100 truncate mt-0.5">{evidence.title}</p>
          {evidence.description && (
            <p className="text-xs text-slate-400 mt-1 line-clamp-2">{evidence.description}</p>
          )}
          {evidence.author_username && (
            <div className="flex items-center gap-1.5 mt-2 text-xs text-slate-400">
              {evidence.author_avatar ? (
                <img
                  src={evidence.author_avatar}
                  alt={evidence.author_username}
                  className="w-4 h-4 rounded-full"
                />
              ) : null}
              <span>@{evidence.author_username}</span>
            </div>
          )}
        </div>
      </div>

      {evidence.url && (
        <a
          href={evidence.url}
          target="_blank"
          rel="noopener noreferrer"
          className="shrink-0 p-1.5 rounded text-slate-400 hover:text-white hover:bg-[#21262d] transition-colors"
          title="Buka bukti di GitHub"
        >
          <ExternalLink className="w-4 h-4" />
        </a>
      )}
    </div>
  );
}
