
<template>
  <v-card class="comment_container mt-4 px-4" ref="comments_container">
    <v-card-title class="d-flex flex-row align-center pl-0 text-h6">Comments 
      <span class="text-h6 font-weight-light pl-2">({{ comments?.num_comments }})</span>
    </v-card-title>

    <v-card-subtitle class="pl-0 my-2" v-if="!loggedIn">
      <span class="text-info font-weight-bold" style="cursor: pointer" @click="routes.push({ name: 'login'})">Log In</span>
      to leave comments
    </v-card-subtitle>

    <v-card-title class="pl-0 my-2" v-if="comments?.allow_comments == false">
      <span class="text-info font-weight-bold" style="white-space: normal;">Creating comments have been blocked by the author of the post</span>
    </v-card-title >

    <v-textarea class="new_comment_text"
      v-if="loggedIn && comments?.allow_comments"
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
                <v-icon v-if="width >= mobileWidthLimit" class="clickable" medium v-bind="props">mdi-emoticon</v-icon>
              </template>

              <v-card width="300">
                <EmojiContent></EmojiContent>
              </v-card>
            </v-menu>

            <v-icon v-if="width < mobileWidthLimit" class="clickable" medium @click="mobileEmoticonDrawer = !mobileEmoticonDrawer">mdi-emoticon</v-icon>
            <v-icon class="clickable" medium @click="saveNewComment">mdi-send</v-icon>
      </template>
    </v-textarea>

    <v-divider :thickness="2" class="mt-5"></v-divider>

    <v-chip-group v-model="selectedCommentOrder" @update:modelValue="onOrderChange" selected-class="text-primary" class="my-2" >
      <v-chip value="popularity">By popularity</v-chip>
      <v-chip value="date">By date</v-chip>
    </v-chip-group>

    <Comment 
      class='comment_element'
      :class="{componentIsSticky: 'sticky'}" 
      style=" min-width: 300px;" 
      v-for="comment in comments?.comments" :key="comment.id" 
      :comment="comment" 
      :websocket="websocket"
      />

      <div class="pagination text-center">
        <v-pagination
            v-model="current_page"
            @update:model-value="handlePageChange"
            :length="page_count"
            :total-visible="7"
            size="small"
        ></v-pagination>
    </div>
  </v-card>

  <v-navigation-drawer v-if="width < mobileWidthLimit" class="mobile_emoticon h-50" v-model="mobileEmoticonDrawer" location="bottom" temporary>
    <v-card class="h-100">
      <EmojiContent></EmojiContent>
    </v-card>
  </v-navigation-drawer>


  

</template>


<script setup>
import { ref, onUnmounted, onBeforeMount, computed, defineProps } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import routes from '@/router/router'
import {useDisplay} from 'vuetify'

import Comment from './Comment.vue'
import EmojiContent from '../Emoji/EmojiContent.vue';

const store = useStore();
const props = defineProps(['post_id'])
const { width } = useDisplay();

const url = `ws://${axios.defaults.baseURL.split('http://')[1]}ws/comment_socket-server/`
const websocket = new WebSocket(url)

const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})
const loggedIn = computed(() => {return store.getters['auth/loginState']})
const comments = computed(() => {return store.getters['comments/getComments']})

const current_page = ref(1)
const page_count = ref(1)
const page_size = 10
let page_url = ref(`?post_id=${props.post_id}&page=1&page_size=${page_size}`)
let filters = ref([])
let orderings = ref('')

const newTextComment = ref('')
const selectedCommentOrder = ref('date')
const mobileEmoticonDrawer = ref(false)


const onOrderChange = async () => {
  const order_param = selectedCommentOrder.value
  const page_url_params_list = page_url.value.slice(1).split('&')
  const index_in_url = page_url_params_list.findIndex(item => item.includes("ordering="));

  if(index_in_url != -1){page_url_params_list.splice(index_in_url, 1, `ordering=${order_param}`)}
  else{page_url_params_list.push(`ordering=${order_param}`)}
  orderings.value = order_param

  page_url.value = '?' + page_url_params_list.join('&')
  page_count.value = Math.ceil((await store.dispatch('comments/getCommentsList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count / page_size)
};

const handlePageChange = async(newPage) => {
    current_page.value = newPage
    page_url.value = `?post_id=${props.post_id}&page=${newPage}&page_size=${page_size}` + `&${filters.value}`
    await store.dispatch('comments/getCommentsList', {'paginate_url': page_url.value, 'request_type': 'initial'})
}

const saveNewComment = async() => {
  await store.dispatch('comments/createComment', {'post_id': props.post_id, 'text': newTextComment.value})
  newTextComment.value = ''
};


onBeforeMount(async() => {
  page_count.value = Math.ceil((await store.dispatch('comments/getCommentsList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count / page_size)
})

onUnmounted(() => {
  websocket.close()
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

.sticky {
  position: fixed;
  top: 0;
}

</style>



