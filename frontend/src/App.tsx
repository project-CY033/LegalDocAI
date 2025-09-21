import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { Box } from '@mui/material';

import { RootState, AppDispatch } from './store/store';
import { getCurrentUser } from './store/slices/authSlice';

// Components
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import DocumentUpload from './pages/DocumentUpload';
import DocumentList from './pages/DocumentList';
import DocumentView from './pages/DocumentView';
import AnalysisView from './pages/AnalysisView';
import Profile from './pages/Profile';
import PrivateRoute from './components/PrivateRoute';
import LoadingScreen from './components/LoadingScreen';

function App() {
  const dispatch = useDispatch<AppDispatch>();
  const { isAuthenticated, isLoading, token } = useSelector((state: RootState) => state.auth);

  useEffect(() => {
    // If we have a token but no user info, fetch current user
    if (token && !isAuthenticated) {
      dispatch(getCurrentUser());
    }
  }, [dispatch, token, isAuthenticated]);

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Routes>
        {/* Public Routes */}
        <Route 
          path="/login" 
          element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" replace />} 
        />
        <Route 
          path="/register" 
          element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" replace />} 
        />
        
        {/* Private Routes */}
        <Route path="/" element={<PrivateRoute />}>
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="upload" element={<DocumentUpload />} />
            <Route path="documents" element={<DocumentList />} />
            <Route path="documents/:id" element={<DocumentView />} />
            <Route path="analysis/:id" element={<AnalysisView />} />
            <Route path="profile" element={<Profile />} />
          </Route>
        </Route>
        
        {/* Fallback route */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Box>
  );
}

export default App;