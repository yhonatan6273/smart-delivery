import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { toast } from 'react-toastify';
import { formatDate, calculateTargetTime, getStatusColor, sortDeliveriesByStatus} from '../utils/DeliveryHelpers';
import { useFetchDeliveries } from '../hooks/useFetchDeliveries';
import LiveFleetMap from '../components/LiveFleetMap';
import{deleteDelivery} from '../services/deliveryService';



const ManagerPage = () => {

  const { deliveries, loading, error, isAdmin, removeDeliveryFromState, token } = useFetchDeliveries();

  // State to hold the encoded polyline string from the backend
  const [currentRoutePolyline, setCurrentRoutePolyline] = useState(null);
  // State for loading the route calculation
  const [isRouteLoading, setIsRouteLoading] = useState(false);

  // Define the store location as the fixed origin
  const STORE_ORIGIN = "Tel Aviv, Dizengoff Center";

  const sortedDeliveries = sortDeliveriesByStatus(deliveries);

  
  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete?")) return;
    try {
      
      
      await deleteDelivery(id, token);

      removeDeliveryFromState(id); 
      toast.success("Deleted successfully");
    } catch (err) {
      toast.error(err.message);
    }
  };

  // Function to fetch route from backend
  const handleShowRoute = async (destinationAddress) => {
    setIsRouteLoading(true);
    setCurrentRoutePolyline(null);
    try {
      // We use URLSearchParams to properly encode the query parameters
      const params = new URLSearchParams({
        origin: STORE_ORIGIN,
        destination: destinationAddress
      });

      const res = await fetch(`http://localhost:8000/route?${params.toString()}`, {
        method: 'GET'
       
      });

      if (!res.ok) {
        throw new Error("Failed to calculate route");
      }

      const data = await res.json();
      
      if (data.directions && data.directions.polyline) {
        setCurrentRoutePolyline(data.directions.polyline);
        toast.success(`Route calculated to ${destinationAddress}`);
      } else {
        toast.warning("No route data found");
      }

    } catch (err) {
      console.error(err);
      toast.error("Could not fetch route from server");
    } finally {
      setIsRouteLoading(false);
    }
  };

  if (loading) return <div className="text-center p-10">Loading...</div>;
  if (error) return <div className="text-red-500 text-center p-10">{error}</div>;

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">Manager Dashboard</h1>
      {/* Map Section */}
      <div className="mb-8 shadow-lg border-4 border-white rounded-xl overflow-hidden">
        <LiveFleetMap 
            deliveries={deliveries} 
            routePolyline={currentRoutePolyline} 
        />
        {isRouteLoading && <p className="text-center text-blue-500 font-bold p-2">Calculating Route...</p>}
      </div>
      {/* Deliveries Table */}
      <div className="overflow-x-auto shadow-md sm:rounded-lg">
        <table className="w-full text-sm text-left text-gray-500">
          <thead className="text-xs text-gray-700 uppercase bg-gray-100">
            <tr>
              <th className="px-6 py-3">ID</th>
              <th className="px-6 py-3">Customer</th>
              <th className="px-6 py-3">Order Info</th>
              <th className="px-6 py-3">Status</th>
              <th className="px-6 py-3">Address</th>
              <th className="px-6 py-3">Created At</th>
              <th className="px-6 py-3">Target Time</th>
              <th className="px-6 py-3">Actions</th>
              <th className="px-6 py-3">Route</th>
            </tr>
          </thead>
          <tbody>
            {sortedDeliveries.map((delivery) => (
              <tr key={delivery.id} className="bg-white border-b hover:bg-gray-50">
                <td className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                  {delivery.id}
                </td>
                <td className="px-6 py-4">
                  {delivery.customer_name}<br/>
                  <span className="text-xs text-gray-400">{delivery.customer_phone}</span>
                </td>
                <td className="px-6 py-4">
                  {delivery.delivery_type}
                </td>
                <td className="px-6 py-4">
                  <span className={`font-bold ${getStatusColor(delivery.status)}`}>
                    {delivery.status}
                  </span>
                </td>
                <td className="px-6 py-4">
                  {delivery.customer_address}
                </td>
                <td className="px-6 py-4">
                  {formatDate(delivery.created_at)}
                </td>
                <td className="px-6 py-4 text-red-600 font-bold">
                  {calculateTargetTime(delivery.created_at, delivery.predicted_eta_minutes)}
                </td>
                <td className="px-6 py-4 flex gap-2">
                <div className="flex items-center gap-4"> 
                  {/* Edit and Delete Buttons */}
                    <NavLink 
                      to={`/edit-delivery/${delivery.id}`} 
                      state={{ delivery }}
                      className="text-blue-500 hover:text-blue-700 font-medium "
                    >
                      Edit
                    </NavLink>
                    <button 
                      onClick={() => handleDelete(delivery.id)}
                      className="text-red-500 !bg-white hover: font-medium
             !outline-none !border-none !ring-0 focus:!outline-none focus:!ring-0 focus:!border-none shadow-none"
                    >
                      Delete
                    </button>
                  </div>
                </td>
                {/* Show Route Button */}
                <td className="px-6 py-4">
                    <button
                        onClick={() => handleShowRoute(delivery.customer_address)}
                        className="!bg-indigo-600 text-white px-3 py-1 rounded hover:!bg-indigo-700 transition text-xs"
                    >
                        Show Route
                    </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ManagerPage;