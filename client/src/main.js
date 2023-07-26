import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router.js'
import store from './store'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'


import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'




loadFonts()

createApp(App)
  .use(store)
  .use(vuetify)
  .use(router)
  .component('VueDatePicker', VueDatePicker)
  .mount('#app')
