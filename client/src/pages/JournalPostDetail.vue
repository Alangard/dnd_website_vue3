<template>
    <div class="post_item_wrapper">

        <Comments></Comments>
    </div>

</template>

<script setup>
    import { ref, defineAsyncComponent } from 'vue';
    const Comments = defineAsyncComponent(() => import('@/components/Comments/Comments.vue'));
</script>

<style lang="scss" scoped>
    .post_item_wrapper{
        width: 100%;
        max-width: 750px;
        padding: 0;
        margin: 0;
        position: relative;
    }
</style>