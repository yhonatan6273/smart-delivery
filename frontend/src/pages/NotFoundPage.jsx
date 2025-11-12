import React from 'react'
import {FaExclamationTriangle} from 'react-icons/fa'
const NotFoundPage = () => {
  return (
    <>
    <FaExclamationTriangle className='text-yellow-500 text-3xl font-bold ' />
    <div className='text-red-700 text-2xl font-bold '>This Page Not Found </div>
    </>
  )
}

export default NotFoundPage