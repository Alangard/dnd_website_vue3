
<template>
  <v-card class="comment_container mt-4 pa-4">
    <v-card-title class="d-flex flex-row align-center pl-0 text-h6">Comments 
      <span class="text-h6 font-weight-light pl-2"> {{ comments.num_comments }}</span>
    </v-card-title>

    <v-card-subtitle class="pl-0 mb-2" v-if="!loggedIn">
      <span class="text-info font-weight-bold" style="cursor: pointer" @click="routes.push({ name: 'login'})">Log In</span>
      to leave comments
    </v-card-subtitle>

    <v-textarea
        variant="solo"
        label="Comment"
        clearable
        clear-icon="mdi-close-circle"
        rows="2"
        no-resize
        hide-details
        auto-grow
        v-model="newTextComment"
      >


      <template v-slot:append-inner>
            <v-menu :close-on-content-click="false"  location="start">
              <template v-slot:activator="{ props }">  
                <v-icon v-if="width >= 600" class="clickable" medium v-bind="props">mdi-emoticon</v-icon>
              </template>

              <v-card width="300">
                <EmojiContent></EmojiContent>
              </v-card>
            </v-menu>

            <v-icon v-if="width < 600" class="clickable" medium @click="mobileEmoticonDrawer = !mobileEmoticonDrawer">mdi-emoticon</v-icon>
            <v-icon class="clickable" medium @click="sendMessage">mdi-send</v-icon>
      </template>
    </v-textarea>

    <v-divider :thickness="2" class="mt-5"></v-divider>

    <v-chip-group v-model="selectedCommentOrder" @update:modelValue="onOrderChange" selected-class="text-primary" class="my-2" >
      <v-chip value="popularity">By popularity</v-chip>
      <v-chip value="date">By date</v-chip>
    </v-chip-group>

    <Comment 
      class='comment_element' 
      style=" min-width: 300px;" 
      v-for="comment in comments.comments" :key="comment.id" 
      :comment="comment" 
      :websocket="websocket"
      />
  </v-card>

  <v-navigation-drawer v-if="width < 600" class="mobile_emoticon h-50" v-model="mobileEmoticonDrawer" location="bottom" temporary>
    <v-card class="h-100">
      <EmojiContent></EmojiContent>
    </v-card>
  </v-navigation-drawer>


  

</template>












<script setup>
import { ref, onMounted, onUnmounted, computed, watchEffect } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import routes from '@/router/router'
import {useDisplay} from 'vuetify'
import interceptorsInstance, {authHeader} from '@/api/main'


import Comment from './Comment.vue'
import EmojiBlock from '../Emoji/EmojiBlock.vue';
import EmojiContent from '../Emoji/EmojiContent.vue';

const store = useStore();
const { width } = useDisplay();

const url = `ws://${axios.defaults.baseURL.split('http://')[1]}ws/comment_socket-server/`
const websocket = new WebSocket(url)

const loggedIn = computed(() => {return store.getters['auth/loginState']})
const comments = computed(() => {return store.getters['journal/getComments']})


// Блок ввода нового комментария
const newTextComment = ref('')
const selectedCommentOrder = ref('popularity')
const mobileEmoticonDrawer = ref(false)

const sendMessage = () => {
  console.log(`send:${newTextComment.value}`)
};

const renderedText = computed(() => {
  return newTextComment.value.replace(
        /(\[link\])\((.*?)\)/g,
        '<a href="$2">$2</a>'
      );
})

const onOrderChange = async () => {
  console.log(`New parametr: ${selectedCommentOrder.value}`)
};


onUnmounted(() => {
  websocket.close()
})


onMounted(() => {
  const post_id = routes.currentRoute.value.params.id
  store.dispatch("journal/getPostsComments", post_id)
})




</script>

<style lang='scss' scoped> 

.clickable:first-child{
  margin-right: 14px;
  margin-left: 10px;
  &:hover{
    cursor: pointer;
  }
}

</style>



