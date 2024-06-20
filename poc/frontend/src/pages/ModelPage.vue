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
              <div><strong>MSE:</strong> {{ formatDecimals(model.mean_squared_error) }}</div>
              <div><strong>MAE:</strong> {{ formatDecimals(model.mean_absolute_error) }}</div>
              <div><strong>R²:</strong> {{ formatDecimals(model.r2_score) }}</div>
              <div><strong>Type:</strong> {{ model.model_type }}</div>
            </div>
            <button class="delete-button" @click="confirmDelete(model)"><i class="fa-solid fa-trash"></i></button>
          </div>
        </div>
      </div>

      <!-- Confirmation Dialog -->
      <q-dialog v-model="deleteDialogVisible" persistent>
        <q-card class="custom-card">
          <q-card-section class="text-h6">
            Confirm Deletion
          </q-card-section>
          <q-card-section>
            Are you sure you want to delete this model?
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="Cancel" color="primary" v-close-popup />
            <q-btn flat label="Delete" color="negative" @click="deleteModel" />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Error Dialog -->
      <q-dialog v-model="errorDialogVisible" persistent>
        <q-card class="custom-card">
          <q-card-section class="text-h6">
            Error
          </q-card-section>
          <q-card-section>
            {{ errorMessage }}
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="Close" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
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
    const deleteDialogVisible = ref(false);
    const errorDialogVisible = ref(false);
    const errorMessage = ref('');
    const modelToDelete = ref(null);

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

    const formatDecimals = (input) => {
      return input.toFixed(2);
    };

    const confirmDelete = (model) => {
      modelToDelete.value = model;
      deleteDialogVisible.value = true;
    };

    const deleteModel = async () => {
      try {
        await api.deleteModel(modelToDelete.value.id);
        models.value = models.value.filter(model => model.id !== modelToDelete.value.id);
        deleteDialogVisible.value = false;
        modelToDelete.value = null;
      } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Failed to delete model';
        errorDialogVisible.value = true;
        deleteDialogVisible.value = false;
      }
    };

    onMounted(() => {
      fetchModels();
    });

    return {
      handleClose,
      models,
      formatDate,
      formatDecimals,
      confirmDelete,
      deleteDialogVisible,
      deleteModel,
      errorDialogVisible,
      errorMessage
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
  justify-content: space-between; /* Add this line */
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

.delete-button {
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  font-size: 16px;
  margin-left: 16px;
  transition: color 0.3s ease;
}

.delete-button:hover {
  color: #a71d2a;
}

.custom-card {
  border-radius: 16px; 
}
</style>


