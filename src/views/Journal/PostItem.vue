<template>
    <div class="post_item_wrapper">
        
        <comments></comments>
        
    </div>

</template>


<script setup>
import { ref, defineAsyncComponent } from 'vue';
const Comments = defineAsyncComponent(() => import('@/components/Journal/Comments/Comments.vue'));
</script>

<style lang="scss" scoped>
    .post_item_wrapper{
        padding: 0;
        margin: 0;
        position: relative;
    }
</style>