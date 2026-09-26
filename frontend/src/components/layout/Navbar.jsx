import React, { useState } from 'react';
import { GitPullRequest, GitMerge, AlertTriangle, Sparkles, Database, RotateCcw, MessageSquare, ChevronDown, GitBranch } from 'lucide-react';
import { demoApi } from '../../services/api';

export default function Navbar({
  onRefresh,
  onToggleChat,
  isChatOpen = false,
  selectedRepo = 'all',
  onSelectRepo = null,
  availableRepos = []
}) {
  const [demoLoading, setDemoLoading] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleDemoAction = async (actionFn, desc) => {
    setDemoLoading(true);
    try {
      await actionFn();
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error(`Demo action error: ${desc}`, err);
    } finally {
      setDemoLoading(false);
      setDropdownOpen(false);
    }
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-[#30363d] bg-[#161b22]/90 backdrop-blur-md px-4 lg:px-8 py-3 flex items-center justify-between gap-4">
      {/* Brand & Project Info */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-[#0f62fe] flex items-center justify-center text-white font-bold text-sm shadow-md shadow-blue-500/20">
          IBM
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-sm font-bold text-white tracking-tight">Bob Task Management</h1>
            <span className="px-1.5 py-0.2 rounded text-[10px] font-mono bg-blue-900/40 text-blue-300 border border-blue-700/50">
              watsonx.ai
            </span>
          </div>
          <div className="flex items-center gap-1.5 mt-0.5">
            <GitBranch className="w-3 h-3 text-slate-400 shrink-0" />
            <select
              value={selectedRepo}
              onChange={(e) => onSelectRepo && onSelectRepo(e.target.value)}
              className="bg-[#0d1117] border border-[#30363d] rounded text-[11px] font-mono text-slate-300 px-1.5 py-0.5 focus:outline-none focus:border-blue-500 cursor-pointer"
              title="Filter board by target repository"
            >
              <option value="all">All Repositories (Unified)</option>
              {availableRepos.map((r) => (
                <option key={r} value={r}>{r}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Demo Actions Toolbar (Judges Pitch Bar) */}
      <div className="flex items-center gap-2">
        <div className="hidden lg:flex items-center gap-1.5 bg-[#0d1117] p-1 rounded-xl border border-[#30363d]">
          <span className="text-[10px] uppercase font-bold text-slate-500 px-2 font-mono">Demo:</span>

          <button
            onClick={() => handleDemoAction(() => demoApi.simulatePROpened(), 'Simulate PR Open')}
            disabled={demoLoading}
            className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium rounded-lg text-emerald-300 hover:bg-emerald-950/60 border border-transparent hover:border-emerald-800/50 transition-all"
            title="Scenario 2: Developer opens a new PR → Auto-create In Progress card"
          >
            <GitPullRequest className="w-3.5 h-3.5 text-emerald-400" />
            <span>PR Open</span>
          </button>

          <button
            onClick={() => handleDemoAction(() => demoApi.simulatePRMerged(42), 'Simulate PR Merged')}
            disabled={demoLoading}
            className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium rounded-lg text-purple-300 hover:bg-purple-950/60 border border-transparent hover:border-purple-800/50 transition-all"
            title="Scenario 2: Developer merges PR → Card automatically moves to Done"
          >
            <GitMerge className="w-3.5 h-3.5 text-purple-400" />
            <span>PR Merge</span>
          </button>

          <button
            onClick={() => handleDemoAction(() => demoApi.simulateStaleAlarm(), 'Trigger Stale Alert')}
            disabled={demoLoading}
            className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium rounded-lg text-red-300 hover:bg-red-950/60 border border-transparent hover:border-red-800/50 transition-all"
            title="Bonus #6: Stale PR alert (>2 days without activity)"
          >
            <AlertTriangle className="w-3.5 h-3.5 text-red-400" />
            <span>Stale PR Alert</span>
          </button>

          <button
            onClick={() => handleDemoAction(() => demoApi.seedSampleData(), 'Seed Demo Data')}
            disabled={demoLoading}
            className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium rounded-lg text-slate-300 hover:bg-[#21262d] transition-all"
            title="Populate complete sample sprint data"
          >
            <Database className="w-3.5 h-3.5 text-blue-400" />
            <span>Seed</span>
          </button>

          <button
            onClick={() => handleDemoAction(() => demoApi.resetBoard(), 'Reset Board')}
            disabled={demoLoading}
            className="p-1 text-xs rounded-lg text-slate-400 hover:text-rose-400 hover:bg-[#21262d] transition-all"
            title="Reset board to empty"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Mobile dropdown for demo actions */}
        <div className="relative lg:hidden">
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium rounded-lg bg-[#21262d] text-slate-200 border border-[#30363d]"
          >
            <span>Demo Menu</span>
            <ChevronDown className="w-3.5 h-3.5" />
          </button>
          {dropdownOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-[#161b22] border border-[#30363d] rounded-xl shadow-xl py-1 z-50 flex flex-col">
              <button
                onClick={() => handleDemoAction(() => demoApi.simulatePROpened(), 'Simulate PR Open')}
                className="px-3 py-2 text-xs text-left text-emerald-300 hover:bg-[#21262d]"
              >
                Simulate PR Open
              </button>
              <button
                onClick={() => handleDemoAction(() => demoApi.simulatePRMerged(42), 'Simulate PR Merged')}
                className="px-3 py-2 text-xs text-left text-purple-300 hover:bg-[#21262d]"
              >
                Simulate PR Merge
              </button>
              <button
                onClick={() => handleDemoAction(() => demoApi.simulateStaleAlarm(), 'Trigger Stale Alarm')}
                className="px-3 py-2 text-xs text-left text-red-300 hover:bg-[#21262d]"
              >
                Trigger Stale Alarm
              </button>
              <button
                onClick={() => handleDemoAction(() => demoApi.seedSampleData(), 'Seed Data')}
                className="px-3 py-2 text-xs text-left text-blue-300 hover:bg-[#21262d]"
              >
                Seed Sample Data
              </button>
              <button
                onClick={() => handleDemoAction(() => demoApi.resetBoard(), 'Reset')}
                className="px-3 py-2 text-xs text-left text-rose-300 hover:bg-[#21262d]"
              >
                Reset Board
              </button>
            </div>
          )}
        </div>

        {/* AI Chat Drawer Button */}
        <button
          onClick={onToggleChat}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all shadow-sm ${
            isChatOpen
              ? 'bg-[#0f62fe] text-white'
              : 'bg-[#21262d] text-slate-200 hover:bg-[#30363d] border border-[#30363d]'
          }`}
        >
          <Sparkles className="w-3.5 h-3.5 text-blue-400" />
          <span>AI Chat</span>
        </button>
      </div>
    </header>
  );
}
