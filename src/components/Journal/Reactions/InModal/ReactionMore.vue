<template>
    <div class="wrapper">

        <div class="btn-left" @click="scroll_left">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 18l-6-6 6-6"/>
            </svg>
        </div>
        
        <div ref='emot_container' class="emot_container" @mousewheel="scrollX">

            <div class="emoticon_element all_emoticons_btn" @click="isClicked">
                <input type="radio" name="emoticonGroup" value="all_emoticons" id="all_emoticons">
                <label for="all_emoticons">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                    </svg>
                </label>
            </div>

            <div class="emoticon_element total_reactions_count_btn" @click="isClicked">
                <input type="radio" name="emoticonGroup" value="total_reactions_count" id="total_reactions_count">
                <label for="total_reactions_count">
                    <span>Reacted {{totalReactionsCount}}</span>
                </label>
            </div>

            <reaction-more-btn
                @react="reacted"
                @click="isClicked"
                :user_info="getUserInfo"
                v-for='reaction in props.reactions_obj_by_post_id' :key='reaction'>
            </reaction-more-btn>

        </div>

        <div class="btn_right" @click="scroll_right">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 18l6-6-6-6"/>
            </svg>
        </div>
        
    </div>
</template>

<script setup>
import ReactionMoreBtn from './ReactionMoreBtn.vue';

import { ref, computed, defineProps, defineEmits } from 'vue';
import { useStore } from 'vuex';

const props = defineProps(['reactions_obj_by_post_id', 'post_id']);
const emit = defineEmits(['renderReactorsList']);
const store = useStore();

const emot_container = ref(null);
const getUserInfo = computed(() => store.state.user_info);
const totalReactionsCount = computed(() => {
    let sum = 0;
    for(const reaction of props.reactions_obj_by_post_id){sum += reaction.users_data.length;}
    return sum;
});

function isClicked(event){
    if(event.target.tagName == 'INPUT'){
        const element_id = event.target.id;
        emit('renderReactorsList', element_id);
    }
};

// Handle reaction button press event *Need to divide to computed functions*
function reacted(emoticon_data){
    debugger
    const {emoticon_id, emoticon_url} = emoticon_data;
    store.dispatch('changeReactionStatus', {'post_id': props.post_id, 'pressed_emoticon_id': emoticon_id, 'pressed_emoticon_url': emoticon_url});
};

function scrollX(e) {emot_container.value.scrollLeft += e.deltaY;};

function scroll_left() {emot_container.value.scrollLeft -= 100;};
        
function scroll_right() {emot_container.value.scrollLeft += 100;}
</script>


<style lang="scss" scoped>
    .wrapper{
        position: relative;
        display: flex;
        flex-direction: row;
        width: 100%;

        .btn-left{
            position: absolute;
            display: flex;
            z-index: 2;
            align-items: center;
            justify-self: flex-start;
            height: 100%;
            width: 30px;
            border-top-left-radius: 5px;
            border-bottom-left-radius: 5px;
            background-image: linear-gradient(to right, var(--bg_button_color), transparent);
            cursor: pointer;

            svg{stroke: var(--text_color_secondary);}

            &:hover{background-image: linear-gradient(to right, var(--gradien_to_transparent_color), transparent);}

        }

        .btn_right{
            position: absolute;
            right: 0px;
            display: flex;
            z-index: 2;
            align-items: center;
            justify-content: flex-end;
            height: 100%;
            width: 45px;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            background-image: linear-gradient(to left, var(--bg_button_color), transparent);
            cursor: pointer;

            svg{stroke: var(--text_color_secondary);}

            &:hover{background-image: linear-gradient(to left, var(--gradien_to_transparent_color), transparent);}
        }
    }


    .emot_container{
        display: flex;
        z-index: 1;
        flex-direction: row;
        justify-content: flex-start;
        padding: 0 30px;
        border-radius: 5px;
        width: 100%;
        background-color: var(--bg_button_color);
        font-weight: 400;
        scroll-behavior: smooth;

        overflow-x: scroll;
        -ms-overflow-style: none; /* for Internet Explorer, Edge */
        scrollbar-width: none; /* for Firefox */
        
        &::-webkit-scrollbar {
            display: none; /* for Chrome, Safari, and Opera */
        }

        .emoticon_element{
            cursor: pointer;

            svg{stroke: var(--text_color_secondary); pointer-events: none;}
            input{display: none;}

            input:checked + label{
                background-color: var(--active_section_color);
                border-bottom: 3px solid var(--bg_button_active_color);
                color: var(--bg_button_active_color);
            }
            
            input:checked + label > img{
                transform: scale(1.2);
                filter: drop-shadow(0 0 5px var(--bg_button_active_color));
            }

            input:checked + label > svg{
                stroke: var(--bg_button_active_color);
            }

            label{
                display: flex;
                align-items: center;
                color: var(--text_color_secondary);
                padding: 8px 12px 5px 12px;
                height: 100%;
                border: 2px solid transparent;
                border-bottom: 3px solid var(--bg_button_color);
                cursor: pointer;
                white-space: nowrap;

                img{
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    object-fit: contain;
                    margin-right: 10px;
                    pointer-events: none;
                }

                
                &:hover > svg {stroke: var(--bg_button_active_color);}
                &:hover {color: var(--bg_button_active_color);}
            }
        }
    }
</style>