<template>
    <div class='main_container'>

        <div v-for='reactor in this.reactors_list' :key='reactor.username'>

            <div class='reactor_element'
                
                :class="{reacted: reactor.username == this.$store.getters.getUserInfo.username}">
                <!-- :class="{reacted: this.dataOfUserReaction}"> -->

                <div class="leftside_container">
                    <img class="profile_img"  v-if='reactor.profile_img_url != ""' :src="reactor.profile_img_url" alt="" 
                        @click="$router.push({ name: 'user', params: {id: reactor.username} })"
                    >

                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        v-else
                        class="profile_img" 
                        @click="$router.push({ name: 'user', params: {id: reactor.username} })">
                            <path d="M5.52 19c.64-2.2 1.84-3 3.22-3h6.52c1.38 0 2.58.8 3.22 3"/>
                            <circle cx="12" cy="10" r="3"/>
                            <circle cx="12" cy="12" r="10"/>
                    </svg>


                    <div class="user_info">
                        <span class='username' @click="$router.push({ name: 'user', params: {id: reactor.username} })">
                            {{this.$store.getters.capitalizeFirstLetter(reactor.username.split('.')[0])}}
                        </span>
                        <span class='datetime'>Reacted {{this.$store.getters.dateTimeFormat(reactor.date)}}</span>
                    </div>
                </div>
                
                <div class="rightside_container" v-if="this.btn_type =='totalReaction'">
                    <img :src="reactor.emot_url" alt="" :title="':'+ reactor.emot_id">
                </div>

            </div>
        </div>
        
    </div>

</template>

<script>

export default {
    props: ['reactors_list', 'post_id', 'btn_type'],
    data(){return{}},
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
            justify-content: space-between;
            background-color: var(--bg_button_color);
            border: 2px solid var(--bg_button_color);
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 5px;

            &:hover > .rightside_container img{
                transform: scale(1.2);
            }

            &.reacted > .leftside_container .profile_img, .rightside_container img{
                transform: scale(1.2);
            }

            &.reacted{
                border: 2px solid var(--bg_button_active_color);
            }

            &.reacted > .leftside_container .username{
                color: var(--bg_button_active_color);
            }

            .leftside_container{
                display: flex;
                flex-direction: row;

                &:hover > .profile_img {
                    transform: scale(1.2);
                }

                svg.profile_img{
                    background-color: var(--active_section_color);
                }

                .profile_img{
                    height: 45px;
                    width: 45px;
                    border-radius: 50%;
                    margin-right: 10px;
                    cursor: pointer;
                    background-color: #ffff;
                    stroke: var(--text_color_secondary);
                    object-fit: cover;
                }

                .user_info{
                    display: flex;
                    flex-direction: column;
                    .username:hover{
                        color: var(--bg_button_active_color);
                        cursor: pointer;
                    }

                    .datetime{
                        font-weight: 300;
                        font-size: 14px;
                    }
                }
            }

            .rightside_container img{
                width: 30px;
                height: 30px;
                border-radius: 50%;
                object-fit: contain;
            }
        }
        
    }
</style>