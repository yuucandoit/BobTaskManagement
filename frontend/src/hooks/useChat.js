import { useState } from 'react';
import { chatApi } from '../services/api';

export function useChat(onCardCreated = null) {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'ai',
      text: 'Hello! Describe any task to generate a new card. For example:\n*"create card: refactor auth module, assign to Alex, deadline Friday"*',
      timestamp: new Date(),
    },
  ]);
  const [sending, setSending] = useState(false);

  const sendMessage = async (text, repo = null) => {
    if (!text.trim() || sending) return;

    const userMsg = {
      id: Date.now().toString(),
      sender: 'user',
      text: text.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setSending(true);

    try {
      const response = await chatApi.sendMessage(text, repo);
      const aiMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: response.reply,
        cardCreated: response.card_created,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMsg]);

      if (onCardCreated && response.card_created) {
        onCardCreated(response.card_created);
      }
    } catch (err) {
      console.error('Chat error:', err);
      const errorMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: '❌ Failed to process instruction. Ensure the backend is reachable.',
        isError: true,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setSending(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: 'welcome',
        sender: 'ai',
        text: 'Chat cleared. Enter a new task instruction anytime.',
        timestamp: new Date(),
      },
    ]);
  };

  return {
    messages,
    sending,
    sendMessage,
    clearChat,
  };
}
