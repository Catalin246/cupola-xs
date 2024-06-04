import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5000' // Backend URL for API calls. Might be adjusted based on the backend server
});

// Add an interceptor to set the token in the request headers
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Enable CORS headers
apiClient.interceptors.response.use(response => {
  // Add CORS headers to the response
  response.headers['Access-Control-Allow-Origin'] = '*';
  response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE';
  response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization';

  return response;
}, error => {
  return Promise.reject(error);
});
export default {
  // User Login
  login(loginData) {
    return apiClient.post('/login', loginData);
  },
  getCinemaVisitor(date) {
    return apiClient.get('/predict/cinema', date);
  },
  uploadCinemaData(formData) {
    return apiClient.post('/cinema', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
//add the remaining end points below here

};
