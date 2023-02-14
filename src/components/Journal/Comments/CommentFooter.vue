<template>
    <div class="comment_footer_container">
        <div class='wrapper' v-if="comment_item.comment_status == 'normal'">

            <button class='btn_add_reply' type="button" @click="this.$emit('openReplyCommentField', $event)"> 
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
                    :class="{'negative': comment_item.rate_summ < 0, 'positive': comment_item.rate_summ > 0}"
                    :title="`Positive votes: ${comment_item.positive_rates_list.length}, negative votes: ${comment_item.negative_rates_list.length}`">
                    {{ comment_item.rate_summ }}
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
</template>

<script>

export default {
    props:['comment_item','user_info'],
    data(){
        return{
            like_btn_pressed: false,
            dislike_btn_pressed: false,
        }
    },
    computed: {
        //A method indicating whether a comment has been rated by the current user
        user_leaved_rate(){
            for(const element of Object.keys(this.comment_item.rate)){
                if(element == this.user_info.username){
                    if(this.comment_item.rate[element] > 0){
                        return this.like_btn_pressed = true;
                    }
                    else if(this.comment_item.rate[element] < 0){
                        return this.dislike_btn_pressed = true;
                    }
                }
            }
        },
    },
    methods: {

        //A methods that increases the number of likes and dislikes and changes the class (style) of the button
        leave_like(){
            debugger
            if(this.user_info.username in this.comment_item.rate){
                if(this.comment_item.rate[this.user_info.username] <= 0){
                    this.comment_item.rate[this.user_info.username] = 1;
                    this.comment_item.negative_rates_list.shift(this.user_info.username);
                    this.comment_item.positive_rates_list.push(this.user_info.username);
                    this.comment_item.rate_summ += 2;
                    this.like_btn_pressed = true;
                    this.dislike_btn_pressed = false;
                }
                else if(this.comment_item.rate[this.user_info.username] > 0){
                    delete this.comment_item.rate[this.user_info.username];
                    this.comment_item.positive_rates_list.shift(this.user_info.username);
                    this.comment_item.rate_summ --;
                    this.like_btn_pressed = false;
                }
            }
            else{
                this.comment_item.rate[this.user_info.username] = 1;
                this.comment_item.positive_rates_list.push(this.user_info.username);
                this.comment_item.rate_summ ++;
                this.like_btn_pressed = true;
                
            }
        },

        leave_dislike(){
            debugger
            if(this.user_info.username in this.comment_item.rate){
                if(this.comment_item.rate[this.user_info.username] < 0){
                    delete this.comment_item.rate[this.user_info.username];
                    this.comment_item.negative_rates_list.shift(this.user_info.username);
                    this.comment_item.rate_summ ++;
                    this.dislike_btn_pressed = false;
                }
                else if(this.comment_item.rate[this.user_info.username] >= 0){
                    this.comment_item.rate[this.user_info.username] = -1;
                    this.comment_item.positive_rates_list.shift(this.user_info.username);
                    this.comment_item.negative_rates_list.push(this.user_info.username);
                    this.comment_item.rate_summ += -2;
                    this.dislike_btn_pressed = true;
                    this.like_btn_pressed = false;
                }
            }
            else{
                this.comment_item.rate[this.user_info.username] = -1;
                this.comment_item.negative_rates_list.push(this.user_info.username);
                this.dislike_btn_pressed = true;
                this.comment_item.rate_summ --;
            }
        },
    }
}
</script>

<style lang="scss" scoped>
.comment_footer_container{
    width: 100%;
    padding-left: 36px;
    margin-bottom: 8px;
    background-color: var(--bg_button_color);
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;

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
</style>