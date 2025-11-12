
import Navbar  from './components/Navbar'
import { 
  createBrowserRouter,
  RouterProvider,
  createRoutesFromElements,
  Route
 } from "react-router-dom"
import React from 'react'
import HomePage from './pages/HomePage';
import DeliveriesPage from './pages/DeliveriesPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AddDeliveryPage from './pages/AddDeliveryPage';
import MainLayout from './layouts/MainLayout';
import EditDeliveryPage from './pages/EditDeliveryPage';
import NotFoundPage from './pages/NotFoundPage';


const App = () => {
  
  const addLogin = async (loginData) => {
    
    const formData = new URLSearchParams();
    
    formData.append('username', loginData.email);
    formData.append('password', loginData.password);

    try {
      const res = await fetch('http://localhost:8000/login', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        console.error('Login failed! Check credentials.');
        return null; 
      }

      const data = await res.json();
      console.log('Login successful, token:', data.access_token);
      
      
      return data;

    } catch (error) {
      console.error('Server connection error:', error);
      return null;
    }
  }




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
        {/* get deliveries */}
        <Route path='deliveries' element={<DeliveriesPage />} />
        {/* post login */}
        <Route path='login' element={<LoginPage LoginSubmit={addLogin} />} />
        {/* post users */}
        <Route path='register' element={<RegisterPage RegisterSubmit={addRegister} />} />
        {/* post deliveries */}
        <Route path='add-delivery' element={<AddDeliveryPage />} />
        {/* put deliveries */}
        <Route path='edit-delivery/:id' element={<EditDeliveryPage />} />
        <Route path='*' element={<NotFoundPage />} />
      </Route>
    )
  );

  return <RouterProvider router={router} />;
};

export default App