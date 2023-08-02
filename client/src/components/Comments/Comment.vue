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
          <v-btn v-if="comment.status != 'd'" class="pb-1" variant="text">
            Reply
          </v-btn>

          <v-btn class="pb-1" variant="text" @click="deleteComment(comment.id)">
            Delete
          </v-btn>

          <div class="reactions_container px-3">
            <div class="d-flex flex-row align-center">
              <v-btn
                  :disabled="comment.status == 'd'"
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
                  :disabled="comment.status == 'd'"
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

    <div class="ml-5">
      <Comment v-for="reply in comment.replies" :key="reply.id" :comment="reply" />
    </div>
  </div>
</template>
  
<script setup>
import { ref, defineProps, onMounted, onUnmounted } from 'vue';
import routes from '@/router/router'
import { useStore } from 'vuex'
import {DateTimeFormat} from '@/helpers'

const props = defineProps(['comment'])
const store = useStore();
const comment = ref(props.comment);


onMounted(() => {
  // DateTimeFormat(comment.created_datetime);
  // const DateFormat = setInterval(updateTime, 5000);
})

onUnmounted(() => {
  // clearInterval(DateFormat);
})

const ratingPercentage = (comment_reactions_obj) => {
    let totalVotes = comment_reactions_obj.num_likes + comment_reactions_obj.num_dislikes;
    if (totalVotes === 0) {return 0; }
    const rating = (comment_reactions_obj.num_likes / totalVotes) * 100;
    return Math.round(rating);
}

const deleteComment = (comment_id) => {
  store.dispatch("journal/deleteComment", comment_id)
}




</script>

<style lang="scss" scoped>
  .clickable{
      &:hover{cursor: pointer;}
  }

  .transformable{
      &:hover{transform: scale(1.1);}
  }

</style>