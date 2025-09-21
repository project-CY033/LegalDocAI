import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  full_name: string;
  password: string;
  company?: string;
  role?: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
  company?: string;
  role?: string;
  preferred_language: string;
  created_at: string;
  last_login?: string;
  documents_processed: number;
  api_calls_count: number;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface Document {
  id: string;
  filename: string;
  original_filename: string;
  file_size: number;
  file_type: string;
  document_type?: string;
  status: string;
  page_count?: number;
  word_count?: number;
  created_at: string;
  updated_at: string;
}

export interface DocumentList {
  documents: Document[];
  total: number;
  skip: number;
  limit: number;
}

export interface Analysis {
  id: string;
  analysis_type: string;
  status: string;
  summary?: string;
  simplified_explanation?: string;
  key_points?: string[];
  risk_assessment?: any;
  legal_implications?: any;
  clauses_analyzed?: any[];
  problematic_clauses?: any[];
  confidence_score?: number;
  processing_time_seconds?: number;
  created_at: string;
  completed_at?: string;
}

export interface AnalysisRequest {
  analysis_type: string;
  language?: string;
  focus_areas?: string[];
}

export interface QuestionRequest {
  question: string;
  language?: string;
}

export interface QuestionResponse {
  question: string;
  answer: string;
  confidence_score?: number;
  analysis_id: string;
}

// Auth API
export const authAPI = {
  login: (credentials: LoginCredentials): Promise<LoginResponse> =>
    api.post('/auth/login', credentials).then(res => res.data),
  
  register: (userData: RegisterData): Promise<User> =>
    api.post('/auth/register', userData).then(res => res.data),
  
  getCurrentUser: (): Promise<User> =>
    api.get('/users/me').then(res => res.data),
  
  logout: (): Promise<void> =>
    api.post('/auth/logout').then(res => res.data),
};

// Documents API
export const documentsAPI = {
  upload: (file: File): Promise<Document> => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(res => res.data);
  },
  
  list: (params?: { skip?: number; limit?: number; status_filter?: string }): Promise<DocumentList> =>
    api.get('/documents/', { params }).then(res => res.data),
  
  get: (id: string): Promise<Document> =>
    api.get(`/documents/${id}`).then(res => res.data),
  
  delete: (id: string): Promise<void> =>
    api.delete(`/documents/${id}`).then(res => res.data),
  
  download: (id: string): Promise<Blob> =>
    api.get(`/documents/${id}/download`, { responseType: 'blob' }).then(res => res.data),
};

// Analysis API
export const analysisAPI = {
  analyze: (documentId: string, request: AnalysisRequest): Promise<Analysis> =>
    api.post(`/analysis/analyze/${documentId}`, request).then(res => res.data),
  
  askQuestion: (documentId: string, request: QuestionRequest): Promise<QuestionResponse> =>
    api.post(`/analysis/question/${documentId}`, request).then(res => res.data),
  
  list: (params?: { 
    document_id?: string; 
    analysis_type?: string; 
    skip?: number; 
    limit?: number; 
  }): Promise<{ analyses: Analysis[]; total: number; skip: number; limit: number }> =>
    api.get('/analysis/', { params }).then(res => res.data),
  
  get: (id: string): Promise<Analysis> =>
    api.get(`/analysis/${id}`).then(res => res.data),
  
  submitFeedback: (id: string, rating: number, feedback?: string): Promise<void> =>
    api.post(`/analysis/${id}/feedback`, { rating, feedback }).then(res => res.data),
};

export default api;