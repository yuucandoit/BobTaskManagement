import React from 'react';
import TaskCard from './TaskCard';
import { Circle, PlayCircle, CheckCircle2, Plus } from 'lucide-react';

export default function KanbanColumn({ columnId, title, count, cards = [], onCardClick, onAddCard }) {
  const columnConfig = {
    to_do: {
      color: 'border-slate-600',
      badge: 'bg-slate-800 text-slate-300',
      icon: Circle,
      iconColor: 'text-slate-400',
      dotColor: 'bg-slate-400',
    },
    in_progress: {
      color: 'border-blue-500/40',
      badge: 'bg-blue-950/60 text-blue-400 border border-blue-800/40',
      icon: PlayCircle,
      iconColor: 'text-blue-400',
      dotColor: 'bg-blue-500',
    },
    done: {
      color: 'border-emerald-500/40',
      badge: 'bg-emerald-950/60 text-emerald-400 border border-emerald-800/40',
      icon: CheckCircle2,
      iconColor: 'text-emerald-400',
      dotColor: 'bg-emerald-500',
    },
  };

  const config = columnConfig[columnId] || columnConfig.to_do;
  const Icon = config.icon;

  return (
    <div className="flex flex-col bg-[#0d1117]/80 rounded-2xl border border-[#30363d] overflow-hidden min-h-[600px] flex-1">
      {/* Column Header */}
      <div className="flex items-center justify-between px-4 py-3.5 border-b border-[#30363d] bg-[#161b22]/70 backdrop-blur-xs">
        <div className="flex items-center gap-2.5">
          <span className={`w-2.5 h-2.5 rounded-full ${config.dotColor}`} />
          <h3 className="font-semibold text-sm text-slate-100 tracking-wide">{title}</h3>
          <span className={`px-2 py-0.5 rounded-full text-xs font-mono font-medium ${config.badge}`}>
            {count}
          </span>
        </div>

        {columnId === 'to_do' && onAddCard && (
          <button
            onClick={onAddCard}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-[#21262d] transition-colors"
            title="Tambah kartu baru manual / chat"
          >
            <Plus className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Cards List */}
      <div className="p-3 flex-1 flex flex-col gap-3 overflow-y-auto">
        {cards.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center py-16 text-center text-slate-500">
            <Icon className={`w-8 h-8 mb-2 opacity-30 ${config.iconColor}`} />
            <p className="text-xs font-medium">Belum ada kartu di {title}</p>
          </div>
        ) : (
          cards.map((card) => (
            <TaskCard key={card.id} card={card} onClick={onCardClick} />
          ))
        )}
      </div>
    </div>
  );
}
