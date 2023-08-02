
<template>
  <v-card class="comment_container mt-4 pa-4">
    <v-card-title class="pl-0" @click="deleteCommentWithReplies">Comments {{ comments.num_comments }}</v-card-title>
    <v-card-subtitle class="pl-0 mb-2" v-if="!loggedIn">
      <span class="text-info font-weight-bold" style="cursor: pointer" @click="routes.push({ name: 'login'})">Log In</span>
      to leave comments
    </v-card-subtitle>
    <Comment class='comment_element' style="  min-width: 300px;" v-for="comment in comments.comments" :key="comment.id" :comment="comment" />
  </v-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import routes from '@/router/router'
import interceptorsInstance, {authHeader} from '@/api/main'

import Comment from './Comment.vue'

const store = useStore();

const url = `ws://${axios.defaults.baseURL.split('http://')[1]}ws/comment_socket-server/`
const socket = new WebSocket(url)

const loggedIn = computed(() => {return store.getters['auth/loginState']})
const comments = computed(() => {return store.getters['journal/getComments']})

const createComment =() => {
  const payload = {
    text: 'test comment',
    post: 1,
  }
  store.dispatch('journal/createComment', {'socket': socket, 'payload': payload})
}

const createCommentReply =() => {
  const payload = {
    text: 'reply to test comment id = 3',
    parent: 1,
    post: 1,
  }

  store.dispatch('journal/createCommentReply', {'socket': socket, 'payload': payload})
}

const deleteCommentWithReplies =() => {
  const payload = {
    id: 62,
    author:{
      avatar:"",
      id:1,
      username:"admin",
    }
  }
  store.dispatch('journal/deleteCommentWithReplies', {'socket': socket, 'payload': payload})
}





onMounted(() => {
  const post_id = routes.currentRoute.value.params.id
  store.dispatch("journal/getPostsComments", post_id)

  socket.onmessage = function(e){
        let data = JSON.parse(e.data)

        switch (data.action){
          case 'create':
            store.commit('journal/addCommentInStore', data.data)
          case 'create_reply':
            store.commit('journal/addCommentReplyInStore', data.data)
          case 'delete_with_replies':
            store.commit('journal/deleteCommentWithRepliesInStore', data.data)
          case 'delete':
            store.commit('journal/deleteCommentInStore', data.data)
          case 'partial_update':
            store.commit('journal/partialUpdateCommentInStore', data.data)
          case 'get_list':
            store.commit('journal/getListCommentInStore', data.data)

        }




        // if(data.action === 'list'){
        //     store.commit('journal/setPostsList', data.data)
            
        //     // postsList.value = data.data
        // }
        // else if(data.action === 'create'){
        //     store.commit('journal/updatePostsList', data.data)
        //     // postsList.value.unshift(data.data)
        //     console.log(data.data)
        // }
  }
})

onUnmounted(() => {
    clearInterval(interval);
    socket.close()
})


</script>

<style lang='scss' scoped> 
</style>



