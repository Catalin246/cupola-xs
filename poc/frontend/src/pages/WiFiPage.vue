<template>
  <q-responsive :ratio="16/9" class="col">
    <q-page class="q-pa-md">
      <div class="header">
        <q-btn icon="arrow_back" label="Previous Week" @click="changeWeek(-1)" class="week-btn" style="border-top-left-radius: 25px; border-bottom-left-radius: 25px;" />
        <q-btn :label="currentWeekLabel" disable class="week-dropdown" />
        <q-btn icon-right="arrow_forward" label="Next Week" @click="changeWeek(1)" class="week-btn" style="border-top-right-radius: 25px ; border-bottom-right-radius: 25px;"/>
      </div>
      <div class="chart-container">
        <apexchart class="bar-chart" type="bar" :options="chartOptions" :series="series" />
      </div>
      <template v-if="hasToken">
        <q-btn label="Upload CSV/Excel" @click="uploadFile" color="primary" />
      </template>
      <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" />
    </q-page>
  </q-responsive>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../axios'
import dayjs from 'dayjs'

// Series and chart options for the chart
const series = ref([
  { name: 'Devices', data: [] },
])
const chartOptions = ref({
  chart: {
    type: 'bar',
  },
  plotOptions: {
    bar: {
      columnWidth: '50%',
      distributed: true
    }
  },
  xaxis: {
    categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  },
  dataLabels: {
    enabled: false
  },
  title: {
    text: 'Wifi Devices by Day',
    align: 'center'
  },
  colors: ['#7DCFB6'],
  yaxis: {
    title: {
      text: 'Number of Connected Devices'
    }
  },
  legend: {
    show: false // This hides the legend
  }
})
// Function to fetch visitor data
const fetchVisitorData = async () => {
  try {
    const response = await api.getWifiPrediction(currentWeek.value.format('DD-MM-YYYY'))
    series.value[0].data = response.data.map(dayData => dayData[0])
  } catch (error)  {
    console.error(error)
  }
}

// Computed property to check if JWT token exists
const hasToken = computed(() => {
  return !!localStorage.getItem('jwt')
})

// State to track the current week
const currentWeek = ref(dayjs().startOf('week'))

const currentWeekLabel = computed(() => {
  const startOfWeek = currentWeek.value.format('DD MMM')
  const endOfWeek = currentWeek.value.add(6, 'day').format('DD MMM')
  return `${startOfWeek} - ${endOfWeek}`
})

// Function to handle file upload
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await api.uploadWifiData(formData)
    if (response.data.success) {
      console.log('File uploaded successfully')
    }
  } catch (error) {
    console.error('File upload failed:', error)
  }
}

// Function to trigger file input
const uploadFile = () => {
  const fileInput = document.querySelector('input[type="file"]')
  if (fileInput) {
    fileInput.click()
  }
}

// Function to change the current week
const changeWeek = (direction) => {
  currentWeek.value = currentWeek.value.add(direction * 7, 'day')
  fetchVisitorData()
}

onMounted(() => {
  fetchVisitorData()
})

</script>

<style scoped>
.q-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  padding-bottom: 3em;
}
.week-btn {
  background-color: #4E8FF1;
  color: white;
  width: 200px; /* Set a fixed width to ensure all buttons are the same size */
  text-align: center;
}
.week-dropdown {
  width: 200px; /* Set a fixed width to ensure all buttons are the same size */
  text-align: center;
}

.chart-container {
  margin-bottom: 20px;
  width: 75%;
  padding: 1em;
}
.bar-chart {
  width: 100%;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 1em;
}

input[type="file"] {
  display: none;
}
</style>
