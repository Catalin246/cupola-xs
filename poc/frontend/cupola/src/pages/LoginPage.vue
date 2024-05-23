<template>
  <div class="login-page">
    <div class="login-form">
      <button class="close-button" @click="handleClose"><i class="fa-solid fa-x"></i></button>
      <h2>Welcome</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Email Address</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
          />
        </div>
        <div class="form-group">
          <button type="submit">Sign in</button>
        </div>
      </form>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import '@fortawesome/fontawesome-free/css/all.min.css';

export default {
  name: 'LoginPage',
  setup() {
    const username = ref('');
    const password = ref('');
    const error = ref('');
    const router = useRouter();

    const handleLogin = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/auth/login', {
          email: username.value,
          password: password.value
        });
        
        if (response.data.status === 'success') {
          error.value = '';
          const token = response.data.Authorization;
          // Store the token in local storage or any preferred storage
          localStorage.setItem('jwt', token);
          router.push('/'); // Redirect to home page after successful login
        } else {
          error.value = response.data.message || 'Login failed';
        }
      } catch (err) {
        error.value = err.response?.data?.message || 'An error occurred';
      }
    };

    const handleClose = () => {
      router.push('/');
    };

    return {
      username,
      password,
      error,
      handleLogin,
      handleClose,
    };
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url('/login_background.png');
  background-size: cover;
  background-position: center;
}

.login-form {
  position: relative; /* Add this */
  background-color: white;
  padding: 40px;
  width: 25%;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.login-form h2 {
  font-size: 24px;
  font-weight: bold;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  padding: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border-radius: 10px;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #4E8FF1;
  border: none;
  color: white;
  border-radius: 40px;
  cursor: pointer;
}

button:hover {
  background-color: #D1D3D6;
}

.error {
  color: red;
  margin-top: 15px;
}

.close-button {
  position: absolute; 
  top: 10px; 
  right: 10px;
  font-weight: bold;
  color: #000000;
  background-color: #ffffff;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.close-button:hover {
  color: #808080;
  background-color: #ffffff;
}

.close-button i {
  font-size: 16px;
}
</style>
