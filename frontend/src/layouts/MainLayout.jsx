
import { Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar.jsx'
import { ToastContainer} from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'


export const MainLayout = () => {
  return (
    <>
      <Navbar />
      <Outlet />
      <ToastContainer />
    </>
  )
}

