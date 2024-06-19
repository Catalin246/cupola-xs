<template>
  <div class="model-page">
    <div class="message-box">
      <button class="close-button" @click="handleClose"><i class="fa-solid fa-x"></i></button>
      <h2>This is the model page. Our team is still working on it.</h2>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import '@fortawesome/fontawesome-free/css/all.min.css';

export default {
  name: 'ModelPage',
  setup() {
    const router = useRouter();

    const handleClose = () => {
      router.push('/');
    };

    return {
      handleClose,
    };
  },
};
</script>

<style scoped>
.model-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;
}

.message-box {
  position: relative;
  background-color: white;
  padding: 40px;
  width: 50%;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.message-box h2 {
  font-size: 24px;
  font-weight: bold;
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
