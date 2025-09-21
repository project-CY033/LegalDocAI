// Netlify API Configuration for React
// This file handles API endpoints for both local development and Netlify deployment

declare const process: {
  env: {
    [key: string]: string | undefined;
  };
};

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const FUNCTIONS_PATH = process.env.REACT_APP_FUNCTIONS_PATH || '/.netlify/functions';

export const apiConfig = {
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
};

// Netlify-specific configuration
export const netlifyConfig = {
  functionsPath: FUNCTIONS_PATH,
  endpoints: {
    health: '/health',
    upload: '/upload',
    analyze: '/analyze',
    question: '/question',
    auth: '/auth'
  }
};

// API endpoint builder for Netlify functions
export const buildEndpoint = (endpoint: string, params?: string) => {
  const base = process.env.REACT_APP_PLATFORM === 'netlify' 
    ? FUNCTIONS_PATH 
    : API_BASE_URL;
  
  return params ? `${base}${endpoint}/${params}` : `${base}${endpoint}`;
};

export default apiConfig;