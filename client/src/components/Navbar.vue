<template>
    <v-container fluid class="pb-12">
        <v-app-bar >
            <v-btn>Main</v-btn>
            <v-btn>Post</v-btn>
            <v-switch
                v-model="darkMode"
                @change="toggleDarkMode"
                hide-details
                inset
                :label="`Theme: ${switchLabel} mode`"
            ></v-switch>
        </v-app-bar>
    </v-container>
</template>


<script setup>
import {ref, computed, onBeforeMount} from 'vue'
import { useTheme } from 'vuetify/lib/framework.mjs';

    let darkMode = ref(false)
    let theme = useTheme()

    onBeforeMount(() => {
        if(localStorage.getItem('theme')){
            theme.global.name.value = localStorage.getItem('theme');
            darkMode.value = theme.global.name.value == 'light'? false : true
        }
        else{
            theme.global.name.value = 'light'
            darkMode = false
        }
    })

    const toggleDarkMode = () => {
        theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
        localStorage.setItem('theme', theme.global.name.value)
    }
        
        
    

    const switchLabel = computed(() => {return darkMode.value ? 'dark' : 'light';})
    
</script>

<style lang='scss' scoped>
</style>