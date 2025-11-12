import React from 'react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'


const LoginPage = ({LoginSubmit }) => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const navigate = useNavigate();
  const submitForm = async (e) => {
    e.preventDefault()
    const loginData ={
      email,
      password
    }
    const result= await LoginSubmit(loginData);
    if(result){
      // if the login is successful Save the token to localStorage  and navigate to deliveries page
      localStorage.setItem('token', result.access_token);
      return navigate('/deliveries');
    }
    else{
      alert('Login failed! Check credentials.');
    }
  }
  return (
    <section className='p-4'>
      <h1 className=" font-bold text-center">LoginPage</h1>
      <form className="flex flex-col gap-10 bg-gray-200 p-4" onSubmit={submitForm}>
          <input
            type= 'email'
            id="email"
            name="email"
            className="border rounded p-2 w-full px-3"
            placeholder='enter your email:'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            />
          

          <input
            
            type="password"
            id="password"
            name="password"
            className="border rounded p-2 w-full px-3"
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

    
    