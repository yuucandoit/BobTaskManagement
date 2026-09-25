import React, { useState } from 'react';
import KanbanBoard from '../components/board/KanbanBoard';
import CardDetailPage from './CardDetailPage';
import Modal from '../components/common/Modal';
import ChatBox from '../components/chat/ChatBox';
import Loader from '../components/common/Loader';
import Button from '../components/common/Button';
import { Plus, Sparkles, RefreshCw } from 'lucide-react';
import { cardsApi } from '../services/api';

export default function BoardPage({ board, loading, error, refreshBoard, chatProps, isChatOpen, setIsChatOpen }) {
  const [selectedCard, setSelectedCard] = useState(null);
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const [isManualModalOpen, setIsManualModalOpen] = useState(false);

  // Manual Card Form State
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [newAssignee, setNewAssignee] = useState('');
  const [newStatus, setNewStatus] = useState('To Do');
  const [newPriority, setNewPriority] = useState('Medium');
  const [newType, setNewType] = useState('feature');
  const [creatingManual, setCreatingManual] = useState(false);

  const handleCardClick = (card) => {
    setSelectedCard(card);
    setIsDetailOpen(true);
  };

  const handleManualCreate = async (e) => {
    e.preventDefault();
    if (!newTitle.trim() || creatingManual) return;

    setCreatingManual(true);
    try {
      await cardsApi.create({
        title: newTitle.trim(),
        description: newDesc.trim() || 'Manual card created by PM',
        status: newStatus,
        priority: newPriority,
        task_type: newType,
        assignee_name: newAssignee.trim() || null,
        estimation_hours: 2.0,
        story_points: 2,
        origin: 'manual',
      });
      setIsManualModalOpen(false);
      setNewTitle('');
      setNewDesc('');
      setNewAssignee('');
      refreshBoard();
    } catch (err) {
      console.error('Failed to create manual card:', err);
    } finally {
      setCreatingManual(false);
    }
  };

  if (loading && !board) {
    return <Loader size="lg" text="Menghubungkan ke IBM watsonx.ai & Kanban board..." />;
  }

  if (error && !board) {
    return (
      <div className="p-8 text-center flex flex-col items-center justify-center gap-4">
        <p className="text-rose-400 font-semibold">{error}</p>
        <Button onClick={refreshBoard} icon={RefreshCw}>
          Coba Lagi
        </Button>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6 relative">
      {/* Board Top Action Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <span>Sprint Board Real-Time</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Auto-sync dengan GitHub Pull Requests & Commit Evidence.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={refreshBoard}
            icon={RefreshCw}
            title="Refresh manual data board"
          >
            Sync
          </Button>

          <Button
            variant="primary"
            size="sm"
            onClick={() => setIsManualModalOpen(true)}
            icon={Plus}
          >
            Tambah Kartu
          </Button>
        </div>
      </div>

      {/* Main Kanban Columns */}
      <KanbanBoard
        board={board}
        onCardClick={handleCardClick}
        onAddCard={() => setIsManualModalOpen(true)}
        onRefresh={refreshBoard}
      />

      {/* Slide-out / Floating Chat Drawer (Fitur Wajib #4) */}
      {isChatOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-96 max-w-[calc(100vw-3rem)] shadow-2xl animate-in slide-in-from-bottom-5 duration-200">
          <ChatBox
            messages={chatProps.messages}
            sending={chatProps.sending}
            onSendMessage={chatProps.sendMessage}
            onClear={chatProps.clearChat}
          />
        </div>
      )}

      {/* Modal: Card Detail & Evidence Trail (Fitur Wajib #3) */}
      <Modal
        isOpen={isDetailOpen}
        onClose={() => setIsDetailOpen(false)}
        title={selectedCard ? `Detail Tugas: ${selectedCard.title}` : 'Detail Kartu'}
        maxWidth="max-w-2xl"
      >
        <CardDetailPage
          card={selectedCard}
          onClose={() => setIsDetailOpen(false)}
          onCardUpdated={(updated) => {
            setSelectedCard(updated);
            refreshBoard();
          }}
        />
      </Modal>

      {/* Modal: Manual Card Creation Form */}
      <Modal
        isOpen={isManualModalOpen}
        onClose={() => setIsManualModalOpen(false)}
        title="Buat Kartu Baru (Manual)"
        maxWidth="max-w-lg"
      >
        <form onSubmit={handleManualCreate} className="flex flex-col gap-4 text-xs">
          <div className="flex flex-col gap-1.5">
            <label className="font-medium text-slate-300">Judul Tugas *</label>
            <input
              type="text"
              required
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="Contoh: Refactor auth middleware"
              className="bg-[#0d1117] border border-[#30363d] rounded-xl px-3.5 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="font-medium text-slate-300">Deskripsi</label>
            <textarea
              rows={3}
              value={newDesc}
              onChange={(e) => setNewDesc(e.target.value)}
              placeholder="Rincian scope pekerjaan..."
              className="bg-[#0d1117] border border-[#30363d] rounded-xl px-3.5 py-2 text-slate-100 focus:outline-none focus:border-blue-500 resize-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="flex flex-col gap-1.5">
              <label className="font-medium text-slate-300">Assignee</label>
              <input
                type="text"
                value={newAssignee}
                onChange={(e) => setNewAssignee(e.target.value)}
                placeholder="Nama developer"
                className="bg-[#0d1117] border border-[#30363d] rounded-xl px-3 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="font-medium text-slate-300">Kolom</label>
              <select
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
                className="bg-[#0d1117] border border-[#30363d] rounded-xl px-3 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
              >
                <option value="To Do">To Do</option>
                <option value="In Progress">In Progress</option>
                <option value="Done">Done</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="flex flex-col gap-1.5">
              <label className="font-medium text-slate-300">Prioritas</label>
              <select
                value={newPriority}
                onChange={(e) => setNewPriority(e.target.value)}
                className="bg-[#0d1117] border border-[#30363d] rounded-xl px-3 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="font-medium text-slate-300">Tipe Task</label>
              <select
                value={newType}
                onChange={(e) => setNewType(e.target.value)}
                className="bg-[#0d1117] border border-[#30363d] rounded-xl px-3 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
              >
                <option value="feature">feature</option>
                <option value="bugfix">bugfix</option>
                <option value="refactor">refactor</option>
                <option value="chore">chore</option>
                <option value="docs">docs</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end gap-2 pt-2 border-t border-[#30363d]">
            <Button variant="ghost" onClick={() => setIsManualModalOpen(false)}>
              Batal
            </Button>
            <Button type="submit" disabled={creatingManual}>
              {creatingManual ? 'Menyimpan...' : 'Simpan Kartu'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
