<template>
    <div>
        <div class="container" ref="dropdown_more_func_container" @keydown.esc="menuIsOpen = false">
            <div class="dropdown_header">
                <!-- <slot name="header"></slot> -->
                <button class="more_btn" @click="openMenu()" :class='{"opened": menuIsOpen == true}'>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="1"></circle>
                        <circle cx="12" cy="5" r="1"></circle>
                        <circle cx="12" cy="19" r="1"></circle>
                    </svg>
                </button>
    
            </div>
            <div class="dropdown_body" v-if="menuIsOpen == true">
                    <div v-if="props.isBlock == true">
                        <div v-if="props.current_user_info.username != props.user_info.username">
                            <ul>
                                <li class='report' @click="menuIsOpen = false"> 
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"></path>
                                        <line x1="4" y1="22" x2="4" y2="15"></line>
                                    </svg>
                                    Report
                                </li>
                                <li class='hide_content' @click="menuIsOpen = false">
                                    <svg width="800px" height="800px" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" fill="var(--text_color_secondary)">
                                        <path d="M 3.71875 2.28125 L 2.28125 3.71875 L 8.5 9.90625 L 19.59375 21 L 21.5 22.9375 L 28.28125 29.71875 L 29.71875 28.28125 L 23.5 22.0625 C 27.734375 19.964844 30.574219 16.851563 30.75 16.65625 L 31.34375 16 L 30.75 15.34375 C 30.480469 15.042969 24.085938 8 16 8 C 14.042969 8 12.195313 8.429688 10.5 9.0625 Z M 16 10 C 18.152344 10 20.1875 10.605469 22 11.4375 C 22.644531 12.515625 23 13.734375 23 15 C 23 16.816406 22.296875 18.476563 21.15625 19.71875 L 18.3125 16.875 C 18.730469 16.363281 19 15.714844 19 15 C 19 13.34375 17.65625 12 16 12 C 15.285156 12 14.636719 12.269531 14.125 12.6875 L 12.09375 10.65625 C 13.335938 10.273438 14.636719 10 16 10 Z M 6.6875 10.90625 C 3.480469 12.878906 1.398438 15.175781 1.25 15.34375 L 0.65625 16 L 1.25 16.65625 C 1.507813 16.945313 7.429688 23.425781 15.0625 23.9375 C 15.371094 23.96875 15.683594 24 16 24 C 16.316406 24 16.628906 23.96875 16.9375 23.9375 C 17.761719 23.882813 18.566406 23.773438 19.34375 23.59375 L 17.5625 21.8125 C 17.054688 21.929688 16.539063 22 16 22 C 12.140625 22 9 18.859375 9 15 C 9 14.46875 9.070313 13.949219 9.1875 13.4375 Z M 7.25 12.9375 C 7.089844 13.613281 7 14.300781 7 15 C 7 16.738281 7.488281 18.339844 8.34375 19.71875 C 6.054688 18.40625 4.304688 16.867188 3.40625 16 C 4.152344 15.277344 5.496094 14.078125 7.25 12.9375 Z M 24.75 12.9375 C 26.503906 14.078125 27.84375 15.277344 28.59375 16 C 27.695313 16.867188 25.917969 18.4375 23.625 19.75 C 24.484375 18.371094 25 16.738281 25 15 C 25 14.300781 24.910156 13.609375 24.75 12.9375 Z"/>
                                    </svg>
                                    Hide author's comments
                                </li>
                            </ul>
                        </div>
                        <div v-else>Nothing</div>
                    </div>

                    <div v-else>
                        <div v-if="props.comment_status != 'deleted'">
                            <div v-if="props.current_user_info.username != props.user_info.username">
                                <ul>
                                    <li class='report' @click="menuIsOpen = false"> 
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"></path>
                                            <line x1="4" y1="22" x2="4" y2="15"></line>
                                        </svg>
                                        Report
                                    </li>
                                    <li class='hide_content' @click="menuIsOpen = false">
                                        <svg width="800px" height="800px" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" fill="var(--text_color_secondary)">
                                            <path d="M 3.71875 2.28125 L 2.28125 3.71875 L 8.5 9.90625 L 19.59375 21 L 21.5 22.9375 L 28.28125 29.71875 L 29.71875 28.28125 L 23.5 22.0625 C 27.734375 19.964844 30.574219 16.851563 30.75 16.65625 L 31.34375 16 L 30.75 15.34375 C 30.480469 15.042969 24.085938 8 16 8 C 14.042969 8 12.195313 8.429688 10.5 9.0625 Z M 16 10 C 18.152344 10 20.1875 10.605469 22 11.4375 C 22.644531 12.515625 23 13.734375 23 15 C 23 16.816406 22.296875 18.476563 21.15625 19.71875 L 18.3125 16.875 C 18.730469 16.363281 19 15.714844 19 15 C 19 13.34375 17.65625 12 16 12 C 15.285156 12 14.636719 12.269531 14.125 12.6875 L 12.09375 10.65625 C 13.335938 10.273438 14.636719 10 16 10 Z M 6.6875 10.90625 C 3.480469 12.878906 1.398438 15.175781 1.25 15.34375 L 0.65625 16 L 1.25 16.65625 C 1.507813 16.945313 7.429688 23.425781 15.0625 23.9375 C 15.371094 23.96875 15.683594 24 16 24 C 16.316406 24 16.628906 23.96875 16.9375 23.9375 C 17.761719 23.882813 18.566406 23.773438 19.34375 23.59375 L 17.5625 21.8125 C 17.054688 21.929688 16.539063 22 16 22 C 12.140625 22 9 18.859375 9 15 C 9 14.46875 9.070313 13.949219 9.1875 13.4375 Z M 7.25 12.9375 C 7.089844 13.613281 7 14.300781 7 15 C 7 16.738281 7.488281 18.339844 8.34375 19.71875 C 6.054688 18.40625 4.304688 16.867188 3.40625 16 C 4.152344 15.277344 5.496094 14.078125 7.25 12.9375 Z M 24.75 12.9375 C 26.503906 14.078125 27.84375 15.277344 28.59375 16 C 27.695313 16.867188 25.917969 18.4375 23.625 19.75 C 24.484375 18.371094 25 16.738281 25 15 C 25 14.300781 24.910156 13.609375 24.75 12.9375 Z"/>
                                        </svg>
                                        Hide author's comments
                                    </li>
                                </ul>
                            </div>
                            <div v-else>
                                <li @click="emit('StartEdit'), menuIsOpen = false">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <polygon points="14 2 18 6 7 17 3 17 3 13 14 2"></polygon>
                                        <line x1="3" y1="22" x2="21" y2="22"></line>
                                    </svg>
                                    Edit
                                </li>
                                <li class='delete_comment' @click="emit('showDeleteAlert'), menuIsOpen = false">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <polyline points="3 6 5 6 21 6"></polyline>
                                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                                        <line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line>
                                    </svg>
                                    Delete
                                </li>
                            </div>
                        </div>
                        <div v-else>Nothing</div>
                    </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits} from 'vue';
