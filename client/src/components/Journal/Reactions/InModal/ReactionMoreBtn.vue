<template>
    <long-press-btn class='reaction_more_block_section' 
        v-if="reaction.users_data.length != 0"
        :title="':' + reaction.emoticon_id"
        :class="{reacted: reaction_is_checked != -1}"
        @LongPressEvent="react">
    
        
        <input type="radio" name="emoticonGroup" :value="`${reaction.emoticon_id}`" :id="`${reaction.emoticon_id}`">
        <label :for="`${reaction.emoticon_id}`">
            <img :src="reaction.emoticon_url" :alt="`:${reaction.emoticon_id}`">
            <span>{{reaction.users_data.length}}</span>
        </label>
    </long-press-btn>
</template>

<script setup>
import LongPressBtn from '@/components/Templates_components/LongPressBtn.vue';

import { computed, defineProps, defineEmits, getCurrentInstance } from 'vue';

const props = defineProps(['user_info']);
const emit = defineEmits(['react']);
const instance = getCurrentInstance();

const reaction = typeof instance.vnode.key === 'symbol' ? String(instance.vnode.key) : instance.vnode.key;
const reaction_is_checked = computed(() => reaction.users_data.findIndex(element => element.username == props.user_info.username));

function react(){emit('react', {"emoticon_id": reaction.emoticon_id, "emoticon_url":reaction.emoticon_url});}


</script>



<!-- // import LongPressBtn from '@/components/Templates_components/LongPressBtn.vue'

// export default {
//     components: { LongPressBtn },

//     props:['isMobile', 'user_info'],

//     data(){
//         return{
//             reaction: this.$.vnode.key,
//         }
//     },

//     computed:{

//         //Get the object index of the user of the current session who left this response. Use to set the styles
//         reaction_is_checked(){
//             const user_index = this.reaction.users_data.findIndex(element => element.username == this.user_info.username);
//             return user_index;
//         }
//     },

//     methods:{

//         //A method that leaves a user reaction. Click handling proccessing in the ReactionMore component
//         react(){
//             this.$emit('react', {"emoticon_id":this.reaction.emoticon_id, "emoticon_url":this.reaction.emoticon_url});
//         },
//     }
// 
// -->

<style lang="scss" scoped>
.reaction_more_block_section{
    cursor: pointer;

    svg{stroke: var(--text_color_secondary); pointer-events: none;}
    input{display: none;}

    label{
        display: flex;
        position: relative;
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

    &.reacted input + label img{
        filter: drop-shadow(0 0 5px var(--bg_button_active_color));
    }

    &.reacted input + label{
        color:var(--bg_button_active_color);
    }

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
}
</style>
