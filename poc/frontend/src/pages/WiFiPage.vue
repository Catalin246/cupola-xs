<template>
  <q-page class="q-pa-md">
    <div class="header">
      <q-btn icon="arrow_back" label="Previous Week" @click="changeWeek(-1)" :disable="!canNavigate(-1)"
             class="week-btn" style="border-top-left-radius: 25px; border-bottom-left-radius: 25px;"/>
      <q-btn :label="currentWeekLabel" disable class="week-dropdown"/>
      <q-btn icon-right="arrow_forward" label="Next Week" @click="changeWeek(1)" :disable="!canNavigate(1)"
             class="week-btn" style="border-top-right-radius: 25px ; border-bottom-right-radius: 25px;"/>
    </div>
    <div class="chart-container">
      <apexchart class="bar-chart" type="bar" :options="chartOptions" :series="series" />
    </div>
    <h5 align="center">Please note predictions after {{ accuratePredictionDate }} are less reliable </h5>
    <template v-if="hasToken">
      <q-btn label="Upload CSV/Excel" @click="uploadFile" color="primary" />
    </template>
    <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" />
  </q-page>
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
  colors: ['#F0803C'],
  yaxis: {
    title: {
      text: 'Number of Connected Devices'
    }
  },
  legend: {
    show: false // This hides the legend
  }
})
const currentWeek = ref(dayjs().startOf('week'))
const monthlyData = ref([])
const accuratePredictionDate = ref('')
const fetchVisitorData = async () => {
  try {
    const response = await api.getWifiPrediction();
    monthlyData.value = response.data.map(item => ({
      date: formatStringToDate(item.date),
      devices: item.total_online_devices
    }))

    // Set the current week to the start of the data
    const startDate = new Date(monthlyData.value[0].date);
    currentWeek.value = dayjs(startDate).startOf('week').clone();
    updateChartData();
  } catch (error) {
    console.error(error);
  }
};
const formatStringToDate = (dateString) => {
  const [day, month, year] = dateString.split('-').map(Number)
  return new Date(year, month - 1, day)
}

const updateChartData = () => {
  // Ensure that monthlyData has been populated
  if (Object.keys(monthlyData.value).length === 0) return;

  // Update accuratePredictionDate
  accuratePredictionDate.value = dayjs(monthlyData.value[0].date).add(30, 'day').format('DD MMM YYYY');

  // Get the data for the current week
  const currentWeekDevices = [];
  const currentWeekColors = [];
  for (let i = 0; i < 7; i++) {
    const currentDate = currentWeek.value.add(i, 'day').toDate();
    const matchingData = monthlyData.value.find(item => dayjs(item.date).isSame(currentDate, 'day'));
    currentWeekDevices.push(matchingData ? matchingData.devices : 0);

    // If the item.date is 30 days or more after the first item.date, then the color will be red
    if (matchingData && dayjs(matchingData.date).diff(dayjs(monthlyData.value[0].date), 'day') >= 30) {
      currentWeekColors.push('#FFD542');
    } else {
      currentWeekColors.push('#F0803C');
    }
  }

  // Update the series with the current week's data
  series.value = [{ name: 'Devices', data: currentWeekDevices }];

  // Assign the colors array
  chartOptions.value = {
    ...chartOptions.value,
    colors: currentWeekColors
  };
};

// Function to check if navigation is possible
const canNavigate = (direction) => {
  if (Object.keys(monthlyData.value).length === 0) return false;
  if (currentWeek.value.isBefore(dayjs(monthlyData.value[0].date), 'day') && direction === -1) {
    return false;
  }
  return !(currentWeek.value.isAfter(dayjs(monthlyData.value[monthlyData.value.length - 1].date), 'day') && direction === 1);
};

// Function to change the current week
const changeWeek = (direction) => {
  if (canNavigate(direction)) {
    currentWeek.value = currentWeek.value.add(direction * 7, 'day').clone()
    updateChartData()
  }
}

// Computed property to check if JWT token exists
const hasToken = computed(() => {
  return !!localStorage.getItem('jwt')
})

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
