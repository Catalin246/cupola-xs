<template>
  <q-page class="q-pa-md">
    <div class="model-page">
      <div class="">
        <button class="close-button" @click="handleClose"><i class="fa-solid fa-x"></i></button>
        <div v-for="model in models" :key="model.id" :class="['model-card', { 'active-model': model.is_active, 'inactive-model': !model.is_active }]">
          <div class="model-card-content">
            <i class="fa-solid fa-robot model-icon"></i>
            <div>
              <div><strong>Date:</strong> {{ formatDate(model.date) }}</div>
              <div><strong>Status:</strong> {{ model.is_active ? 'This model is in use' : 'This model is not currently in use' }}</div>
              <div><strong>MSE:</strong> {{ model.mean_squared_error }}</div>
              <div><strong>MAE:</strong> {{ model.mean_absolute_error }}</div>
              <div><strong>R²:</strong> {{ model.r2_score }}</div>
              <div><strong>Type:</strong> {{ model.model_type }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import dayjs from 'dayjs';
import api from '../../axios';
import '@fortawesome/fontawesome-free/css/all.min.css';

export default {
  name: 'ModelPage',
  setup() {
    const router = useRouter();
    const models = ref([]);

    const handleClose = () => {
      router.push('/');
    };

    const fetchModels = async () => {
      try {
        const response = await api.getModels();
        models.value = response.data.models;
      } catch (error) {
        console.error('Failed to fetch models:', error);
      }
    };

    const formatDate = (dateString) => {
      return dayjs(dateString).format('YYYY-MM-DD HH:mm:ss');
    };

    onMounted(() => {
      fetchModels();
    });

    return {
      handleClose,
      models,
      formatDate
    };
  },
};
</script>

<style scoped>
.model-page {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  flex-direction: column;
  height: 100vh;
  background-color: #ffffff;
}

.message-box {
  position: relative;
  background-color: white;
  padding: 40px;
  width: 80%;
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

.model-card {
  background-color: #ffffff;
  border: 2px solid #ddd;
  border-radius: 16px;
  padding: 24px;
  margin-top: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  margin: 2%;
  margin-left: 25%;
  width: 100%; /* Default to full width */
}

.active-model {
  border-color: #28a745; /* Green border for active models */
}

.inactive-model {
  border-color: #dc3545; /* Red border for inactive models */
}

.model-card-content {
  display: flex;
  align-items: center;
  font-size: 16px;
}

.model-icon {
  font-size: 24px;
  margin-right: 16px;
  color: #4e8ff1;
}

/* Media query for larger screens */
/* @media (min-width: 992px) {
  .model-card {
    width: 25%; /* Set to 25% of the screen width */
</style>

