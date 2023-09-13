<template>

    <FilterAside 
        v-if='filterAsideState' 
        :isOpenAside="filterAsideState"
        @filterToolbarIsOpen="filterAsideState =! filterAsideState">
    </FilterAside>

    <v-container style="max-width: 750px;">
    
        <Filters @filterToolbarIsOpen="filterAsideState =! filterAsideState"></Filters>

    
        <v-row class='mb-4' no-gutters>
            <v-col :cols="width < 600 ? '12' : '8'" v-if="new_posts_count > 0">
                <v-sheet class="mr-2">
                    <v-btn class="load_new_posts w-100" rounded="sm" @click="LoadNewPost()">
                        <span class="text-info">+{{new_posts_count}} &nbsp;</span><span> new posts</span> 
                    </v-btn>
                </v-sheet>
            </v-col>

            <v-col :cols="new_posts_count > 0 ? '4' : '12'" v-if="width >= 600">
                <v-btn class="create_post_btn w-100" rounded="sm" prepend-icon="mdi-plus-thick" @click="routes.push({name: 'journal_create'})">Create post</v-btn>
            </v-col>
        </v-row>            
        



        <div class="d-flex flex-column align-center h-auto" ref="scrollComponent">

            <v-card class="main-container elevation-8 w-100" v-for="post in postsList" :key="post">
                        <div class="user_data d-flex flex-row align-center justify-start mb-1" style="width:max-content"
                           >

                            <v-avatar class="clickable transformable avatar" size="x-small"
                                @click="routes.push({name: 'user_profile', params: { username: post.author.username }})">
                                <v-img v-if="post.author.avatar != ''"
                                    :src="post.author.avatar"
                                    :alt="post.author.username">
                                </v-img>
                                <v-icon icon="mdi-account-circle" v-else></v-icon>
                            </v-avatar>

                            <span class="username clickable transformable px-1 text-caption text-capitalize font-weight-regular"
                                @click="routes.push({name: 'user_profile', params: { username: post.author.username }})">
                                {{post.author.username}}
                            </span> 

                            <span class="pr-1">•</span>
                            <span class="post_date clickable text-caption font-weight-regular">
                                Posted {{DateTimeFormat(post.created_datetime)}}
                            </span>
                        </div>

                        <div class="title clickable font-weight-bold text-justify text-subtitle-1 mb-2"
                            @click="routes.push({name: 'journal_detail', params: { id: post.id }})">
                            {{post.title}}
                        </div>

                        <v-img 
                            class='thumbnail clickable mw-100 rounded mb-2'
                            @click="routes.push({name: 'journal_detail', params: { id: post.id }})"
                            v-if="post.thumbnail"
                            :src="post.thumbnail"
                            alt="post_img"
                            aspect-ratio="16/9"
                            cover>
                        </v-img>
                                            
                        <div class="description clickable text-justify text-subtitle-1 mb-2 "
                            @click="routes.push({name: 'journal_detail', params: { id: post.id }})">
                            <div v-html="post.description" :text-data="post.description"></div>
                            <!-- {{post.description}} -->
                        </div>

                        <div class="tags_container d-flex f-row flex-wrap mb-2" v-if="post.tags.length">
                            <v-chip
                                class="tag_element clickable transformable rounded mr-2 mb-2" size="small"
                                v-for="tag in post.tags"
                                @click="handleFilterChange(`tags=${tag.slug}`)">
                                #{{ tag.name }}
                            </v-chip>
                        </div>

                        <v-divider></v-divider>



                        <div class="d-flex flex-row justify-space-between pt-2 w-100">

                            <div class="reactions_container">
                                <!-- <div class="d-flex flex-row align-center">
                                    <div class="like clickable transformable d-flex flex-column align-center justify-space-between"
                                        :class="{ 'text-info': post.user_reaction.reaction_type == 'like' }" 
                                        :id="`post_${post.id}_like_btn`" 
                                        @click="pressReaction({'post_id':post.id, 'reaction_type': 'like', 'user_reaction': post.user_reaction})">
                                            <v-icon class="like">mdi-arrow-up-bold-circle-outline</v-icon>
                                    </div>

                                    <span class="mx-3" :class="{ 'text-info': post.user_reaction.reacted}">{{ post.post_reactions.total_reactions }}</span>

                                    <div class="dislike clickable transformable d-flex flex-column align-center justify-space-between"
                                        :class="{ 'text-info': post.user_reaction.reaction_type == 'dislike' }"
                                        :id="`post_${post.id}_dislike_btn`" 
                                        @click="pressReaction({'post_id':post.id, 'reaction_type': 'dislike', 'user_reaction': post.user_reaction})">
                                            <v-icon class="dislike">mdi-arrow-down-bold-circle-outline</v-icon>
                                    </div>
                                </div> -->


                 
                                <div class="d-flex flex-row align-center">
                                    <v-btn
                                        size="24"
                                        variant="text"
                                        class="like mx-0" 
                                        :id="`post_${post.id}_like_btn`" 
                                        @click="pressReaction({'post_id':post.id, 'reaction_type': 'like', 'user_reaction': post.user_reaction})">
                                            <v-icon 
                                                size="24" 
                                                class="like"  
                                                :class="{ 'text-info': post.user_reaction.reaction_type == 'like'}">
                                                mdi-arrow-up-bold-circle-outline
                                            </v-icon>
                                    </v-btn>

                                    <span class="mx-3" :class="{ 'text-info': post.user_reaction.reacted}">{{ post.post_reactions.total_reactions }}</span>

                                    <v-btn
                                        size="24"
                                        variant="text"
                                        class="dislike mx-0"
                                        :id="`post_${post.id}_dislike_btn`" 
                                        @click="pressReaction({'post_id':post.id, 'reaction_type': 'dislike', 'user_reaction': post.user_reaction})">
                                            <v-icon 
                                                size="24" 
                                                class="dislike" 
                                                :class="{ 'text-info': post.user_reaction.reaction_type == 'dislike' }">
                                                mdi-arrow-down-bold-circle-outline
                                            </v-icon>
                                    </v-btn>
                                </div>
                              
                                <v-progress-linear
                                    class="mt-1"
                                    :model-value="ratingPercentage(post.post_reactions)"
                                    color="green"
                                    bg-color="red"
                                    bg-opacity="1"
                                ></v-progress-linear>
                            </div>

                            <div class="d-flex flex-row align-center">

                                    <v-btn class="btn clickable transformable mr-2 px-0" @click="share">
                                        <v-icon size='large' icon="mdi-share-variant-outline"></v-icon>         
                                    </v-btn>
        
                                    <v-btn class='btn clickable transformable' 
                                        rounded="lg" 
                                        :class="{'text-info': post.commented}"
                                        @click="routes.push({name: 'journal_detail', params: { id: post.id }})">
                                            <v-icon class="pr-2" icon="mdi-comment-text-outline"></v-icon>
                                        {{post.num_comments}}
                                    </v-btn>

                            </div>
                        </div>


                
            </v-card >
        </div>


    </v-container>

    <div class="pagination text-center">
        <v-pagination
            v-model="current_page"
            @update:model-value="handlePageChange"
            :length="page_count"
            :total-visible="7"
        ></v-pagination>
    </div>

    <!-- <v-theme-provider :theme="theme.global.name.value =='dark' ? 'light' : 'dark'">
        <v-btn 
            v-if="!filterAsideState && v-if="width < 600""
            class="create_post_btn"
            icon="mdi-plus-thick"
            position="fixed"
            style="bottom: 14px; right: 43%; z-index: 9999;">
        </v-btn>
    </v-theme-provider> -->
    
