<template>
  <div>
    <v-card class="mb-3" width="100%" v-if="!commentIsEdit">
      <div class="title pb-0 pr-1 pl-3">
        <div class="d-flex flex-row justify-space-between align-center">
          <div class="avatar_username_container d-flex flex-row">
            <v-avatar class="clickable transformable avatar" size="41"
                @click="routes.push({name: 'user_profile', params: { username: comment.author.username }})">
                <v-img v-if="comment.author.avatar !== null"
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

          <v-menu location="start">
              <template v-slot:activator="{ props }">  
                <v-btn v-if="width >= mobileWidthLimit" icon="mdi-dots-vertical" variant="text" v-bind="props"></v-btn>
              </template>
              <v-card>
                <ComentFuncMenuContent 
                  @comment-action="(action) => commentAdditionalActionManager(action)">
                </ComentFuncMenuContent>
              </v-card>
          </v-menu>

          <v-btn v-if="width < mobileWidthLimit" icon="mdi-dots-vertical" variant="text" @click="mobileAdditionalActionsDrawer = !mobileAdditionalActionsDrawer"></v-btn>
          
        </div>

      </div>

      <v-card-text class="text-subtitle-1 pt-2 pb-2">
        <div>
          <span class="user_link text-info clickable" v-if="comment?.parent" 
            @click="routes.push({name: 'user_profile', params: { username:comment?.parent?.author?.username}})">
              {{`@${comment?.parent?.author?.username}, `}}
          </span>
          <span v-if="comment.status == 'n'">{{comment.text}}</span>
          <span v-else class="text-info">*{{comment.text}}*</span>
        </div>   
      </v-card-text>
      <v-card-actions>
        <div class="d-flex flex-row justify-space-between w-100">
          <v-btn v-if="comment.status == 'n'" class="pb-1" variant="text" :disabled="!loggedIn" @click="replyPressed">
            Reply
          </v-btn>

          <div class="reactions_container px-3">
            <div class="d-flex flex-row align-center">
              <v-btn
                  :disabled="comment.status == 'd' || comment.status == 'b' || !loggedIn"
                  class="mx-0" 
                  size="24"
                  :id="`post_${comment.post}_comment_${comment.id}_like_btn`" 
                  @click="pressReaction({'reaction_type': 'like', 'user_reaction': comment.user_reaction, 'comment_id': comment.id})">
                      <v-icon 
                        size="24" 
                        class="like"  
                        :class="{ 'text-info': comment.user_reaction.reaction_type == 'like' }" >
                        mdi-arrow-up-bold-circle-outline
                    </v-icon>
              </v-btn>

              <span class="mx-3" :class="{ 'text-info': comment.user_reaction.reacted}">{{ comment.comment_reactions.total_reactions }}</span>

              <v-btn
                  :disabled="comment.status == 'd' || comment.status == 'b' || !loggedIn"
                  class="mx-0"
                  size="24"
                  :id="`post_${comment.post}_comment_${comment.id}_dislike_btn`"
                  @click="pressReaction({'reaction_type': 'dislike', 'user_reaction': comment.user_reaction, 'comment_id': comment.id})">
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

      <v-container v-if="commentIsEdit" class="edit_comment_container d-flex flex-row align-center pa-0 mb-3"  >
        
        <v-icon class="clickable_relpy mx-2" medium @click="commentIsEdit = !commentIsEdit">mdi-cancel</v-icon>

        <v-textarea
          variant="solo"
          :label="`Edit Reply for @${comment.author.username}`"
          clear-icon="mdi-close-circle"
          rows="2"
          hide-details
          no-resize
          auto-grow
          v-model="commentEditText">

          <template v-slot:append-inner>

            <v-menu :close-on-content-click="false"  location="start">
              <template v-slot:activator="{ props }">  
                <v-icon v-if="width >= mobileWidthLimit" class="clickable_relpy" medium v-bind="props">mdi-emoticon</v-icon>
              </template>
              <v-card width="300">
                <EmojiContent></EmojiContent>
              </v-card>
            </v-menu>


            <v-icon v-if="width < mobileWidthLimit" class="clickable_relpy" medium @click="mobileEmoticonDrawer = !mobileEmoticonDrawer">mdi-emoticon</v-icon>
            <v-icon class="clickable_relpy" medium @click="updateComment()">mdi-send</v-icon>
          </template>
        </v-textarea>
      </v-container>



    <!-- Reply insert text -->
    <v-container v-if="replyIsPressed == comment.id" class="reply_comment_container d-flex flex-row align-center pa-0 mb-3">
      
        <v-icon class="clickable_relpy mx-2" medium @click="closeReply()">mdi-cancel</v-icon>

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
                <v-icon v-if="width >= mobileWidthLimit" class="clickable_relpy" medium v-bind="props">mdi-emoticon</v-icon>
              </template>
              <v-card width="300">
                <EmojiContent></EmojiContent>
              </v-card>
            </v-menu>


            <v-icon v-if="width < mobileWidthLimit" class="clickable_relpy" medium @click="mobileEmoticonDrawer = !mobileEmoticonDrawer">mdi-emoticon</v-icon>
            <v-icon class="clickable_relpy" medium @click="createReply">mdi-send</v-icon>
          </template>
        </v-textarea>
    </v-container>

    <!-- Show all replies -->
    <v-expansion-panels v-if="comment?.replies?.length >= numberOfVisibleReplies" class="mb-3">
      <v-expansion-panel elevation="0" class="pa-0">
        <v-expansion-panel-title expand-icon="mdi-plus" collapse-icon="mdi-minus">Other replies ({{ countOfReplies(comment)}})</v-expansion-panel-title>
        <v-expansion-panel-text class="pt-2 pl-5 pr-0">
          <Comment v-for="reply in comment.replies" :key="reply.id" :comment="reply" :websocket="websocket"/>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
    
    <!-- Replies objects -->
    <div class="ml-5" v-if="comment?.replies?.length < numberOfVisibleReplies ">
      <Comment v-for="reply in comment.replies" :key="reply.id" :comment="reply" :websocket="websocket"/>
    </div>
  </div>


