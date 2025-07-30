import React, { useEffect, useState } from 'react'

const LoginPage = () => {

  const authenticateUser = async() => {
    // fetch() can't follow redirects across origins with credentials or user interaction
    window.location.href = "http://127.0.0.1:8000/login";
  }

  return (
    <div className="bg-gradient-to-tr from-pink-100 to-blue-100 h-screen flex flex-col justify-center items-center">
      <h1>
        Welcome Back
      </h1>
      <button className="login-button" onClick={authenticateUser}>Log In With Zoho</button>
    </div>
  )
}

export default LoginPage;