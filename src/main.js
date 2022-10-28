import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router'
import store from './store'
import { Quasar } from 'quasar'
import quasarUserOptions from './quasar-user-options'



const app = createApp(App);


app.use(store);
app.use(router);
app.use(Quasar, quasarUserOptions);
app.mount('#app');
