<template>
  <q-page class="q-pa-md">
    <div class="header">
      <q-btn icon="arrow_back" label="Previous Week" @click="changeWeek(-1)" :disable="!canNavigate(-1)"
             class="week-btn" style="border-top-left-radius: 25px; border-bottom-left-radius: 25px;" />
      <q-btn :label="currentWeekLabel" disable class="week-dropdown" />
      <q-btn icon-right="arrow_forward" label="Next Week" @click="changeWeek(1)" :disable="!canNavigate(1)"
             class="week-btn" style="border-top-right-radius: 25px; border-bottom-right-radius: 25px;" />
    </div>

    <div class="chart-container">
      <div style="text-align: center; margin-bottom: 10px; padding-bottom: 1em">
        Click on a day to show hourly predictions.
      </div>
      <apexchart class="bar-chart" type="bar" :options="chartOptions" :series="series" @dataPointSelection="onBarClick" />
    </div>


    <!-- Selected Date Section -->
    <div v-if="selectedDate" class="selected-date q-mt-md">
      <q-card class="hourly-card">
        <q-card-section>
          <div class="text-h6">Selected Date</div>
          <div>{{ selectedDate }}</div>
        </q-card-section>
        <!-- Line Chart Section -->
        <div v-if="selectedDayHourlyData.length > 0">
          <apexchart class="line-chart" type="line" :options="lineChartOptions" :series="lineSeries" />
        </div>
      </q-card>
    </div>

    <!-- Model Performance Metrics Section -->
    <div class="metrics-section q-pa-md">
      <q-card>
        <q-card-section>
          <div class="text-h6">Model Performance Metrics</div>
          <div>Mean Squared Error: {{ meanSquaredError }}</div>
          <div>Mean Absolute Error: {{ meanAbsoluteError }}</div>
          <div>R² Score: {{ r2Score }}</div>
          <div>Accuracy: {{ accuracyPercentage }}%</div>
        </q-card-section>
      </q-card>
    </div>

    <!-- Upload CSV/Excel Button -->
    <template v-if="hasToken">
      <q-btn label="Upload CSV/Excel" @click="uploadFile" color="primary" />
    </template>
    <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" />

    <!-- Success and Error Dialogs -->
    <q-dialog v-model="successDialogVisible" title="Success">
      <div style="background-color: #66FF66; padding: 1rem;">{{ message }}</div>
    </q-dialog>

    <q-dialog v-model="errorDialogVisible" title="Error">
      <div style="background-color: #ffcccc; padding: 1rem;">{{ message }}</div>
    </q-dialog>
  </q-page>
