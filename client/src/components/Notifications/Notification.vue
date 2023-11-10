<template>
    
    <div class="notification_container d-flex flex-row align-start justify-space-between my-1 mx-2">
        <div class="d-flex flex-row justify-start mr-2">
            <div class="avatar">
                <v-avatar class="avatar mr-2" style="cursor:pointer" size="32">
                    <v-img 
                        v-if="prop?.notification?.data?.author?.avatar != null" 
                        :src="prop.notification?.data?.author?.avatar " 
                        :alt="prop?.notification?.data?.author?.username">
                    </v-img>
                    <v-icon icon="mdi-account-circle" size='x-large' v-else></v-icon>
                </v-avatar>
            </div>
            <div class="notification_text">
                <div class="text">

                    <span class="username text-info clickable"
                        @click="routes.push({name: 'user_profile', params: { username:  prop?.notification?.data?.author?.username }})">
                        @{{ prop?.notification?.data?.author?.username }}
                    </span>
                    
                    <span class='text-high-emphasis font-weight-light' v-if="prop?.notification.notification_type == 'post_comment'">
                        <span> left a 
                            <span class="text-info clickable" @click="goToComment(prop?.notification?.data?.id, prop?.notification?.data?.post?.id)">
                                comment
                            </span> 
                            on your post 
                        </span>
                        <span class="post_data text-info clickable" 
                            @click="routes.push({name: 'journal_detail', params: { post_id:  prop?.notification?.data?.post?.id }})">
                            #{{prop?.notification?.data?.post?.id}} - {{prop?.notification.data?.post?.title.length > 100 ? prop?.notification.data?.post?.title.slice(0, 100) + '...' : prop?.notification.data?.post?.title}}
                        </span>
                        <div class="notification_datetime text-subtitle-2 text-high-emphasis font-weight-light">{{ DateTimeFormat(prop?.notification?.data?.created_datetime) }}</div>
                    </span>
                    
                    <span class='text-high-emphasis font-weight-light'  v-else-if="prop?.notification.notification_type == 'post_reaction'">
                        <span> 
                            left a
                            <span :style="prop?.notification?.data?.reaction_type == 'like' ? 'color: green;' : 'color: red;'">{{ prop?.notification?.data?.reaction_type }}</span> 
                            to your post
                        </span>
                        <span class="comment_data text-info font-italic clickable" 
                            @click="routes.push({name: 'journal_detail', params: { post_id:  prop?.notification?.data?.post?.id }})">
                            #{{prop?.notification?.data?.post?.id}} - {{prop?.notification.data?.post?.title.length > 100 ? prop?.notification.data?.post?.title.slice(0, 100) + '...' : prop?.notification.data?.post?.title}}
                        </span>
                        <div class="notification_datetime text-subtitle-2 text-high-emphasis font-weight-light">{{ DateTimeFormat(prop?.notification?.data?.created_datetime) }}</div>
                    </span>

                    <span class='text-high-emphasis font-weight-light'  v-else-if="prop?.notification.notification_type == 'comment_reply'">
                        <span> left a
                            <span class="text-info clickable"
                                @click="goToComment(prop?.notification?.data?.id, prop?.notification?.data?.post)">
                                reply
                            </span> 
                            to your 
                        </span>

                        <span class="text-info font-italic clickable"
                            @click="goToComment(prop?.notification?.data?.parent?.id, prop?.notification?.data?.post)">
                            comment
                        </span>

                        <div class="notification_datetime text-subtitle-2 text-high-emphasis font-weight-light">{{ DateTimeFormat(prop?.notification?.data?.created_datetime) }}</div>

                        <v-textarea class="comment_data font-italic ml-3 py-2"
                            :model-value="prop?.notification?.data?.parent?.text.length > 100 ? '“'+prop?.notification?.data?.parent?.text.slice(0, 100) + '...”' : '“'+prop?.notification?.data?.parent?.text+'”'"
                            variant="solo"
                            readonly
                            hide-details
                            auto-grow
                            rows="1">
                        </v-textarea>
                    </span>

                    <span class='text-high-emphasis font-weight-light'  v-else-if="prop?.notification.notification_type == 'comment_reaction'">
                        <span> 
                            left a
                            <span :style="prop?.notification?.data?.reaction_type == 'like' ? 'color: green;' : 'color: red;'">{{ prop?.notification?.data?.reaction_type }}</span> 
                            to your 
                            <span class="text-info font-italic clickable"
                                @click="goToComment(prop?.notification?.data?.comment?.id, prop?.notification?.data?.comment?.post)">
                                comment
                            </span> 
                        </span>

                        <div class="notification_datetime text-subtitle-2 text-high-emphasis font-weight-light">{{ DateTimeFormat(prop?.notification?.data?.created_datetime) }}</div>

                        <v-textarea class="comment_data font-italic ml-3 py-2"
                            :model-value="prop?.notification?.data?.comment?.text.length > 100 ? '“'+prop?.notification?.data?.comment?.text.slice(0, 100) + '...”' : '“'+prop?.notification?.data?.comment?.text+'”'"
                            variant="solo"
                            readonly
                            hide-details
                            auto-grow
                            rows="1">
                        </v-textarea>

                    </span>

                    <span class='text-high-emphasis font-weight-light'  v-else-if="prop?.notification.notification_type == 'subscribe'">
                        <span> subscribed to you</span>
                        <div class="notification_datetime text-subtitle-2 text-high-emphasis font-weight-light">{{ DateTimeFormat(prop?.notification?.data?.created_datetime) }}</div>
                    </span>
                
                </div>
            </div>
        </div>

        <v-checkbox-btn class="seen_checkbox"
            style="flex: 0 0;"
            v-model="prop.notification.seen"
            @change="seenNotification(prop.notification.notification_id, prop.notification.seen)"
            :hide-details="false"
            density="compat" 
            true-icon="mdi-eye" 
            false-icon="mdi-eye-off">
        </v-checkbox-btn>
    </div>
</template>

<script setup>
import { ref, defineProps} from 'vue'
import routes from '@/router/router'
import {DateTimeFormat} from '@/helpers' 

const prop = defineProps(['notification'])

const goToComment = (comment_id, post_id) => {
    store.commit('comments/setScrollToCommentState', true)
    store.commit('comments/setScrollToCommentId', comment_id)
    routes.push({name: 'journal_detail', params: { post_id:  post_id }})
}

const seenNotification = (notification_id, notification_state) => {
    console.log(notification_id, notification_state)
}
</script>


<style lang="scss" scoped>
.clickable{
    &:hover{
        cursor: pointer !important;
        text-decoration: underline;
    }
}
</style>