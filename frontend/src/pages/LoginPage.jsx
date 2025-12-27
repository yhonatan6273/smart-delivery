
import { useState } from 'react'
import { useAuth } from '../Context/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  //email and password states
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  //take the value login from useAuth
  const { login } = useAuth();
  const navigate = useNavigate();

  //Function for the submit 
  const submitForm = async (e) => {
    //Dont reload the page
    e.preventDefault()
    const loginData ={
      email,
      password
    }
    //user the function login 
    const success = await login(loginData);
    if (success) {
      navigate('/deliveries');
    } 
  }


  
  return (
    <section className='p-4'>
      <h1 className=" font-bold text-center">LoginPage</h1>
      <form className="flex flex-col gap-10 bg-gray-200 p-4" onSubmit={submitForm}>

       
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
      
          <button type="submit" className="w-full !bg-blue-200 text-blue p-3 rounded-md font-semibold hover:!bg-blue-600 disabled:!bg-gray-400">
          Login
        </button>
      </form>
    </section>
    
  )
}

export default LoginPage

    
    