</template>

 <script setup>
 import { ref, computed, onMounted } from 'vue'
 import api from '../../axios'
 import dayjs from 'dayjs'
 import { Dialog } from 'quasar'

 const meanSquaredError = ref('0.00');
 const meanAbsoluteError = ref('0.00');
 const r2Score = ref('0.00');
 const accuracyPercentage = ref('0.00');

 function getWifiMetrics() {
   api.getWifiMetrics().then((response) => {
     meanSquaredError.value = response.data.mean_squared_error.toFixed(2);
     meanAbsoluteError.value = response.data.mean_absolute_error.toFixed(2);
     r2Score.value = response.data.r2_score.toFixed(2);
     accuracyPercentage.value = (response.data.r2_score * 100).toFixed(2);
   }).catch((error) => {
     console.error('Failed to get WiFi metrics:', error);
   });
 }

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
   },
   responsive: [
     {
       breakpoint: 600,
       options: {
         plotOptions: {
           bar: {
             columnWidth: '70%',
           }
         },
         xaxis: {
           labels: {
             style: {
               fontSize: '10px',
             }
           }
         },
         yaxis: {
           labels: {
             style: {
               fontSize: '10px',
             }
           }
         },
         title: {
           style: {
             fontSize: '12px',
           }
         }
       }
     }
   ],
   tooltip: {
     custom: function({ series, seriesIndex, dataPointIndex }) {
       const currentDate = currentWeek.value.add(dataPointIndex, 'day').toDate();
       const matchingData = monthlyData.value.find(item => dayjs(item.date).isSame(currentDate, 'day'));

       if (matchingData) {
         return `<div class="tooltip-custom" style="background: #fff; padding: 10px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                <div style="font-weight: bold; margin-bottom: 5px;">Date: ${dayjs(matchingData.date).format('DD MMM YYYY')}</div>
                <div>Devices: ${series[seriesIndex][dataPointIndex]}</div>
              </div>`;
       } else {
         return ''; // If no matching data, return an empty string or handle as needed
       }
     }
   }
  })

   // Series and chart options for the line chart
 const selectedDayHourlyData = ref([]);
 const lineSeries = computed(() => [
   {
     name: 'Hourly Devices',
     data: selectedDayHourlyData.value.map(item => item.value)
   }
 ])
 const lineChartOptions = ref({
   chart: {
     type: 'line',
   },
   xaxis: {
     categories: selectedDayHourlyData.value.map(item => item.hour)
   },
   dataLabels: {
     enabled: false
   },
   title: {
     text: 'Hourly Wifi Devices',
     align: 'center'
   },
   colors: ['#007BFF'],
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
 const message = ref('')
 const successDialogVisible = ref(false);
 const errorDialogVisible = ref(false);
 const selectedDate = ref(null);

 const fetchVisitorData = async () => {
   try {
     const response = await api.getWifiPrediction();
     monthlyData.value = response.data.map(item => ({
       date: formatStringToDate(item.date),
       devices: item.max_online_devices,
       hourly_values: item.hourly_values
     }))

     // Set the current week to the start of the data
     const startDate = new Date(monthlyData.value[0].date);
     currentWeek.value = dayjs(startDate).startOf('week').clone();
     updateChartData();
   } catch (error) {
     console.error(error);
   }
 };

 const onBarClick = (event, chartContext, { dataPointIndex }) => {
   // Get the date for the clicked bar from the current week's data
   const currentDate = currentWeek.value.add(dataPointIndex, 'day').toDate();

   // Find the corresponding data in monthlyData.value
   const matchingData = monthlyData.value.find(item => dayjs(item.date).isSame(currentDate, 'day'));

   if (matchingData) {
     selectedDayHourlyData.value = matchingData.hourly_values;
     selectedDate.value = dayjs(matchingData.date).format('DD MMM YYYY');
   } else {
     // Handle case when no matching data is found
     selectedDayHourlyData.value = [];
     selectedDate.value = null; // Or handle as needed
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
   const xAxisCategories = [];
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

     // Build the xAxis categories
     xAxisCategories.push(dayjs(currentDate).format('dddd')); // Use dayjs to format the day
   }

   // Update the series with the current week's data
   series.value = [{ name: 'Devices', data: currentWeekDevices }];

   // Assign the colors array
   chartOptions.value = {
     ...chartOptions.value,
     xaxis: {
       categories: xAxisCategories
     },
     colors: currentWeekColors
   };
 };

 // Function to check if navigation is possible
 const canNavigate = (direction) => {
   if (!monthlyData.value.length) return false;

   const newWeek = currentWeek.value.add(direction * 7, 'day');
   const firstDate = dayjs(monthlyData.value[0].date);
   const lastDate = dayjs(monthlyData.value[monthlyData.value.length - 1].date);

   return !(newWeek.isBefore(firstDate, 'day') || newWeek.endOf('week').isAfter(lastDate, 'day'));
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
       message.value = response.data.message;
       successDialogVisible.value = true;
     }
   } catch (error) {
     console.error('File upload failed:', error)
     message.value = error.response.data.message;
     errorDialogVisible.value = true;
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
   getWifiMetrics()
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
   width: 200px;
   /* Set a fixed width to ensure all buttons are the same size */
   text-align: center;
 }

 .week-dropdown {
   width: 200px;
   /* Set a fixed width to ensure all buttons are the same size */
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

 .selected-date {
   width: 75%;
   padding: 1em;
 }

 input[type="file"] {
   display: none;
 }

 .hourly-card {
    padding: 2em;
   border-radius: 15px;
   box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
 }

 @media (max-width: 600px) {
   .chart-container {
     width: 100%;
     padding: 0.5em;
   }

   .bar-chart {
     padding: 0.5em;
   }

   .selected-date {
     width: 100%;
     padding: 0.5em;
   }

   .week-btn,
   .week-dropdown {
     width: 150px;
     height: 50px;
   }
 }
 </style>