import { onClickOutside } from '@vueuse/core';

const props = defineProps(['isMobile', 'isBlock','current_user_info','user_info','comment_text','comment_status']);
const emit = defineEmits(['moreFuncOpenMobile', 'StartEdit', 'showDeleteAlert']);


const menuIsOpen = ref(false);
const dropdown_more_func_container = ref(null);

onClickOutside(dropdown_more_func_container, (event) => menuIsOpen.value = false);

function openMenu(){
    if(props.isMobile == false){menuIsOpen.value = !menuIsOpen.value}
    else{emit('moreFuncOpenMobile');}
}
</script>

<!-- <script>
import { onClickOutside } from '@vueuse/core';
export default {
    props:['isMobile', 'isBlock','current_user_info','user_info','comment_text','comment_status'],
    data(){
        return{
            menuIsOpen: false,
        }
    },
    methods:{
        openMenu(){
            if(this.isMobile == false){
                this.menuIsOpen = !this.menuIsOpen
            }
            else{
                this.$emit('moreFuncOpenMobile');
            }
        },
    },

    mounted(){
        onClickOutside(this.$refs.dropdown_more_func_container, (event) => 
            this.menuIsOpen = false
        )
    }
}
</script> -->

<style lang="scss" scoped>
    *{
        padding: 0;
        margin: 0;
        font-family: 'Lato', sans-serif;
        font-size: 14px;
        font-weight: 300;
        color: var(--text_color_primary);
    }

    svg{
        height: 24px;
        width: 24px;
        stroke: var(--text_color_secondary);
    }

    button{
        background-color: transparent;
        border: 2px solid transparent;
        outline: none;
        border-radius: 5px;
        &:hover > svg, &.opened > svg {stroke: var(--bg_button_active_color);}

    }

    li{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        list-style: none;
        padding: 5px;
        border-radius: 5px;

        &:hover{cursor: pointer;background-color: var(--bg_button_color);}  

        svg{
            height: 18px;
            width: 18px;
            margin: 0 10px 0 3px;
        }
    }

    .container{
        position: relative;
        width: auto;
        height: auto;

        .more_btn{padding: 2px 0;}

        .dropdown_body{
            z-index: 99;
            position: absolute;
            right: 3px;
            top: 30px;
            padding: 4px;
            width: max-content;
            background-color: var(--bg_block_color);
            box-shadow: var(--box_shadow);
            border-radius: 5px;

            .delete_comment, .delete_comment > svg{
                stroke: var(--error_color);
                color: var(--error_color);
            }
        }
    }

</style>