</template>

<script setup>
import { getCurrentInstance, defineAsyncComponent, onMounted, onUnmounted, ref, defineEmits, computed, onBeforeMount, toRaw, watch} from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import { useTheme, useDisplay } from 'vuetify/lib/framework.mjs';
import {DateTimeFormat} from '@/helpers'

import routes from '@/router/router' 

const Filters = defineAsyncComponent(() => import('@/components/Filters/Filters.vue'));
const FilterAside = defineAsyncComponent(() => import('@/components/Filters/FilterAside.vue'));

const store = useStore();
const { width } = useDisplay();

const current_page = ref(1)
const page_count = ref(1)
const page_size = 15
let page_url = ref(`?page=1&page_size=${page_size}`)

let new_posts_count = ref(0)
let isLoading = ref(false);

const url = `ws://${axios.defaults.baseURL.split('http://')[1]}ws/post_socket-server/`
const websocket = new WebSocket(url)

let filterAsideState = ref(false);
const postsList = computed(() => {return store.getters['journal/getPosts']});

const handlePageChange = async(newPage) => {
    page_url.value = `?page=${newPage}&page_size=${page_size}`
    await store.dispatch('journal/getPostList', {'paginate_url': page_url.value, 'request_type': 'normal'})
    window.scrollTo({top: 0,behavior: "smooth"});
}

