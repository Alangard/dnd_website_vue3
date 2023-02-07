<template>

    <div class="comment_block">
        <div v-if="showEditableCommentForm == false && this.comment_item.comment_status == 'normal'"
            @click="StartEditComment">
            {{ this.comment_item.comment_text }}
        </div>

        <div class="banned" v-if="this.comment_item.comment_status == 'banned'">
            *Comment was deleted due to violation of the rules*
            <ul>
                <li v-for="report_reason in this.comment_item.report_reasons" :key="report_reason">
                    {{ report_reason }}
                </li>
            </ul>
        </div>

        <div v-if="this.comment_item.comment_status == 'deleted'">
            {{ this.comment_item.comment_text }}
        </div>
    </div>

    <form ref="comment_form" class="comment_form" action="" 
        @keydown.enter.prevent="sendEditedComment"
        @keydown.esc="endEditComment">

        <textarea id="comment_form_textarea"
            v-if="showEditableCommentForm == true"
            v-model="this.comment_text"
            rows="3"
            autofocus>
        </textarea>
    </form>
</template>

<script>
import { onClickOutside } from '@vueuse/core';
export default {
    props:['current_user_info', 'comment_item','comment_status'],
    data(){
        return{
            showNotEditableComment: true, // The style variable is responsible for displaying the finished version of the comment (true = p element, false = textarea)
            comment_text: this.comment_item.comment_text,
        }
    },

    mounted(){
        onClickOutside(this.$refs.comment_form, (event) => 
            this.endEditComment()
        )
    },

    methods:{
        //A method executed after the form has been accepted. 
        //Commits the date of the last change and changes the visibility variable of the final comment block
        sendEditedComment(){
            this.$emit('saveComment',{'comment_text':this.comment_text, 'date': this.$store.getters.getDatetimeNow});
            this.endEditComment();
        },

        //Method called after clicking on the finished comment, replacing the p block with textarea
        StartEditComment(){
            if(this.current_user_info.username == this.comment_item.user_info.username){ 
                this.showEditableCommentForm = true;
                this.$refs.comment_form.style.caretColor='var(--text_color_secondary)';
            }            
        },

        endEditComment(){
            this.showEditableCommentForm = false;
        },

        
    }
}
</script>

<style lang="scss" scoped>
.comment_form{
    width: 100%;

    textarea{
        resize:none;
        width: 100%;
        border: 2px solid var(--bg_button_color);
        border-radius: 5px;
        outline: none;

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

        &:hover{border-color: var(--bg_button_active_color);}

        &.empty{
            overflow: hidden;
        }
    }
}
.comment_block {
    margin: 0;
    word-wrap: break-word;
    width: 100%;
    padding: 0 5px 0 43px;
    height: inherit;
    border: 1px solid transparent;
    font-weight: 400;
    word-wrap: break-word;
    word-break: break-word;
    max-width: 690px;

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
}
</style>