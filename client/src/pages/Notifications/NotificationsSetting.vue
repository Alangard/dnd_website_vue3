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

const tab = ref('option-1')
const notificationSettings = ref(
    {
        'new_follower': {'title': 'New follower', 'text': 'Someone starts following you', 'value': false},
        'new_comment': {'title': 'New comment', 'text': 'Someone wrote comment to your post', 'value': false},
        'new_reply': {'title': 'New reply', 'text': 'Someone wrote a reply to your comment', 'value': false},
        'new__post_reaction': {'title': 'New reaction yo your post', 'text': 'Someone reacts to your post', 'value': false},
        'new__comment_reaction': {'title': 'New reaction on comment', 'text': 'Someone reacts to your comment', 'value': false},
        'new__feed_post': {'title': 'New feed post', 'text': "Someone you're following posted something", 'value': false},
        'new__feed_reaction': {'title': 'New feed reaction', 'text': "Someone you're following left a reaction.", 'value': false},
    }   
)


onBeforeMount(() => {
    if(width.value >= mobileWidthLimit.value){routes.push({name: 'home'})}
})
</script>

<style lang='scss' scoped>
</style>
