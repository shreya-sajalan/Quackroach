// Example in your api service file
import axios from 'axios';

const api = axios.create({
  // This will look for the variable in Vercel or your local .env
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
});

export default api;