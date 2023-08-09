<template>

    <FilterAside 
        v-if='filterAsideState' 
        :isOpenAside="filterAsideState"
        @filterToolbarIsOpen="filterAsideState =! filterAsideState">
    </FilterAside>

    <QuillEditor :options="options" v-model:content="inputValue" content-type="html" class="mb-5"/>

    <button @click="test()"> save </button>

    <v-container style="max-width: 750px;">
    
        <Filters @filterToolbarIsOpen="filterAsideState =! filterAsideState"></Filters>

        <div class="d-flex flex-column align-center h-auto" ref="scrollComponent" v-if="postListStyle == 'list'">

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
                            @click="routes.push({name: 'post_detail', params: { id: post.id }})">
                            {{post.title}}
                        </div>

                        <v-img 
                            class='thumbnail clickable mw-100 rounded mb-2'
                            @click="routes.push({name: 'post_detail', params: { id: post.id }})"
                            v-if="post.thumbnail"
                            :src="post.thumbnail"
                            alt="post_img"
                            aspect-ratio="16/9"
                            cover>
                        </v-img>
                                            
                        <div class="description clickable text-justify text-subtitle-1 mb-2 "
                            @click="routes.push({name: 'post_detail', params: { id: post.id }})">
                            <div v-html="post.description" :text-data="post.description"></div>
                            <!-- {{post.description}} -->
                        </div>

                        <div class="tags_container d-flex f-row flex-wrap mb-2" v-if="post.tags.length">
                            <v-chip
                                class="tag_element clickable transformable rounded mr-2 mb-2" size="small"
                                v-for="tag in post.tags"
                                @click="setTagFilter(tag.slug)">
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
                                        @click="routes.push({name: 'post_detail', params: { id: post.id }})">
                                            <v-icon class="pr-2" icon="mdi-comment-text-outline"></v-icon>
                                        {{post.num_comments}}
                                    </v-btn>

                            </div>
                        </div>


                
            </v-card >
        </div>

        <!-- <div class=" test-grid " ref="scrollComponent" v-else>
            <v-card class="main-container-grid elevation-8" v-for="post in store.getters.getPostsList" :key="post">
                <v-img 
                    class='thumbnail mw-100 rounded mb-2' style="cursor:pointer"
                    v-if="post.thumbnail"
                    @click="$router.push({ name: 'postdetail', params: {id: post.id} })"
                    :src="post.thumbnail"
                    alt="post_img"
                    aspect-ratio="4/3"
                    cover>
                </v-img>

                <div class="title text-subtitle-2 font-weight-bold text-left mt-4 mx-3 mb-2"
                    @click="$router.push({ name: 'postdetail', params: {id: post.id} })">
                    {{post.title}}
                </div>

                <div class="user_data d-flex flex-row align-center justify-space-between mb-3 mx-3 w-auto">

                    <div class='d-flex flex-column'>
                        <span class="username text-subtitle-1 font-weight-bold text-capitalize" style="cursor:pointer" 
                            @click="$router.push({ name: 'user', params: {id: post.author.username} })">
                            {{post.author.username}}
                        </span> 

                        <span class="post_date text-caption font-weight-regular" style="cursor:pointer">
                            {{DateTimeFormat(post.created_datetime)}}
                        </span>   
                    </div>

                    <v-avatar class="avatar" size="large" style="cursor:pointer" 
                        @click="$router.push({ name: 'user', params: {id: post.author.username} })">
                        <v-img v-if="post.author.avatar != ''"
                            :src="post.author.avatar"
                            :alt="post.author.username">
                        </v-img>
                        <v-icon icon="mdi-account-circle" size='48' v-else></v-icon>
                    </v-avatar>
                </div>

            </v-card>
        </div> -->

    </v-container>

    <v-theme-provider :theme="theme.global.name.value =='dark' ? 'light' : 'dark'">
        <v-btn 
            v-if="!filterAsideState"
            class="create_post_btn"
            icon="mdi-plus-thick"
            position="fixed"
            style="bottom: 14px; right: 43%; z-index: 9999;">
        </v-btn>
    </v-theme-provider>
    
</template>

