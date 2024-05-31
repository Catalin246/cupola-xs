<template>
  <div>
    <apexchart type="bar" :options="chartOptions" :series="series" />
  </div>
</template>

<script>
import {onMounted, ref} from 'vue'
import api from '../../axios';

export default {
  name: 'CinemaPage',
  setup() {
    const series = ref([{ name: 'Visitors', data: [] }])
    const chartOptions = ref({
      chart: {
        type: 'bar',
        height: '300px',
        width: '400px'
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
        text: 'Visitors by Day',
        align: 'center'
      },
      colors: ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#FF8333', '#33FFF5', '#FF33D6'], // Add your custom colors here
      yaxis: {
        title: {
          text: 'Number of Visitors'
        }
      }
    })

    const fetchVisitorData = async () => {
      try {
        api.getCinemaVisitor()
          .then((response) => {
            series.value[0].data = response.data
          })
      } catch (error) {
        console.error(error)
      }
    }
    onMounted(() => {
      fetchVisitorData()
    })

    return {
      series,
      chartOptions
    }
  }
}
</script>

<style scoped>

</style>
