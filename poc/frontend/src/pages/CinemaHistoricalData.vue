<template>
    <q-page-container class="container">
      <h3>Cinema Historical Data</h3>
      <div v-for="(chart, index) in charts" :key="index" class="chart-container">
        <h4>{{ chart.year }}</h4>
        <apexchart
          class="line-chart"
          type="line"
          :options="chart.options"
          :series="chart.series"
        />
      </div>
    </q-page-container>
</template>

<script setup>
import api from '../../axios';
import { ref, onMounted } from 'vue';

// Function to group data by year
const groupDataByYear = (data) => {
  const dataByYear = {};
  data.forEach(item => {
    const year = item.date.split('-')[0]; // Extract year from date
    if (!dataByYear[year]) {
      dataByYear[year] = [];
    }
    dataByYear[year].push(item);
  });
  return dataByYear;
};

// Function to generate chart options and series
const generateChartOptionsAndSeries = (dataByYear) => {
  const charts = [];
  Object.keys(dataByYear).forEach(year => {
    const categories = dataByYear[year].map(item => item.date);
    const seriesData = dataByYear[year].map(item => item.visitors);

    charts.push({
      year,
      options: {
        chart: {
          type: 'line',
        },
        xaxis: {
          type: 'datetime',
          categories,
        },
        title: {
          text: `Visitors Over Time - ${year}`,
          align: 'center',
        },
      },
      series: [{
        name: `Visitors ${year}`,
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
    const response = await api.getHistoricalDataCinema();
    const data = response.data.data;

    // Group data by year
    const dataByYear = groupDataByYear(data);

    // Generate charts based on grouped data
    charts.value = generateChartOptionsAndSeries(dataByYear);
  } catch (error) {
    console.error('Failed to get historical data:', error);
  }
});
</script>

<style scoped>
.container {
  align-items: center;
}

.chart-container {
 padding: 2em;
}

.line-chart {
 align-items: flex-start;
}
</style>
