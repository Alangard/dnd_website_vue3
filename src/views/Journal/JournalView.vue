<template>

    <div class="main-content_journal"
        :class="{'light-theme': this.$store.state.theme =='light', 'dark-theme': this.$store.state.theme =='dark'}">

        <PostItemComponent
            v-for="post_id in this.posts_list_data" :key="post_id">
        </PostItemComponent>

    </div>




</template>

<script>
import PostItemComponent from '@/components/Journal/PostItemComponent.vue';
export default {
    components: { PostItemComponent },
    data(){
        return{
            posts_list_data: null,
        }
    },

    mounted (){
        // Step 1. Query the server for minimal post data
        // Step 2. Save the data to VueX
        // Step 3. Modelling data handling with VueX
        
        this.posts_list_data = this.$store.getters.getShrotPostData;
    },

}
</script>

<style lang="scss" scoped>
    .main-content_journal{
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>