import React from 'react';
import { LayoutDashboard, GitBranch, Sparkles, Settings, FileText, CheckCircle2 } from 'lucide-react';

export default function Sidebar({ activeTab, onTabChange }) {
  const navItems = [
    { id: 'board', label: 'Kanban Board', icon: LayoutDashboard },
    { id: 'onboarding', label: 'Connect Repo', icon: GitBranch },
    { id: 'chat', label: 'AI Chat Assistant', icon: Sparkles },
  ];

  return (
    <aside className="w-64 border-r border-[#30363d] bg-[#161b22] p-4 flex flex-col justify-between shrink-0 hidden md:flex">
      <div className="flex flex-col gap-6">
        {/* Navigation */}
        <div className="flex flex-col gap-1">
          <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-3 mb-1">
            Workspace
          </span>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-[#0f62fe] text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-[#21262d]'
                }`}
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

        {/* Pitch Quick Flow */}
        <div className="p-3 bg-[#0d1117] rounded-xl border border-[#30363d] text-xs">
          <span className="text-[11px] font-semibold text-blue-400 uppercase tracking-wider block mb-2">
            Pitch Flow Checklist
          </span>
          <ul className="flex flex-col gap-2 text-[11px] text-slate-400">
            <li className="flex items-center gap-1.5 text-emerald-400">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Auto-create PR → Card</span>
            </li>
            <li className="flex items-center gap-1.5 text-emerald-400">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Auto-move on Merge</span>
            </li>
            <li className="flex items-center gap-1.5 text-emerald-400">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Evidence PR Link badge</span>
            </li>
            <li className="flex items-center gap-1.5 text-emerald-400">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Chat to Card Fallback</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Footer Info */}
      <div className="pt-4 border-t border-[#30363d] flex flex-col gap-2">
        <div className="flex items-center justify-between text-[11px] text-slate-400">
          <span>watsonx.ai Engine:</span>
          <span className="text-emerald-400 font-mono flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            Ready
          </span>
        </div>
        <div className="flex items-center justify-between text-[11px] text-slate-400">
          <span>GitHub Listener:</span>
          <span className="text-blue-400 font-mono">Listening</span>
        </div>
      </div>
    </aside>
  );
}
