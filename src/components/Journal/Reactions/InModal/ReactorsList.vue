<template>
    <div class='main_container' v-bind="containerProps">
        <div class="wrapperProps" v-bind="wrapperProps"> 
        
            <div v-for="reactor in list" :key="reactor">

                <div class='reactor_element'
                    :class="{reacted: reactor.data.username == store.getters.getUserInfo.username}">

                    <div class="leftside_container">
                        <img class="profile_img"  v-if='reactor.data.user_profile_img_url != ""' :src="reactor.data.user_profile_img_url" alt="" 
                            @click="$router.push({ name: 'user', params: {id: reactor.data.username} })"
                        >

                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            v-else
                            class="profile_img" 
                            @click="$router.push({ name: 'user', params: {id: reactor.data.username} })">
                                <path d="M5.52 19c.64-2.2 1.84-3 3.22-3h6.52c1.38 0 2.58.8 3.22 3"/>
                                <circle cx="12" cy="10" r="3"/>
                                <circle cx="12" cy="12" r="10"/>
                        </svg>


                        <div class="user_info">
                            <span class='username' @click="$router.push({ name: 'user', params: {id: reactor.data.username} })">
                                {{store.getters.capitalizeFirstLetter(reactor.data.username.split('.')[0])}}
                            </span>
                            <span class='datetime'>Reacted {{ useTimeAgo(new Date(reactor.data.reaction_date)).value }}</span>
                        </div>
                    </div>
                    
                    <div class="rightside_container" v-if="chosen_section =='total_reactions_count'">
                        <img :src="reactor.data.emoticon_url" alt="" :title="':'+ reactor.data.emoticon_id">
                    </div>

                </div>
            </div>
        </div>
        
    </div>

</template>


<script setup>
    import { defineProps, computed  } from 'vue'
    import { useStore} from 'vuex'
    import { useVirtualList, useInfiniteScroll, useTimeAgo } from '@vueuse/core';

    const props = defineProps(['reactors_list_prop','chosen_section']);
    const store = useStore();

    const reactors_list = computed(() => props.reactors_list_prop); //read docs https://vueuse.org/core/usevirtuallist/#reactive-list
    const { list, containerProps, wrapperProps } = useVirtualList(reactors_list, {itemHeight: 74});

    // useInfiniteScroll(
    //     containerProps.ref, 
    //     () => {
    //         // load more
    //         //take the data pack from the database, following the username and date of the last item in current reactors_list (identifier in the database)
    //         const response_reactions_data = []
    //         reactors_list.push(response_reactions_data);
    //     },
    //     {distance: 10} //in pixels
    // )


</script>

<style lang="scss" scoped>
    .main_container{
        display: flex;
        flex-direction: column;
        height: auto;
        padding-right: 5px;
        max-height: 350px;
        overflow: hidden;
        border-radius: 5px;
        color: var(--text_color_secondary);
        font-weight: 400;


        &:hover, &:focus{
            overflow-y: scroll;
        }
        
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

        &.mobile{
            overflow-y: scroll;
        }


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