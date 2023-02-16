<template>
    <comments></comments>
</template>


<script setup>
import { defineAsyncComponent } from 'vue';
const Comments = defineAsyncComponent(() => import('@/components/Journal/Comments/Comments.vue'));
</script>