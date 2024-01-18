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
    component: () => import('@/pages/Journal/JournalList.vue'),
    /// alias and child
  },

  {
    path: '/journal/:filter_params',
    name: 'journal_filters',
    meta: {navbar_name: 'Journal', navbar_style: 'default'},
    component: () => import('@/pages/Journal/JournalList.vue'),
  },

  {
    path: '/journal/:post_id',
    name: 'journal_detail',
    meta: {navbar_name: 'Post detail', navbar_style: 'default'},
    component: () => import('@/pages/Journal/JournalPostDetail.vue'),
  },

  {
    path: '/journal/create',
    name: 'journal_create',
    meta: {navbar_name: 'Post creation', navbar_style: 'default', requiresAuth: true },
    component: () => import('@/pages/Journal/JournalEditable.vue'),
  },

  {
    path: '/journal/:post_id/edit',
    name: 'journal_edit',
    meta: {navbar_name: 'Post editing', navbar_style: 'default', requiresAuth: true },
    component: () => import('@/pages/Journal/JournalEditable.vue'),
  },

  {
    path: '/notifications',
    name: 'notifications',
    meta: {navbar_name: 'Notifications', navbar_style: 'default',  requiresAuth: true},
    component: () => import('@/pages/Notifications/Notifications.vue'),
  },

  {
    path: '/settings/notifications',
    name: 'notifications_settings',
    meta: {navbar_name: 'Notifications settings', navbar_style: 'default',  requiresAuth: true},
    component: () => import('@/pages/Settings/NotificationsSetting.vue'),
  },

  {
    path: '/settings/account',
    name: 'account_settings',
    meta: {navbar_name: 'Account settings', navbar_style: 'default',  requiresAuth: true},
    component: () => import('@/pages/Settings/AccountSetting.vue'),
  },

  {
    path: '/user/:profile_name',
    name: 'user_profile',
    meta: {navbar_name: 'User profile', navbar_style: 'default' },
    component: () => import('@/pages/Profile/Profile.vue'),
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
    path: '/user_activation/:email',
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

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // этот путь требует авторизации, проверяем залогинен ли
    // пользователь, и если нет, перенаправляем на страницу логина
    const user_obj = localStorage.getItem('user')
    if (!user_obj) {
      next({
        path: '/login',
      })
    } else {
      next()
    }
  } else {
    next() // всегда так или иначе нужно вызвать next()!
  }
})

export default router
