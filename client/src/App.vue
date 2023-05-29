<template>
  <v-theme-provider with-background>
    <v-app>
      <Navbar 
        @openAuthDialog="showAuthDialog = !showAuthDialog"
        @openMenuDrawer="main_menu_drawer = !main_menu_drawer"
        @changeTheme="darkTheme = !darkTheme"
        :darkTheme="darkTheme">
      </Navbar>

      <v-sheet class="d-flex flex-column align-center">
        <v-sheet class="main_content_wrapper d-flex flex-column align-center w-100 px-3">
          <Filters @filterToolbarIsOpen="filterAsideState =! filterAsideState"></Filters>
          <Journal></Journal>
        </v-sheet>

      </v-sheet>

      <AuthDialog v-if='showAuthDialog' v-model="showAuthDialog" @closeAuthDialog="showAuthDialog = false"> </AuthDialog>

      <FilterAside v-if='filterAsideState' :isOpenAside="filterAsideState" @filterToolbarIsOpen="filterAsideState =! filterAsideState"></FilterAside>
      <v-btn class="create_post_btn" icon="mdi-plus-thick" v-if="!filterAsideState"></v-btn>


      <v-navigation-drawer v-if="width <= 740" v-model="main_menu_drawer" location="left" temporary>


      </v-navigation-drawer>

    </v-app>
  
  </v-theme-provider>
</template>

<script setup>
import {ref, computed, defineAsyncComponent, onBeforeMount} from 'vue';
import {useStore} from 'vuex';
import { useTheme } from 'vuetify/lib/framework.mjs';
import { useDisplay } from 'vuetify';

const Navbar = defineAsyncComponent(() => import('@/components/Navbar.vue'));
const Journal = defineAsyncComponent(() => import('@/pages/Journal.vue'));
const Filters = defineAsyncComponent(() => import('@/components/Filters/Filters.vue'));
const FilterAside = defineAsyncComponent(() => import('@/components/Filters/FilterAside.vue'));
const AuthDialog = defineAsyncComponent(() => import('@/pages/AuthDialog.vue'));

const store = useStore();
const { width } = useDisplay();
let theme = useTheme();

let filterAsideState = ref(false);
let showAuthDialog = ref(false);
let darkTheme = ref(false);


const main_menu_drawer = ref(false);


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

const LocalStorageJWTManager = () =>{
  if(localStorage.getItem('access_token') && localStorage.getItem('refresh_token')){
      const access_token = localStorage.getItem('access_token');
      const refresh_token = localStorage.getItem('refresh_token');
      store.commit('setJWT', {'access': access_token, 'refresh':refresh_token})
  }
  else{
    store.commit('setJWT', {'access': '', 'refresh':''})
  }
}




onBeforeMount(() => {
  LocalStorageThemeManager();
  LocalStorageJWTManager();
})




</script>

<style lang="scss" scoped>

.main_content_wrapper{
  max-width: 740px;
}
.create_post_btn{
  position: fixed;
  bottom: 14px;
  right: 43%;
  z-index: 9999;
}
</style>
