import  { useState } from 'react';
import { useAuth } from '../Context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

const AddDeliveriesPage = () => {
  
  

 const [formData, setFormData] = useState({
    customerPhone: '',
    customerName: '',
    customerId: '',
    customerAddress: '',
    deliveryType: ''
});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { token } = useAuth();
  const navigate = useNavigate();
  
  
const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
        ...prev,
        [name]: value
    }));
  };


 // Prevent the form from reloading the page
  const handleSubmit = async (e) => {
    e.preventDefault(); 
    
    const { customerName, customerPhone, customerId, deliveryType, customerAddress } = formData;

    if (customerName.length < 2 || customerName.length > 100) {
      setError('Customer Name must be between 2 and 100 characters.');
      return;
    }
    const phoneRegex = /^\+?\d{9,15}$/;
    if (!phoneRegex.test(customerPhone)) {
      setError('Phone number must be between 9 and 15 number digits');
      return;
      }
    const idRegex = /^\d{7,11}$/;
    if (!idRegex.test(customerId)) {
      setError('Customer ID must be between 7 and 11 number digits.');
      return;
      }
    if (deliveryType.length < 2 || deliveryType.length > 100) {
      setError('Delivery Type must be at least 2 characters.');
      return;
      }
    if (customerAddress.length < 2) {
      setError('Value error, Address not valid according to Google Maps');
      return;
    }
    if (deliveryType.length < 2 || deliveryType.length > 100) {
      setError('Delivery Type must be at least 2 characters.');
      return;
    }


    const deliveryData = {
      customer_phone: customerPhone,
      customer_id: customerId,
      customer_name: customerName,
      customer_address: customerAddress,
      delivery_type: deliveryType
    };

     if (!token) {
      setError('You must be logged in to create a delivery.');
      return;
    }

    setLoading(true);
    setError(null);
  try {
      const res = await fetch('http://localhost:8000/deliveries', {
        method: 'POST',
        headers: {
          
          'Authorization': `Bearer ${token}`,
         
          'Content-Type': 'application/json'
        },
        // Send the data as a JSON string
        body: JSON.stringify(deliveryData)
      });
      // If the server returns an error 
      if (!res.ok) {
        
        const errorData = await res.json();
        let errorMessage = `Failed to add delivery. Status: ${res.status}`;
        if (errorData.detail) {
             // If detail is an array of errors
             if (Array.isArray(errorData.detail)) {
                 errorMessage = errorData.detail.map(err => err.msg).join('\n');
             } 
             // If detail is a single string message
             else if (typeof errorData.detail === 'string') {
                 errorMessage = errorData.detail;
             }
            
             else {
                 errorMessage = JSON.stringify(errorData.detail);
             }
        }
        
        throw new Error(errorMessage);
      }

      // If successful:
      setLoading(false);
      toast('Delivery created successfully!');
      // Navigate the user back to the main deliveries list
      navigate('/deliveries');

    } catch (err) {
      // If the fetch itself fails 
      setError(err.message);
      setLoading(false);
    }
  };

  
return (
    <section className="container mx-auto p-4 max-w-lg">
      <h1 className="text-3xl font-bold text-center mb-6">Create New Delivery</h1>
      
      {/* This is the form. When submitted, it calls handleSubmit. */}
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md space-y-4">
        
        <div>
          <label htmlFor="customerName" className="block text-sm font-medium text-gray-700">
            Customer Name:
          </label>
          <input
            name="customerName"
            type="text"
            id="customerName"
            value={formData.customerName}
            onChange={handleChange}
            className="mt-1 block w-full border rounded-md p-2"
            required
          />
        </div>

        <div>
          <label htmlFor="customerPhone" className="block text-sm font-medium text-gray-700">
            Customer Phone:
          </label>
          <input
            name="customerPhone"
            type="text"
            id="customerPhone"
            value={formData.customerPhone}
            onChange={handleChange}
            className="mt-1 block w-full border rounded-md p-2"
            required
          />
        </div>

        <div>
          <label htmlFor="customerId" className="block text-sm font-medium text-gray-700">
            Customer ID:
          </label>
          <input
            name="customerId"
            type="text"
            id="customerId"
            value={formData.customerId}
            onChange={handleChange}
            className="mt-1 block w-full border rounded-md p-2"
            required
          />
        </div>

        <div>
          <label htmlFor="customerAddress" className="block text-sm font-medium text-gray-700">
            Customer Address:
          </label>
          <input
            name="customerAddress"
            type="text"
            id="customerAddress"
            value={formData.customerAddress}
            onChange={handleChange}
            className="mt-1 block w-full border rounded-md p-2"
            required
          />
        </div>

        <div>
          <label htmlFor="deliveryType" className="block text-sm font-medium text-gray-700">
            Delivery Type:
          </label>
          <input
            name="deliveryType"
            type="text"
            id="deliveryType"
            value={formData.deliveryType}
            onChange={handleChange}
            className="mt-1 block w-full border rounded-md p-2"
            placeholder="what do you want to order?"
            required
          />
        </div>
        
        {/* Show error messages here */}
        {error && (
          <div className="text-center text-red-500 font-bold">{error}</div>
        )}

        <div>
          <button 
            type="submit" 
            className="w-full !bg-blue-200 text-blue p-3 rounded-md font-semibold hover:!bg-blue-600 disabled:!bg-gray-400"
            disabled={loading} //Disable button while loading
          >
            {loading ? 'Submitting' : 'Create Delivery'}
          </button>
        </div>

      </form>
    </section>
  );
};

export default AddDeliveriesPage;