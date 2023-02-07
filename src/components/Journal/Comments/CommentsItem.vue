<template>
    <div class="comment-item_container" 
        :class="{'comment_item_container_replied': this.parentItem != undefined,
                 'comment_item_container_replying': this.reply_btn_pressed == true}"
        @keydown.esc="closeReplyCommentField, closeEditComment">
    
        <comment-info-header
            :item="this.item"
            :user_info="this.user_info"
            @startEditComment="startEditComment"
            @showDeleteAlert="this.showAlert = true">
        </comment-info-header>
        
         <div class="comment_field_container">
                <comment-container 
                    :showEditableCommentForm="this.showEditableCommentForm"
                    :current_user_info="this.user_info" 
                    :comment_item="this.item"
                    @saveComment="saveComment">
                </comment-container>

            <div class="comment_footer_container">
                <div class='wrapper' v-if="item.comment_status == 'normal'">

                    <button class='btn_add_reply' type="button" @click="openReplyCommentField"> 
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 9l6 6-6 6"/><path d="M4 4v7a4 4 0 0 0 4 4h11"/>
                        </svg>
                        Reply
                    </button>

                   <div class="vote_container">
                        <button class="likes_btn" 
                            :class="{'pressed': user_leaved_rate && this.like_btn_pressed == true}"
                            @click="leave_like">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3">
                                </path>
                            </svg>
                        </button>

                        <span class="counter" 
                            :class="{'negative': item.rate_summ < 0, 'positive': item.rate_summ > 0}"
                            :title="`Positive votes: ${item.positive_rates_list.length}, negative votes: ${item.negative_rates_list.length}`">
                            {{ item.rate_summ }}
                        </span>

                        <button class="dislikes_btn"
                            :class="{'pressed': user_leaved_rate && this.dislike_btn_pressed == true}" 
                            @click="leave_dislike">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17">
                                </path>
                            </svg>
                        </button>
                    </div>



                </div>

            </div> 
        </div>

        <div class="replies_form_container" v-if="this.reply_btn_pressed == true">

            <form class='comment_form' action="" 
                @keydown.enter.prevent="addReply" 
                @submit.prevent="addReply">

                <img class="profile_img"  
                    v-if='user_info.user_profile_img_url != ""' 
                    :src="user_info.user_profile_img_url"
                    @click="$router.push({ name: 'user', params: {id: user_info.username} })">
                            

                <svg class="profile_img"  xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    v-else
                    @click="$router.push({ name: 'user', params: {id: user_info.username} })">
                        
                    <path d="M5.52 19c.64-2.2 1.84-3 3.22-3h6.52c1.38 0 2.58.8 3.22 3"/>
                    <circle cx="12" cy="10" r="3"/>
                    <circle cx="12" cy="12" r="10"/>
                </svg>

                <div class="comment_container">
                    <textarea id="comment_textarea" placeholder="Comment..." rows="1" title="leave a comment"
                        v-model="this.comment_text"
                        :class="{empty: this.comment_text == ''}"
                        @input="this.resize">
                    </textarea>
                    
                    <button class="reaction_btn" type="button">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 112.066 112.066">
                            <path d="M90.546,15.518C69.858-5.172,36.2-5.172,15.516,15.513C-5.172,36.198-5.17,69.858,15.518,90.547
                            c20.682,20.684,54.34,20.684,75.026-0.004C111.23,69.858,111.228,36.2,90.546,15.518z M84.757,84.758
                            c-17.493,17.494-45.961,17.496-63.455,0.002c-17.498-17.497-17.495-45.966,0-63.46C38.796,3.807,67.262,3.805,84.759,21.302
                            C102.253,38.796,102.251,67.265,84.757,84.758z M33.299,44.364h-3.552c-0.313,0-0.604-0.18-0.738-0.459
                            c-0.055-0.112-0.082-0.236-0.082-0.358c0-0.184,0.062-0.363,0.175-0.507l7.695-9.755c0.158-0.196,0.392-0.308,0.645-0.308
                            s0.486,0.111,0.641,0.304l7.697,9.757c0.189,0.237,0.229,0.58,0.1,0.859c-0.146,0.293-0.428,0.467-0.741,0.467h-3.554
                            c-0.181,0-0.351-0.083-0.463-0.225l-3.68-4.664l-3.681,4.664C33.648,44.281,33.479,44.364,33.299,44.364z M77.898,43.038
                            c0.188,0.237,0.229,0.58,0.1,0.859c-0.146,0.293-0.428,0.467-0.741,0.467h-3.554c-0.181,0-0.352-0.083-0.463-0.225l-3.681-4.664
                            l-3.681,4.664c-0.112,0.141-0.281,0.225-0.462,0.225h-3.552c-0.313,0-0.604-0.18-0.738-0.459c-0.055-0.112-0.082-0.236-0.082-0.358
                            c0-0.184,0.062-0.363,0.175-0.507l7.695-9.755c0.158-0.196,0.392-0.308,0.645-0.308c0.254,0,0.486,0.111,0.642,0.304L77.898,43.038
                            z M76.016,64.068c-3.843,8.887-12.843,14.629-22.927,14.629c-10.301,0-19.354-5.771-23.064-14.703
                            c-0.636-1.529,0.089-3.285,1.62-3.921c0.376-0.155,0.766-0.229,1.149-0.229c1.176,0,2.292,0.695,2.771,1.85
                            c2.776,6.686,9.655,11.004,17.523,11.004c7.69,0,14.528-4.321,17.42-11.011c0.658-1.521,2.424-2.222,3.944-1.563
                            C75.974,60.781,76.674,62.548,76.016,64.068z"/>
                        </svg>
                    </button>
                </div>

                <button class="send_comment_btn" type="submit">
                        <svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
                            <path d="M470.3,271.15,43.16,447.31a7.83,7.83,0,0,1-11.16-7V327a8,8,0,0,1,6.51-7.86l247.62-47c17.36-3.29,17.36-28.15,0-31.44l-247.63-47a8,8,0,0,1-6.5-7.85V72.59c0-5.74,5.88-10.26,11.16-8L470.3,241.76A16,16,0,0,1,470.3,271.15Z"/>
                        </svg>
                </button>

            </form>

        </div>

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

        <Alert
            v-if="this.showAlert"
            :alert_object="{'header': 'Delete comment', 'message': 'Are you sure you want to delete this comment?', 
                            'action':'Delete', 'crtiticality': 'error'}"
            @close_alert='showAlert = false'
            @doAction='this.deleteComment(), this.showAlert = false'>
        </Alert>
    </div>
