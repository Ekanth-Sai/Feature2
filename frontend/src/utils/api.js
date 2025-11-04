import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}${API_VERSION}`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const api = {
  screener: {
    screen: async (query) => {
      const response = await apiClient.post('/screener/screen', { query });
      return response.data;
    },
    
    getSaved: async () => {
      const response = await apiClient.get('/screener/saved');
      return response.data;
    },
    
    save: async (screener) => {
      const response = await apiClient.post('/screener/saved', screener);
      return response.data;
    },
    
    update: async (id, screener) => {
      const response = await apiClient.put(`/screener/saved/${id}`, screener);
      return response.data;
    },
    
    delete: async (id) => {
      const response = await apiClient.delete(`/screener/saved/${id}`);
      return response.data;
    },
  },

  stocks: {
    getAll: async (params = {}) => {
      const response = await apiClient.get('/stocks', { params });
      return response.data;
    },
    
    getDetail: async (symbol) => {
      const response = await apiClient.get(`/stocks/${symbol}`);
      return response.data;
    },
    
    getHistorical: async (symbol, period = '1mo') => {
      const response = await apiClient.get(`/stocks/${symbol}/historical`, {
        params: { period }
      });
      return response.data;
    },
    
    getSectors: async () => {
      const response = await apiClient.get('/stocks/sectors/list');
      return response.data;
    },
    
    getBatch: async (symbols) => {
      const response = await apiClient.post('/stocks/batch', { symbols });
      return response.data;
    },
  },

  auth: {
    register: async (userData) => {
      const response = await apiClient.post('/auth/register', userData);
      return response.data;
    },
    
    login: async (credentials) => {
      const formData = new FormData();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);
      
      const response = await apiClient.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
      }
      
      return response.data;
    },
    
    logout: () => {
      localStorage.removeItem('access_token');
    },
    
    getCurrentUser: async () => {
      const response = await apiClient.get('/auth/me');
      return response.data;
    },
    
    updateUser: async (userData) => {
      const response = await apiClient.put('/auth/me', userData);
      return response.data;
    },
  },

  markets: {
    getStatus: async () => {
      const response = await apiClient.get('/markets/status');
      return response.data;
    },
  },

  analytics: {
    getPopularQueries: async () => {
      const response = await apiClient.get('/analytics/popular-queries');
      return response.data;
    },
    
    getTrendingSectors: async () => {
      const response = await apiClient.get('/analytics/trending-sectors');
      return response.data;
    },
  },
};

export default api;
