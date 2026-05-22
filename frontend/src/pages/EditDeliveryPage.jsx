import { useState } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../Context/AuthContext';
import { toast } from 'react-toastify';

const EditDeliveryPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { state } = useLocation(); 
  const { token } = useAuth();


  if (!state || !state.delivery) {
    return <div className="text-center mt-10">No delivery data found. Please go back to deliveries list.</div>;
  }

 
  const [formData, setFormData] = useState({status: state.delivery.status});

  const handleChange = (e) => {
    // create event destructuring
    const { name, value } = e.target;
    // keep the previous form data and only update the changed field
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const res = await fetch(`/api/deliveries/${id}`, {
        method: 'PUT', 
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || 'Failed to update delivery');
      }

      toast.success("Delivery updated successfully!");
      navigate('/deliveries'); 

    } catch (err) {
      console.error(err);
      toast.error(err.message);
    }
  };

  return (
    <section className="bg-indigo-50 min-h-screen py-10">
      <div className="container m-auto max-w-2xl">
        <div className="bg-white px-6 py-8 shadow-md rounded-md border">
          <h2 className="text-3xl text-center font-semibold mb-6">Edit Delivery: {id}</h2>
          
          <form onSubmit={handleSubmit}>

            <div className="mb-4">
              <label className="block text-black-400 font-bold mb-2">Status</label>
              <select
                name="status"
                className="border rounded w-full py-2 px-3 bg-white"
                value={formData.status}
                onChange={handleChange}
              >
                <option className='block text-blue-500 font-bold mb-2' value="approve">Approve</option>
                <option className='block text-red-500 font-bold mb-2' value="in-transit">In-Transit</option>
                <option className='block text-green-500 font-bold mb-2' value="delivered">Delivered</option>
              </select>
            </div>

            <div className="flex gap-4">
              <button
                className="!bg-indigo-500 hover:!bg-indigo-600 text-white font-bold py-2 px-4 rounded-full w-full "
                type="submit"
              >
                Update Delivery
              </button>
              
              <button
                type="button"
                onClick={() => navigate('/deliveries')}
                className="!bg-red-500 hover:!bg-red-600 text-white font-bold py-2 px-4 rounded-full w-full "
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </section>
  );
};

export default EditDeliveryPage;