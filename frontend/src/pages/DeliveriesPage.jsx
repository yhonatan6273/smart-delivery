import React, { useState, useEffect } from 'react';
import { useAuth } from '../Context/AuthContext'; 
import { Link } from 'react-router-dom'; 

//the loading  page
const LoadingSpinner = () => (
  <div className="flex justify-center items-center h-64">
    <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
  </div>
);

const DeliveriesPage = () => {
  
  //State to hold the array of deliveries fetched from the API
  const [deliveries, setDeliveries] = useState([]);
  //State to manage the loading status 
  //We start with 'true' to fetch immediately on mount.
  const [loading, setLoading] = useState(true);
  //State to hold any potential fetch errors
  const [error, setError] = useState(null);
  //Get the 'token' from our global AuthContext.
  const { token } = useAuth();

  
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
        
      
        const res = await fetch('http://localhost:8000/deliveries', {
          method: 'GET',
          headers: {
            //Include the JWT token in the Authorization header
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

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
  }, [token]);


  //Show spinner while loading
  if (loading) {
    return <LoadingSpinner />;
  }

  //Show error message if fetch failed
  if (error) {
    return <div className="text-center text-red-500 p-8">Error: {error}</div>;
  }
  
  //Show message if there are no deliveries
  if (deliveries.length === 0) {
    return <div className="text-center text-gray-500 p-8">There is no Deliveries</div>;
  }

  //Render the list of deliveries using .map()
  return (
    <section className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6"> My Deliveries lists</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/*Iterate over the deliveries array */}
        {deliveries.map((delivery) => (
          //Each item in a map needs a unique 'key' prop
          <div key={delivery.id} className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            
            
            <h2 className="text-xl font-semibold mb-2"> {delivery.id}</h2>
            <p className="text-gray-700 mb-1">
              <strong>status:</strong> 
              
              <span className="font-medium text-blue-600"> {delivery.status}</span>
            </p>
            
            <p className="text-gray-700 mb-1">
              <strong>order information:</strong> {delivery.delivery_type}
            </p>

            <p className="text-gray-700 mb-1">
              <strong>address:</strong> {delivery.customer_address}
            </p>
            
            <p className="text-gray-700 mb-1">
              <strong>contact phone:</strong> {delivery.customer_phone}
            </p>


            
            <Link 
              to={`/edit-delivery/${delivery.id}`} 
              className="text-blue-500 hover:text-blue-700 font-medium"
            >
              Edit Delivery
            </Link>
          </div>
        ))}

      </div>
    </section>
  );
};

export default DeliveriesPage;