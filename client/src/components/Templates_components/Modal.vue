<template>
    <div class="modal_wrapper">
        <div class="modal_container" ref='modal_container'>
            <div class="header">
                <div class="close_btn" @click="emit('close_modal')">
                    <svg @click="emit('close_modal')" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </div>

                <slot name='modal_header'></slot>
            </div>

            <div class="body">
                <slot name='modal_body'></slot> 
            </div>
        </div>
    </div> 
</template>

<script setup>
import { ref, defineEmits, onBeforeUnmount } from 'vue';
import { onClickOutside } from '@vueuse/core';

const emit = defineEmits(['close_modal']);
const modal_container = ref(null);

onClickOutside(modal_container, (event) => emit('close_modal'));

// Disable scrolling background page when modal is open
document.querySelector('body').style.overflow ='hidden';

onBeforeUnmount(() => {
    //Before the page is unmounted, toggle overflow back
    document.querySelector('body').style.overflow = 'visible'
})
</script>


<style lang="scss" scoped>

.modal_wrapper{
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1060;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0,0,0, 0.5);
    overflow: hidden;

    .modal_container{
        position: relative;
        width: 90%;
        max-width: 500px;
        border-radius: 5px;
        padding: 0px 10px 10px 10px;
        background-color:var(--bg_color);
        color: var(--text_color_primary);

        .header{
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: flex-start;
            margin-bottom: 10px;

            .close_btn{
                display: flex;
                flex-direction: row;
                align-items: center;
                justify-content: flex-end;
                width: 100%;
                padding: 5px 0;

                svg{
                    cursor: pointer;
                    stroke: var(--text_color_secondary);;

                    &:hover{
                        stroke: var(--bg_button_active_color);;
                    }

                }
            }
        }

        .body{
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
    }
}

</style>