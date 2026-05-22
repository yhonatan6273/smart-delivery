
export const deleteDelivery = async (id, token) => {
    // This function is passed down as a prop to handle the API call.
    try {
      const res = await fetch(`/api/deliveries/${id}`, {
        method: 'DELETE',
        headers: {
          // Pass the JWT token for authorization
          'Authorization': `Bearer ${token}`,
        }
      });

      if (!res.ok) {
        // Handle server-side errors 
        const errorData = await res.json();
        throw new Error(errorData.detail || `Server error: ${res.status}`);
      }
      
      // If res.ok is true, the DELETE was successful.
      // No data is returned on a successful DELETE, so we just return implicitly.
    } catch (err) {
    
      console.error("API delete error:", err.message);
      // Re-throw the error to be caught by the component
      throw err;
    }
  }
  