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
          <span>Skenario 1 — Setup Awal Repositori</span>
        </div>
        <h2 className="text-2xl font-bold text-white tracking-tight">
          Hubungkan GitHub Repository
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Hubungkan repo proyek Anda agar setiap Pull Request & branch baru langsung otomatis disintesis menjadi kartu tugas Kanban.
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
            <h3 className="text-sm font-semibold text-white">Salin Webhook Payload URL</h3>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Buka menu <strong>Settings → Webhooks → Add Webhook</strong> di repository GitHub Anda, lalu tempel URL berikut:
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
              title="Salin URL"
            >
              {copied ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
            </button>
          </div>

          <div className="flex flex-col gap-1.5 text-xs text-slate-400 bg-[#0d1117]/60 p-3 rounded-xl border border-[#21262d]">
            <span className="font-semibold text-slate-300">Pengaturan Webhook GitHub:</span>
            <span>• Content type: <code>application/json</code></span>
            <span>• Events: Pilih <code>Pull requests</code> dan <code>Pushes</code></span>
          </div>
        </div>

        {/* Step 2: Target Repository Connection */}
        <div className="p-5 bg-[#161b22] border border-[#30363d] rounded-2xl flex flex-col gap-4">
          <div className="flex items-center gap-2.5">
            <div className="w-6 h-6 rounded-full bg-blue-600/20 text-blue-400 flex items-center justify-center font-mono text-xs font-bold">
              2
            </div>
            <h3 className="text-sm font-semibold text-white">Repository Target</h3>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Pastikan nama repository target sesuai dengan workspace sprint yang sedang aktif:
          </p>

          <div className="flex flex-col gap-2">
            <label className="text-xs font-medium text-slate-300">Nama Repositori GitHub:</label>
            <input
              type="text"
              value={repoName}
              onChange={(e) => setRepoName(e.target.value)}
              className="bg-[#0d1117] border border-[#30363d] rounded-xl px-3.5 py-2 text-xs text-slate-100 font-mono focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="p-3 bg-emerald-950/30 border border-emerald-900/50 rounded-xl flex items-center gap-2 text-xs text-emerald-300 mt-auto">
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Listener aktif! Siap menerima event PR dan commit secara real-time.</span>
          </div>
        </div>
      </div>

      {/* Action Footer */}
      <div className="flex items-center justify-between p-4 bg-[#161b22] border border-[#30363d] rounded-2xl">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs text-slate-300 font-medium">
            Status: Listener Standby & Siap Demo
          </span>
        </div>

        <Button onClick={onReady} icon={PlayCircle}>
          Buka Kanban Board Sekarang
        </Button>
      </div>
    </div>
  );
}
