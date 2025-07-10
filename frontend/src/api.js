import axios from 'axios';

const api = axios.create({
  baseURL: 'http://10.131.18.144:8000'
});

export default api;
