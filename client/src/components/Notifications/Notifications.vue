<template>

    <v-menu class="notifications_menu" location="bottom" transition="slide-y-transition">
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

        <v-card class="notifications_menu_card" width="400px">
            <div class="notification_top_menu d-flex flex-row align-center justify-space-between">
                <v-btn class="read_all_btn" 
                    variant="text" 
                    rounded="sm"
                    @click="console.log('read_all')">
                    Read all
                </v-btn>
                <v-btn class="notifications_settings_btn" 
                    icon="mdi-cog-outline" 
                    variant="text" 
                    rounded="sm" 
                    @click="console.log('notifications_settings')">
                </v-btn>
            </div>
            

            <v-divider class="mb-2"></v-divider>


            <div v-for="notification in notificationsList" :key="notification">
                <div class="notification_container d-flex flex-row align-start justify-start pb-1 mx-2">
                    <div class="avatar">
                        <v-avatar class="avatar mr-2" style="cursor:pointer" size="32">
                            <v-img 
                                v-if="notification?.data?.author?.avatar != null" 
                                :src="notification?.data?.author?.avatar " 
                                :alt="notification?.data?.author?.username">
                            </v-img>
                            <v-icon icon="mdi-account-circle" size='x-large' v-else></v-icon>
                        </v-avatar>
                    </div>
                    <div class="notification_text d-flex flex-column align-start">
                        <div class="text">
                            <span class="username text-info clickable"
                                @click="routes.push({name: 'user_profile', params: { username:  notification?.data?.author?.username }})">
                                @{{ notification?.data?.author?.username }}
                            </span>
                            
                            <span v-if="notification.notification_type == 'post_comment'">
                                <span> left a 
                                    <span class="text-info clickable" @click="goToComment(notification?.data?.id, notification?.data?.post?.id)">
                                        comment
                                    </span> 
                                    on your post 
                                </span>
                                <span class="post_data text-info clickable" 
                                    @click="routes.push({name: 'journal_detail', params: { post_id:  notification?.data?.post?.id }})">
                                    #{{notification?.data?.post?.id}} - {{notification.data?.post?.title.length > 100 ? notification.data?.post?.title.slice(0, 100) + '...' : notification.data?.post?.title}}
                                </span>
                            </span>
                            
                            <span v-else-if="notification.notification_type == 'post_reaction'">
                                <span> 
                                    left a
                                    <span :style="notification?.data?.reaction_type == 'like' ? 'color: green;' : 'color: red;'">{{ notification?.data?.reaction_type }}</span> 
                                    to your post
                                </span>
                                <span class="comment_data text-info font-italic clickable" 
                                    @click="routes.push({name: 'journal_detail', params: { post_id:  notification?.data?.post?.id }})">
                                    #{{notification?.data?.post?.id}} - {{notification.data?.post?.title.length > 100 ? notification.data?.post?.title.slice(0, 100) + '...' : notification.data?.post?.title}}
                                </span>
                            </span>

                            <span v-else-if="notification.notification_type == 'comment_reply'">
                                <span> left a
                                    <span class="text-info clickable"
                                        @click="goToComment(notification?.data?.id, notification?.data?.post)">
                                        reply
                                    </span> 
                                    to your comment </span>
                                <span class="comment_data text-info font-italic clickable" 
                                    @click="goToComment(notification?.data?.parent?.id, notification?.data?.post)">
                                    {{notification?.data?.parent?.text.length > 100 ? notification?.data?.parent?.text.slice(0, 100) + '...' : notification?.data?.parent?.text}}
                                </span>
                            </span>

                            <span v-else-if="notification.notification_type == 'comment_reaction'">
                                <span> 
                                    left a
                                    <span :style="notification?.data?.reaction_type == 'like' ? 'color: green;' : 'color: red;'">{{ notification?.data?.reaction_type }}</span> 
                                    to your comment
                                </span>
                                <span class="comment_data text-info font-italic clickable" 
                                    @click="goToComment(notification?.data?.comment?.id, notification?.data?.comment?.post)">
                                    {{notification?.data?.comment?.text.length > 100 ? notification?.data?.comment?.text.slice(0, 100) + '...' : notification?.data?.comment?.text}}
                                </span>
                            </span>

                            <span v-else-if="notification.notification_type == 'subscribe'">
                                <span> subscribed to you</span>
                            </span>
                        </div>
                        <div class="notification_datetime text-subtitle-2 text-high-emphasis font-weight-light">{{ DateTimeFormat(notification?.data?.created_datetime) }}</div>
                    </div>
                </div>
                <v-divider class="pb-2"></v-divider>
            </div>
           

            <v-card-action class="d-flex flex-row align-center justify-center w-100 mb-2">
                <v-btn class="show_all_notifications w-100" variant="text" @click="console.log('show_all')">Show all</v-btn>
            </v-card-action>
        </v-card>
    </v-menu>
        
</template>

<script setup>
import { ref, computed, onBeforeMount, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex';
import axios from 'axios';
import {DateTimeFormat} from '@/helpers'
import routes from '@/router/router' 

const store = useStore();
const websocket = ref(null);

const current_page = ref(1)
const page_count = ref(1)
const page_size = 10
let page_url = ref(`?page=1&page_size=${page_size}`)

let notifications_count = ref(0)
const notificationsList = computed(() => {return store.getters['accounts/getNotificationsList']});

const LoadNewPost = async() =>{
    try{
        await store.dispatch('journal/getPostFeedList', {'paginate_url': `feed/?page=1&page_size=${new_posts_count.value}`, 'request_type': 'load_more'})  
        notifications_count.value = 0
    }
    catch(error){console.log(error)}
 
    window.scrollTo({top: 0,behavior: "smooth"});
}

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
                store.commit('accounts/addNotifiactionInStore', data.data)
            }
        }

    }
})

onBeforeUnmount(() => {
    if (websocket.value && websocket.value.readyState === WebSocket.OPEN) {websocket.value.close();}
})

const goToComment = (comment_id, post_id) => {
    store.commit('comments/setScrollToCommentState', true)
    store.commit('comments/setScrollToCommentId', comment_id)
    routes.push({name: 'journal_detail', params: { post_id:  post_id }})
}



</script>

<style lang="scss" scoped>
.clickable{
    &:hover{
        cursor: pointer;
        text-decoration: underline;
    }
}
</style>