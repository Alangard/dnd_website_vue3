<template>

    <div class="replies_form_container">
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
                    :class="{empty: this.comment_text == ''}">
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
</template>

<script>
export default {
    props:['comment_item','user_info','comment'],
    data(){
        return{
            comment_text: this.comment,
        }
    },
    methods:{
        addReply(event) {
            const id = Math.floor(Math.random() * 100);
            const comment_data = {
                id,
                user_info: this.user_info,
                comment_text: this.comment_text.split(',')[1],
                date: this.$store.getters.getDatetimeNow,
                comment_status:'normal',
                report_reasons:[],
                rate: {},
                rate_summ: 0,
                positive_rates_list: [],
                negative_rates_list: [],
                replies: []
            }
            this.comment_item.replies.push(comment_data);
            this.comment_text = ''

            const comment_item_el = document.querySelectorAll('.comment-item_container');
            for(let element of comment_item_el){element.style.filter ='blur(0)';}
            this.$emit('closeReplyCommentField');
        },

    }    
}
</script>

<style lang="scss" scoped>
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
</style>

