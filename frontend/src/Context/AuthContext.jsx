import React, { createContext, useContext, useState, useEffect } from 'react';


//The context itself, which components will consume.
const AuthContext = createContext();

//Creating the provider
export const AuthProvider = ({ children }) => {
  //keep the user LoggedIn even if he reload the page
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [isLoggedIn, setIsLoggedIn] = useState(Boolean(localStorage.getItem('token')));
  

  //This ensures state is synchronized
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
      setIsLoggedIn(true);
    }
  }, []);// [] dependency array = run only once on mount.

  //Handles API call, state update, and token persistence
  const login = async (loginData) => {
    const formData = new URLSearchParams();
    formData.append('username', loginData.email);
    formData.append('password', loginData.password);

    try {
      const res = await fetch('http://localhost:8000/login', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        console.error('Login failed! Check credentials.');
        alert('Login failed! Check credentials.'); 
        return false;
      }

      const data = await res.json();
      
      
      setToken(data.access_token);
      localStorage.setItem('token', data.access_token);
      setIsLoggedIn(true);
      
      console.log('Login successful, token:', data.access_token);
      
      return true;
    //Handle network/fetch errors
    } catch (error) {
      console.error('Server connection error:', error);
      alert('Server connection error.');
      return false;
    }
  };

  //Clears both local state and persisted token
  const logout = () => {
    setToken(null);
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    
  };
  //Provide the state and the updater functions to the entire app
  const value={ token, isLoggedIn, login, logout }
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
//Custom hook to make consuming the context cleaner
export const useAuth = () => {
  return useContext(AuthContext);
};