<template>

    <div class="main-content_journal"
        :class="{'light-theme': this.$store.state.theme =='light', 'dark-theme': this.$store.state.theme =='dark'}">

        <PostItemComponent
            v-for="post_id in getPostData" :key="post_id">
        </PostItemComponent>

    </div>




</template>

<script>
import PostItemComponent from '@/components/Journal/PostItemComponent.vue';
export default {
    data(){
        return{
            access_level: true,
        }
    },
    computed:{
        getPostData(){
            return this.$store.getters.getPostData;
        }
    },
    components: { PostItemComponent }
}
</script>

<style lang="scss" scoped>
    .main-content_journal{
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>