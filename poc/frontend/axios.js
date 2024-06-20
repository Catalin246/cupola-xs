import axios from 'axios';

// Create an Axios instance
const apiClient = axios.create({
  baseURL: 'http://localhost:5000', // Backend URL for API calls
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add a request interceptor to set the token in the request headers
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('jwt');
  if (token) {
    config.headers['Authorization'] = `${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// You don't need to add CORS headers on the client-side. The server should handle CORS.
// If you want to handle responses or errors globally, you can use the response interceptor.
apiClient.interceptors.response.use(response => {
  return response;
}, error => {
  return Promise.reject(error);
});

export default {
  // User Login
  login(loginData) {
    return apiClient.post('/login', loginData);
  },
  getCinemaVisitor() {
    return apiClient.post('/predict/cinema');
  },
  uploadCinemaData(formData) {
    return apiClient.post('/cinema/', formData, {
      headers: {
        'Authorization': `${localStorage.getItem('jwt')}`,
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  getWifiPrediction() {
    return apiClient.post('/predict/wifi');
  },
  // Add remaining endpoints below here
  uploadWifiData(formData) {
    return apiClient.post('/wifi/', formData, {
      headers: {
        'Authorization': `${localStorage.getItem('jwt')}`,
        'Content-Type': 'multipart/form-data'
      }
    });

  },
  getCinemaMetrics() {
    return apiClient.get('/predict/cinema/metrics');
  },
  getWifiMetrics() {
    return apiClient.get('/predict/wifi/metrics');
  },
  getHistoricalDataCinema() {
    return apiClient.get('/cinema/');
  },
  getHistoricalDataWifi() {
    return apiClient.get('/wifi/');
  },
  retrainModel(type) {
    const formData = new FormData();
    formData.append('type', type);
    return apiClient.post('/ai_model/retrain', formData, {
      headers: {
        'Authorization': `${localStorage.getItem('jwt')}`,
        'Content-Type': 'multipart/form-data'
      }
    });
  }
};
