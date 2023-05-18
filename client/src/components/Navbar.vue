<template>
    <v-container fluid class="pb-12">
        <v-app-bar class="d-flex flex-row justify-space-between">

            <v-app-bar-nav-icon variant="text" @click.stop="openMenuDrawer"></v-app-bar-nav-icon>

            <v-toolbar-title>Journal</v-toolbar-title>

            <v-spacer></v-spacer>

            <!-- <v-btn class="text-none" stacked>
                <v-badge content="2" color="error">
                    <v-icon>mdi-bell-outline</v-icon>
                </v-badge>
            </v-btn> -->

            <v-btn prepend-icon="mdi-login" variant="text" @click="openAuthDalog">
                Login
            </v-btn>

            <!-- <v-btn class="btn mr-1" rounded="lg" icon="mdi-account-circle" @click="login_Dialog = !login_Dialog"></v-btn> -->


            

        </v-app-bar>

    </v-container>
</template>


<script setup>
import {ref, computed, onBeforeMount, defineEmits,} from 'vue';

const emit = defineEmits(['openAuthDalog', 'openMenuDrawer'])

const openMenuDrawer = () => {emit('openMenuDrawer')}

const openAuthDalog = () => {emit('openAuthDalog');}
    



    
</script>

<style lang='scss' scoped>
</style>