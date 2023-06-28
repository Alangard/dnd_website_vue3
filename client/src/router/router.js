import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'home',
    redirect: to => {
      return {path: '/journal'}
    },
  },
  {
    path: '/journal',
    name: 'journal',
    component: () => import('./pages/Journal'),
  },
]

const router = createRouter({
  // history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