<script setup>
import { getCurrentInstance, defineAsyncComponent, onMounted, onUnmounted, ref, defineEmits, computed, onBeforeMount, toRaw} from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import { useTheme } from 'vuetify/lib/framework.mjs';
import {DateTimeFormat} from '@/helpers'
import routes from '@/router/router' 

import interceptorsInstance, {authHeader} from '@/api/main'


const Filters = defineAsyncComponent(() => import('@/components/Filters/Filters.vue'));
const FilterAside = defineAsyncComponent(() => import('@/components/Filters/FilterAside.vue'));

const store = useStore();
let theme = useTheme();

const token = authHeader()['Authorization'].split('Bearer ')[1]
let url = `ws://${axios.defaults.baseURL.split('http://')[1]}ws/post_socket-server/?token=${token}`
const socket = new WebSocket(url)

let toggleReaction = ref(null);
let filterAsideState = ref(false);
let postListStyle = ref('list');
const postsList = computed(() => {return store.getters['journal/getPosts']});

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


// to do: check out infinity scroll for mobile version
/*Fetch post_list_data ****************************************************/ 

let scrollComponent = ref(null)
let isLoading = ref(false);


/*Filter post_list by one tag*/
const setTagFilter = async (tag_slug) => {
    store.dispatch('fetchPostData', {'url': `posts/?page=1&page_size=7&tags=${tag_slug}`, 'setVariable': true})
}

/*Infinite scrolling (dynamic pagination)*/
// to do: check infinite scroller vuetify
const LoadMorePosts = async () => {
    const nextPageUrl = store.getters.getNextPostPageUrl
        if(nextPageUrl !== null){
            const url = 'posts/' + nextPageUrl.split('/api/v1/posts/')[1]
            store.dispatch('fetchPostData', {'url': url})
        }
    isLoading.value = false
}

const handleScroll = (e) => {
    let element = scrollComponent.value
    if(Math.floor(element.getBoundingClientRect().bottom) <= window.innerHeight){
        isLoading.value = true
        LoadMorePosts() 
    }
}



const inputValue = ref('<h1>This is header</h1><p>This is paragraph</p>')
const test =() =>{

console.log(inputValue , inputValue.value)
const text = inputValue.value

const data ={
    author:{
        avatar:"",
        id:1,
        username:"admin"
    },
    body:"asda",
    commented:false,
    created_datetime:"2023-07-22T12:10:50.666272Z",
    description: inputValue.value,
    id:4,
    is_publish:true,
    num_comments:0,
    post_reactions:{
        num_dislikes:0,
        num_likes:0,
        total_reactions:0
    },
    publish_datetime:null,
    tags:[],
    thumbnail:null,
    title:"test5",
    updated_datetime:"2023-07-22T12:10:50.666272Z",
    user_reaction:{
        reacted:false,
        reaction_type:""
    }

}

  store.commit('journal/addPostInStore', data)

}

const options = ref({
    modules: {
        toolbar: [
            [{ 'font': [] }, { 'size': ['small', false, 'large', 'huge'] }],
            ['bold', 'italic', 'underline', 'strike'],
            ['link', 'blockquote', { 'color': [] }],
            [{ 'align': [] }, { 'list': 'ordered'}, { 'list': 'bullet' }],
            ['clean']  

        ]
    },
    placeholder: 'Enter a comment...',
    readOnly: false,
    theme: 'snow'
})




onMounted(async () => {
    store.dispatch('journal/get_posts', 'posts/?page=1&page_size=7')
    window.addEventListener('scroll', handleScroll);

    socket.onmessage = function(e){
        let data = JSON.parse(e.data)
        if(data.action === 'list'){
            store.commit('journal/setPostsList', data.data)
            
            // postsList.value = data.data
        }
        else if(data.action === 'create'){
            store.commit('journal/updatePostsList', data.data)
            // postsList.value.unshift(data.data)
            console.log(data.data)
        }
    }

})

const share =() => {
    
    console.log(authHeader()['Authorization'])
    chatSocket.send(JSON.stringify(
        {   
            'operation_type': 'create_post',
            'auth_header': authHeader()['Authorization'].split(),
            'post_data': 
                {
                    'title': 't',
                    'description': 'test_d',
                    'body': 'test_b'
                }
            
        }

    
    ))
}

onUnmounted(() => {
    socket.close()
    window.removeEventListener("scroll", handleScroll)
})

const openReactionModal = () => {

}

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