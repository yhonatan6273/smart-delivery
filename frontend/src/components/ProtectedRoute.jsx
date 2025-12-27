import { useAuth } from '../Context/AuthContext';
import { Navigate, Outlet } from 'react-router-dom';
import { toast } from 'react-toastify';
import { useEffect } from 'react';

export const ProtectedRoute = () => {
  const { isLoggedIn } = useAuth(); 
  
useEffect(() => {
    if (!isLoggedIn) {
     toast.error("You need to log in first", {
        toastId: 'login-error' 
      });
    }
  }, [isLoggedIn]);


  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }
  
  return <Outlet />;
};

