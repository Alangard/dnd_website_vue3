<template>
    <div class="d-flex flex-column align-center mt-10 h-auto" ref="scrollComponent">

            <v-card class="main-container elevation-8"
                v-for="post in postList" :key="post" >

                <div class="d-flex flex-column justify-space-around w-auto pl-2">
                    <div class="user_data d-flex flex-row align-center justify-start mb-1" style="width:max-content">

                            <v-avatar class="avatar" size="x-small" style="cursor:pointer" 
                                @click="$router.push({ name: 'user', params: {id: post.author.username} })">
                                <v-img v-if="post.author.avatar != ''"
                                    :src="post.author.avatar"
                                    :alt="post.author.username">
                                </v-img>
                                <v-icon icon="mdi-account-circle" v-else></v-icon>
                            </v-avatar>

                            <span class="username px-1 py-0 text-caption font-weight-regular" style="cursor:pointer" 
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
                            @click="setTagFilter(tag.id)">
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


                </div>
            </v-card >
    </div>
    
</template>

<script setup>
import { defineAsyncComponent, onMounted, onUnmounted, ref, defineEmits, computed, onBeforeMount} from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import { DateTimeFormat } from '@/helpers'


const store = useStore();


// to do: check out infinity scroll for mobile version
/*Fetch post_list_data ****************************************************/ 


let scrollComponent = ref(null)
let page_size = ref(7);
let postData = ref({})
let postList = ref([])
let page = ref(1);
let isLoading = ref(false);
let baseUrl = `/api/v1/posts/?page=${page.value}&page_size=${page_size.value}`


/*Filter post_list by one tag*/

const setTagFilter = async (tag_id) => {
    try{
        baseUrl = baseUrl.split('&tags=')[0] + `&tags=${tag_id}`
        await axios.get(baseUrl).then(response => {postList.value = response.data.results; postData.value = response.data})
        store.commit('setPostData', postData.value)
        store.commit('setPostsList', postList.value)
    }
    catch(err){console.log(err)}
}

/*Infinite scrolling (dynamic pagination)*/

const LoadMorePosts = async () => {
    try{ 
        if(postData.value.next !== null){
            let url = '/api/v1/posts/' + postData.value.next.split('/api/v1/posts/')[1]
            await axios.get(url).then(response => {postList.value.push(...response.data.results); postData.value = response.data})
            store.commit('setPostsList', postList.value)

        }
    }
    catch(err){console.log(err)}
    finally{isLoading.value = false}
}

const handleScroll = (e) => {
    let element = scrollComponent.value
    if(element.getBoundingClientRect().bottom <= window.innerHeight){
        isLoading.value = true
        LoadMorePosts() 
    }
}

onMounted(async () => {
    postData.value = await axios.get(baseUrl).then(response => {return response.data})
    postList.value = postData.value.results
    store.commit('setPostData', postData.value)
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
        align-items: center;
        width: auto;
        max-width: 740px;
        margin: 2px 5px 15px 5px;
        padding: 10px 15px 10px 10px;
        border-radius: 5px;
        caret-color: transparent;


        .btn{
            height: 30px;
            width: 30px;
            cursor: pointer;
        }
    }
    

</style>