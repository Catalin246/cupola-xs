<template>
  <q-page class="q-pa-md">
    <div class="header">
      <h3>WiFi Weekly Usage</h3>
    </div>
    <div class="calendar-container">
      <q-date
        v-model="selectedRange"
        range
        mask="YYYY-MM-DD"
        label="Select a week"
        @update:model-value="onDateChange"
      />
    </div>
    <div class="container">
      <div v-for="(chart, index) in filteredCharts" :key="index" class="chart-container">
        <h4>{{ chart.date }}</h4>
        <apexchart
          class="line-chart"
          type="line"
          :options="chart.options"
          :series="chart.series"
        />
      </div>
      <div v-if="filteredCharts.length === 0">
        <p>No data available for the selected week.</p>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../../axios';
import { QDate } from 'quasar';
import ApexCharts from 'vue3-apexcharts';

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

// Function to generate chart options and series for a specific date
const generateChartOptionsAndSeriesForDate = (date, data) => {
  const categories = data.map(item => item.date.split('T')[1].split(':')[0]); // Extract hour
  const seriesData = data.map(item => Number(item.total_online_devices));

  return {
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
  };
};

// Reactive variables
const charts = ref([]);
const selectedRange = ref({ from: null, to: null });

// Fetch data when the component is mounted
onMounted(async () => {
  try {
    const response = await api.getHistoricalDataWifi();
    const data = response.data.data; // Extract data array from response

    // Group data by date
    const dataByDate = groupDataByDate(data);

    // Generate charts based on grouped data
    charts.value = Object.keys(dataByDate).map(date => generateChartOptionsAndSeriesForDate(date, dataByDate[date]));
  } catch (error) {
    console.error('Failed to get historical data:', error);
  }
});

// Filter charts based on selected date range
const filteredCharts = computed(() => {
  const { from, to } = selectedRange.value;
  if (!from || !to) {
    return [];
  }
  return charts.value.filter(chart => chart.date >= from && chart.date <= to);
});

const onDateChange = (newRange) => {
  // Ensure we handle the new range correctly
  selectedRange.value = newRange;
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: center;
}
.calendar-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1em;
}
.container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 1em;
  margin-bottom: 1em;
}
.chart-container {
  width: 100%;
  max-width: 500px; /* Adjust size as needed */
}
</style>
