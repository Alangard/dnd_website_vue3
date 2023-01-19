<template>
    <div class="comment-item_container" 
        :class="{'comment_item_container_replied': this.parentItem != undefined,
                 'comment_item_container_replying': this.reply_btn_pressed == true}"
                 @keydown.esc="closeReplyCommentField">
        
        <div class="user-info_container">

            <img class="profile_img"  
                v-if='item.user_info.user_profile_img_url != ""' 
                :src="item.user_info.user_profile_img_url"
                @click="$router.push({ name: 'user', params: {id: item.user_info.username} })">
                        

            <svg class="profile_img"  xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                v-else
                @click="$router.push({ name: 'user', params: {id: item.user_info.username} })">
                    
                <path d="M5.52 19c.64-2.2 1.84-3 3.22-3h6.52c1.38 0 2.58.8 3.22 3"/>
                <circle cx="12" cy="10" r="3"/>
                <circle cx="12" cy="12" r="10"/>
            </svg>

            <div>
                <span class='username' 
                    @click="$router.push({ name: 'user', params: {id: item.user_info.username} })">
                    {{ this.$store.getters.capitalizeFirstLetter(item.user_info.username.split('.')[0]) }}
                </span>

                <span class='comment_date_container' v-if="this.editable_comment == false">
                    Commented {{ this.$store.getters.dateTimeFormat(item.date) }}
                </span>

                <span class='comment_date_container' v-if="this.editable_comment == true">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 14.66V20a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h5.34"></path>
                        <polygon points="18 2 22 6 12 16 8 16 8 12 18 2"></polygon>
                    </svg>
                    Last change {{ this.$store.getters.dateTimeFormat(item.date) }}
                </span>
            </div>

        </div>

    
        <div class="comment_field_container">

            <form ref="edit_comment_form" class="edit_comment_form" action="" 
                @keydown.enter.prevent="editComment">

                <textarea 
                    v-if="this.comment_is_visible == false"
                    v-model="this.item.comment_text"
                    rows="3"
                    autofocus>
                </textarea>

            </form>

            <p class="leaved_comment_section" 
                v-if="this.editable_comment == true && this.comment_is_visible == true" 
                @click="StartEditComment">
                {{ item.comment_text }}
            </p>
            
            <p class="leaved_comment_section" v-if="this.editable_comment == false">{{ item.comment_text }}</p>

            <div class="buttons_container">
                <button class='btn_delete' v-if="parentItem" @click="deleteReply">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        <line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line>
                    </svg>
                </button>
                <button class='btn_delete' v-if="!parentItem" @click="this.$emit('deleteComment', this.index)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        <line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line>
                    </svg>
                </button>


                <button class='btn_add_reply' type="button" @click="openReplyCommentField"> 
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 9l6 6-6 6"/><path d="M4 4v7a4 4 0 0 0 4 4h11"/>
                    </svg>
                    Reply
                </button>

                <button class='btn_share' type="button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="18" cy="5" r="3"></circle>
                        <circle cx="6" cy="12" r="3"></circle>
                        <circle cx="18" cy="19" r="3"></circle>
                        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
                    </svg>
                    Share
                </button>

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
                    @deleteReply="deleteReply"
                />
        </div>

    </div>
</template>

<script>
import { useDebouncedRefHistory } from '@vueuse/core';
import CommentsItem from './CommentsItem.vue';
export default {
    components: { CommentsItem } ,
    props:['item', 'index', 'parentItem', 'user_info'],
    data(){
        return{
            comment_text: '',
            editable_comment: true, // Variable limiting the ability to edit a comment
            comment_is_visible: true, // The style variable is responsible for displaying the finished version of the comment (true = p element, false = textarea)
            reply_btn_pressed: false,
        }
    },


    methods: {
        deleteReply() {
            this.parentItem.replies.splice(this.index, 1);
        },

        addReply(event) {
            const id = Math.floor(Math.random() * 100);
            const comment_data = {
                id,
                user_info: this.user_info,
                comment_text: this.comment_text,
                date: this.$store.getters.getDatetimeNow,
                replies: []
            }
            this.item.replies.push(comment_data);
            this.comment_text = ''

            this.closeReplyCommentField();
        },

        //A method executed after the form has been accepted. 
        //Commits the date of the last change and changes the visibility variable of the final comment block
        editComment(){
            this.item.date = this.$store.getters.getDatetimeNow;
            this.comment_is_visible = true;
        },

        //Method called after clicking on the finished comment, replacing the p block with textarea
        StartEditComment(){
            this.comment_is_visible = false;
            this.$refs.edit_comment_form.style.caretColor='var(--text_color_secondary)';
        },

        //A method called after clicking on the "reply" button. 
        //Calls the reply textbox and changes the styles and adds blur to comments outside the branch or non-parent 
        openReplyCommentField(event){
            this.reply_btn_pressed = true;
            this.comment_text = `@${this.$store.getters.capitalizeFirstLetter(this.user_info.username)}, `
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

    .comment_item_container_replied{
        padding: 0 0 0 35px;
    }

    .user-info_container{
        display: flex;
        flex-direction: row;

        .profile_img{
            height: 35px;
            width: 35px;
            margin: 0 5px 0 0;
            object-fit: cover;
            border-radius: 5px;
            stroke: var(--text_color_secondary);
            cursor: pointer;
        }

        div{
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            width: 100%;

            .username{
                font-weight: 700;
                font-size: 14px;
                line-height: 14px;
                cursor: pointer;
            }

            .comment_date_container{
                display: flex;
                flex-direction: row;
                align-items: flex-start;
                font-weight: 300;
                font-size: 13px;
                line-height: 13px;

                & svg{
                    height: 13px;
                    width: 13px;
                    stroke: var(--text_color_primary);
                    margin-right: 5px;
                }
            }
        }

    }

    .comment_field_container{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin: 8px;
        margin-left: 0px; 
        padding: 2px 0 0 0px;
        caret-color: transparent;

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
        }
        .buttons_container{
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: flex-end;
            width: 100%;
            margin-top: 3px;

            button{
                background-color: transparent;
                border: none;
                outline: none;
                font-weight: 300;
                font-size: 13px;
                line-height: 13px;
                color: var(--text_color_primary);
            }

            button > svg{
                height: 20px;
                width: 20px;
                stroke: var(--text_color_secondary);
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