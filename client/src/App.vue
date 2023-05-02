<template>
  <v-theme-provider with-background>
    <v-app>
      <Navbar></Navbar>
      <v-sheet class="d-flex flex-column align-center">
        <v-sheet class="main_content_wrapper d-flex flex-column align-center w-100 px-3">
          <Filters></Filters>
          <Journal></Journal>
        </v-sheet>

      </v-sheet>
      <v-btn class="create_post_btn" icon="mdi-plus-thick" ></v-btn>
    </v-app>
    
    <!-- <v-app>
      <Navbar></Navbar>
      <v-spacer></v-spacer>
      <v-col>
        <div class="main_content_wrapper">
          <Journal></Journal>
        </div>
      </v-col>
      <v-spacer></v-spacer>
        <v-btn class="create_post_btn" icon="mdi-plus-thick" ></v-btn>
    </v-app> -->

  </v-theme-provider>
</template>

<script setup>
import {ref} from 'vue';
import {useStore} from 'vuex';

import Navbar from '@/components/Navbar.vue';
import Journal from '@/pages/Journal.vue';
import Filters from '@/components/Filters.vue'

const store = useStore();

</script>

<style lang="scss" scoped>

.main_content_wrapper{
  max-width: 740px;
}
.create_post_btn{
  position: fixed;
  bottom: 10px;
  right: 10px;
  z-index: 9999;
}
</style>
