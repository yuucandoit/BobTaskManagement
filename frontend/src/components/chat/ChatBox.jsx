import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import { Send, Sparkles, Trash2 } from 'lucide-react';

export default function ChatBox({ messages, sending, onSendMessage, onClear }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const quickPrompts = [
    'buat kartu: refactor auth module, assign ke Firza, deadline Jumat',
    'buat kartu: fix memory leak in worker pool, assign ke Budi, priority urgent',
    'buat kartu: buat dokumentasi API watsonx endpoint',
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || sending) return;
    onSendMessage(input);
    setInput('');
  };

  const handleQuickPrompt = (prompt) => {
    setInput(prompt);
  };

  return (
    <div className="flex flex-col h-full bg-[#161b22] border border-[#30363d] rounded-2xl overflow-hidden shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-[#30363d] bg-[#0d1117]/80">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-md bg-blue-600 flex items-center justify-center text-white">
            <Sparkles className="w-3.5 h-3.5" />
          </div>
          <div>
            <h3 className="text-xs font-semibold text-white tracking-wide">
              AI Task Assistant <span className="text-[10px] text-blue-400 font-mono font-normal">(watsonx.ai)</span>
            </h3>
            <span className="text-[10px] text-slate-400">Natural Language Card Generator</span>
          </div>
        </div>

        {onClear && (
          <button
            onClick={onClear}
            className="p-1 rounded text-slate-400 hover:text-rose-400 hover:bg-[#21262d] transition-colors"
            title="Bersihkan chat"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Message List */}
      <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3 min-h-[300px] max-h-[460px]">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}

        {sending && (
          <div className="flex items-center gap-2 text-xs text-blue-400 font-mono animate-pulse">
            <Sparkles className="w-3.5 h-3.5 animate-spin" />
            <span>watsonx.ai sedang menganalisis prompt & membuat kartu...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts */}
      <div className="px-3 py-2 border-t border-[#30363d] bg-[#0d1117]/40 flex items-center gap-1.5 overflow-x-auto text-[11px]">
        <span className="text-slate-500 font-medium shrink-0">Contoh:</span>
        {quickPrompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => handleQuickPrompt(p)}
            className="px-2 py-0.5 rounded bg-[#21262d] text-slate-300 hover:bg-[#30363d] hover:text-blue-400 truncate max-w-[220px] transition-colors shrink-0 text-left"
          >
            {p}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="p-3 border-t border-[#30363d] bg-[#0d1117] flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ketik tugas manual, misal: buat kartu: refactor auth module..."
          disabled={sending}
          className="flex-1 bg-[#161b22] border border-[#30363d] rounded-xl px-3.5 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!input.trim() || sending}
          className="p-2 rounded-xl bg-[#0f62fe] hover:bg-[#0043ce] text-white disabled:opacity-40 disabled:cursor-not-allowed transition-colors shrink-0"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
