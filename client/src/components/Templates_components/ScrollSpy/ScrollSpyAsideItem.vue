<template>
    <a class='aside_link' :id="props.item_id" @click="scrollToTop">
        <slot name='scrollspy_aside__body'></slot>
    </a>
</template>


<script setup>
import { defineProps } from 'vue';

const props = defineProps(['item_id', 'isMobile']);

function scrollToTop(event){
    const href = event.target.getAttribute('id');
    const el = href ? document.querySelector("#" + href) : null;
    if(el) {
        document.querySelector('.article').scrollTop = el.offsetTop
    }    
}
</script>


<style lang="scss">
.aside_link{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    padding: 10px 0;
    border: 3px solid transparent;
    border-radius: 5px;
    cursor: pointer;

    svg{
        width: 20px;
        height: 20px;
        stroke: var(--text_color_secondary);
        pointer-events: none;
    }

    &:hover{background-color: var(--active_section_color);}
    &:hover > svg{stroke: var(--bg_button_active_color);}
    &.active > svg{stroke: var(--bg_button_active_color);}
    &.active{
        border-left: 3px solid var(--bg_button_active_color);
        background-color: var(--active_section_color);
    }

}

.aside.mobile{
    .aside_link:hover{background-color: transparent;}
    .aside_link:hover > svg{stroke:var(--text_color_secondary);}
    .aside_link.active > svg{stroke: var(--bg_button_active_color);}
    .aside_link.active{
        border-left: 3px solid var(--bg_button_active_color);
        background-color: var(--active_section_color);
    }
   
}

</style>