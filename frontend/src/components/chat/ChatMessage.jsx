import React from 'react';
import { Bot, User, CheckCircle2 } from 'lucide-react';

export default function ChatMessage({ message }) {
  const isAI = message.sender === 'ai';

  return (
    <div className={`flex gap-3 ${isAI ? 'items-start' : 'items-start flex-row-reverse'}`}>
      <div
        className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
          isAI ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-200'
        }`}
      >
        {isAI ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
      </div>

      <div
        className={`max-w-[85%] rounded-2xl p-3 text-xs leading-relaxed ${
          isAI
            ? 'bg-[#21262d] text-slate-200 border border-[#30363d] rounded-tl-xs'
            : 'bg-[#0f62fe] text-white rounded-tr-xs'
        }`}
      >
        <p className="whitespace-pre-line">{message.text}</p>

        {message.cardCreated && (
          <div className="mt-2.5 p-2 rounded-lg bg-[#161b22] border border-[#30363d] flex items-center justify-between gap-2">
            <div className="min-w-0">
              <span className="text-[10px] text-emerald-400 font-semibold uppercase tracking-wider block">
                Kartu Ditambahkan ke {message.cardCreated.status}
              </span>
              <p className="font-semibold text-slate-200 truncate mt-0.5">
                {message.cardCreated.title}
              </p>
            </div>
            <span className="shrink-0 text-[10px] font-mono px-1.5 py-0.5 rounded bg-blue-900/50 text-blue-300 border border-blue-700/40">
              {message.cardCreated.estimation_hours}h
            </span>
          </div>
        )}

        <span className="text-[10px] opacity-50 block mt-1">
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  );
}
