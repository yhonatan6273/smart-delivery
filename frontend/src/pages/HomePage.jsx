
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-grey-50 flex flex-col">
      
      {/* creating border*/}
      <div className="bg-white border-b border-gray-200">
        <div className=" py-20 text-center">
          
          {/* creating status indicator for the system */}
          <div className="inline-flex items-center px-4 py-2 rounded-full border border-blue-100 bg-blue-50 text-blue-700 text-sm font-semibold mb-8 shadow-sm">
            <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
            System Operational
          </div>

          {/* creating the main title and subtitle */}
          <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-6 tracking-tight">
            Smart Delivery <br />
            <span className="text-blue-600">Management Platform</span>
          </h1>
          <p className="mt-4 text-xl text-gray-500 max-w-3xl mx-auto mb-10">
            Effortlessly create and track your deliveries. 
            <br />
            Advanced routing and fleet management tools for system administrators.
          </p>
          
          {/* creating login and register buttons */}
          <div className="flex justify-center gap-4">
            <Link 
              to="/login" 
              className=" px-8 py-4 rounded-lg font-bold text-lg hover:bg-blue-700 transition shadow-lg"
            >
              Login to Account
            </Link>
            <Link 
              to="/register" 
              className=" px-8 py-4 rounded-lg font-bold text-lg hover:bg-blue-700 transition shadow-lg"
            >
              Create Account
            </Link>
          </div>
        </div>
      </div>

      {/* creating platform features section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">Platform Features</h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Tailored for Users & Managers
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
        {/* creating the feature cards */}  
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Create Deliveries</h3>
            <p className="text-gray-500">
              Anyone can register and dispatch new packages. Simple forms with instant address validation.
            </p>
          </div>

        
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Track Your Orders</h3>
            <p className="text-gray-500">
              View the status and history of all deliveries you've created. Get real-time updates and ETA predictions.
            </p>
          </div>

         
          <div className="relative bg-gray-50 p-8 rounded-2xl shadow-inner border border-gray-200 overflow-hidden">
     
            <div className="absolute top-0 right-0 bg-gray-800 text-white px-3 py-1 rounded-bl-lg text-xs font-bold uppercase tracking-wider flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
              </svg>
              Admin Only
            </div>
            
            <div className="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-800 mb-3">Full Management</h3>
            <p className="text-gray-600">
              System-wide control. Delete orders, manage users, and oversee the entire logistics network.
            </p>
          </div>

        </div>
      </div>
    </div>
  )
}

export default HomePage