<!-- Popovers -->
  <v-navigation-drawer v-if="width < mobileWidthLimit" class="mobile_emoticon h-50" v-model="mobileEmoticonDrawer" location="bottom" temporary>
    <v-card class="h-100">
      <EmojiContent></EmojiContent>
    </v-card>
  </v-navigation-drawer>

  <v-navigation-drawer v-if="width < mobileWidthLimit" class="mobile_comment_additional-action h-auto" v-model="mobileAdditionalActionsDrawer" location="bottom" temporary>
    <v-card class="h-100">
      <ComentFuncMenuContent 
        @comment-action="(action) => commentAdditionalActionManager(action)">
      </ComentFuncMenuContent>
    </v-card>
  </v-navigation-drawer>

  <v-dialog v-model="deleteCommentDialog" width="auto" transition="dialog-bottom-transition">
    <v-card>
        <v-card-title class="text-h5"  style="white-space: normal; overflow: hidden;">Do you really want to delete this comment?</v-card-title>
        <v-card-text class="px-4">After confirming the action, this comment will be deleted if it has no replies, otherwise, the comment will be marked as "deleted"</v-card-text>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="outlined" prepend-icon="mdi-cancel" @click="deleteCommentDialog = false" >Cancel</v-btn>
            <v-btn variant="outlined" prepend-icon="mdi-delete-outline" color="error" @click="deleteComment()">Delete</v-btn>
        </v-card-actions>
    </v-card>
  </v-dialog>



</template>
  
<script setup>
import { ref, defineProps, onMounted, onUnmounted, computed } from 'vue';
import routes from '@/router/router'
import { useStore } from 'vuex'
import {useDisplay} from 'vuetify'
import {DateTimeFormat} from '@/helpers'

import EmojiContent from '../Emoji/EmojiContent.vue';
import ComentFuncMenuContent from './ComentFuncMenuContent.vue';

const props = defineProps(['comment', 'websocket'])
const emit = defineEmits(['replyIsPressed'])
const store = useStore();
const { width } = useDisplay();

const loggedIn = computed(() => {return store.getters['auth/loginState']}) 
const replyIsPressed = computed(() => {return store.getters['comments/getReplyIsPressed']})
const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})

