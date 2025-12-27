import { createBrowserRouter,RouterProvider,createRoutesFromElements, Route} from "react-router-dom"
import HomePage from './pages/HomePage';
import DeliveriesPage from './pages/DeliveriesPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AddDeliveryPage from './pages/AddDeliveryPage';
import {MainLayout} from './layouts/MainLayout';
import EditDeliveryPage from './pages/EditDeliveryPage';
import NotFoundPage from './pages/NotFoundPage';
import { AuthProvider } from './Context/AuthContext';
import {ProtectedRoute} from './components/ProtectedRoute';
import {AdminRoute} from './components/AdminRoute';
import ManagerPage from './pages/ManagerPage';
import{deleteDelivery} from './services/deliveryService';



const App = () => {
 
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path='/' element={<MainLayout />}>
        <Route index element={<HomePage />} />
        {/* post login */}
        <Route path='login' element={<LoginPage  />} />
        {/* post users */}
        <Route path='register' element={<RegisterPage  />} />
        {/* Routers that can be access after login */}
      <Route element={<ProtectedRoute />}>
        <Route path="/deliveries" element={<DeliveriesPage deleteDelivery={deleteDelivery} />} />
        <Route path="/add-delivery" element={<AddDeliveryPage />} />
        <Route element={<AdminRoute />}>
          <Route path="/edit-delivery/:id" element={<EditDeliveryPage />} />
          <Route path="/manager" element={<ManagerPage />} />
        </Route>
      </Route>
      {/* Router for NotFoundPage if the url not leading to any Router*/}
      <Route path='*' element={<NotFoundPage />} />
    </Route>
  ));
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