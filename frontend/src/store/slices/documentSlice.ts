import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { documentsAPI, Document, DocumentList } from '../../services/api';

interface DocumentState {
  documents: Document[];
  currentDocument: Document | null;
  isLoading: boolean;
  uploadProgress: number;
  error: string | null;
  total: number;
  skip: number;
  limit: number;
}

const initialState: DocumentState = {
  documents: [],
  currentDocument: null,
  isLoading: false,
  uploadProgress: 0,
  error: null,
  total: 0,
  skip: 0,
  limit: 20,
};

// Async thunks
export const uploadDocument = createAsyncThunk(
  'documents/upload',
  async (file: File, { rejectWithValue }) => {
    try {
      const response = await documentsAPI.upload(file);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Upload failed');
    }
  }
);

export const fetchDocuments = createAsyncThunk(
  'documents/fetchDocuments',
  async (params: { skip?: number; limit?: number; status_filter?: string } = {}, { rejectWithValue }) => {
    try {
      const response = await documentsAPI.list(params);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch documents');
    }
  }
);

export const fetchDocument = createAsyncThunk(
  'documents/fetchDocument',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await documentsAPI.get(id);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch document');
    }
  }
);

export const deleteDocument = createAsyncThunk(
  'documents/deleteDocument',
  async (id: string, { rejectWithValue }) => {
    try {
      await documentsAPI.delete(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to delete document');
    }
  }
);

const documentSlice = createSlice({
  name: 'documents',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setUploadProgress: (state, action: PayloadAction<number>) => {
      state.uploadProgress = action.payload;
    },
    clearCurrentDocument: (state) => {
      state.currentDocument = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Upload document
      .addCase(uploadDocument.pending, (state) => {
        state.isLoading = true;
        state.error = null;
        state.uploadProgress = 0;
      })
      .addCase(uploadDocument.fulfilled, (state, action) => {
        state.isLoading = false;
        state.documents.unshift(action.payload);
        state.uploadProgress = 100;
        state.error = null;
      })
      .addCase(uploadDocument.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        state.uploadProgress = 0;
      })
      // Fetch documents
      .addCase(fetchDocuments.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDocuments.fulfilled, (state, action) => {
        state.isLoading = false;
        state.documents = action.payload.documents;
        state.total = action.payload.total;
        state.skip = action.payload.skip;
        state.limit = action.payload.limit;
        state.error = null;
      })
      .addCase(fetchDocuments.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch single document
      .addCase(fetchDocument.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDocument.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentDocument = action.payload;
        state.error = null;
      })
      .addCase(fetchDocument.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Delete document
      .addCase(deleteDocument.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(deleteDocument.fulfilled, (state, action) => {
        state.isLoading = false;
        state.documents = state.documents.filter(doc => doc.id !== action.payload);
        if (state.currentDocument?.id === action.payload) {
          state.currentDocument = null;
        }
        state.error = null;
      })
      .addCase(deleteDocument.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, setUploadProgress, clearCurrentDocument } = documentSlice.actions;
export default documentSlice.reducer;