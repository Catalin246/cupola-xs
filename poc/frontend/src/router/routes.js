// Description: The routes of the application.
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },
  {
    path: '/cinema',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/CinemaPage.vue') }
    ]
  },
  {
    path: '/admin/login',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/LoginPage.vue') }
    ]
  },
  {
    path: '/admin/model',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/ModelPage.vue') }
    ]
  },
  {
    path: '/wifi',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/WiFiPage.vue') }
    ]
  },
  {
    path: '/cinema-actual',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',component: () => import('pages/CinemaHistoricalData.vue')
      }
    ]
  },
  {
    path: '/wifi-actual',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '', component: () => import('pages/WiFiHistoricalData.vue')
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
];

export default routes;
