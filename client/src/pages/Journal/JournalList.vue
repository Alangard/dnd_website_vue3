<template>
<FilterAside class="aside_filter mobile"
    v-if='filterAsideState && width < mobileWidthLimit' 
    :type="'mobile'"
    :isOpenAside="filterAsideState"
    @filterToolbarIsOpen="filterAsideState =! filterAsideState"
    @setFilter="(value) => {handleFilterChange(value)}">
</FilterAside>


    <v-container class="d-flex flex-row justify-center">
        <FilterAside class="aside_filter desktop"
            v-if='width >= mobileWidthLimit'
            :type="'desktop'"
            :isOpenAside="filterAsideState"
            @setFilter="(value) => {handleFilterChange(value)}">
        </FilterAside>
        

        <div class="d-flex flex-column" :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'">
            <Filters 
                @filterToolbarIsOpen="filterAsideState =! filterAsideState"
                @orderChange="(value) => {handleOrderChange(value)}"
                @clickContentType="(contentType) => {changeContentType(contentType)}">
            </Filters>
        
            <v-row class='mb-4' no-gutters>
                <v-col :cols="width < mobileWidthLimit ? '12' : '8'" v-if="new_posts_count > 0">
                    <v-sheet class="mr-2">
                        <v-btn class="load_new_posts w-100" rounded="sm" @click="LoadNewPost()">
                            <span class="text-info">+{{new_posts_count}} &nbsp;</span><span> new posts</span> 
                        </v-btn>
                    </v-sheet>
                </v-col>

                <v-col :cols="new_posts_count > 0 ? '4' : '12'" v-if="width >= mobileWidthLimit">
                    <v-btn class="create_post_btn w-100" rounded="sm" prepend-icon="mdi-plus-thick" @click="routes.push({name: 'journal_create'})">Create post</v-btn>
                </v-col>
            </v-row>            

            <div class="d-flex flex-column align-center h-auto" ref="scrollComponent">
                <v-card class="main-container elevation-8 w-100" v-for="post in postsList" :key="post">
                    <div class="user_data d-flex flex-row align-center justify-space-between mb-1 w-100" >
                        <div class="d-flex flex-row align-center justify-start">
                            <v-avatar class="clickable transformable avatar" size="x-small"
                                @click="routes.push({name: 'user_profile', params: { username: post.author.username }})">
                                <v-img v-if="post.author.avatar"
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

                        <v-tooltip location="bottom" v-if="post.author.id != userData?.id && userData && width >= mobileWidthLimit">
                            <template v-slot:activator="{ props }">
                                <v-btn icon v-bind="props" variant="text" density="compact" @click="changeSubscribeState(post.author.id)">
                                    <v-icon>{{ isSubscribedTo(post.author.id) != -1 ? 'mdi-bell-check-outline':'mdi-bell-ring-outline' }}</v-icon>
                                </v-btn>
                            </template>
                            <span>{{isSubscribedTo(post.author.id) != -1 ? 'You are subscribed': 'You are unsubscribed'}}</span>
                        </v-tooltip>
                        
                    </div>

                    <div class="title clickable font-weight-bold text-justify text-subtitle-1 mb-2"
                        @click="routes.push({name: 'journal_detail', params: { post_id: post.id }})">
                        {{post.title}}
                    </div>

                    <v-img class='thumbnail clickable mw-100 rounded mb-2'
                        @click="routes.push({name: 'journal_detail', params: { post_id: post.id }})"
                        v-if="post.thumbnail"
                        :src="post.thumbnail"
                        alt="post_img"
                        aspect-ratio="16/9"
                        cover>
                    </v-img>
                                        
                    <div class="description clickable text-justify text-subtitle-1 mb-2 "
                        @click="routes.push({name: 'journal_detail', params: { post_id: post.id }})">
                        {{post.description}}
                    </div>

                    <div class="tags_container d-flex f-row flex-wrap mb-2" v-if="post.tags.length">
                        <v-chip
                            class="tag_element clickable transformable rounded mr-2 mb-2" size="small"
                            v-for="tag in post.tags"
                            @click="handleFilterChange([`tags=${tag.slug}`])">
                            #{{ tag.name }}
                        </v-chip>
                    </div>

                    <v-divider></v-divider>

                    <div class="d-flex flex-row justify-space-between pt-2 w-100">

                        <div class="reactions_container">
            
                            <div class="d-flex flex-row align-center">
                                <v-btn
                                    size="24"
                                    variant="text"
                                    class="like mx-0" 
                                    :id="`post_${post?.id}_like_btn`"
                                    :disabled="!loggedIn" 
                                    @click="pressReaction({'post_id':post?.id, 'reaction_type': 'like', 'user_reaction': post?.user_reaction})">
                                        <v-icon 
                                            size="24" 
                                            class="like"  
                                            :class="{ 'text-info': post.user_reaction.reaction_type == 'like'}">
                                            mdi-arrow-up-bold-circle-outline
                                        </v-icon>
                                </v-btn>

                                <span class="mx-3" :class="{ 'text-info': post?.user_reaction.reacted}">{{ post?.post_reactions.total_reactions }}</span>

                                <v-btn
                                    size="24"
                                    variant="text"
                                    class="dislike mx-0"
                                    :id="`post_${post?.id}_dislike_btn`"
                                    :disabled="!loggedIn"
                                    @click="pressReaction({'post_id':post?.id, 'reaction_type': 'dislike', 'user_reaction': post?.user_reaction})">
                                        <v-icon 
                                            size="24" 
                                            class="dislike" 
                                            :class="{ 'text-info': post?.user_reaction.reaction_type == 'dislike' }">
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

            <div class="pagination text-center">
                <v-pagination
                    v-model="current_page"
                    @update:model-value="handlePageChange"
                    :length="page_count"
                    :total-visible="7"
                    size="small"
                ></v-pagination>
            </div>
        </div>


    </v-container>



    <v-theme-provider :theme="theme?.global?.name?.value =='dark' ? 'light' : 'dark'">
        <v-btn 
            v-if="!filterAsideState && width < mobileWidthLimit"
            @click="routes.push({name: 'journal_create'})"
            class="create_post_btn"
            icon="mdi-plus-thick"
            position="fixed"
            style="bottom: 70px; right: 10%; z-index: 9999;">
        </v-btn>
    </v-theme-provider>
    
