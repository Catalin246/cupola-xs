<template>
  <q-page class="q-pa-md">
    <div class="header">
      <h3>WiFi Hourly Usage</h3>
    </div>
    <div class="container">
      <div v-for="(chart, index) in charts" :key="index" class="chart-container">
        <h4>{{ chart.date }}</h4>
        <apexchart
          class="line-chart"
          type="line"
          :options="chart.options"
          :series="chart.series"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import api from '../../axios';
import { ref, onMounted } from 'vue';

// Function to group data by date
const groupDataByDate = (data) => {
  const dataByDate = {};
  data.forEach(item => {
    const date = item.date.split('T')[0]; // Extract date without time
    if (!dataByDate[date]) {
      dataByDate[date] = [];
    }
    dataByDate[date].push(item);
  });
  return dataByDate;
};

// Function to generate chart options and series
const generateChartOptionsAndSeries = (dataByDate) => {
  const charts = [];
  Object.keys(dataByDate).forEach(date => {
    const categories = dataByDate[date].map(item => item.date.split('T')[1].split(':')[0]); // Extract hour
    const seriesData = dataByDate[date].map(item => Number(item.total_online_devices));

    charts.push({
      date,
      options: {
        chart: {
          type: 'line',
        },
        xaxis: {
          categories,
          title: {
            text: 'Hour',
          },
        },
        yaxis: {
          title: {
            text: 'Number of Devices',
          },
        },
        title: {
          text: `Hourly WiFi Usage - ${date}`,
          align: 'center',
        },
      },
      series: [{
        name: `Devices ${date}`,
        data: seriesData,
      }],
    });
  });
  return charts;
};

// Reactive variables
const charts = ref([]);

// Fetch data when the component is mounted
onMounted(async () => {
  try {
    const response = await api.getHistoricalDataWifi();
    const data = response.data.data; // Extract data array from response

    // Group data by date
    const dataByDate = groupDataByDate(data);

    // Generate charts based on grouped data
    charts.value = generateChartOptionsAndSeries(dataByDate);
  } catch (error) {
    console.error('Failed to get historical data:', error);
  }
});
</script>

<style scoped>
.header {
  display: flex;
  justify-content: center;
}
.container {
  justify-content: center;
  align-items: center;
  margin-bottom: 1em;
}
</style>
