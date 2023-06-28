<template>

    <FilterAside 
        v-if='filterAsideState' 
        :isOpenAside="filterAsideState"
        @filterToolbarIsOpen="filterAsideState =! filterAsideState">
    </FilterAside>

    <v-date-picker></v-date-picker>

    <v-container style="max-width: 750px;">

    
        <Filters @filterToolbarIsOpen="filterAsideState =! filterAsideState"></Filters>

        <div class="d-flex flex-column align-center h-auto" ref="scrollComponent" v-if="store.getters.getPostListStyle=='list'">

            <v-card class="main-container elevation-8" v-for="post in store.getters.getPostsList" :key="post">
                        <div class="user_data d-flex flex-row align-center justify-start mb-1" style="width:max-content">

                                <v-avatar class="avatar" size="x-small" style="cursor:pointer" 
                                    @click="$router.push({ name: 'user', params: {id: post.author.username} })">
                                    <v-img v-if="post.author.avatar != ''"
                                        :src="post.author.avatar"
                                        :alt="post.author.username">
                                    </v-img>
                                    <v-icon icon="mdi-account-circle" v-else></v-icon>
                                </v-avatar>

                                <span class="username px-1 text-caption text-capitalize font-weight-regular" style="cursor:pointer" 
                                    @click="$router.push({ name: 'user', params: {id: post.author.username} })">
                                    {{post.author.username}}
                                </span> 

                                <span class="pr-1">•</span>
                                <span class="post_date text-caption font-weight-regular" style="cursor:pointer">
                                    Posted {{DateTimeFormat(post.created_datetime)}}
                                </span>
                        </div>

                        <div class="title font-weight-bold text-justify mb-2"
                            @click="$router.push({ name: 'postdetail', params: {id: post.id} })">
                            {{post.title}}
                        </div>

                        <v-img 
                            class='thumbnail mw-100 rounded mb-2' style="cursor:pointer"
                            v-if="post.thumbnail"
                            @click="$router.push({ name: 'postdetail', params: {id: post.id} })"
                            :src="post.thumbnail"
                            alt="post_img"
                            aspect-ratio="16/9"
                            cover>
                        </v-img>
                                            

                        <div class="description text-justify mb-2">{{post.description}}</div>

                        <div class="tags_container d-flex f-row flex-wrap mb-2" v-if="post.tags.length">
                            <v-chip
                                class="tag_element rounded mr-1 mb-2" size="small"
                                v-for="tag in post.tags"
                                @click="setTagFilter(tag.slug)">
                                {{ tag.name }}
                            </v-chip>
                        </div>

                        <v-divider></v-divider>



                        <div class="d-flex flex-row justify-space-between pt-2">
                        
                            <!-- <v-img 
                                class='reaction mw-100 rounded mb-2' style="cursor:pointer"
                                v-for="reaction in post.reactions"
                                :src="post.thumbnail"
                                alt="post_img"
                                aspect-ratio="16/9"
                                cover>
                            </v-img> -->
                            <v-btn class='btn' rounded="lg" icon="mdi-plus-circle-outline"
                                    @click="openReactionModal">
                            </v-btn>
                

                                <!-- <ReactionModal
                                    v-if="modalIsOpen"
                                    @close_modal='modalIsOpen = false'
                                    :post_id='key.id'>
                                </ReactionModal> -->
                            


                            <div class="d-flex flex-row align-center">

                                    <v-btn class="btn mr-1" rounded="lg" icon="mdi-share-variant-outline"
                                        @click="share"
                                    ></v-btn>
        
                                    <v-btn class='btn' rounded="lg" prepend-icon="mdi-comment-text-outline" 
                                        @click="$router.push({ name: 'postdetail', params: {id: key.id} })">
                                        {{post.comments_count}}
                                    </v-btn>
            



                            </div>
                        </div>


                
            </v-card >

        </div>

        <div class=" test-grid " ref="scrollComponent" v-else>
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

        </div>
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
import { defineAsyncComponent, onMounted, onUnmounted, ref, defineEmits, computed, onBeforeMount} from 'vue';
import { useStore } from 'vuex';
import { useTheme } from 'vuetify/lib/framework.mjs';
import DateTimeFormat from '@/helpers'

const Filters = defineAsyncComponent(() => import('@/components/Filters/Filters.vue'));
const FilterAside = defineAsyncComponent(() => import('@/components/Filters/FilterAside.vue'));

let dates = ref(['2022-03-05', '2022-03-15'])

const store = useStore();
let theme = useTheme();

let filterAsideState = ref(false);

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

onMounted(async () => {
    store.dispatch('fetchPostData',{'url': 'posts/?page=1&page_size=7'})
    window.addEventListener('scroll', handleScroll);
})

onUnmounted(() => {
    window.removeEventListener("scroll", handleScroll)
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

</style>