import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL 

export const handleUserQuery = async (query: string) => {
  try {
    const res = await axios.post(`${API_BASE_URL}/query/handle`, { query });
    return res.data;
  } catch (err) {
    console.error("Error in handleUserQuery", err);
    throw err;
  }
}; 

const authUser = async() => { 
    const response = await fetch("http://127.0.0.1:8001/login", {
  method: "GET",
  headers: {
    "Content-Type": "application/json"
  },
})
if (!response.ok) {
    throw new Error('Network response was not ok');
  }

    return response.json();

}

const zohoAPI = async(url: string) => { 
   const response = await fetch(url, {
  method: "GET",
  headers: {
    "Content-Type": "application/json"
  },
//   body: JSON.stringify({ username: "admin", password: "123" })
})
if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return response.json();
}

const authService = {
    authUser,
    zohoAPI
}

export default authService