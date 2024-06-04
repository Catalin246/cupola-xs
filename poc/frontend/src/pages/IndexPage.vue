<template>
  <q-page class="q-pa-md">
    <div class="header">
      <h3>Welcome to Cupola XS</h3>
    </div>
    <div class="weather-container">
      <div v-if="weather">
        <h5>{{ today }}</h5>
        <div class="weather-icon">
          <div class="weather-main">
            <img
              :src="`http://openweathermap.org/img/wn/${weather.weather[0].icon}@2x.png`"
              :alt="weather.weather[0].description"
              class="weather-icon-img"
            >
            <h4>{{ weather.main.temp }} °C</h4>
          </div>
          <p>{{ weather.name }}, {{ weather.sys.country }}</p>
        </div>
        <div class="weather-info">
          <h6>{{ weather.weather[0].description }}</h6>
          <h6>Humidity: {{ weather.main.humidity }}%</h6>
          <h6>Wind Speed: {{ weather.wind.speed }} m/s</h6>
        </div>
      </div>
      <div v-else>
        <img alt="Cupola logo" src="cupolaLogo.png" class="logo">
        <h4>Weather data temporarily unavailable...</h4>
      </div>
    </div>
  </q-page>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

defineOptions({
  name: 'IndexPage'
});

const weather = ref(null);
const today = ref('');

const fetchWeather = async () => {
  const API_KEY = 'f676622c4e91cfb9ac3bccc666c5ef92';
  const CITY = 'Haarlem';
  const URL = `https://api.openweathermap.org/data/2.5/weather?q=${CITY}&appid=${API_KEY}&units=metric`;
  try {
    const response = await axios.get(URL);
    weather.value = response.data;
    updateDate();
  } catch (error) {
    console.error('Error fetching weather data:', error);
  }
};

const updateDate = () => {
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  today.value = new Date().toLocaleDateString('en-GB', options);
};

onMounted(() => {
  fetchWeather();
});
</script>

<style scoped>
.logo {
  width: 300px;
  height: auto;
}
.header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
}
.weather-container {
  text-align: center;
  padding-left: 1em;
  padding-right: 1em;
  border: 2px solid #ccc;
  background-color: #f9f9f9;
  border-radius: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 0 auto;
}

.weather-icon {
  border: 1px solid #ccc;
  border-radius: 45px;
  padding: 1em;
  background-color: rgba(255, 213, 66, 0.7); /* Adjust the alpha value (0.7) to control opacity */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.weather-main {
  display: flex;
  align-items: center;
  justify-content: center;
}

.weather-icon-img {
  margin-right: 2em; /* Adjust the spacing between the icon and the temperature */
}

.weather-info {
  display: flex;
  align-items: center;
}

</style>
