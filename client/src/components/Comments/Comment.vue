<template>
  <div>
    <v-card class="mb-3" width="100%">
      <div class="title pb-0 pr-1 pl-3">
        <div class="d-flex flex-row justify-space-between align-center">
          <div class="avatar_username_container d-flex flex-row">
            <v-avatar class="clickable transformable avatar" size="41"
                @click="routes.push({name: 'user_profile', params: { username: comment.author.username }})">
                <v-img v-if="comment.author.avatar != ''"
                    :src="comment.author.avatar"
                    :alt="comment.author.username">
                </v-img>
                <v-icon icon="mdi-account-circle" size="41" v-else></v-icon>
            </v-avatar>
            <div>
              <span class="clickable font-weight-bold text-subtitle-1" style="line-height: 0"
                @click="routes.push({name: 'user_profile', params: { username: comment.author.username }})">
                  {{ comment.author.username }}
              </span>
              <div class="font-weight-light text-subtitle-2">{{ DateTimeFormat(comment.created_datetime) }}</div>
            </div>
          </div>

          <v-btn icon="mdi-dots-vertical" variant="text"></v-btn>
        </div>

      </div>

      <v-card-text class="text-subtitle-1 pt-2 pb-2">
        <div v-if="comment.text.match(/@(\w+),/)">
          <span class="user_link text-info clickable" 
            @click="routes.push({name: 'user_profile', params: { username: comment.text.match(/@(\w+),/)[1] }})">
              {{comment.text.match(/@(\w+),/)[0]}}
          </span>
          <span>
            {{comment.text.split(/@(\w+),/)[2]}}
          </span>
        </div>

        <div v-else>
          {{ comment.text}}
        </div>

      
      </v-card-text>
      <v-card-actions>
        <div class="d-flex flex-row justify-space-between w-100">
          <v-btn v-if="comment.status == 'n'" class="pb-1" variant="text" @click="replyPressed">
            Reply
          </v-btn>

          <v-btn class="pb-1" variant="text">
            Delete
          </v-btn>

          <div class="reactions_container px-3">
            <div class="d-flex flex-row align-center">
              <v-btn
                  :disabled="comment.status == 'd' || comment.status == 'b'"
                  class="mx-0" 
                  size="24"
                  :id="`post_${comment.post}_comment_${comment.id}_like_btn`" 
                  @click="pressReaction({'post_id':comment.post, 'reaction_type': 'like', 'user_reaction': comment.user_reaction})">
                      <v-icon 
                        size="24" 
                        class="like"  
                        :class="{ 'text-info': comment.user_reaction.reaction_type == 'like' }" >
                        mdi-arrow-up-bold-circle-outline
                    </v-icon>
              </v-btn>

              <span class="mx-3" :class="{ 'text-info': comment.user_reaction.reacted}">{{ comment.comment_reactions.total_reactions }}</span>

              <v-btn
                  :disabled="comment.status == 'd' || comment.status == 'b'"
                  class="mx-0"
                  size="24"
                  :id="`post_${comment.post}_comment_${comment.id}_dislike_btn`"
                  @click="pressReaction({'post_id':comment.post, 'reaction_type': 'dislike', 'user_reaction': comment.user_reaction})">
                      <v-icon 
                        size="24" 
                        class="dislike" 
                        :class="{ 'text-info': comment.user_reaction.reaction_type == 'dislike' }">
                        mdi-arrow-down-bold-circle-outline
                    </v-icon>
              </v-btn>
            </div>

        
            <v-progress-linear
                class="mt-1"
                :model-value="ratingPercentage(comment.comment_reactions)"
                color="green"
                bg-color="red"
                bg-opacity="1"
            ></v-progress-linear>
          </div>

        </div>

      </v-card-actions>
    </v-card>

    <v-container v-if="replyIsPressed == comment.id" class="d-flex flex-row align-center pa-0 mb-3">
      
        <v-icon class="clickable_relpy mx-2" medium @click="replyPressed()">mdi-close-circle-outline</v-icon>

        <v-textarea
          variant="solo"
          :label="`Reply for @${comment.author.username}`"
          clear-icon="mdi-close-circle"
          rows="2"
          hide-details
          no-resize
          auto-grow
          v-model="replyTextComment">

          <template v-slot:append-inner>

            <v-menu :close-on-content-click="false"  location="start">
              <template v-slot:activator="{ props }">  
                <v-icon v-if="width >= 600" class="clickable_relpy" medium v-bind="props">mdi-emoticon</v-icon>
              </template>
              <v-card width="300">
                <EmojiContent></EmojiContent>
              </v-card>
            </v-menu>


            <v-icon v-if="width < 600" class="clickable_relpy" medium @click="mobileEmoticonDrawer = !mobileEmoticonDrawer">mdi-emoticon</v-icon>
            <v-icon class="clickable_relpy" medium @click="createReply">mdi-send</v-icon>
          </template>
        </v-textarea>
    </v-container>

    <div class="ml-5">
      <Comment v-for="reply in comment.replies" :key="reply.id" :comment="reply" :websocket="websocket"/>
    </div>
  </div>

  <v-navigation-drawer v-if="width < 600" class="mobile_emoticon h-50" v-model="mobileEmoticonDrawer" location="bottom" temporary>
    <v-card class="h-100">
      <EmojiContent></EmojiContent>
    </v-card>
  </v-navigation-drawer>


  <!-- <v-menu :activator="`#emoticon-activator_${comment.id}`" transition="slide-x-reverse-transition" location="start" :close-on-content-click="false">
    <v-card width="300">
      <v-tabs v-model="emoticonTab" background="primary" fixed-tabs>
        <v-tab value="emoji">Emoji</v-tab>
        <v-tab value="stickers">Stickers</v-tab>
      </v-tabs>

      <v-card-text>
        <v-window class="mt-2" v-model="emoticonTab" color="primary" background="primary">
          <v-window-item value="emoji">
            Elements emoji...
            dasdasdasdasd
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasda
          </v-window-item>

          <v-window-item value="stickers">
            Elements stickers...
            DAsdasdasdasdaddasdasdasdasd
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasdaasdad
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasdaasdaddasd
          </v-window-item>

        </v-window>
      </v-card-text>
    </v-card>
  </v-menu>

  <v-navigation-drawer v-if="width < 600" class="mobile_emoticon h-50" v-model="mobileEmoticonDrawer" location="bottom" temporary>
    <v-card class="h-100">
      <v-tabs v-model="emoticonTab" background="primary" fixed-tabs>
        <v-tab value="emoji">Emoji</v-tab>
        <v-tab value="stickers">Stickers</v-tab>
      </v-tabs>

      <v-card-text>
        <v-window class="mt-2" v-model="emoticonTab" color="primary" background="primary">
          <v-window-item value="emoji">
            Elements emoji...
            dasdasdasdasd
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasda
          </v-window-item>

          <v-window-item value="stickers">
            Elements stickers...
            DAsdasdasdasdaddasdasdasdasd
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasdaasdad
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasdaasdaddasd
          </v-window-item>

        </v-window>
      </v-card-text>
    </v-card>
     
    
  </v-navigation-drawer> -->



