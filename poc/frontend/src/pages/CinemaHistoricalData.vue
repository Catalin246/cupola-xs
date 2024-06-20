<template>
  <q-page class="q-pa-md">
    <div class="header">
      <h3>Cinema Historical Data</h3>
    </div>
    <div class="graph-container">
      <q-card class="historic-cinema">
        <q-card-section class="historic-cinema-section">
          <div v-for="(chart, index) in charts" :key="index" class="chart-container">
            <apexchart
              class="line-chart"
              type="line"
              :options="chart.options"
              :series="chart.series"
            />
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
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
.header {
  display: flex;
  justify-content: center;
}

.graph-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.historic-cinema {
  width: 80%;
  padding: 1em 2em;
}
.chart-container {
  margin-bottom: 3em;
}

.line-chart {
  max-width: 100%;
}
</style>

