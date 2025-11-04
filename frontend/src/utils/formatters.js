export const formatCurrency = (value, decimals = 2) => {
    if (value === null || value === undefined) return 'N/A';
    return `₹${Number(value).toLocaleString('en-IN', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    })}`;
  };
  
  export const formatPercent = (value, decimals = 2, includeSign = true) => {
    if (value === null || value === undefined) return 'N/A';
    const sign = includeSign && value > 0 ? '+' : '';
    return `${sign}${Number(value).toFixed(decimals)}%`;
  };
  
  export const formatLargeNumber = (value) => {
    if (value === null || value === undefined) return 'N/A';
    
    const num = Number(value);
    
    if (num >= 10000000) {
      return `${(num / 10000000).toFixed(2)} Cr`;
    } else if (num >= 100000) {
      return `${(num / 100000).toFixed(2)} L`;
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(2)} K`;
    }
    
    return num.toLocaleString('en-IN');
  };
  
  export const formatMarketCap = (value) => {
    if (value === null || value === undefined) return 'N/A';
    
    const num = Number(value);
    
    if (num >= 10000000000) {
      return `₹${(num / 10000000000).toFixed(2)} Lakh Cr`;
    } else if (num >= 10000000) {
      return `₹${(num / 10000000).toFixed(2)} Cr`;
    }
    
    return formatCurrency(num, 0);
  };
  
  export const formatDate = (date, format = 'short') => {
    if (!date) return 'N/A';
    
    const d = new Date(date);
    
    if (format === 'short') {
      return d.toLocaleDateString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      });
    } else if (format === 'long') {
      return d.toLocaleDateString('en-IN', {
        day: '2-digit',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } else if (format === 'time') {
      return d.toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit'
      });
    }
    
    return d.toISOString();
  };
  
  export const formatTimeAgo = (date) => {
    if (!date) return 'N/A';
    
    const now = new Date();
    const past = new Date(date);
    const diffMs = now - past;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    
    return formatDate(date);
  };
  
  export const getChangeColor = (value) => {
    if (value > 0) return 'text-green-400';
    if (value < 0) return 'text-red-400';
    return 'text-slate-300';
  };
  
  export const getRSIColor = (rsi) => {
    if (rsi < 30) return 'text-green-400';
    if (rsi > 70) return 'text-red-400';
    return 'text-slate-300';
  };
  
  export const getVolumeColor = (ratio) => {
    if (ratio > 2) return 'text-yellow-400';
    if (ratio > 1.5) return 'text-green-400';
    return 'text-slate-300';
  };
  
  export const truncate = (text, length = 50) => {
    if (!text) return '';
    if (text.length <= length) return text;
    return `${text.substring(0, length)}...`;
  };
  
  export const formatFilters = (filters) => {
    const formatted = [];
    
    if (filters.sector) {
      formatted.push(`Sector: ${filters.sector}`);
    }
    if (filters.market_cap) {
      formatted.push(`Market Cap: ${filters.market_cap}`);
    }
    if (filters.rsi_min !== undefined || filters.rsi_max !== undefined) {
      const min = filters.rsi_min || 0;
      const max = filters.rsi_max || 100;
      formatted.push(`RSI: ${min}-${max}`);
    }
    if (filters.volume_ratio_min) {
      formatted.push(`Volume: ${filters.volume_ratio_min}x+`);
    }
    if (filters.momentum) {
      formatted.push(`Momentum: ${filters.momentum}`);
    }
    
    return formatted.join(' | ');
  };
  
  export const isValidEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };
  
  export const sanitizeInput = (input) => {
    if (!input) return '';
    return input.trim().replace(/[<>]/g, '');
  };
  