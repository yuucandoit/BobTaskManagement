import React, { useState } from 'react';
import Navbar from './components/layout/Navbar';
import Sidebar from './components/layout/Sidebar';
import BoardPage from './pages/BoardPage';
import OnboardingPage from './pages/OnboardingPage';
import ChatPage from './pages/ChatPage';
import { useBoard } from './hooks/useBoard';
import { useChat } from './hooks/useChat';

export default function App() {
  const [activeTab, setActiveTab] = useState('board');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [selectedRepo, setSelectedRepo] = useState('all');

  // Core board hook with multi-repo filter and 3s polling
  const { board, loading, error, refreshBoard } = useBoard(selectedRepo, 3000);

  // Chat hook: when card created via chat, trigger board refresh
  const chatProps = useChat((newCard) => {
    refreshBoard();
  });

  const availableRepos = board?.stats?.available_repos || [];

  return (
    <div className="min-h-screen flex flex-col bg-[#0d1117] text-slate-100 font-sans">
      {/* Top Navbar with multi-repo switcher */}
      <Navbar
        onRefresh={refreshBoard}
        onToggleChat={() => setIsChatOpen(!isChatOpen)}
        isChatOpen={isChatOpen}
        selectedRepo={selectedRepo}
        onSelectRepo={setSelectedRepo}
        availableRepos={availableRepos}
      />

      {/* Main Body with Sidebar & Content */}
      <div className="flex-1 flex overflow-hidden">
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

        <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">
          {activeTab === 'board' && (
            <BoardPage
              board={board}
              loading={loading}
              error={error}
              refreshBoard={refreshBoard}
              chatProps={chatProps}
              isChatOpen={isChatOpen}
              setIsChatOpen={setIsChatOpen}
            />
          )}

          {activeTab === 'onboarding' && (
            <OnboardingPage onReady={() => setActiveTab('board')} />
          )}

          {activeTab === 'chat' && (
            <ChatPage
              chatProps={chatProps}
              onGoToBoard={() => setActiveTab('board')}
            />
          )}
        </main>
      </div>
    </div>
  );
}
