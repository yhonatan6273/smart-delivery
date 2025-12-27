import  { useMemo } from 'react';
import { GoogleMap, MarkerF,PolylineF, useJsApiLoader} from '@react-google-maps/api';

// Container style for the map
const containerStyle = {
  width: '100%',
  height: '500px',
  marginTop: '20px',
  borderRadius: '10px'
};

// Default center (Tel Aviv)
//lat=the latitude of the location 
//lng=the longitude of the location
const defaultCenter = {
  lat: 32.0853,
  lng: 34.7818
};

// Define libraries array outside of the component to prevent infinite re-renders
const libraries =["geometry"];

const polylineOptions = {
  strokeColor: "#3b82f6",
  strokeOpacity: 0.8,
  strokeWeight: 6,
  geodesic: true,
};

const LiveFleetMap = ({ deliveries, routePolyline }) => {
    const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_API_KEY,
    libraries: libraries
  });
  
  // Memoize the decoded path to prevent re-calculations on every render only if google reload
  const decodedPath = useMemo(() => {
    if (!isLoaded || !routePolyline || !window.google || !window.google.maps|| !window.google.maps.geometry){ 
        return [];
    }
    try {
      // Decode the polyline using Google Maps Geometry library
      return window.google.maps.geometry.encoding.decodePath(routePolyline);
    } catch (error) {
      console.error("Failed to decode polyline:", error);
      return [];
    }
  }, [routePolyline, isLoaded]);
 
  // Function to determine marker icon based on status (Day 11 Bonus)
  const getMarkerIcon = (status) => {
    let color = "red";  // Default for 'in-transit' 
    
    if (status === 'delivered') color = "green"; // Default for 'delivered' 
      
    else if (status === 'approve') color = "blue"; // Default for 'approve' 
        
    // Return the URL for the colored marker icon
    return `https://maps.google.com/mapfiles/ms/icons/${color}-dot.png`;
  };


  if (!isLoaded) return <div>Loading Map...</div>;

  
return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={defaultCenter}
      zoom={12}
    >
     
      {decodedPath.length > 0 && (
        <PolylineF
          path={decodedPath}
          options={polylineOptions}
        />
      )}

      {deliveries.map(delivery => {
        
        const lat = parseFloat(delivery.latitude);
        const lng = parseFloat(delivery.longitude);
        console.log("Full Delivery Object:", delivery);
        // check if the conversion succeed
        if (!isNaN(lat) && !isNaN(lng)) {
          return (
            <MarkerF
              key={delivery.id}
              position={{ lat, lng }}
              title={`Order #${delivery.id} - ${delivery.customer_name}`}
              icon={getMarkerIcon(delivery.status)}
            />
          );
        }
        return null;
      })}
    </GoogleMap>
  );
};

export default LiveFleetMap;