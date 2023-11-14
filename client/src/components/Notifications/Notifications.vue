<template>

    <v-menu class="notifications_menu" location="bottom" transition="slide-y-transition" :close-on-content-click="false" v-model="notificationMenuOpen">
        <template v-slot:activator="{ props }">
            <v-btn stacked class="notifications_btn text-none pa-0 mr-3" width="auto" min-width="40" v-bind="props">
                <v-badge 
                    v-if="notifications_count > 0"
                    :content="notifications_count > 50 ? '50+' : notifications_count" color="error">
                    <v-icon>mdi-bell-outline</v-icon>
                </v-badge>
                <v-icon v-else>mdi-bell-outline</v-icon>
            </v-btn>
        </template>

        <v-card class="notifications_menu_card" max-width="400px">
            <div class="notification_top_menu d-flex flex-row align-center justify-space-between">
                <v-card-title>Notifications</v-card-title>
                <v-btn class="notifications_settings_btn" 
                    icon="mdi-cog-outline" 
                    variant="text" 
                    rounded="sm" 
                    @click="()=> {notificationMenuOpen = !notificationMenuOpen; routes.push({name: 'notifications_settings'})}">
                </v-btn>
            </div>
            
            <v-divider></v-divider>

            <div class="content_container" style="overflow-y: auto; max-height: 440px;">
                <v-card class="my-1" v-for="notification in notificationsList" :key="notification.notification_id"
                    rounded="0" 
                    :variant="notification?.seen ? 'default' : 'tonal'" 
                    color="indigo">   

                    <Notification :notification="notification" :checkbox_with_icon="true" @selectCheckbox="console.log('select_notification_comp')"></Notification>

                    <v-divider></v-divider>
                </v-card>

                <v-card-action class="d-flex flex-row align-center justify-center w-100">
                    <v-btn class="show_all_notifications w-100" variant="text" @click="notificationMenuOpen = !notificationMenuOpen; routes.push({name: 'notifications'})">Show all</v-btn>
                </v-card-action>
            </div>
        </v-card>
    </v-menu>
        
</template>

<script setup>
import { ref, computed, onBeforeMount, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex';
import axios from 'axios';
import routes from '@/router/router' 

import Notification from '@/components/Notifications/Notification.vue'

const store = useStore();
const websocket = ref(null);

const current_page = ref(1)
const page_count = ref(1)
const page_size = 10
let page_url = ref(`?page=1&page_size=${page_size}`)

let notifications_count = ref(0)
const notificationMenuOpen = ref(false)
const notificationsList = computed(() => {return store.getters['accounts/getNotificationsList']});

onBeforeMount(async () => {
    if(store.getters['auth/loginState'] == true){
  
        let url = `ws://${axios.defaults.baseURL.split('http://')[1]}ws/notification_socket-server/?token=`

        const verify_response = await store.dispatch('auth/verifyToken')
        if(verify_response?.data?.code  == "token_not_valid"){
            const token = store.getters['auth/getAccessToken']
            url += token
        }
        else{
            const refresh_response = await store.dispatch('auth/refreshToken')
            url += refresh_response.access
        }

        notifications_count.value = (await store.dispatch('accounts/getNotificationsList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count 
        page_count.value = Math.ceil(notifications_count.value / page_size)
        
        websocket.value = new WebSocket(url)

        websocket.value.onmessage = function(e){
            let data = JSON.parse(e.data)
            if(data.status == '200'){
                notifications_count.value += 1
                store.commit('accounts/addNotificationInStore', data.data)
            }
        }

    }
})

onBeforeUnmount(() => {
    if (websocket.value && websocket.value.readyState === WebSocket.OPEN) {websocket.value.close();}
})





</script>

