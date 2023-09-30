<template>
    <div class="main_wrapper">

        <v-card class="post_detail_wrapper">
            <div class="my-2 mx-4 d-flex flex-row justify-start ">
                <div class="author_container mr-2 d-flex flex-row align-center clickable" 
                    @click="routes.push({name: 'user_profile', params: { username: postDetail?.author?.username }})">
                    <v-avatar class="avatar mr-1">
                        <v-img v-if="postDetail?.author?.avatar != null"
                            :src="postDetail?.author?.avatar"
                            :alt="postDetail?.author?.username"
                            cover>
                        </v-img>
                        <v-icon v-if="postDetail?.author?.avatar == null" icon="mdi-account-circle" size="40"></v-icon>
                    </v-avatar> 
                    
                    <span class="username px-1 text-capitalize font-weight-bold text-body-1">
                        {{postDetail?.author?.username}}
                    </span> 
                </div>

                <span class="post_date d-flex flex-row align-center font-weight-regular font-weight-regular text-body-1">
                    Posted {{DateTimeFormat(postDetail?.created_datetime)}}
                </span>
            </div>

            <v-img
                class="bg-white"
                :src="postDetail?.thumbnail"
                max-height="430"
                aspect-ratio="16/9"
                contain>
            </v-img>

            <v-card-title class="title pa-4" style=" white-space: normal; line-height: 1.56rem;">{{postDetail.title}}</v-card-title>    
            <v-card-subtitle class="description text-h6 mb-2" style=" white-space: normal;line-height: 1.56rem;">{{ postDetail.description }}</v-card-subtitle>
            <v-card-text class="body text-body-1 mb-2" >
                <editor-content class="text-editor w-100" :editor="editor"/>
            </v-card-text>

            <div class="tags_container d-flex f-row flex-wrap my-4 mx-4" v-if="postDetail?.tags?.length">
                <v-chip
                    class="tag_element clickable transformable rounded mr-2" size="small"
                    v-for="tag in postDetail?.tags"
                    @click="handleFilterChange(`tags=${tag?.slug}`)">
                    #{{ tag?.name }}
                </v-chip>
            </div>

            <v-divider></v-divider>

            <v-card-actions class="px-4">
                <div class="d-flex flex-row justify-space-between w-100">

                    <div class="reactions_container">
                        <div class="d-flex flex-row align-center">
                            <v-btn
                                size="24"
                                variant="text"
                                class="like mx-0" 
                                :id="`post_${postDetail?.id}_like_btn`" 
                                :disabled="!loggedIn"
                                @click="pressReaction({'post_id':postDetail?.id, 'reaction_type': 'like', 'user_reaction': postDetail?.user_reaction})">
                                    <v-icon 
                                        size="24" 
                                        class="like"  
                                        :class="{ 'text-info': postDetail?.user_reaction?.reaction_type == 'like'}">
                                        mdi-arrow-up-bold-circle-outline
                                    </v-icon>
                            </v-btn>

                            <span class="mx-3" :class="{ 'text-info': postDetail?.user_reaction?.reacted}">{{ postDetail?.post_reactions?.total_reactions }}</span>

                            <v-btn
                                size="24"
                                variant="text"
                                class="dislike mx-0"
                                :id="`post_${post?.id}_dislike_btn`" 
                                :disabled="!loggedIn"
                                @click="pressReaction({'post_id':postDetail?.id, 'reaction_type': 'dislike', 'user_reaction': postDetail?.user_reaction})">
                                    <v-icon 
                                        size="24" 
                                        class="dislike" 
                                        :class="{ 'text-info': postDetail?.user_reaction?.reaction_type == 'dislike' }">
                                        mdi-arrow-down-bold-circle-outline
                                    </v-icon>
                            </v-btn>
                        </div>
                    
                        <v-progress-linear
                            class="mt-1"
                            :model-value="ratingPercentage(postDetail?.post_reactions)"
                            color="green"
                            bg-color="red"
                            bg-opacity="1"
                        ></v-progress-linear>
                    </div>

                    <div class="d-flex flex-row align-center">
                        <v-btn class="btn clickable transformable" variant="elevated" @click="share">
                            <v-icon size='large' icon="mdi-share-variant-outline"></v-icon>         
                        </v-btn>
                    </div>
                </div>
            </v-card-actions>
        </v-card>

        <Comments
            ref="comments_container" 
            :post_id="post_id">
        </Comments>
    </div>

