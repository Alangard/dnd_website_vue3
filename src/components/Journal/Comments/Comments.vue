<template>

    <div class="comments_items_container">
        <div>
            <CommentsItem 
                :item="item" 
                :index="index" 
                v-for="(item, index) in items" 
                :key="item.id"
                @deleteComment="deleteComment"/>
        </div>
        <form class='comment_form' action="" @keydown.enter.prevent="addComment" @submit.prevent="addComment">

                <label for="comment_textarea">Leave your comment</label>
                <div class="comment_text_container">
                    <textarea id="comment_textarea" placeholder="Comment..." rows="1" required title="leave a comment"
                        v-model="this.comment_text" 
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
                    <button class="send_comment_btn" type="submit">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460.003 460.003">
                            <path d="M455.608,4.394c-4.192-4.192-10.459-5.521-15.99-3.394L9.616,166.376c-5.624,2.163-9.409,7.482-9.607,13.505
                            c-0.199,6.023,3.225,11.58,8.694,14.11l175.93,81.379l81.379,175.93c2.46,5.318,7.782,8.703,13.612,8.703
                            c0.165,0,0.332-0.003,0.498-0.008c6.023-0.199,11.342-3.983,13.505-9.607L459.002,20.385C461.13,14.852,459.8,8.585,455.608,4.394
                            z M278.354,406.523l-68.807-148.751c-0.747-1.615-1.769-3.07-3.008-4.309L418.887,41.116L278.354,406.523z"/>
                        </svg>
                    </button>
                </div>
            
        </form>
        
    </div>
</template>

<script>
import CommentsItem from './CommentsItem.vue';
export default {
    components: { CommentsItem } ,
    data(){
        return{
            items: [],
            comment_text: '',
        }
    },


    methods: {
        addComment() {
            const id = Math.floor(Math.random() * 100);
            const comment_data = {
                id,
                username: `Comment from User${id}`,
                comment_text: this.comment_text,
                replies: []
            }
            this.items.push(comment_data);
            this.comment_text = ''
        },

        deleteComment(index) {
            this.items.splice(index, 1);
        },

        resize(event) {
            console.log(event)
            let element = event.target;

            element.style.height = "18px";
            element.style.height = element.scrollHeight + "px";
        },

  }
}

</script>

<style lang="scss" scoped> 
    .comments_items_container{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: max-content;
        margin-bottom: 15px;
        padding: 10px 10px 5px 10px;
        border-radius: 5px;
        background-color: var(--bg_block_color);
        box-shadow: var(--box_shadow);
        font-family: 'Lato', sans-serif;
        font-size: 17px;
        font-weight: 400;
        color: var(--text_color_primary);

        .profile_img{
            height: 40px;
            width: 40px;
            object-fit: cover;
        }

        .comment_form{
            display: flex;
            flex-direction: column;
            width: 100%;

            label{
                font-size: 17px;
                font-weight: 300;
                margin-left: 5px;
            }
            .comment_text_container{
                position: relative;
                display: flex;
                flex-direction: row;
                align-items: flex-end;
                justify-content: flex-start;

                textarea{
                    width: 100%;
                    max-height: 150px;
                    min-height: 52px;
                    padding: 5px 10px 5px 10px;
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
                    &::-webkit-scrollbar{width: 0.7vw;}

                    &::-webkit-scrollbar-track{
                        background-color: var(--bg_button_color);
                        border-radius: 5px;
                    }

                    &::-webkit-scrollbar-thumb{
                        background-color: var(--text_color_secondary);
                        border-radius: 5px;
                    }

                    &:hover{border-color: var(--bg_button_active_color);}   
                }

                button{
                    display: flex;
                    padding: 0;
                    border: none;
                    background: none;
                    cursor: pointer;

                    svg{
                        height: 24px;
                        width: 24px;
                        fill: var(--text_color_secondary);
                    }

                    &:hover > svg {fill: var(--bg_button_active_color);} 
                }
                .reaction_btn{
                    position: absolute;
                    right: 35px;
                    bottom: 7px;
                }

                .send_comment_btn{
                    margin: 0 0 5px 5px;
                    
                    svg{transform: rotate(45deg);}    
                }

                
            }
           
        }

    }
</style>
