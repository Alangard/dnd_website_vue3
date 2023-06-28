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
    meta: {navbar_name: 'Journal', navbar_style: 'default'},
    component: () => import('@/pages/Journal.vue'),
  },

  {
    path: '/login',
    name: 'login',
    meta: {navbar_name: 'Login', navbar_style: 'auth'},
    component: () => import('@/pages/Auth/LogIn.vue'),
  },

  {
    path: '/signup',
    name: 'signup',
    meta: {navbar_name: 'Sign Up', navbar_style: 'auth'},
    component: () => import('@/pages/Auth/SignUp.vue'),
  },

  {
    path: '/reset_password',
    name: 'reset_password',
    meta: {navbar_name: 'Reset Password', navbar_style: 'auth'},
    component: () => import('@/pages/Auth/ResetPass.vue'),
  },

  {
    path: '/activate*',
    name: 'activation_link',
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
