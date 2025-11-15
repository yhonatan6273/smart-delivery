import React from 'react'
import { useState } from 'react'
import { useAuth } from '../Context/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  //State for the form's controlled inputs
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  
  const { login } = useAuth();
  const navigate = useNavigate();

  
  const submitForm = async (e) => {
    e.preventDefault()
    const loginData ={
      email,
      password
    }

    const success = await login(loginData);
    if (success) {
      navigate('/deliveries');
    } 
  }


  
  return (
    <section className='p-4'>
      <h1 className=" font-bold text-center">LoginPage</h1>
      <form className="flex flex-col gap-10 bg-gray-200 p-4" onSubmit={submitForm}>
          <input
            type= 'email'
            className="border rounded p-2  px-3"
            placeholder='enter your email:'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            />
          

          <input
            
            type="password"
            className="border rounded p-2 px-3"
            placeholder='enter your password:'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            />
      
          <button type="submit" className="text-black   ">
          Login
        </button>
      </form>
    </section>
    
  )
}

export default LoginPage

    
    