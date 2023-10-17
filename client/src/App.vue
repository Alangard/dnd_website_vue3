<template>
  <v-theme-provider with-background>
    <v-app>
      <Navbar
        @openAuthDialog="showAuthDialog = !showAuthDialog"
        @openMenuDrawer="main_menu_drawer = !main_menu_drawer"
        @changeTheme="darkTheme = !darkTheme"
        :darkTheme="darkTheme">
      </Navbar>

      <div class="content-wrapper d-flex flex-column align-center w-100 h-100">
        <router-view/>
      </div>


      <v-navigation-drawer v-model="main_menu_drawer" location="left" temporary>


      </v-navigation-drawer>

    </v-app>
  
  </v-theme-provider>
</template>

<script setup>
import {ref, defineAsyncComponent, onBeforeMount, computed, onBeforeUnmount} from 'vue';
import { useTheme } from 'vuetify/lib/framework.mjs';
import { useStore } from 'vuex';
import axios from 'axios';
import routes from '@/router/router' 

const Navbar = defineAsyncComponent(() => import('@/components/Navbar.vue'));

let theme = useTheme();
const store = useStore();

let showAuthDialog = ref(false);
let darkTheme = ref(false);
const main_menu_drawer = ref(false);

const token = computed(() => {return store.getters['auth/getAccessToken']})
const url = `ws://${axios.defaults.baseURL.split('http://')[1]}ws/notification_socket-server/?token=${token.value}`
const websocket = new WebSocket(url)


const LocalStorageThemeManager = () => {
    if(localStorage.getItem('theme')){
        theme.global.name.value = localStorage.getItem('theme');
        darkTheme.value = theme.global.name.value == 'light'? false : true
    }
    else{
        theme.global.name.value = 'light'
        darkTheme = false
    }
}


onBeforeMount(() => {
  LocalStorageThemeManager();
  const user_data = store.getters['auth/getUserData']
  store.dispatch('auth/getMyData', user_data?.id)
  
  websocket.onmessage = function(e){
        let data = JSON.parse(e.data)
        console.log(data)
  }
})

onBeforeUnmount(() => {
    websocket.close()
})



</script>

<style lang="scss" scoped>
</style>
