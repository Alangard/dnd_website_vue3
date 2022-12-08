<template>
    <div class="container">
        <h3>{{ item.username }}</h3>
        <div class="container2">
            <img class="profile_img" src="https://source.unsplash.com/random" alt />
            <div class="container2_1">
                <p>{{ item.comment_text }}</p>
                <ul v-if="item.replies && item.replies.length > 0">
                    <CommentsItem 
                        v-for="(child, subIndex) in item.replies" 
                        v-bind:item="child"
                        :index="subIndex"
                        :key="child.id"
                        :parentItem="item"
                        @deleteReply="deleteReply"
                        />
                </ul>
            </div>
        </div>
        <button v-if="parentItem" @click="deleteReply">Delete reply</button>
        <button v-if="!parentItem" @click="this.$emit('deleteComment', this.index)">Delete comment</button>
        <button type="button" @click="addReply">Add reply</button>
  </div>
</template>

<script>
import CommentsItem from './CommentsItem.vue';
export default {
    components: { CommentsItem } ,
    props:['item', 'index', 'parentItem'],
    data(){
        return{
            comment_text: '',
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
                username: `Comment from User${id}${id}`,
                comment_text: this.comment_text,
                replies: []
            }
            this.item.replies.push(comment_data);
            this.comment_text = ''
        }
  }  
}
</script>

<style lang="scss" scoped>

.container{
    margin:10px;

    h3{font-weight: 700;}

    .container2{
        display: flex;
        align-items: center;

        .profile_img{
            height: 40px;
            width: 40px;
            object-fit: cover;
        }

        .container2_1{
            padding: 0 10px;
            
            p{
                text-align: left;
                font-weight: 700;
            }

            ul{
                list-style-type: none;
                margin: 0 10px;
            }

        }

    }

    button{
        padding: 2px 4px;
        margin-top: 1rem;
        color: #ffff;
        background-color: blue;
        border-radius: 5px;

        &:hover{
            background-color: rgb(3, 3, 173);
        }
    }

}

</style>