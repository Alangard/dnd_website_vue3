<template>
  <v-theme-provider with-background>
    <v-app>
        <Navbar></Navbar>
        <Journal></Journal>
        <v-btn class="create_post_btn" icon="mdi-plus-thick" ></v-btn>
    </v-app>
  </v-theme-provider>
</template>

<script setup>
import {ref} from 'vue';
import {useStore} from 'vuex';

import Navbar from '@/components/Navbar.vue';
import Journal from '@/pages/Journal.vue';

const store = useStore();

</script>

<style lang="scss" scoped>

.create_post_btn{
  position: fixed;
  bottom: 10px;
  right: 10px;
  z-index: 9999;
}
</style>
