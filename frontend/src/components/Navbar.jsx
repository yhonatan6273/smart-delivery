import { NavLink } from 'react-router-dom'
import { useAuth } from '../Context/AuthContext';

const Navbar = () => {
  const { token, isAdmin } = useAuth();

  
  return (
    <nav className="flex flex-col gap-10 bg-blue-200 p-4">
      <div className="flex flex-col gap-2 p-4 ">
        <div className="font-bold">manager phone: 053-9236230</div>
        <div className="font-bold"> shop address: Tel aviv dizengoff center</div>
      </div>
      
      <div 
        className="text-purple-700 text-3xl font-bold text-center">Smart Delivery Project
      </div>
      
      <div className="flex flex-row gap-5 justify-center">
       
        <NavLink to="/">Home</NavLink>
        
        {/* show only for users that didn't login yet */}
        {!token && (
            <>
                <NavLink to="/login">Login</NavLink>
                <NavLink to="/register">Register</NavLink>
            </>
        )}

        {/* show only to users that login already */}
        {token && (
            <>
                <NavLink to="/deliveries">Deliveries</NavLink>
                <NavLink to="/add-delivery">Add Delivery</NavLink>
            </>
        )}
      
        {/* show only to admin users */}
        {isAdmin && (
           <NavLink 
             to="/manager" 
           >
             Manager
           </NavLink>
        )}
        
      </div>
      
    </nav>
  )
}

export default Navbar