const handleFilterChange = async(filter_str) =>{
    page_url.value = `?page=${current_page.value}&page_size=${page_size}` + `&${filter_str}`
    page_count.value = Math.ceil((await store.dispatch('journal/getPostList', {'paginate_url': page_url.value, 'request_type': 'normal'})).count / page_size)
    window.scrollTo({top: 0,behavior: "smooth"}); 
}

const LoadNewPost = async() =>{
    try{
        await store.dispatch('journal/getPostList', {'paginate_url': `?page=1&page_size=${new_posts_count.value}`, 'request_type': 'load_more'})  
        new_posts_count.value = 0
    }
    catch(error){console.log(error)}
 
    window.scrollTo({top: 0,behavior: "smooth"});
}

const ratingPercentage = (post_reactions_obj) => {
    let totalVotes = post_reactions_obj.num_likes + post_reactions_obj.num_dislikes;
    if (totalVotes === 0) {return 0; }
    const rating = (post_reactions_obj.num_likes / totalVotes) * 100;
    return Math.round(rating);
}

const pressReaction = (data) =>{

    store.dispatch('journal/set_reaction', 
        {
            'post_id': data.post_id,
            'reaction_type': data.reaction_type,
            'user_reaction': data.user_reaction
        }
    )   
}





/*Filter post_list by one tag*/
const setTagFilter = async (tag_slug) => {
    store.dispatch('fetchPostData', {'url': `posts/?page=1&page_size=7&tags=${tag_slug}`, 'setVariable': true})
}


const createPost = () => {
        const payload ={
            title:'Test title post',
            body:"<h1>This is header</h1><p>This is paragraph</p>",
            description: 'Test description post',
            is_publish:true,
            publish_datetime:null,
            tags:['test12', 'abya'],
        }
    store.dispatch('journal/createPost', payload)
}

const deletePost = () => {
    const post_id = 1000
    store.dispatch('journal/deletePost', post_id)
}

const partialUpdatePost =() => {
    const payload ={
        id: 14,
        description: "nnnn",
        title: 'mmmmm'
    }
    store.dispatch('journal/partialUpdatePost', payload)
}

const getPostList =(paginate_url) => {
    store.dispatch('journal/getPostList', paginate_url)
}

const getPostDetail =() => {
    const post_id = 5
    store.dispatch('journal/getPostDetail', post_id)
}


onMounted(async () => {
    page_count.value = Math.ceil((await store.dispatch('journal/getPostList', {'paginate_url': page_url.value, 'request_type': 'normal'})).count / page_size)
    
    websocket.onmessage = function(e){
        let data = JSON.parse(e.data)
        if(data.action == 'create_post'){new_posts_count.value += 1}
    }
})


onUnmounted(() => {
    websocket.close()
})


</script>

<style lang="scss" scoped>

    

    .main-container{
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: auto;
        margin: 2px 0 15px 0;
        padding: 10px 15px 10px 10px;
        border-radius: 5px;
        caret-color: transparent;

        .btn{
            height: 30px;
            width: 30px;
            cursor: pointer;
        }
    }

    .main-container-grid{
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: auto;
        border-radius: 5px;
        caret-color: transparent;
    }
    
    .test-grid{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 2fr));
        grid-gap: 15px;
        align-items: stretch;
    }

    .clickable{
        &:hover{cursor: pointer;}
    }

    .transformable{
        &:hover{transform: scale(1.1);}
    }


</style>