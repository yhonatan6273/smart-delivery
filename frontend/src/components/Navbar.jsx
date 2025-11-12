import React from 'react'
import { NavLink} from 'react-router-dom'

const Navbar = () => {
  return (
    
    <nav className="flex flex-col gap-10 bg-blue-200 p-4">
      

      <div 
        className="text-purple-700 text-3xl font-bold text-center">Smart Delivery
      </div>
      
      <div className="flex flex-row gap-5 justify-center">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/login">Login</NavLink>
        <NavLink to="/register">Register</NavLink>
        <NavLink to="/deliveries">Deliveries</NavLink>
        <NavLink to="/add-delivery">Add Delivery</NavLink>
        <NavLink to="/edit-delivery/:id">Edit Delivery</NavLink>
      </div>
      
    </nav>
  )
}

export default Navbar