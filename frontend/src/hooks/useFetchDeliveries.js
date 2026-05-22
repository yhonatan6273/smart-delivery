import { useState, useEffect } from 'react';
import { useAuth } from '../Context/AuthContext';






export const useFetchDeliveries = () => {
  
  //State to hold the array of deliveries fetched from the API
  const [deliveries, setDeliveries] = useState([]);
  //State to manage the loading status 
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { token,isAdmin,logout} = useAuth();


   //This useEffect hook runs once on component mount (and if the token changes).
  useEffect(() => {
    const fetchDeliveries = async () => {
      
      if (!token) {
        setLoading(false);
        setError('No authorization token provided.');
        return;
      }

      try {
        setError(null);
      
        const res = await fetch(`/api/deliveries`, {
          method: 'GET',
          headers: {
         
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        if (res.status === 401) {
           logout();
            throw new Error("Session expired. Please login again.");
        }
        if (!res.ok) {
          //If the server responds with an error 
          throw new Error(`Failed to fetch deliveries. Status: ${res.status}`);
        }

        const data = await res.json();
        setDeliveries(data); //Store the fetched array in state
        

      } 
      //Catch any network errors or thrown errors
      catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    //Execute the fetch function
    fetchDeliveries();
    
    //The dependency array ensures this effect re-runs if the token changes.
  }, [token,logout]);


  const removeDeliveryFromState = (id) => {
    setDeliveries(prev => prev.filter(d => d.id !== id));
  };

  return { deliveries, loading, error, isAdmin, removeDeliveryFromState, token };
};

