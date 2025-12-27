

import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../Context/AuthContext';



export const AdminRoute = () => {
  const { token, isAdmin } = useAuth();
  
  if (!token || !isAdmin) {
    //If he is not admin send him to home page
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
};

