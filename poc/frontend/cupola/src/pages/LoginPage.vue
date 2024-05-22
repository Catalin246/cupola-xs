<template>
  <div class="login-page">
    <div class="login-form">
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

    return {
      username,
      password,
      error,
      handleLogin,
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
  background-color: #f5f5f5;
}

.login-form {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4E8FF1;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #D1D3D6;
}

.error {
  color: red;
  margin-top: 15px;
}
</style>
