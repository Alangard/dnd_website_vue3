<template>

    <div class="main-content"
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
    .main-content{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 20px;

        background-color: var(--bg_color);

    }
</style>