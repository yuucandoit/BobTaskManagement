import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const boardApi = {
  getBoard: async () => {
    const res = await api.get('/board');
    return res.data;
  },
};

export const cardsApi = {
  getAll: async (status) => {
    const res = await api.get('/cards', { params: { status } });
    return res.data;
  },
  getById: async (id) => {
    const res = await api.get(`/cards/${id}`);
    return res.data;
  },
  create: async (data) => {
    const res = await api.post('/cards', data);
    return res.data;
  },
  update: async (id, data) => {
    const res = await api.put(`/cards/${id}`, data);
    return res.data;
  },
  delete: async (id) => {
    const res = await api.delete(`/cards/${id}`);
    return res.data;
  },
  attachEvidence: async (id, evidenceData) => {
    const res = await api.post(`/cards/${id}/evidence`, evidenceData);
    return res.data;
  },
};

export const chatApi = {
  sendMessage: async (message, contextRepo = null) => {
    const res = await api.post('/chat', { message, context_repo: contextRepo });
    return res.data;
  },
};

export const demoApi = {
  simulatePROpened: async (payload = null) => {
    const res = await api.post('/demo/simulate-pr-opened', payload);
    return res.data;
  },
  simulateCommitPush: async (prNumber = 42, repoName = 'ibm-bob/smart-tracker', additionalLoc = 280) => {
    const res = await api.post('/demo/simulate-commit-push', null, {
      params: { pr_number: prNumber, repo_name: repoName, additional_loc: additionalLoc },
    });
    return res.data;
  },
  simulatePRMerged: async (prNumber = 42, repoName = 'ibm-bob/smart-tracker') => {
    const res = await api.post('/demo/simulate-pr-merged', null, {
      params: { pr_number: prNumber, repo_name: repoName },
    });
    return res.data;
  },
  simulateStaleAlarm: async (cardId = null, daysBack = 3.5) => {
    const res = await api.post('/demo/simulate-stale-alarm', null, {
      params: { card_id: cardId, days_back: daysBack },
    });
    return res.data;
  },
  seedSampleData: async () => {
    const res = await api.post('/demo/seed-sample-data');
    return res.data;
  },
  resetBoard: async () => {
    const res = await api.post('/demo/reset');
    return res.data;
  },
};

export default api;
