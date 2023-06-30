<template>


            
</template>

<script setup>

import { ref, defineProps } from 'vue'; 

const props = defineProps(['item_id']);
const collapseOpen = ref(false);
</script>

<style lang="scss" scoped>
    .collapse_header_container{
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-left: 38px;
        font:var(--font_header);
        font-size: 13px;
        color: var(--bg_button_active_color);
        cursor: pointer;

        svg{
            width: 15px;
            height: 15px;
            stroke-width: 3px;
            stroke: var(--bg_button_active_color);
        }
    }
</style>