import  { createContext, useContext, useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { jwtDecode } from "jwt-decode";

//Create the context 
const AuthContext = createContext();

//Creating the provider
export const AuthProvider = ({ children }) => {
  
  //State to hold the token and login status we try to get from localStorage 
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  //Boolean to track if user is logged in
  const [isLoggedIn, setIsLoggedIn] = useState(Boolean(localStorage.getItem('token')));
  // state to give Permissions only to admin user
  const [isAdmin, setIsAdmin] = useState(false)


  useEffect(() => {
     if (token) {
        try {
           
           const decoded = jwtDecode(token);
           setIsAdmin(decoded.role === 'admin');
        } catch (error) {
           console.error("Invalid token:", error);
           //if the token as an error he is not admin
           setIsAdmin(false); 
        }
        //no token
     } else {
        setIsAdmin(false); 
     }
  }, [token]);


  //This ensures state is synchronized
  //Will check again if there is a token in localStorage on mount and update state accordingly
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
      setIsLoggedIn(true);
    }
  }, []);

  const register = async (registerData) => {

    try {
      const res = await fetch('/api/users', { 
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

  //Function to handle login 
  const login = async (loginData) => {
    //Using URLSearchParams to encode form data and not JSON
    const formData = new URLSearchParams();
    formData.append('username', loginData.email);
    formData.append('password', loginData.password);

    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        console.error('Login failed! Check credentials.');
        toast('Login failed! Check credentials.'); 
        return false;
      }
      // convert the response from formdata to jason
      const data = await res.json();
      
      
      setToken(data.access_token);
      //Store the token in localStorage to persist login state
      localStorage.setItem('token', data.access_token);
      setIsLoggedIn(true);
      
      console.log('Login successful, token:', data.access_token);
      
      return true;
    //Handle network/fetch errors
    } catch (error) {
      console.error('Server connection error:', error);
      toast('Server connection error.');
      return false;
    }
  };

  //Function to handle logout
  const logout = () => {
    setToken(null);
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    
  };
  //Provide the state and the updater functions that will be used in other components
  const value={ token, isLoggedIn,isAdmin, login, logout, register }
  //give access to the value prop to all children components
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
//shortcut to use the context in other components
export const useAuth = () => {
  return useContext(AuthContext);
};