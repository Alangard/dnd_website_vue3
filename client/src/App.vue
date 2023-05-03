<template>
  <v-theme-provider with-background>
    <v-app>
      <Navbar></Navbar>
      <v-sheet class="d-flex flex-column align-center">
        <v-sheet class="main_content_wrapper d-flex flex-column align-center w-100 px-3">
          <Filters @filterToolbarIsOpen="filterAsideState =! filterAsideState"></Filters>
          <Journal></Journal>
        </v-sheet>

      </v-sheet>



      <FilterAside :isOpenAside="filterAsideState" @filterToolbarIsOpen="filterAsideState =! filterAsideState"></FilterAside>
      <v-btn class="create_post_btn" icon="mdi-plus-thick" v-if="!filterAsideState"></v-btn>

    </v-app>
  
  </v-theme-provider>
</template>

<script setup>
import {ref} from 'vue';
import {useStore} from 'vuex';

import Navbar from '@/components/Navbar.vue';
import Journal from '@/pages/Journal.vue';
import Filters from '@/components/Filters/Filters.vue'
import FilterAside from '@/components/Filters/FilterAside.vue'

const store = useStore();
let filterAsideState = ref(false);


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
