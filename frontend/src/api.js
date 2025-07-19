import axios from 'axios';

const api = axios.create({
  //baseURL: 'http://10.131.18.144:8000' // pi ip address
  //baseURL: 'http://localhost:8000',
  baseURL: 'http://10.161.1.185:8000', // laptop ip address
});

export default api;
