
<template>
  <v-card class="comment_container mt-4 pa-4">
    <v-card-title class="pl-0">Comments {{ comments.num_comments }}</v-card-title>
    <v-card-subtitle class="pl-0 mb-2" v-if="!loggedIn">
      <span class="text-info font-weight-bold" style="cursor: pointer" @click="routes.push({ name: 'login'})">Log In</span>
      to leave comments
    </v-card-subtitle>
    <Comment class='comment_element' style="  min-width: 300px;" v-for="comment in comments.comments" :key="comment.id" :comment="comment" />
  </v-card>
</template>

<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import { useStore } from 'vuex';
import routes from '@/router/router'
import Comment from './Comment.vue'

const store = useStore();
const loggedIn = computed(() => {return store.getters['auth/loginState']})
const comments = computed(() => {return store.getters['journal/getComments']})


onBeforeMount(() => {
  const post_id = routes.currentRoute.value.params.id
  store.dispatch("journal/getPostsComments", post_id)
})

</script>

<style lang='scss' scoped> 
</style>



