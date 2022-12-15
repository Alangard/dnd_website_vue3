<template>
    <div class="comment-item_container">
        
        <div class="user-info_container">

            <img class="profile_img"  
                v-if='item.user_info.profile_img_url != ""' 
                :src="item.user_info.profile_img_url"
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

                <span class='comment_date_container' v-if="this.edit == false">
                    Commented {{ this.$store.getters.dateTimeFormat(item.date) }}
                </span>

                <span class='comment_date_container' v-if="this.edit == true">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 14.66V20a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h5.34"></path>
                        <polygon points="18 2 22 6 12 16 8 16 8 12 18 2"></polygon>
                    </svg>
                    Last change {{ this.$store.getters.dateTimeFormat(item.date) }}
                </span>
            </div>

        </div>

    
        <div class="comment_field_container">
            <p>{{ item.comment_text }}</p>
        </div>
        <button v-if="parentItem" @click="deleteReply">Delete</button>
        <button v-if="!parentItem" @click="this.$emit('deleteComment', this.index)">Delete</button>
        <button type="button" @click="addReply">Add</button>

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
import CommentsItem from './CommentsItem.vue';
export default {
    components: { CommentsItem } ,
    props:['item', 'index', 'parentItem', 'user_info'],
    data(){
        return{
            comment_text: '',
            edit: true
        }
    },


    methods: {
        deleteReply() {
            this.parentItem.replies.splice(this.index, 1);
        },

        addReply() {
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
        },

        
  }  
}
</script>

<style lang="scss" scoped>

.comment-item_container{
    display: flex;
    flex-direction: column;
    padding:10px;
    width: 100%;

    .user-info_container{
        display: flex;
        flex-direction: row;

        &:hover > .profile_img{
            box-shadow: var(--box_shadow);
            transform: scale(1.1);
        }

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
        margin:10px 0 0 5px;
        
        p {
            word-wrap: break-word;
            width: 100%;
        }

    }

   

}

</style>