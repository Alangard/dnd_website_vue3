<template>
    <div class="main-container" 
        :class="{'light-theme': store.getters.getTheme =='light', 'dark-theme':store.getters.getTheme =='dark'}">
        
        <div class="rightside_container">
            <div class="autor_data_container">
                    <img class="profile_img" :src="key.data.creator_profile_img_url" alt="" 
                        v-if="key.data.creator_profile_img_url != ''"
                        @click="$router.push({ name: 'user', params: {id: key.data.creator_nickname} })"
                    >

                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        v-else
                        class="profile_img" 
                        @click="$router.push({ name: 'user', params: {id: key.data.creator_nickname} })">
                            <path d="M5.52 19c.64-2.2 1.84-3 3.22-3h6.52c1.38 0 2.58.8 3.22 3"/>
                            <circle cx="12" cy="10" r="3"/>
                            <circle cx="12" cy="12" r="10"/>
                    </svg>

                    <span class="profile_name"
                        @click="$router.push({ name: 'user', params: {id: key.data.creator_nickname} })">
                        {{store.getters.capitalizeFirstLetter(key.data.creator_nickname.split('.')[0])}}
                    </span> 

                    <span class="dot_divider">•</span>
                    <span class="post_date">Posted {{useTimeAgo(new Date(key.data.post_date)).value}}</span>
            </div>

            <div class="title_field"
                @click="$router.push({ name: 'postitem', params: {id: key.data.post_id} })">
                {{store.getters.capitalizeFirstLetter(key.data.title)}}
            </div>

            <img class="post_img" :src="key.data.post_img_url" alt='post_img'
                v-if="key.data.post_img_url"
                @click="$router.push({ name: 'postitem', params: {id: key.data.post_id} })">

            <div class="description_field">{{store.getters.capitalizeFirstLetter(key.data.description)}}</div>

        </div>

        <div class="bottom_container">

            <EmoticonContainer
                @click="modalIsOpen =! modalIsOpen"
                :short_post_data_reactions = 'key.reactions' 
                :post_id='key.data.post_id'>
            </EmoticonContainer>

            <Transition name='modal'>

                <ReactionModal
                    v-if="modalIsOpen"
                    @close_modal='modalIsOpen = false'
                    :post_id='key.data.post_id'>
                </ReactionModal>

            </Transition>

            <div class="user_activities_rightside_container">
                <div class="comments_container"
                    :class="{commented: key.comments.commented}"
                    @click="$router.push({ name: 'postitem', params: {id: key.data.post_id} })">

                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                        </svg>
                        <span>{{key.comments.counter}}</span>
                </div>
            
                <WebShare></WebShare>

            </div>
        </div>
    </div>

</template>

<script setup>
import { ref, defineAsyncComponent, getCurrentInstance } from 'vue';
import { useStore } from 'vuex';
import { useTimeAgo } from '@vueuse/core';

const ReactionModal = defineAsyncComponent(() => import('@/components/Journal/Reactions/ReactionModal.vue'));
const EmoticonContainer = defineAsyncComponent(() => import( './Reactions/EmoticonContainer.vue'));
const WebShare = defineAsyncComponent(() => import('./Share/WebShare.vue'));

const modalIsOpen = ref(false);
const store = useStore();
const instance = getCurrentInstance();

const key = typeof instance.vnode.key === 'symbol' ? String(instance.vnode.key) : instance.vnode.key;
</script>

<style lang="scss" scoped>

.modal-enter-active,
.modal-leave-active{
    transition: all 0.25s ease;
}

.modal-enter-from,
.modal-leave-to{
    opacity: 0;
    transform: scale(1.1);
}

.main-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    height: max-content;
    margin-bottom: 15px;
    padding: 10px 10px 5px 10px;
    border-radius: 5px;

    background-color: var(--bg_block_color);

    box-shadow: var(--box_shadow);

    caret-color: transparent;
    font: var(--font_header);

        .rightside_container{
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            width: auto;
            padding-left: 10px;
            color: var(--text_color_primary);

            .autor_data_container{
                display: flex;
                flex-direction: row;
                align-items: center;
                justify-content: flex-start;
                width: max-content;
                margin-bottom: 5px;

                .profile_img{
                    width: 25px;
                    height: 25px;
                    border-radius: 5px;
                    object-fit: cover;
                    background-color: #ffff;
                    stroke: var(--text_color_secondary);
                    cursor: pointer;
                }

                .profile_name{
                    padding: 0 5px;
                    font-size: 12px;
                    color: var(--text_color_primary);
                    cursor: pointer;
                }

                .dot_divider{padding-right:5px; color: var(--text_color_secondary)}

                .post_date{
                    font-weight: 400;
                    font-size: 12px;
                    cursor: pointer;
                }
            }

            .title_field{
                display: inline-block; 
                color: var(--text_color_primary);
                margin-bottom: 10px;
                cursor: pointer;
            }

            .post_img{
                display: block;
                height: auto;
                max-height: 420px;
                width: 604px;
                max-width: 100%;
                margin-bottom: 10px;
                border-radius: 5px;
                object-fit: contain;
                overflow: hidden;
                cursor: pointer;

            }

            .description_field{
                padding-bottom:10px;
                font-weight: 300;

            }
        }
    

    .bottom_container{
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: calc(98%);
        border-top: 2px solid var(--text_color_primary);
        padding-top: 5px;

        .reactions_container{
            display: flex;
            flex-direction: row;
            position: relative;

            img{
                position: absolute;
                height: 25px;
                width: 25px;
            }
        }

        .user_activities_rightside_container{
            display: flex;
            flex-direction: row;
        }

        .comments_container{
            display: flex;
            align-items: center;
            height: 31px;
            padding: 0 2px;
            margin-right: 10px;
            border: 1px solid var(--bg_button_color);
            border-radius: 5px;
            cursor: pointer;
            background-color: var(--bg_button_color);
            color: var(--text_color_secondary);

            svg{
               stroke: var(--text_color_secondary); 
               width: 25px;
               height: 25px; 
            }

            span{
                margin: 0 4px 3px 4px;
                font-weight: 300;
                font-size: 14px;
            }

            &.commented{
                border-color: var(--bg_button_active_color);
                color: var(--bg_button_active_color);
                svg{stroke: var(--bg_button_active_color);}
            }

            &:hover{
                background-color: var(--bg_button_active_color);
                color: #ffff;
            }

            &:hover > svg{
                stroke: #ffff;;
            }
        }

        .tag_container{
            display: flex;
            flex-direction: row;
            justify-content: flex-start;
            flex-wrap: wrap;
            overflow: hidden;
            row-gap: 4px;
            width: calc(100% - 100px);
            cursor: pointer;

            .tag_element{
                display: flex;
                align-items: center;
                justify-content: center;
                height: 2em;
                width: max-content;
                padding: 0 5px;
                margin: 0 2px;
                border: 1px solid var(--block_border_color);
                border-radius: 5px;
                font-size: 14px;
                font-weight: 400;
                color: var(--text_color_secondary);
                cursor: pointer;
            }
        }
    }


}

</style>