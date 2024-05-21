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
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue' // Adjust the import according to your folder structure

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
  },
  {
    title: 'Logout',
    caption: 'Logout',
    icon: 'logout',
    link: '/logout',
    requiresAuth: true
  }
]

// Define the drawer open state
const leftDrawerOpen = ref(true)

// Function to toggle the drawer open state
function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>

<style scoped>
.logo {
  width: 100%;
  padding: 16px;
  box-sizing: border-box;
}
</style>
