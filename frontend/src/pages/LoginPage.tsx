import React, { useEffect, useState } from 'react'

const LoginPage = () => {

  const authenticateUser = async() => {
    // fetch() can't follow redirects across origins with credentials or user interaction
    window.location.href = "http://127.0.0.1:8000/login";
  }

  return (
    <div>
      <h1>
        Welcome Back
      </h1>
      <button className="login-button" onClick={authenticateUser}>Log In</button>
    </div>
  )
}

export default LoginPage;