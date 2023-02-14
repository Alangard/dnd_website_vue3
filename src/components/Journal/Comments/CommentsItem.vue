<template>
    <div class="comment-item_container" 
        :class="{'replied': this.parentItem != undefined,
                 'replying': this.reply_btn_pressed == true}"
        @keydown.esc="closeReplyCommentField, closeEditComment">

        <div class="comment_header">
            <comment-info-header
                :item="this.item"
                :user_info="this.user_info"
                @startEditComment="startEditComment"
                @showDeleteAlert="this.showAlert = true">
            </comment-info-header>
        </div>
        
        <div class="comment_body">
            <comment-container 
                :showNotEditableComment="this.showNotEditableComment"
                :current_user_info="this.user_info" 
                :comment_item="this.item"
                :parentItem="this.parentItem"
                @startEditComment="startEditComment"
                @saveComment="saveComment"
                @sendEditedComment="sendEditedComment"
                @endEditComment="this.showNotEditableComment = false" 
                >
            </comment-container>
        </div>

        <div class="comment_footer">
            <comment-footer
                :comment_item="this.item"
                :user_info="this.user_info"
                @openReplyCommentField="openReplyCommentField">
            </comment-footer>
        </div>

        <reply-text-form
            v-if="this.reply_btn_pressed == true"
            :user_info="this.user_info"
            :comment_item="this.item"
            :comment="this.comment_text"
            @closeReplyCommentField="closeReplyCommentField">
        </reply-text-form>

        <div v-if="this.item.replies.length >= 3">
            <collapsable-replies :item_id="this.item.id" :replies_count="item.replies.length">
                <template #collapse_body>
                    <div v-if="item.replies && item.replies.length > 0">
                        <CommentsItem 
                            v-for="(child, subIndex) in item.replies" 
                            v-bind:item="child"
                            :index="subIndex"
                            :key="child.id"
                            :parentItem="item"
                            :user_info="this.user_info"
                            @deleteComment="deleteComment"
                        />
                    </div>
                </template>
            </collapsable-replies>
        </div>

        <div v-else>
            <div v-if="item.replies && item.replies.length > 0">
                <CommentsItem 
                    v-for="(child, subIndex) in item.replies" 
                    v-bind:item="child"
                    :index="subIndex"
                    :key="child.id"
                    :parentItem="item"
                    :user_info="this.user_info"
                    @deleteComment="deleteComment"
                />
            </div>
        </div>

        <Alert
            v-if="this.showAlert"
            :alert_object="{'header': 'Delete comment', 'message': 'Are you sure you want to delete this comment?', 
                            'action':'Delete', 'crtiticality': 'error'}"
            @close_alert='showAlert = false'
            @doAction='this.deleteComment(), this.showAlert = false'>
        </Alert>

        <swipe-bottom-sheet 
            v-if="this.showBottomSheet == true"
            @close_bottomSheet="this.showBottomSheet = false">
        </swipe-bottom-sheet>
    </div>
</template>

<script>
import CommentsItem from './CommentsItem.vue';
import CommentInfoHeader from './CommentInfoHeader.vue';
import CommentFooter from './CommentFooter.vue'
import ReplyTextForm from './ReplyTextForm.vue';
import Dropdown from '@/components/Templates_components/Dropdown/Dropdown.vue';
import Alert from '@/components/Templates_components/Alert.vue';
import CommentContainer from './CommentContainer.vue';
import CollapsableReplies from './CollapsableReplies.vue';
import SwipeBottomSheet from '@/components/Templates_components/BottomSheet/SwipeBottomSheet.vue';

export default {
    components: { CommentsItem, CommentInfoHeader, Dropdown, Alert, CommentContainer, CommentFooter, ReplyTextForm, CollapsableReplies, SwipeBottomSheet},
    props:['item', 'index', 'parentItem', 'user_info'],
    data(){
        return{
            showAlert: false,
            comment_text:'',
            reply_btn_pressed: false,
            showNotEditableComment: false,
            showBottomSheet: true,
        }
    },

    methods: {

        //A method called after clicking on the "reply" button. 
        //Calls the reply textbox and changes the styles and adds blur to comments outside the branch or non-parent 
        openReplyCommentField(event){
            this.reply_btn_pressed = true;
            this.comment_text = `@${this.$store.getters.capitalizeFirstLetter(this.item.user_info.username)}, `
            const comment_item_el = document.querySelectorAll('.comment-item_container');
            for(let element of comment_item_el){
                    if(!element.contains(event.target)){element.style.filter='blur(2px)';}
            }
            
        },
    
        saveComment(comment_info){
            debugger
            this.item.comment_text = comment_info.comment_text.split(',')[1];
            this.item.date = comment_info.date;
        },


        deleteComment(){
            if(this.parentItem){
                // this.parentItem.replies.splice(this.index, 1);
                this.item.comment_status = 'deleted';
                this.item.comment_text ='*Comment was deleted by author*';

            }
            else{this.$emit('deleteComment', this.index);}
        },

        banComment(){},


        //Method called after clicking on the finished comment, replacing the p block with textarea
        startEditComment(){
            debugger
            if(this.item.report_reasons.length == 0){
                this.showNotEditableComment = true;
            }
        },

        closeEditComment(){
            debugger
            this.showNotEditableComment = false;
        },

        //A method executed after the form has been accepted. 
        //Commits the date of the last change and changes the visibility variable of the final comment block
        sendEditedComment(comment_text){
            debugger
            this.item.date = this.$store.getters.getDatetimeNow;
            this.item.comment_text = comment_text
            this.closeEditComment();
        },

        //Method to remove styles (blur comments not related to branch or parent)
        closeReplyCommentField(){
            debugger
            const comment_item_el = document.querySelectorAll('.comment-item_container');
            for(let element of comment_item_el){element.style.filter='blur(0)';}
            this.reply_btn_pressed = false;
        },      

      
       
  }
}
</script>

<style lang="scss" scoped>
.comment-item_container{
    display: flex;
    flex-direction: column;
    padding:0 10px 0 10px;
    width: 100%;
    caret-color: transparent;
    margin-bottom: 8px;

    &.replied{
        padding: 0 0 0 35px;
        margin-bottom: 0;

    }

    &.replying:not(.replied){
        
        .comment_body{
            filter:blur(0) !important;
        }
    }
}

</style>