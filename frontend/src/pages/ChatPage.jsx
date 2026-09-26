import React from 'react';
import ChatBox from '../components/chat/ChatBox';
import { Sparkles, Bot, Zap, ArrowRight } from 'lucide-react';
import Button from '../components/common/Button';

export default function ChatPage({ chatProps, onGoToBoard }) {
  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-6 py-6 h-[calc(100vh-8rem)]">
      {/* Header */}
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-400 mb-1">
            <Sparkles className="w-4 h-4" />
            <span>Scenario 3 — AI Natural Language Task Creation</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            AI Scrum Assistant
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Instantly create cards by describing tasks in natural language powered by IBM watsonx.ai.
          </p>
        </div>

        <Button variant="secondary" onClick={onGoToBoard} icon={ArrowRight}>
          View Board
        </Button>
      </div>

      {/* Main Chat Box Container */}
      <div className="flex-1 min-h-0">
        <ChatBox
          messages={chatProps.messages}
          sending={chatProps.sending}
          onSendMessage={chatProps.sendMessage}
          onClear={chatProps.clearChat}
        />
      </div>
    </div>
  );
}
