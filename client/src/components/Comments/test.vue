<template>
    <v-app>
      <v-main>
        <v-container>
          <h1>Комментарии</h1>
          <v-card>
            <v-card-text>
              <form @submit.prevent="addComment">
                <v-text-field v-model="comment.author" label="Автор" required></v-text-field>
                <v-textarea v-model="comment.text" label="Комментарий" required></v-textarea>
                <v-btn type="submit" color="primary">Добавить комментарий</v-btn>
              </form>
            </v-card-text>
          </v-card>
          <div v-for="comment in comments" :key="comment.id">
            <v-card>
              <v-card-title>
                <span>{{ comment.author }}</span>
              </v-card-title>
              <v-card-text>
                <p>{{ comment.text }}</p>
                <v-btn @click="addReply(comment)">Ответить</v-btn>
                <v-card v-for="reply in comment.replies" :key="reply.id">
                  <v-card-title>
                    <span>{{ reply.author }}</span>
                  </v-card-title>
                  <v-card-text>
                    <p>{{ reply.text }}</p>
                  </v-card-text>
                </v-card>
              </v-card-text>
            </v-card>
          </div>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { v4 as uuidv4 } from 'uuid';
  
  const comment = ref({
    author: '',
    text: '',
    replies: [],
  });
  
  const comments = ref([]);
  
  const addComment = () => {
    const newComment = { ...comment.value, id: uuidv4() };
    comments.value.push(newComment);
    comment.value = { author: '', text: '', replies: [] };
  };
  
  const addReply = (parentComment) => {
    const newReply = { ...comment.value, id: uuidv4() };
    parentComment.replies.push(newReply);
    comment.value = { author: '', text: '', replies: [] };
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>