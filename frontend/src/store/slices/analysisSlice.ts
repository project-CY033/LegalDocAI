import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { analysisAPI, Analysis, AnalysisRequest, QuestionRequest, QuestionResponse } from '../../services/api';

interface AnalysisState {
  analyses: Analysis[];
  currentAnalysis: Analysis | null;
  isLoading: boolean;
  isAnalyzing: boolean;
  questionAnswer: QuestionResponse | null;
  error: string | null;
}

const initialState: AnalysisState = {
  analyses: [],
  currentAnalysis: null,
  isLoading: false,
  isAnalyzing: false,
  questionAnswer: null,
  error: null,
};

// Async thunks
export const analyzeDocument = createAsyncThunk(
  'analysis/analyzeDocument',
  async ({ documentId, request }: { documentId: string; request: AnalysisRequest }, { rejectWithValue }) => {
    try {
      const response = await analysisAPI.analyze(documentId, request);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Analysis failed');
    }
  }
);

export const askQuestion = createAsyncThunk(
  'analysis/askQuestion',
  async ({ documentId, request }: { documentId: string; request: QuestionRequest }, { rejectWithValue }) => {
    try {
      const response = await analysisAPI.askQuestion(documentId, request);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Question failed');
    }
  }
);

export const fetchAnalyses = createAsyncThunk(
  'analysis/fetchAnalyses',
  async (params: { document_id?: string; analysis_type?: string; skip?: number; limit?: number } = {}, { rejectWithValue }) => {
    try {
      const response = await analysisAPI.list(params);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch analyses');
    }
  }
);

export const fetchAnalysis = createAsyncThunk(
  'analysis/fetchAnalysis',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await analysisAPI.get(id);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch analysis');
    }
  }
);

export const submitFeedback = createAsyncThunk(
  'analysis/submitFeedback',
  async ({ id, rating, feedback }: { id: string; rating: number; feedback?: string }, { rejectWithValue }) => {
    try {
      await analysisAPI.submitFeedback(id, rating, feedback);
      return { id, rating, feedback };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to submit feedback');
    }
  }
);

const analysisSlice = createSlice({
  name: 'analysis',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentAnalysis: (state) => {
      state.currentAnalysis = null;
    },
    clearQuestionAnswer: (state) => {
      state.questionAnswer = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Analyze document
      .addCase(analyzeDocument.pending, (state) => {
        state.isAnalyzing = true;
        state.error = null;
      })
      .addCase(analyzeDocument.fulfilled, (state, action) => {
        state.isAnalyzing = false;
        state.currentAnalysis = action.payload;
        state.analyses.unshift(action.payload);
        state.error = null;
      })
      .addCase(analyzeDocument.rejected, (state, action) => {
        state.isAnalyzing = false;
        state.error = action.payload as string;
      })
      // Ask question
      .addCase(askQuestion.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(askQuestion.fulfilled, (state, action) => {
        state.isLoading = false;
        state.questionAnswer = action.payload;
        state.error = null;
      })
      .addCase(askQuestion.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch analyses
      .addCase(fetchAnalyses.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchAnalyses.fulfilled, (state, action) => {
        state.isLoading = false;
        state.analyses = action.payload.analyses;
        state.error = null;
      })
      .addCase(fetchAnalyses.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch single analysis
      .addCase(fetchAnalysis.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchAnalysis.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentAnalysis = action.payload;
        state.error = null;
      })
      .addCase(fetchAnalysis.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Submit feedback
      .addCase(submitFeedback.fulfilled, (state, action) => {
        const analysis = state.analyses.find(a => a.id === action.payload.id);
        if (analysis) {
          // Update local state to reflect feedback submission
        }
      });
  },
});

export const { clearError, clearCurrentAnalysis, clearQuestionAnswer } = analysisSlice.actions;
export default analysisSlice.reducer;