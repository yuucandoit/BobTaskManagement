import React, { useState } from 'react';
import { GitBranch, Key, CheckCircle2, Copy, ExternalLink, ShieldCheck, PlayCircle } from 'lucide-react';
import Button from '../components/common/Button';

export default function OnboardingPage({ onReady }) {
  const [repoName, setRepoName] = useState('ibm-bob/smart-tracker');
  const [webhookUrl, setWebhookUrl] = useState('http://localhost:8000/api/v1/webhook/github');
  const [copied, setCopied] = useState(false);
  const [connected, setConnected] = useState(true);

  const copyWebhook = () => {
    navigator.clipboard.writeText(webhookUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-8 py-6">
      {/* Hero Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-400 mb-1">
          <GitBranch className="w-4 h-4" />
          <span>Scenario 1 — Repository Setup</span>
        </div>
        <h2 className="text-2xl font-bold text-white tracking-tight">
          Connect GitHub Repository
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Connect your project repository so every Pull Request and branch is automatically synthesized into a Kanban task card.
        </p>
      </div>

      {/* Setup Steps Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Step 1: Webhook Configuration */}
        <div className="p-5 bg-[#161b22] border border-[#30363d] rounded-2xl flex flex-col gap-4">
          <div className="flex items-center gap-2.5">
            <div className="w-6 h-6 rounded-full bg-blue-600/20 text-blue-400 flex items-center justify-center font-mono text-xs font-bold">
              1
            </div>
            <h3 className="text-sm font-semibold text-white">Copy Webhook Payload URL</h3>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Go to <strong>Settings → Webhooks → Add Webhook</strong> in your GitHub repository, then paste this URL:
          </p>

          <div className="flex items-center gap-2 bg-[#0d1117] p-2.5 rounded-xl border border-[#30363d]">
            <input
              type="text"
              readOnly
              value={webhookUrl}
              className="bg-transparent flex-1 text-xs text-slate-300 font-mono focus:outline-none"
            />
            <button
              onClick={copyWebhook}
              className="p-1.5 rounded-lg bg-[#21262d] text-slate-300 hover:text-white hover:bg-[#30363d] transition-colors"
              title="Copy URL"
            >
              {copied ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
            </button>
          </div>

          <div className="flex flex-col gap-1.5 text-xs text-slate-400 bg-[#0d1117]/60 p-3 rounded-xl border border-[#21262d]">
            <span className="font-semibold text-slate-300">GitHub Webhook Configuration:</span>
            <span>• Content type: <code>application/json</code></span>
            <span>• Events: Select <code>Pull requests</code> and <code>Pushes</code></span>
          </div>
        </div>

        {/* Step 2: Multi-Repo & Target Connection */}
        <div className="p-5 bg-[#161b22] border border-[#30363d] rounded-2xl flex flex-col gap-4">
          <div className="flex items-center gap-2.5">
            <div className="w-6 h-6 rounded-full bg-blue-600/20 text-blue-400 flex items-center justify-center font-mono text-xs font-bold">
              2
            </div>
            <h3 className="text-sm font-semibold text-white">Multi-Repo & Org Connection</h3>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Bob Task Management supports multiple repositories concurrently:
          </p>

          <div className="flex flex-col gap-2 text-xs">
            <div className="p-2.5 bg-[#0d1117] rounded-xl border border-[#30363d]">
              <span className="font-semibold text-blue-400 block mb-0.5">Option A — Multiple Repositories:</span>
              <p className="text-[11px] text-slate-400">
                Paste the same webhook URL in Repo 1 (e.g. <code>auth-service</code>) and Repo 2 (e.g. <code>frontend-app</code>). Both will automatically appear in the board filter.
              </p>
            </div>

            <div className="p-2.5 bg-[#0d1117] rounded-xl border border-[#30363d]">
              <span className="font-semibold text-purple-400 block mb-0.5">Option B — GitHub Organization Webhook:</span>
              <p className="text-[11px] text-slate-400">
                Go to <strong>Organization Settings → Webhooks</strong>. All repositories within the organization will be linked automatically!
              </p>
            </div>
          </div>

          <div className="p-3 bg-emerald-950/30 border border-emerald-900/50 rounded-xl flex items-center gap-2 text-xs text-emerald-300 mt-auto">
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Multi-Repo Ready: Every card records <code>repo_name</code> automatically.</span>
          </div>
        </div>
      </div>

      {/* Action Footer */}
      <div className="flex items-center justify-between p-4 bg-[#161b22] border border-[#30363d] rounded-2xl">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs text-slate-300 font-medium">
            Status: Webhook Listener Ready
          </span>
        </div>

        <Button onClick={onReady} icon={PlayCircle}>
          Open Kanban Board
        </Button>
      </div>
    </div>
  );
}
