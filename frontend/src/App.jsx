
import Navbar  from './components/Navbar'
import { 
  createBrowserRouter,
  RouterProvider,
  createRoutesFromElements,
  Route
 } from "react-router-dom"

import HomePage from './pages/HomePage';
import DeliveriesPage from './pages/DeliveriesPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AddDeliveryPage from './pages/AddDeliveryPage';
import MainLayout from './layouts/MainLayout';
import EditDeliveryPage from './pages/EditDeliveryPage';
import NotFoundPage from './pages/NotFoundPage';
import { AuthProvider } from './Context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

const App = () => {
  const addRegister = async (registerData) => {
    
    try {
      const res = await fetch('http://localhost:8000/users', { 
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(registerData)
      });
      if (!res.ok) {
        const errorData = await res.json()
        return { error: true, message: errorData.detail };
      }

      const data = await res.json();
      console.log('Register Successful:', data);
      
      
      return data;

    } catch (error) {
      return{error: true, message: 'Error connecting to server try again later'};
      
    }
  }

  
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path='/' element={<MainLayout />}>
        <Route index element={<HomePage />} />
        {/* post login */}
        <Route path='login' element={<LoginPage  />} />
        {/* post users */}
        <Route path='register' element={<RegisterPage RegisterSubmit={addRegister} />} />
        {/* Routers that can be access after login */}
        <Route element={<ProtectedRoute />}>
          <Route path="/deliveries" element={<DeliveriesPage />} />
          <Route path="/add-delivery" element={<AddDeliveryPage />} />
          <Route path="/edit-delivery/:id" element={<EditDeliveryPage />} />
        </Route>
        {/* Router for NotFoundPage if the url not leading to any Router*/}
        <Route path='*' element={<NotFoundPage />} />
      </Route>
      
    )
  );
/**
   *The entire app is wrapped in AuthProvider to make auth state
   *(isLoggedIn, login, logout) globally available to any component.
   *The RouterProvider then consumes the router config.
   */
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
};

export default App