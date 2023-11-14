<template>    
    <v-card class="notifications_container mt-8" 
        height="100%" 
        :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'">
        This is settings
    </v-card>
</template>

<script setup>
import { ref, computed, onBeforeMount} from 'vue'
import {useDisplay } from 'vuetify/lib/framework.mjs';
import { useStore } from 'vuex';
import routes from '@/router/router' 

const { width } = useDisplay();
const store = useStore();

const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})

onBeforeMount(() => {
    if(width.value >= mobileWidthLimit.value){routes.push({name: 'home'})}
})
</script>

<style lang='scss' scoped>
</style>
