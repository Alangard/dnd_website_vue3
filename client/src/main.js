import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router.js'
import store from './store'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'


import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

import { QuillEditor } from '@vueup/vue-quill';
import '@vueup/vue-quill/dist/vue-quill.snow.css';






loadFonts()

createApp(App)
  .use(store)
  .use(vuetify)
  .use(router)
  .component('VueDatePicker', VueDatePicker)
  .component('QuillEditor', QuillEditor)
  .mount('#app')
