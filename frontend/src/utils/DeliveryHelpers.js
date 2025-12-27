

  
//Function to make the DATE readable 
export const formatDate = (dateString) => {
    
    const date = new Date(dateString);
    
   
    return date.toLocaleString('en-GB', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

//Function to calculate the total time between predicted ETA in minutes and Created At time.
//added 30 min to the target time so the manager can make and send the delivery on time
export const calculateTargetTime = (createdAt, etaMinutes) => {
    if (!createdAt || etaMinutes === undefined) return "N/A";
    //time of when the delivery created
    const date = new Date(createdAt);
    //the target time
    const targetTimeMs = date.getTime() + (etaMinutes * 60 * 1000)+(30 *60 *1000);
    const targetDate = new Date(targetTimeMs);

    return targetDate.toLocaleTimeString('en-GB', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };
//Function to get the color class based on delivery status  
export const getStatusColor = (status) => {
    switch (status) {
      case 'approve':
        return 'text-blue-500'; 
      case 'in-transit':
        return 'text-red-500';  
      case 'delivered':
        return 'text-green-500'; 
    }
  };
//Define priority for each status
const statusPriority = {
  'approve': 1,
  'in-transit': 2,
  'delivered': 3
};

//Function to sort deliveries based on status priority
export const sortDeliveriesByStatus = (deliveriesList) => {
 
  if (!deliveriesList) return [];

 //create a copy of the deliveries list and then sort it
  return [...deliveriesList].sort((a, b) => {
    //Get priority values for each status from the statusPriority object
    const priorityA = statusPriority[a.status]; 
    const priorityB = statusPriority[b.status];
    //Compare priorities(lower number = higher priority)
    return priorityA - priorityB;
  });
};

