<template>
    <div class='main_container'>

        <div class='reactor_element' v-for='reactor in this.reactors_list' :key='reactor.username'>

            <img class="profile_img" src="../../../../assets/test_blog_photo.png" alt="" 
                @click="$router.push({ name: 'user', params: {id: reactor.username} })"
            >

            <div class="user_info">
                <span class='username' @click="$router.push({ name: 'user', params: {id: reactor.username} })">
                    {{capitalizeFirstLetter(reactor.username.split('.')[0])}}
                </span>
                <span class='datetime'>Reacted on {{}}</span>
            </div>

        </div>
    </div>

</template>

<script>

export default {
    props: ['reactors_list'],
    data(){return{}},
    methods:{
        capitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        }
    }
    
}
</script>

<style lang="scss" scoped>
    .main_container{
        display: flex;
        flex-direction: column;
        color: var(--text_color_secondary);
        font-weight: 400;
        border-radius: 5px;

        .reactor_element{
            display: flex;
            flex-direction: row;
            align-items: center;
            background-color: var(--bg_button_color);
            border-radius: 5px;
            padding: 10px 5px;
            margin-bottom: 5px;

            &:hover > img {
                transform: scale(1.2);
            }

            img{
                height: 45px;
                width: 45px;
                border-radius: 50%;
                margin-right: 10px;
                cursor: pointer;
                background-color: #ffff;
                object-fit: cover;
            }

            .user_info{
                display: flex;
                flex-direction: column;

                span:hover{
                    color: var(--bg_button_active_color);
                    cursor: pointer;
                }

                .datetime{
                    font-weight: 300;
                    font-size: 14px;
                }

                
            }
        }
        
    }
</style>