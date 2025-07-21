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
