<template>

    <div class="comment_block" 
        :class="{'banned':this.comment_item.comment_status == 'banned', 'deleted':this.comment_item.comment_status == 'deleted'}">
        <div v-if="showNotEditableComment== false && this.comment_item.comment_status == 'normal'">
            <span>
                <span class="parent_username" 
                    v-if="this.parentItem != undefined"
                    @click="$router.push({ name: 'user', params: {id: this.parentItem.user_info.username} })">
                    @{{this.parentItem.user_info.username}},  
                </span>
                <span>{{this.comment_item.comment_text}}</span>
            </span>
        </div>

        <div class="banned" v-if="this.comment_item.comment_status == 'banned'">
            *Comment was deleted due to violation of the rules*
            <ul>
                <li v-for="report_reason in this.comment_item.report_reasons" :key="report_reason">
                    {{ report_reason }}
                </li>
            </ul>
        </div>

        <div class="deleted" v-if="this.comment_item.comment_status == 'deleted'">
            {{ this.comment_item.comment_text }}
        </div>
    </div>

    <form ref="comment_form" class="comment_form" action="" 
        @keydown.enter.prevent="this.$emit('sendEditedComment', comment_text)"
        @keydown.esc="this.$emit('endEditComment')">

        <textarea
            v-if="this.showNotEditableComment == true"
            v-model="this.comment_text"
            rows="3"
            autofocus>
        </textarea>
    </form>
</template>

<script>
import { onClickOutside } from '@vueuse/core';
export default {
    props:['current_user_info', 'comment_item','parentItem', 'showNotEditableComment'],
    data(){
        return{
            comment_text: this.comment_item.comment_text,
        }
    },

    mounted(){
        onClickOutside(this.$refs.comment_form, (event) => 
            this.$emit('endEditComment')
        )
    },
}
</script>

<style lang="scss" scoped>
.comment_form{
    width: 100%;
    padding: 0 5px 0 43px;
    background-color: var(--bg_button_color);

    textarea{
        resize:none;
        width: 100%;
        border: 2px solid  var(--bg_button_active_color);
        border-radius: 5px;
        background-color: transparent;
        outline: none;
        caret-color: var(--text_color_secondary);
        color: var(--text_color_primary);

        scroll-behavior: smooth;
        &::-webkit-scrollbar{
            width: 0.7vw; 
            max-width: 5px;
        }

        &::-webkit-scrollbar-track{
            background-color: var(--bg_button_color);
            border-radius: 5px;
        }

        &::-webkit-scrollbar-thumb{
            background-color: var(--text_color_secondary);
            border-radius: 5px;
        }

        &.empty{
            overflow: hidden;
        }
    }
}
.comment_block {
    display: block;
    width: 100%;
    max-width: 690px;
    height: inherit;
    margin: 0;
    padding: 0 5px 3px 43px;
    border: 1px solid transparent;
    font-weight: 400;
    word-wrap: break-word;
    word-break: break-word;
    caret-color: transparent;
    background-color: var(--bg_button_color);

    &.banned, &.deleted{
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
    }

    .banned{
        font-weight: bold;
        color: var(--error_color);

        ul{
            margin: 0;
            li{ 
                font-style: normal;
                font-weight: 300;
            }
        }
    }

    .deleted{
        font-weight: bold;
        color: var(--error_color);
    }

    .parent_username{
        cursor: pointer;
        font-weight: 700;

        &:hover{color: var(--bg_button_active_color);}
    }
}
</style>