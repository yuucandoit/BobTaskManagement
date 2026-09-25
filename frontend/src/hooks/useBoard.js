import { useState, useEffect, useCallback } from 'react';
import { boardApi } from '../services/api';

export function useBoard(pollIntervalMs = 3000) {
  const [board, setBoard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastRefreshed, setLastRefreshed] = useState(new Date());

  const fetchBoard = useCallback(async (isSilent = false) => {
    if (!isSilent) setLoading(true);
    try {
      const data = await boardApi.getBoard();
      setBoard(data);
      setError(null);
      setLastRefreshed(new Date());
    } catch (err) {
      console.error('Failed to fetch board data:', err);
      setError('Unable to connect to Kanban backend.');
    } finally {
      if (!isSilent) setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchBoard(false);

    // Auto-polling for real-time demo synchronization
    if (pollIntervalMs > 0) {
      const interval = setInterval(() => {
        fetchBoard(true);
      }, pollIntervalMs);
      return () => clearInterval(interval);
    }
  }, [fetchBoard, pollIntervalMs]);

  return {
    board,
    loading,
    error,
    lastRefreshed,
    refreshBoard: () => fetchBoard(false),
  };
}