const comment = ref(props.comment);
const websocket = ref(props.websocket);

const replyTextComment = ref('')
let commentIsEdit = ref(false)
let commentEditText = ref(comment.value.text)
let mobileEmoticonDrawer = ref(false)
let mobileAdditionalActionsDrawer = ref(false)
let deleteCommentDialog = ref(false)
const numberOfVisibleReplies = 2


onMounted(async() => {

  // (await store.dispatch('comments/getCommentsList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count / page_size)

})


const ratingPercentage = (comment_reactions_obj) => {
    let totalVotes = comment_reactions_obj.num_likes + comment_reactions_obj.num_dislikes;
    if (totalVotes === 0) {return 0; }
    const rating = (comment_reactions_obj.num_likes / totalVotes) * 100;
    return Math.round(rating);
}


const pressReaction = (data) => {

  store.dispatch('comments/set_reaction', 
        {
            'comment_id': data.comment_id,
            'reaction_type': data.reaction_type,
            'id': data.user_reaction.id,
            'user_reaction': data.user_reaction,
        }
  )   
}

const commentAdditionalActionManager = (action) => {
  switch(action){
    case 'edit':
      commentIsEdit.value = true
      break
    case 'delete':
      deleteCommentDialog.value = true
      break
    
  }


  mobileAdditionalActionsDrawer.value = false
}


const replyPressed = () => {
  store.commit('comments/openReply', comment.value.id)
}

const closeReply = () => {
  store.commit('comments/openReply', comment.value.id)
}

const createReply = async() => {
  const payload = {
    text: replyTextComment.value,
    parent: comment.value.id,
    post_id: comment.value.post,
  }
  await store.dispatch('comments/createReplyComment', payload)
  closeReply()
};

const deleteComment = () => {
  store.dispatch('comments/deleteComment', comment.value.id)
  deleteCommentDialog.value = false;
}

const updateComment = () => {
  const payload = {
    comment_id: comment.value.id,
    new_comment_text: commentEditText.value,
  }
  store.dispatch('comments/partialUpdateComment', payload)
  commentIsEdit.value = false
}

const countOfReplies = (comment) => {
  let count = 0;
  
  if (comment.replies) {
    count += comment.replies.length;
    
    comment.replies.forEach((reply) => {
      count += countOfReplies(reply);
    });
  }
  
  return count;
};



const updateCommentFunc = () => {
  comment.value.text = commentEditText.value;
  partialUpdateComment(comment.value)
  commentIsEdit.value = false
}







const createComment =(comment_data) => {
  const payload = {
    text: 'test comment',
    post: comment_data.post,
  }
  store.dispatch('comments/createComment', {'socket': websocket.value, 'payload': payload})
}

const createCommentReply =(comment_data) => {
  const payload = {
    text: 'reply to test comment id = 3',
    parent: comment_data.parent,
    post: comment_data.post,
  }

  store.dispatch('comments/createCommentReply', {'socket': websocket.value, 'payload': payload})
}

const deleteCommentWithReplies =(comment_data) => {
  const payload = {
    id: comment_data.id,
    post: comment_data.post,
    author: comment_data.author
  }
  store.dispatch('comments/deleteCommentWithReplies', {'socket': websocket.value, 'payload': payload})
}

// const deleteComment =(comment_data) => {
//   const payload = {
//     id: comment_data.id,
//     post: comment_data.post,
//     author: comment_data.author
//   }
//   store.dispatch('comments/deleteComment', {'socket': websocket.value, 'payload': payload})
// }

const partialUpdateComment =(comment_data) => {
  const payload = {
    id: comment_data.id,
    post: comment_data.post,
    text: comment_data.text,
    author: comment_data.author
  }
  store.dispatch('comments/partialUpdateComment', {'socket': websocket.value, 'payload': payload})
}

const banComment =(comment_data) => {
  const payload = {
    id: comment_data.id,
    post: comment_data.post,
    author: comment_data.author
  }
  store.dispatch('comments/banComment', {'socket': websocket.value, 'payload': payload})
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

::v-deep .v-expansion-panel-text__wrapper {
  padding-right: 0px;
}

</style>