<template>
    <div class="post_item_wrapper">
        <!-- <Comments></Comments> -->
        <test></test>
    </div>

</template>

<script setup>
    import { ref, defineAsyncComponent } from 'vue';
    const test = defineAsyncComponent(() => import('@/components/Comments/test.vue'));
</script>

<style lang="scss" scoped>
    .post_item_wrapper{
        padding: 0;
        margin: 0;
        position: relative;
    }
</style>