</template>

<script>
import CommentsItem from './CommentsItem.vue';
import CommentInfoHeader from './CommentInfoHeader.vue';
import Dropdown from '@/components/Templates_components/Dropdown/Dropdown.vue';
import Alert from '@/components/Templates_components/Alert.vue';
import CommentContainer from './CommentContainer.vue';

export default {
    components: { CommentsItem, CommentInfoHeader, Dropdown, Alert, CommentContainer} ,
    props:['item', 'index', 'parentItem', 'user_info'],
    data(){
        return{
            showAlert: false,
            comment_text: '',
            like_btn_pressed: false,
            dislike_btn_pressed: false,
            hasPermission: this.item.user_info.username == this.user_info.username || this.user_info.user_role == 'admin', // Variable limiting the ability to edit a comment
            reply_btn_pressed: false,
        }
    },
    computed: {
        user_leaved_rate(){
            for(const element of Object.keys(this.item.rate)){
                if(element == this.user_info.username){
                    if(this.item.rate[element] > 0){
                        return this.like_btn_pressed = true;
                    }
                    else if(this.item.rate[element] < 0){
                        return this.dislike_btn_pressed = true;
                    }
                }
            }
        },
    },
    methods: {
    
        saveComment(comment_info){
            this.item.comment_text = comment_info.comment_text;
            this.item.date = comment_info.date;
        },


        deleteComment(){
            if(this.parentItem){
                // this.parentItem.replies.splice(this.index, 1);
                this.item.comment_status = 'deleted';
                this.item.comment_text ='*Comment was deleted*';

            }
            else{this.$emit('deleteComment', this.index);}
        },

        addReply(event) {
            const id = Math.floor(Math.random() * 100);
            const comment_data = {
                id,
                user_info: this.user_info,
                comment_text: this.comment_text,
                date: this.$store.getters.getDatetimeNow,
                comment_status:'normal',
                report_reasons:[],
                rate: {},
                rate_summ: 0,
                positive_rates_list: [],
                negative_rates_list: [],
                replies: []
            }
            this.item.replies.push(comment_data);
            this.comment_text = ''

            this.closeReplyCommentField();
        },

        //Method called after clicking on the finished comment, replacing the p block with textarea
        startEditComment(){
            if(this.item.report_reasons.length == 0){
                this.showNotEditableComment = false;
                document.querySelector('.edit_comment_form textarea').style.caretColor='var(--text_color_secondary)';
            }
        },

        closeEditComment(){
            this.showNotEditableComment = true;
        },

        //A method executed after the form has been accepted. 
        //Commits the date of the last change and changes the visibility variable of the final comment block
        sendEditedComment(){
            this.item.date = this.$store.getters.getDatetimeNow;
            this.showNotEditableComment = true;
            this.closeEditComment();
        },


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

        //Method to remove styles (blur comments not related to branch or parent)
        closeReplyCommentField(){
            const comment_item_el = document.querySelectorAll('.comment-item_container');
            for(let element of comment_item_el){element.style.filter ='blur(0)';}
            this.reply_btn_pressed = false;
        },      

        //A methods that increases the number of likes and dislikes and changes the class (style) of the button

        leave_like(){
            debugger
            if(this.user_info.username in this.item.rate){
                if(this.item.rate[this.user_info.username] <= 0){
                    this.item.rate[this.user_info.username] = 1;
                    this.item.negative_rates_list.shift(this.user_info.username);
                    this.item.positive_rates_list.push(this.user_info.username);
                    this.item.rate_summ += 2;
                    this.like_btn_pressed = true;
                    this.dislike_btn_pressed = false;
                }
                else if(this.item.rate[this.user_info.username] > 0){
                    delete this.item.rate[this.user_info.username];
                    this.item.positive_rates_list.shift(this.user_info.username);
                    this.item.rate_summ --;
                    this.like_btn_pressed = false;
                }
            }
            else{
                this.item.rate[this.user_info.username] = 1;
                this.item.positive_rates_list.push(this.user_info.username);
                this.item.rate_summ ++;
                this.like_btn_pressed = true;
                
            }
        },

        leave_dislike(){
            debugger
            if(this.user_info.username in this.item.rate){
                if(this.item.rate[this.user_info.username] < 0){
                    delete this.item.rate[this.user_info.username];
                    this.item.negative_rates_list.shift(this.user_info.username);
                    this.item.rate_summ ++;
                    this.dislike_btn_pressed = false;
                }
                else if(this.item.rate[this.user_info.username] >= 0){
                    this.item.rate[this.user_info.username] = -1;
                    this.item.positive_rates_list.shift(this.user_info.username);
                    this.item.negative_rates_list.push(this.user_info.username);
                    this.item.rate_summ += -2;
                    this.dislike_btn_pressed = true;
                    this.like_btn_pressed = false;
                }
            }
            else{
                this.item.rate[this.user_info.username] = -1;
                this.item.negative_rates_list.push(this.user_info.username);
                this.dislike_btn_pressed = true;
                this.item.rate_summ --;
            }
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


    .comment_item_container_replied{
        padding: 0 0 0 35px;
        margin-bottom: 0;

    }

    // .user-info_container{
    //     display: flex;
    //     flex-direction: row;
    //     margin-top: 6px;
    //     padding: 8px 5px 0 5px;
    //     border-top-left-radius: 5px;
    //     border-top-right-radius: 5px;
    //     background-color: var(--bg_button_color);

    //     .profile_img{
    //         height: 35px;
    //         width: 35px;
    //         margin: 0 5px 0 0;
    //         object-fit: cover;
    //         border-radius: 5px;
    //         stroke: var(--text_color_secondary);
    //         cursor: pointer;
    //     }

    //     .header_of_comment_info{
    //         display: flex;
    //         flex-direction: row;
    //         align-items: center;
    //         justify-content: space-between;
    //         width: 100%;

    //         .column_wrapper{
    //             display: flex;
    //             flex-direction: column;

    //             .username_and_role{
    //                 display:flex;
    //                 flex-direction: row;
    //                 justify-content: flex-start;
    //                 align-items: center;
    //                 font-weight: 700;
    //                 font-size: 13px;
    //                 line-height: 13px;
    //                 margin-bottom: 4px;
    //                 text-overflow: ellipsis;
    //                 overflow: hidden; 
    //                 white-space: nowrap;
        
    //                 cursor: pointer;

    //                 .user_role{
    //                     font-size: 11px;
    //                     margin-left: 10px;
    //                     padding: 1px 8px;
    //                     border-radius: 20px;
    //                     border: 1px solid var(--bg_button_active_color);
    //                     font-weight: 300;
    //                 }
    //             }

    //             .comment_date_container{
    //                 display: block;
    //                 flex-direction: row;
    //                 align-items: flex-start;
    //                 font-weight: 300;
    //                 margin-bottom: 6px;
    //                 font-size: 11px;
    //                 line-height: 12px;
    //                 text-overflow: ellipsis;
    //                 overflow: hidden; 
    //                 white-space: nowrap;
    //             }
    //         }

    //         .dropdown_btn_continer{
    //             display: none;
    //         }

    //     }

    // }

    .comment_field_container{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-left: 0px; 
        caret-color: transparent;
        background-color: var(--bg_button_color);
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;

        &:hover, &:active, &:focus{
            cursor:default;
        }

        &:hover > .leaved_comment_section{
            border: 1px solid var(--text_color_secondary);
            border-radius: 5px;
        }

        .edit_comment_form{
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

        .leaved_comment_section {
            margin: 0;
            word-wrap: break-word;
            width: 100%;
            padding: 0 5px;
            height: inherit;
            border: 1px solid transparent;

            &.banned{
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
        .comment_footer_container{
            width: 100%;
            margin-top: 3px;
            padding-left: 36px;
            margin-bottom: 8px;

            .wrapper{
                display: flex;
                flex-direction: row;
                align-items: center;
                justify-content: flex-start;
                .vote_container{
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    justify-content: space-between;
                    margin-right: 6px;
                    background-color: transparent;
                    border-radius: 5px;

                    .counter{
                        font-weight: 700;
                        font-size: 13px;
                        &.negative{color: #d42c2f;}
                        &.positive{color:#37ad6d;}
                    }

                    .likes_btn:hover > svg{stroke:#37ad6d;}
                    .dislikes_btn:hover > svg{stroke:#d42c2f;}

                    .likes_btn.pressed > svg{stroke:#37ad6d;}

                    .dislikes_btn.pressed > svg{stroke:#d42c2f;}

                }

                button{
                    border-radius: 5px;
                    padding: 2px 3px;
                    border: 2px solid transparent;
                    outline: none;
                    background-color: transparent;
                    font-weight: 700;
                    font-size: 13px;
                    line-height: 13px;
                    color: var(--text_color_secondary);
                    margin:6px;

                    &:hover {
                        color: var(--bg_button_active_color);
                        cursor:pointer;
                    }

                    &:hover > svg {stroke: var(--bg_button_active_color);}

                    svg{
                        height: 15px;
                        width: 15px;
                        stroke: var(--text_color_secondary);
                    }
                }
            }
        }
    
        


    }

    .replies_form_container{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: max-content;
        background-color: var(--bg_block_color);
        font-family: 'Lato', sans-serif;
        font-size: 17px;
        font-weight: 400;
        margin: 5px 0 5px 35px;
        color: var(--text_color_primary);

        .comment_form{
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            width: 100%;

            .profile_img{
                height: 35px;
                width: 35px;
                margin: 0 5px 0 0;
                object-fit: cover;
                border-radius: 5px;
                stroke: var(--text_color_secondary);
                cursor: pointer;
            }

            button{
                display: flex;
                padding: 0;
                border: none;
                background: none;
                cursor: pointer;

                svg{
                    height: 25px;
                    width: 25px;
                    fill: var(--text_color_secondary);
                }

                &:hover > svg {fill: var(--bg_button_active_color);} 
            }

            .comment_container{
                position: relative;
                width: 100%;

                textarea{
                    width: 100%;
                    max-height: 150px;
                    min-height: 30px;
                    padding: 5px 40px 5px 10px;
                    border: 2px solid var(--bg_button_color);
                    border-radius: 5px;
                    font-size: 15px;
                    font-weight: 400;
                    resize: none;
                    outline: none;
                    background-color: var(--bg_button_color);
                    color: var(--text_color_primary);
                    caret-color: var(--text_color_secondary);

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
                .reaction_btn{
                    position: absolute;
                    right: 10px;
                    bottom: 13px;
                }
            }
        
            .send_comment_btn{margin: 5px;}      
           
        }
    }

   

}

</style>