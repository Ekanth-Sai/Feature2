import { useState, useCallback } from 'react';
import { api } from '../utils/api';

export const useScreener = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState([]);
  const [filters, setFilters] = useState({});
  const [executionTime, setExecutionTime] = useState(0);

  const screen = useCallback(async (query) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.screener.screen(query);
      setResults(response.results);
      setFilters(response.filters);
      setExecutionTime(response.execution_time);
      return response;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to screen stocks';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const clearResults = useCallback(() => {
    setResults([]);
    setFilters({});
    setError(null);
  }, []);

  return {
    screen,
    loading,
    error,
    results,
    filters,
    executionTime,
    clearResults
  };
};

export const useSavedScreeners = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [screeners, setScreeners] = useState([]);

  const fetchScreeners = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await api.screener.getSaved();
      setScreeners(data);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to fetch screeners';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const saveScreener = useCallback(async (screener) => {
    setLoading(true);
    setError(null);
    
    try {
      const saved = await api.screener.save(screener);
      setScreeners(prev => [saved, ...prev]);
      return saved;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to save screener';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteScreener = useCallback(async (id) => {
    setLoading(true);
    setError(null);
    
    try {
      await api.screener.delete(id);
      setScreeners(prev => prev.filter(s => s.id !== id));
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to delete screener';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    screeners,
    loading,
    error,
    fetchScreeners,
    saveScreener,
    deleteScreener
  };
};
