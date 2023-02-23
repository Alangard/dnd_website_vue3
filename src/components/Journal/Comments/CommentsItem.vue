<template>
    <div class="comment-item_container" 
        :class="{'replied': props.parentItem != undefined,
                 'replying': reply_btn_pressed  == true}"
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
                :showNotEditableComment="showNotEditableComment"
                :comment_item="props.item"
                :parentItem="props.parentItem"
                @sendEditedComment="sendEditedComment"
                @endEditComment="showNotEditableComment = false" 
                >
            </comment-container>
        </div>

        <div class="comment_footer">
            <comment-footer
                :comment_item="props.item"
                :user_info="props.user_info"
                @openReplyCommentField="openReplyCommentField">
            </comment-footer>
        </div>

        <reply-text-form
            v-if="reply_btn_pressed == true"
            :user_info="props.user_info"
            :comment_item="props.item"
            :comment="comment_text"
            @closeReplyCommentField="closeReplyCommentField">
        </reply-text-form>

        <div v-if="props.item.replies.length >= 3">
            <collapsable-replies :item_id="props.item.id">
                <template #collapse_body>
                    <div v-if="props.item.replies && props.item.replies.length > 0">
                        <CommentsItem 
                            v-for="(child, subIndex) in props.item.replies" 
                            v-bind:item="child"
                            :index="subIndex"
                            :key="child.id"
                            :parentItem="item"
                            :user_info="props.user_info"
                            @deleteComment="deleteComment"
                        />
                    </div>
                </template>
            </collapsable-replies>
        </div>

        <div v-else>
            <div v-if="props.item.replies && props.item.replies.length > 0">
                <CommentsItem 
                    v-for="(child, subIndex) in props.item.replies" 
                    v-bind:item="child"
                    :index="subIndex"
                    :key="child.id"
                    :parentItem="item"
                    :user_info="props.user_info"
                    @deleteComment="deleteComment"
                />
            </div>
        </div>
    </div>

    <Alert class="delete_alert_modal"
        v-if="this.showAlert"
        :alert_object="{'header': 'Delete comment', 'message': 'Are you sure you want to delete this comment?', 
                        'action':'Delete', 'crtiticality': 'error'}"
        @close_alert='showAlert = false'
        @doAction='this.deleteComment(), this.showAlert = false'>
    </Alert>

    <swipe-bottom-sheet class="swipe_bottom_sheet"
        v-if="showBottomSheet == true"
        @close_bottomSheet="showBottomSheet = false">
    </swipe-bottom-sheet>
</template>


<script setup>
import CommentsItem from './CommentsItem.vue';
import CommentInfoHeader from './CommentInfoHeader.vue';
import CommentFooter from './CommentFooter.vue'

// import ReplyTextForm from './ReplyTextForm.vue';
// import SwipeBottomSheet from '@/components/Templates_components/BottomSheet/SwipeBottomSheet.vue';
// import Alert from '@/components/Templates_components/Alert.vue';
import CommentContainer from './CommentContainer.vue';
import CollapsableReplies from './CollapsableReplies.vue';


import { ref, defineProps, defineEmits, defineAsyncComponent, inject, watch} from 'vue'
import { useStore } from 'vuex';

const ReplyTextForm = defineAsyncComponent(() => import('./ReplyTextForm.vue'));
const SwipeBottomSheet = defineAsyncComponent(() => import('@/components/Templates_components/BottomSheet/SwipeBottomSheet.vue'));
const Alert = defineAsyncComponent(() => import('@/components/Templates_components/Alert.vue'));


const props = defineProps(['item', 'index', 'parentItem', 'user_info']);
const emit = defineEmits(['deleteComment']);
const store = useStore();

let showAlert = ref(false);
let comment_text = ref('');
let reply_btn_pressed = ref(false);
let showNotEditableComment = ref(false);
let showBottomSheet = ref(true);



//A method called after clicking on the "reply" button. 
//Calls the reply textbox and changes the styles and adds blur to comments outside the branch or non-parent 
function openReplyCommentField(event){
    debugger
    reply_btn_pressed.value = true;
    comment_text.value = `@${store.getters.capitalizeFirstLetter(props.item.user_info.username)}, `
    const comment_item_el = document.querySelectorAll('.comment-item_container');
    for(let element of comment_item_el){
            if(!element.contains(event.target)){element.style.filter='blur(2px)';}
    }
    
}

function saveComment(comment_info){
    debugger
    props.item.comment_text = comment_info.comment_text.split(',')[1];
    props.item.date = comment_info.date;
};

function deleteComment(){
    debugger
    if(props.parentItem){
        // this.parentItem.replies.splice(this.index, 1);
        props.item.comment_status = 'deleted';
        props.item.comment_text ='*Comment was deleted by author*';
    }
    else{emit('deleteComment', props.index);}
};

function banComment(){};

//Method called after clicking on the finished comment, replacing the p block with textarea
function startEditComment(){
    debugger
    if(props.item.report_reasons.length == 0){showNotEditableComment.value = true;}
};

function closeEditComment(){
    debugger
    showNotEditableComment.value = false;
};

//A method executed after the form has been accepted. 
//Commits the date of the last change and changes the visibility variable of the final comment block
function sendEditedComment(comment_text){
    debugger
    props.item.date = store.getters.getDatetimeNow;
    props.item.comment_text = comment_text
    closeEditComment();
};

//Method to remove styles (blur comments not related to branch or parent)
function closeReplyCommentField(){
    debugger
    const comment_item_el = document.querySelectorAll('.comment-item_container');
    for(let element of comment_item_el){element.style.filter='blur(0)';}
    reply_btn_pressed.value = false;
};    
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

.delete_alert_modal{
    position: fixed;
}

</style>