</template>

<script setup>
import { ref, defineAsyncComponent, onBeforeMount, onBeforeUnmount, computed} from 'vue';
import { useStore } from 'vuex';
import {useEditor, EditorContent, Editor } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Underline from '@tiptap/extension-underline'
import TextAlign from '@tiptap/extension-text-align'
import Link from '@tiptap/extension-link'
import TextStyle from '@tiptap/extension-text-style'
import { Color } from '@tiptap/extension-color'
import Highlight from '@tiptap/extension-highlight'
import FontFamily from '@tiptap/extension-font-family'
import Mention from '@tiptap/extension-mention';
import suggestion from '@/components/TextEditor/Mention/suggestion'
import Placeholder from '@tiptap/extension-placeholder'
import Gapcursor from '@tiptap/extension-gapcursor'
import Table from '@tiptap/extension-table'
import TableCell from '@tiptap/extension-table-cell'
import TableHeader from '@tiptap/extension-table-header'
import TableRow from '@tiptap/extension-table-row'
import routes from '@/router/router' 
import {DateTimeFormat} from '@/helpers'

const Comments = defineAsyncComponent(() => import('@/components/Comments/Comments.vue'));

let store = useStore();
let editor = ref()

const postDetail = computed(() => store.getters['journal/getPostDetail'])
const loggedIn = computed(() => {return store.getters['auth/loginState']})
const post_id = ref(routes.currentRoute.value.params.post_id)

onBeforeMount(async () => {
    await store.dispatch('journal/getPostDetail', {'post_id': post_id.value, 'editable': false})

    editor.value = new Editor({
        content: postDetail.value.body,
        extensions: [
            StarterKit,
            Underline,
            TextAlign.configure({types: ['heading', 'paragraph']}),
            Link.configure({openOnClick: true,}),
            TextStyle,
            FontFamily,
            Color,
            Highlight.configure({ multicolor: true }),
            Mention.configure({HTMLAttributes: {class: 'text-info px-2',},suggestion,}),
            Placeholder.configure({placeholder: 'Write something …'}),
            Gapcursor,
            Table.configure({resizable: true,}),
            TableRow,
            TableHeader,
            TableCell,
        ],
        editable: false,
    });
})

const ratingPercentage = (post_reactions_obj) => {
    let totalVotes = post_reactions_obj?.num_likes + post_reactions_obj?.num_dislikes;
    if (totalVotes === 0) {return 0; }
    const rating = (post_reactions_obj?.num_likes / totalVotes) * 100;
    return Math.round(rating);
}

const pressReaction = (data) =>{
    // добавить allow_comments поле в response get_comments

    store.dispatch('journal/set_reaction', 
        {
            'post_id': data.post_id,
            'reaction_type': data.reaction_type,
            'id': data.user_reaction.id,
            'user_reaction': data.user_reaction,
            'set_reaction_in': 'post_detail',
        }
    )   

}

onBeforeUnmount(() => {editor.value.destroy();});



    
</script>

<style lang="scss">

.tiptap {
  > * + * {
    margin-top: 0.75em;
  }

  ul,
  ol {
    padding: 0 1rem;
    margin-left: 16px;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    line-height: 1.1;
  }

  code {
    background-color: rgba(#616161, 0.1);
    color: #616161;
  }

  pre {
    background: #0D0D0D;
    color: #FFF;
    font-family: 'JetBrainsMono', monospace;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;

    code {
      color: inherit;
      padding: 0;
      background: none;
      font-size: 0.8rem;
    }
  }

  img {
    max-width: 100%;
    height: auto;
  }

  blockquote {
    padding-left: 1rem;
    border-left: 2px solid rgba(#0D0D0D, 0.1);
  }

  hr {
    border: none;
    border-top: 2px solid rgba(#0D0D0D, 0.1);
    margin: 2rem 0;
  }
}

.main_wrapper{
    width: 100%;
    max-width: 750px;
    padding: 0;
    margin: 0;
    margin-top: 5px;
    position: relative;

    .image_container{position: relative;}
    .title_container{
        white-space: normal;
        padding: 20px 20px;
        z-index: 999;
    }
    
    .clickable{&:hover{cursor: pointer;}}

    .transformable{&:hover{transform: scale(1.1);}}
}
</style>