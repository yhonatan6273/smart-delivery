import { toast } from 'react-toastify';
import { NavLink} from 'react-router-dom'
import { formatDate, calculateTargetTime, getStatusColor } from '../utils/DeliveryHelpers';
import { useFetchDeliveries } from '../hooks/useFetchDeliveries';



//the loading  page
const LoadingSpinner = () => (
  <div className="flex justify-center items-center h-64">
    <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
  </div>
);

const DeliveriesPage = ({deleteDelivery}) => {
  const { deliveries, loading, error, isAdmin, removeDeliveryFromState, token } = useFetchDeliveries();
  
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
  const onDeleteClick = async (deliveryId) => {
    //This is the component-level event handler for the delete button.
    
    //Get user confirmation and abort if user cancels
    if (!window.confirm("Are you sure you want to delete this delivery?")) {
      return; 
    }

    try {
      // Call the prop function (from App.js) to perform the API request.
      // We must pass the 'token' which is available in this component's scope.
      await deleteDelivery(deliveryId, token);

      removeDeliveryFromState(deliveryId);

      toast.success("Deleted successfully!");
   
      
      
    } catch (err) {
      //Handle errors from the API call (thrown by the deleteDelivery prop)
      console.error("Failed to delete delivery:", err.message);
    }
  };
 

  //Render the list of deliveries using .map()
  return (
    <section className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6"> Deliveries lists</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/*Iterate over the deliveries array */}
        {deliveries.map((delivery) => (
          //Each item in a map needs a unique 'key' prop
          <div key={delivery.id} className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            
            
            <h2 className="text-xl font-semibold mb-2"> {delivery.id}</h2>
            <p className="text-gray-700 mb-1">
              <strong>status:</strong> 
      
              <span className={`font-bold ${getStatusColor(delivery.status)}`}>
                 {delivery.status}
              </span>
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

             <p className="text-gray-700 mb-1">
              <strong>customer name:</strong> {delivery.customer_name}
            </p>


            <p className="text-gray-700 mb-1">
              <strong>Created At:</strong> {formatDate(delivery.created_at)}
            </p>


            {isAdmin && (
              <p className="text-gray-700 mb-1">
              <strong>predicted ETA in minutes</strong> {(delivery.predicted_eta_minutes || 0).toFixed(0)}
              </p>
                
            )}
            <p className="text-gray-700 mb-1">
              <strong>Target Time:</strong> {calculateTargetTime(delivery.created_at, delivery.predicted_eta_minutes)}
            </p>


            {isAdmin && (
                <NavLink
                  to={`/edit-delivery/${delivery.id}`} 
                  state={{ delivery: delivery }}
                  className="text-blue-500 hover:text-blue-700 font-medium "
                >
                  Edit Delivery 
                </NavLink>
            )}

            <button 
            onClick={() => onDeleteClick(delivery.id)}
            className="text-red-500 !bg-white hover:bg-gray-100 font-medium
             !outline-none !border-none !ring-0 focus:!outline-none focus:!ring-0 focus:!border-none shadow-none"
            >
              Delete Delivery

            </button>
          </div>
        ))}

      </div>
    </section>
  );
};

export default DeliveriesPage;