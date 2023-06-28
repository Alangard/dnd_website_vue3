import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router.js'
import store from './store'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import axios from 'axios'

import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

axios.defaults.baseURL = 'http://127.0.0.1:8000/'


loadFonts()

createApp(App)
  .use(store)
  .use(vuetify)
  .use(router)
  .component('VueDatePicker', VueDatePicker)
  .mount('#app')
