import React from 'react'
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const RegisterPage = ({RegisterSubmit }) => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  const submitForm = async (e) => {
    e.preventDefault()

    setError('');
     
    if(!email && !password){
      setError('Email and password are required')
      return;
    }
    if(!email){
      setError('Email is required')
      return;
    }

    if(!password){
      setError('Password is required')
      return;
    }

    //basic email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // check if the email that user entered is valid
      if (!emailRegex.test(email)) {
        setError('Invalid Email Format Please Enter a Valid Email');
        return;
      }
    const registerData ={
      email,
      password
    }
    const result= await RegisterSubmit(registerData);
    if(result && result.error){
      setError(result.message);
    }
    else if(result){
      // if valid register navigate to deliveries page
      return navigate('/login');
    }
    else{
      setError('Registration Failed! Try Again Later.');
    }
  }

  return (
    <section className='p-4'>
      <h1 className=" font-bold text-center">RegisterPage</h1>
      <form className="flex flex-col gap-10 bg-gray-200 p-4" onSubmit={submitForm}>
        {error && <p className="text-red-500 text-center font-bold">{error}</p>}
        <div>
          <input
            type= 'email'
            className="border rounded p-2 w-full px-3"
            placeholder='enter your email:'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            />
        </div>
          
        <div>
          <input
            
            type="password"
            className="border rounded p-2 w-full px-3"
            placeholder='enter your password:'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            />
        </div>
      
          <button type="submit" className="text-black   ">
          Register
        </button>
      </form>
    </section>
    
  )
}

export default RegisterPage

