export const SECTORS = [
    'Banking',
    'IT',
    'Pharma',
    'Auto',
    'FMCG',
    'Metals',
    'Energy',
    'Realty'
  ];
  
  export const MARKET_CAP_CATEGORIES = [
    'Large Cap',
    'Mid Cap',
    'Small Cap'
  ];
  
  export const QUERY_SUGGESTIONS = [
    "Show me banking stocks with RSI below 30",
    "Find midcap stocks near 52-week high with high volume",
    "Large cap stocks with volume spike above 2x average",
    "IT sector stocks with positive momentum",
    "Stocks within 5% of 52-week low in pharma sector",
    "High volume breakout stocks in auto sector",
    "Banking stocks with RSI above 60",
    "Midcap stocks with volume above average",
    "Energy stocks with negative momentum",
    "FMCG stocks with RSI between 40 and 60"
  ];
  
  export const CHART_PERIODS = [
    { label: '1 Day', value: '1d' },
    { label: '5 Days', value: '5d' },
    { label: '1 Month', value: '1mo' },
    { label: '3 Months', value: '3mo' },
    { label: '6 Months', value: '6mo' },
    { label: '1 Year', value: '1y' },
    { label: '2 Years', value: '2y' },
    { label: '5 Years', value: '5y' },
  ];
  
  export const RSI_LEVELS = {
    OVERSOLD: 30,
    OVERBOUGHT: 70,
  };
  
  export const VOLUME_THRESHOLD = {
    LOW: 0.5,
    NORMAL: 1,
    HIGH: 1.5,
    SPIKE: 2,
  };
  
  export const TABLE_COLUMNS = [
    { key: 'symbol', label: 'Symbol', sortable: true },
    { key: 'sector', label: 'Sector', sortable: true },
    { key: 'price', label: 'Price', sortable: true },
    { key: 'change_percent', label: 'Change %', sortable: true },
    { key: 'volume', label: 'Volume', sortable: true },
    { key: 'rsi', label: 'RSI', sortable: true },
    { key: 'market_cap_category', label: 'Market Cap', sortable: true },
  ];
  
  export const WEBSOCKET_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
  
  export const NOTIFICATION_TYPES = {
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info',
  };
  
  export const ROUTES = {
    HOME: '/',
    SCREENER: '/screener',
    STOCK_DETAIL: '/stock/:symbol',
    SAVED_SCREENERS: '/saved',
    LOGIN: '/login',
    REGISTER: '/register',
    PROFILE: '/profile',
  };