</template>
  
<script setup>
import { ref, defineProps, onMounted, onUnmounted, computed } from 'vue';
import routes from '@/router/router'
import { useStore } from 'vuex'
import {useDisplay} from 'vuetify'
import {DateTimeFormat} from '@/helpers'
import EmojiContent from '../Emoji/EmojiContent.vue';

const props = defineProps(['comment', 'websocket'])
const emit = defineEmits(['replyIsPressed'])
const store = useStore();
const { width } = useDisplay();

const comment = ref(props.comment);
const websocket = ref(props.websocket);

const replyTextComment = ref('')
const replyIsPressed = computed(() => {return store.getters['journal/getReplyIsPressed']})
const mobileEmoticonDrawer = ref(false)


onMounted(() => {

  websocket.value.onmessage = function(e){
        let data = JSON.parse(e.data)

        switch (data.action){
          case 'create':
            store.commit('journal/addCommentInStore', data.data)
          case 'create_reply':
            store.commit('journal/addCommentReplyInStore', data.data)
          case 'delete_comment':
            store.commit('journal/deleteCommentInStore', data.data)
          case 'update_comment':
            store.commit('journal/updateCommentInStore', data.data)
        }
  }
})


const ratingPercentage = (comment_reactions_obj) => {
    let totalVotes = comment_reactions_obj.num_likes + comment_reactions_obj.num_dislikes;
    if (totalVotes === 0) {return 0; }
    const rating = (comment_reactions_obj.num_likes / totalVotes) * 100;
    return Math.round(rating);
}


const pressReaction = (data) => {
  
}

const replyPressed = () => {
  store.commit('journal/openReply', comment.value.id)
}

const createReply = () => {
  console.log(`send:${newTextComment.value}`)
};







const createComment =(comment_data) => {
  const payload = {
    text: 'test comment',
    post: comment_data.post,
  }
  store.dispatch('journal/createComment', {'socket': websocket.value, 'payload': payload})
}

const createCommentReply =(comment_data) => {
  const payload = {
    text: 'reply to test comment id = 3',
    parent: comment_data.parent,
    post: comment_data.post,
  }

  store.dispatch('journal/createCommentReply', {'socket': websocket.value, 'payload': payload})
}

const deleteCommentWithReplies =(comment_data) => {
  const payload = {
    id: comment_data.id,
    post: comment_data.post,
    author: comment_data.author
  }
  store.dispatch('journal/deleteCommentWithReplies', {'socket': websocket.value, 'payload': payload})
}

const deleteComment =(comment_data) => {
  const payload = {
    id: comment_data.id,
    post: comment_data.post,
    author: comment_data.author
  }
  store.dispatch('journal/deleteComment', {'socket': websocket.value, 'payload': payload})
}

const partialUpdateComment =(comment_data) => {
  const payload = {
    id: comment_data.id,
    post: comment_data.post,
    text: 'this is a normal test comment text',
    author: comment_data.author
  }
  store.dispatch('journal/partialUpdateComment', {'socket': websocket.value, 'payload': payload})
}

const banComment =(comment_data) => {
  const payload = {
    id: comment_data.id,
    post: comment_data.post,
    author: comment_data.author
  }
  store.dispatch('journal/banComment', {'socket': websocket.value, 'payload': payload})
}



</script>

<style lang="scss" scoped>
  .clickable{
      &:hover{cursor: pointer;}
  }

  .transformable{
      &:hover{transform: scale(1.1);}
  }

  .clickable_relpy:first-child{
  margin-right: 14px;
  margin-left: 10px;
  &:hover{
    cursor: pointer;
  }
}

.no-details ::v-deep .v-messages__wrapper {
  display: none;
}

</style>