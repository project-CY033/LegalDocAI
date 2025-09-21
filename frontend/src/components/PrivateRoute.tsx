import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { Outlet } from 'react-router-dom';

const PrivateRoute: React.FC = () => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export default PrivateRoute;