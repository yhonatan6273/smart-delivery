
import {FaExclamationTriangle} from 'react-icons/fa'
const NotFoundPage = () => {
  return (
    <section className= 'flex flex-col justify-center items-center h-96' >
      <FaExclamationTriangle className='text-yellow-500 text-3xl font-bold ' />
      <div className='text-red-700 text-2xl font-bold '>This Page Not Found </div>
    </section>
  )
}

export default NotFoundPage