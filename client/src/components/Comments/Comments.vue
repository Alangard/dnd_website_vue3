
<template>
  <v-card class="comment_container mt-4 pa-4">
    <v-card-title class="pl-0" @click="test">Comments {{ comments.num_comments }}</v-card-title>
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

// const token = authHeader()['Authorization'].split('Bearer ')[1]
let url = `ws://${axios.defaults.baseURL.split('http://')[1]}ws/comment_socket-server/`
const socket = new WebSocket(url)

const loggedIn = computed(() => {return store.getters['auth/loginState']})
const comments = computed(() => {return store.getters['journal/getComments']})

const test = () => {

  store.dispatch('auth/verifyToken').then(response => {
    socket.send(JSON.stringify(message))
  }).catch(error => {
    store.dispatch('auth/refreshToken').then(response => {
      socket.send(JSON.stringify(message))
    }).catch(error => {console.log('get refresh error in a component')})
  })

  // try{
  //   store.dispatch('auth/verifyToken')
  // }
  // catch (err){
  //   console.log('get error')
  // }


  const message =   {
    request_id: Date.now(),
    action: 'create_comment',
    token: authHeader()['Authorization'].split('Bearer ')[1],
    payload: {
      text: 'suck pinus',
      post: 1,
    }
  }

  // socket.send(JSON.stringify(message))
  
}

onMounted(() => {
  const post_id = routes.currentRoute.value.params.id
  store.dispatch("journal/getPostsComments", post_id)

  socket.onmessage = function(e){
        // let data = JSON.parse(e.data)
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
    socket.close()
})


</script>

<style lang='scss' scoped> 
</style>



