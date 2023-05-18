<template>
  <v-theme-provider with-background>
    <v-app>
      <Navbar 
        @openAuthDalog="showAuthDialog = !showAuthDialog"
        @openMenuDrawer="main_menu_drawer = !main_menu_drawer">
      </Navbar>

      <v-sheet class="d-flex flex-column align-center">
        <v-sheet class="main_content_wrapper d-flex flex-column align-center w-100 px-3">
          <Filters @filterToolbarIsOpen="filterAsideState =! filterAsideState"></Filters>
          <Journal></Journal>
        </v-sheet>

      </v-sheet>

      <AuthDialog v-model="showAuthDialog" @closeAuthDialog="showAuthDialog = false"> </AuthDialog>

      <FilterAside :isOpenAside="filterAsideState" @filterToolbarIsOpen="filterAsideState =! filterAsideState"></FilterAside>
      <v-btn class="create_post_btn" icon="mdi-plus-thick" v-if="!filterAsideState"></v-btn>


      <v-navigation-drawer v-if="width <= 740" v-model="main_menu_drawer" location="left" temporary>
        <v-switch
            v-model="darkMode"
            @change="toggleDarkMode"
            hide-details
            inset
            :label="`Theme: ${switchLabel} mode`"
        ></v-switch>

      </v-navigation-drawer>

    </v-app>
  
  </v-theme-provider>
</template>

<script setup>
import {ref, computed, onBeforeMount} from 'vue';
import {useStore} from 'vuex';
import { useTheme } from 'vuetify/lib/framework.mjs';
import { useDisplay } from 'vuetify';

import Navbar from '@/components/Navbar.vue';
import Journal from '@/pages/Journal.vue';
import Filters from '@/components/Filters/Filters.vue'
import FilterAside from '@/components/Filters/FilterAside.vue'
import AuthDialog from '@/pages/AuthDialog.vue';

const store = useStore();
let theme = useTheme();
const { width } = useDisplay()

let filterAsideState = ref(false);
let showAuthDialog = ref(false);
let darkMode = ref(false);
const main_menu_drawer = ref(false);


const LoclaStorageThemeManager = () => {
    if(localStorage.getItem('theme')){
        theme.global.name.value = localStorage.getItem('theme');
        darkMode.value = theme.global.name.value == 'light'? false : true
    }
    else{
        theme.global.name.value = 'light'
        darkMode = false
    }
}

const toggleDarkMode = () => {
    theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
    localStorage.setItem('theme', theme.global.name.value)
}

const switchLabel = computed(() => {return darkMode.value ? 'dark' : 'light';})


onBeforeMount(() => {
  LoclaStorageThemeManager();
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
