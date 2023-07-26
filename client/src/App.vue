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
import {ref, defineAsyncComponent, onBeforeMount} from 'vue';
import {useStore} from 'vuex';
import { useTheme } from 'vuetify/lib/framework.mjs';
import { useDisplay } from 'vuetify';
import router from '@/router/router';

const Navbar = defineAsyncComponent(() => import('@/components/Navbar.vue'));

const store = useStore();
const { width } = useDisplay();
let theme = useTheme();

let filterAsideState = ref(false);
let showAuthDialog = ref(false);
let darkTheme = ref(false);
let currURLObj = ref({});
let ActivationState = ref({state: false, variant: null});

const main_menu_drawer = ref(false);


const checkExpirationToken = () => {
  if(localStorage.getItem('user')){
    // const isExpired = store.dispatch("auth/checkExpirationToken", JSON.parse(localStorage.getItem('user')).access);
    // if(isExpired){store.dispatch("auth/refreshToken")}


    // store.dispatch("auth/verifyToken").catch(error => {
    //   store.dispatch("auth/refreshToken")
    // });
  }
  
};



// }

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
  checkExpirationToken();
  LocalStorageThemeManager();
})



</script>

<style lang="scss" scoped>
</style>
