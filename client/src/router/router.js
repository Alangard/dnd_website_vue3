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
    path: '/journal/:id',
    name: 'post_detail',
    meta: {navbar_name: 'Post detail', navbar_style: 'default'},
    component: () => import('@/pages/JournalPostDetail.vue'),
  },

  {
    path: '/user/:username',
    name: 'user_profile',
    meta: {navbar_name: 'User profile', navbar_style: 'default' },
    component: () => import('@/pages/User.vue'),
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
    path: '/user_activation',
    name: 'user_activation',
    meta: {navbar_name: 'User activation', navbar_style: 'auth'},
    component: () => import('@/pages/Auth/UserActivation.vue')
  },

  // {
  //   path: '/activate/:uid/:token',
  //   name: 'activation_user_link',
  //   redirect: (to) => {
  //     const { uid, token } = to.params;
  //     return `/user_activation_status?uid=${uid}&token=${token}`;
  //   },
  // },

  {
    path: '/reset_password',
    name: 'reset_password',
    meta: {navbar_name: 'Reset Password', navbar_style: 'auth'},
    component: () => import('@/pages/Auth/ResetPass.vue'),
  },

  {
    path: '/reset_password_confirmation',
    name: 'reset_password_confirmation',
    meta: {navbar_name: 'Reset Password Confirmation', navbar_style: 'auth'},
    component: () => import('@/pages/Auth/ResetPassConfirm.vue'),
  },



  // {
  //   path: '/password/reset/confirm/:uid/:token',
  //   name: 'activation_pass_link',
  //   redirect: (to) => {
  //     const { uid, token } = to.params;
  //     return `/reset_password_confirmation?uid=${uid}&token=${token}`;
  //   },
  // }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
