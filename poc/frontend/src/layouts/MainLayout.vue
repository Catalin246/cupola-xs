<template>
  <q-layout view="lHh Lpr lFf">
    <q-drawer
      show-if-above
      :style="drawerStyles"
      side="left"
    >
      <!-- drawer content -->
      <img src="/cupolaLogo.png" alt="Cupola Logo" class="logo">

      <q-list>
        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
        <template v-if="hasToken">
          <q-item clickable v-ripple @click="logout">
            <q-item-section avatar>
              <q-icon name="logout" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Logout</q-item-label>
              <q-item-label caption>Logout</q-item-label>
            </q-item-section>
          </q-item>
        </template>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import {computed, ref} from 'vue'
import {useRouter} from 'vue-router'
import EssentialLink from 'components/EssentialLink.vue' // Adjust the import according to your folder structure
import axios from 'axios';

// Define the sidebar (drawer) styles
const drawerStyles = {
  width: '228px',
  height: '1024px',
  flexShrink: 0,
  backgroundColor: '#4E8FF1'
}

// Define the list of essential links
const linksList = [
  {
    title: 'Wifi',
    caption: 'Wifi prediction',
    icon: 'wifi',
    link: '/wifi'
  },
  {
    title: 'Cinema',
    caption: 'Cinema prediction',
    icon: 'movie',
    link: '/cinema'
  }
]

// Define the drawer open state
const leftDrawerOpen = ref(true)

// Computed property to check if JWT token exists
const hasToken = computed(() => {
  return !!localStorage.getItem('jwt')
})

// Function to toggle the drawer open state
function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

const router = useRouter() // Initialize the router

// Function to handle logout
async function logout() {
  try {
    const token = localStorage.getItem('jwt');
    if (!token) {
      console.error('No token found');
      return;
    }

    await axios.post('http://127.0.0.1:5000/auth/logout', {}, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    localStorage.removeItem('jwt'); // Clear token

    // Navigate to /admin/login and then reload the page
    router.push('/admin/login').then(() => {
      window.location.reload();
    });
  } catch (error) {
    console.error('Logout failed:', error);
  }
}
</script>

<style scoped>
.logo {
  width: 100%;
  padding: 16px;
  box-sizing: border-box;
}
</style>
