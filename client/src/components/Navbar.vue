<template>
    <v-container fluid class="pb-12">
        <v-app-bar class="d-flex flex-row justify-space-between" v-if="routes.currentRoute.value.meta.navbar_style == 'default'">

            <v-app-bar-nav-icon 
                variant="text" 
                @click.stop="openMenuDrawer">
            </v-app-bar-nav-icon>

            <v-toolbar-title>{{currentRouteName }}</v-toolbar-title>

            <v-spacer></v-spacer>

             <v-btn stacked class="text-none pa-0 mr-3" width="auto" min-width="40">
                <v-badge content="2" color="error">
                    <v-icon>mdi-bell-outline</v-icon>
                </v-badge>
            </v-btn>
 
            <v-btn stacked class="theme_btn pa-0 mr-2"  
                width="auto" 
                min-width="40" 
                :icon="prop.darkTheme ? 'mdi-weather-night': 'mdi-weather-sunny'"
                rounded="0"
                variant="text" 
                @click="toggleDarkMode">
            </v-btn>

            <v-btn stacked class="login_btn pa-0 mr-2 br-0" 
                width="auto" 
                min-width="40"
                icon="mdi-login-variant" 
                rounded="0" 
                variant="text" 
                v-if="loggedIn == false" 
                @click="routes.push({name:'login'})">
            </v-btn>

            <v-menu transition="slide-y-transition" offset="16">
                
                <template v-slot:activator="{ props }">
                    <v-btn stacked class="account_menu pa-0 mr-2" 
                        width="auto" 
                        min-width="40"
                        icon="mdi-account-circle" 
                        rounded="0" 
                        variant="text"  
                        v-bind="props" 
                        v-if="loggedIn" >
                    </v-btn>
                </template>

                <v-list>

                    <v-list-item value="0" active-color="primary">
                        <template v-slot:prepend>
                            <v-avatar class="avatar mr-2" style="cursor:pointer" >
                                <v-img v-if="currUserData.avatar" :src="currUserData.avatar" :alt="currUserData.username"></v-img>
                                <v-icon icon="mdi-account-circle" size='x-large' v-else></v-icon>
                            </v-avatar>
                        </template>
                        <v-list-item-content>
                            <v-list-item-title v-text="currUserData.username"></v-list-item-title> 
                            <v-list-item-subtitle v-text="currUserData.role"></v-list-item-subtitle> 
                        </v-list-item-content>
                    </v-list-item>

                    <v-divider></v-divider>

                    <v-list-item class="ml-1"
                        active-color="primary"  
                        v-for="(section, i) in sections" :key="i" 
                        :value="section.section_name" 
                        @click="clickOnSection(section.page_name)"
                    >
                        <template v-slot:prepend>
                            <v-icon class="mr-5" :icon="section.icon"></v-icon>
                        </template>

                        <v-list-item-title v-text="section.section_name"></v-list-item-title>
                    </v-list-item>

                    <v-divider></v-divider>

                    <v-list-item class="ml-1" value="logout" active-color="primary" @click="logout">
                        <template v-slot:prepend >
                            <v-icon class="mr-5" icon="mdi-logout-variant"></v-icon>
                        </template>
                        <v-list-item-title>Logout</v-list-item-title>
                    </v-list-item>

                </v-list>
            </v-menu>
            

        </v-app-bar>

        <v-app-bar class="d-flex flex-row justify-space-between" v-else>

            <v-toolbar-title>{{currentRouteName }}</v-toolbar-title>

            <v-btn stacked class="theme_btn pa-0 mr-2"  
                width="auto" 
                min-width="40" 
                :icon="prop.darkTheme ? 'mdi-weather-night': 'mdi-weather-sunny'"
                rounded="0"
                variant="text" 
                @click="toggleDarkMode">
            </v-btn>

        </v-app-bar>
    </v-container>
</template>


<script setup>
import {ref, computed,  defineEmits, defineProps} from 'vue';
import { useStore } from 'vuex';
import { useTheme } from 'vuetify/lib/framework.mjs';
import routes from '@/router/router';

let theme = useTheme();
const store = useStore();
const emit = defineEmits(['openAuthDialog', 'openMenuDrawer', 'changeTheme'])
const prop = defineProps(['darkTheme'])

const toggleDarkMode = () => {
    theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
    localStorage.setItem('theme', theme.global.name.value)
    emit('changeTheme');
}

const sections = ref([
    { section_name: 'Profile', page_name: 'profile', icon: 'mdi-account' },
    { section_name: 'Settings', page_name: 'settings', icon: 'mdi-cog' },
])

const clickOnSection = (section_name) => {console.log(section_name)}

const logout = () => {store.dispatch("auth/logout")}

const openMenuDrawer = () => {emit('openMenuDrawer')}

const currentRouteName = computed(() => {return routes.currentRoute.value.meta.navbar_name})

const loggedIn = computed(() => {return store.getters['auth/loginState']});

const currUserData = computed(() => {return store.getters.getCurrUserData;})


    



    
</script>

<style lang='scss' scoped>
</style>