</template>

<script setup>
import { getCurrentInstance, defineAsyncComponent, onMounted, onBeforeUnmount, ref, defineEmits, computed, onBeforeMount, toRaw, watch} from 'vue';
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
let filters = ref([])
let orderings = ref([])

let new_posts_count = ref(0)
let isLoading = ref(false);

const url = `ws://${axios.defaults.baseURL.split('http://')[1]}ws/post_socket-server/`
const websocket = new WebSocket(url)

let filterAsideState = ref(false);
let contentType = ref('All posts')
const postsList = computed(() => {return store.getters['journal/getPosts']});
const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})
const loggedIn = computed(() => {return store.getters['auth/loginState']})
const userData = ref(null)
const subscriptions = ref(null)

const changeSubscribeState =(user_id) =>{store.dispatch('accounts/changeSubscription', user_id)}
const isSubscribedTo = (user_id) => {return subscriptions?.value?.subscribed_to.findIndex(user => user.id === user_id)};

const changeContentType = async(type) => {
    contentType.value = type
    if(type == 'Feed'){
        routes.push({name: 'journal_filters', params: { filter_params: `feed/${page_url.value}`}})
        page_count.value = Math.ceil((await store.dispatch('journal/getPostFeedList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count / page_size)
        page_url.value = `feed/` + page_url.value
    }
    else if(type == 'All posts'){
        routes.push({name: 'journal_filters', params: { filter_params: `?page=1&page_size=${page_size}` }})
        page_count.value = Math.ceil((await store.dispatch('journal/getPostList', {'paginate_url': `?page=1&page_size=${page_size}`, 'request_type': 'initial'})).count / page_size)
        page_url.value = `?page=1&page_size=${page_size}`
    }

}

const handlePageChange = async(newPage) => {
    current_page.value = newPage
    page_url.value = `?page=${newPage}&page_size=${page_size}` + `&${filters.value}`
    
    if(contentType.value == 'Feed'){
        routes.push({name: 'journal_filters', params: { filter_params: `feed/${page_url.value}` }})
        await store.dispatch('journal/getPostFeedList', {'paginate_url': page_url.value, 'request_type': 'initial'})
        page_url.value = `feed/` + page_url.value
    }
    else if(contentType.value == 'All posts'){
        routes.push({name: 'journal_filters', params: { filter_params: `${page_url.value}` }})
        await store.dispatch('journal/getPostList', {'paginate_url': page_url.value, 'request_type': 'initial'})
    }
    window.scrollTo({top: 0,behavior: "smooth"});
}

const handleOrderChange = async(order_param) => {
    //orderings можно сделать строкой, всё равно выставить сортировку можно лишь одну
    const new_order_str = order_param.split('=')[1]
    const order_without_direction =  new_order_str[0] == '-' ? new_order_str.slice(1) : new_order_str
    const index_in_orderings = orderings.value.indexOf(order_without_direction)
    const page_url_params_list = page_url.value[0] == '?' ? page_url.value.slice(1).split('&') : page_url.value.split('?')[1].split('&')
    const index_in_url = page_url_params_list.indexOf(order_without_direction)

    if(index_in_orderings != -1){
        orderings.value.splice(index_in_orderings, 1, new_order_str);
        page_url_params_list.splice(index_in_url, 1, order_param)
    }
    else{
        orderings.value.push(new_order_str)
        page_url_params_list.push(order_param)
    }

    page_url.value = '?' + page_url_params_list.join('&')
    if(contentType.value == 'Feed'){
        page_count.value = Math.ceil((await store.dispatch('journal/getPostFeedList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count / page_size)
        routes.replace({name: 'journal_filters', params: { filter_params: `feed/?${page_url_params_list.join('&')}` }})
    }
    else if(contentType.value == 'All posts'){
        page_count.value = Math.ceil((await store.dispatch('journal/getPostList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count / page_size)
        routes.replace({name: 'journal_filters', params: { filter_params: page_url.value }})
    }

}

const handleFilterChange = async(filter_params) =>{
    if(filter_params !== null){
        filters.value = filter_params
        page_url.value = filter_params.length > 0 ? `?${filter_params.join('&')}` : `?page=1&page_size=${page_size}`
        current_page.value = 1
    }
    else{
        page_url.value = `?page=1&page_size=${page_size}`
        current_page.value = 1
        filters.value = []
    } 
    if(contentType.value == 'Feed'){
        page_count.value = Math.ceil((await store.dispatch('journal/getPostFeedList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count / page_size)
        routes.replace({name: 'journal_filters', params: { filter_params: `feed/${page_url.value}` }})
    }
    else if(contentType.value == 'All posts'){
        page_count.value = Math.ceil((await store.dispatch('journal/getPostList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count / page_size)
        routes.replace({name: 'journal_filters', params: { filter_params: page_url.value }})
    } 
    window.scrollTo({top: 0,behavior: "smooth"}); 
}

const LoadNewPost = async() =>{
    try{
        if(contentType.value=='Feed'){
            await store.dispatch('journal/getPostFeedList', {'paginate_url': `feed/?page=1&page_size=${new_posts_count.value}`, 'request_type': 'load_more'})  
            new_posts_count.value = 0
        }
        else if(contentType.value == 'All posts'){
            await store.dispatch('journal/getPostList', {'paginate_url': `?page=1&page_size=${new_posts_count.value}`, 'request_type': 'load_more'})  
            new_posts_count.value = 0
        }
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
            'id': data.user_reaction.id,
            'user_reaction': data.user_reaction,
            'set_reaction_in': 'post_list' ,
        }
    )   
}


onBeforeMount(async () => {
    if(store.getters['auth/loginState'] == true){
        userData.value = store.getters['auth/getUserData']
        subscriptions.value = store.getters['accounts/getSubscriptions']
        await store.dispatch('accounts/getSubscriptions', userData?.value?.id)
    }

    page_count.value = Math.ceil((await store.dispatch('journal/getPostList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count / page_size)

    websocket.onmessage = function(e){
        let data = JSON.parse(e.data)
        if(data.action == 'create_post'){new_posts_count.value += 1}
    }
    
})

onBeforeUnmount(() => {
    if (websocket.value && websocket.value.readyState === WebSocket.OPEN) {websocket.value.close();}
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