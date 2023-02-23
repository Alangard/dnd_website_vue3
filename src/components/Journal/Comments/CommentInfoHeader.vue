<template>

<div class="user-info_container">

    <img class="profile_img"  
        v-if='props.item.user_info.user_profile_img_url != ""' 
        :src="props.item.user_info.user_profile_img_url"
        @click="$router.push({ name: 'user', params: {id: props.item.user_info.username} })">
                

    <svg class="profile_img"  xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
        v-else
        @click="$router.push({ name: 'user', params: {id: props.item.user_info.username} })">
            
        <path d="M5.52 19c.64-2.2 1.84-3 3.22-3h6.52c1.38 0 2.58.8 3.22 3"/>
        <circle cx="12" cy="10" r="3"/>
        <circle cx="12" cy="12" r="10"/>
    </svg>

    <div class="header_of_comment_info">

        <div class="column_wrapper">
            <div class='username_and_role'>
                <span class="username" 
                    @click="$router.push({ name: 'user', params: {id: props.item.user_info.username} })">
                    {{ store.getters.capitalizeFirstLetter(props.item.user_info.username.split('.')[0]) }}
                </span>
                <div class="user_role">
                    {{store.getters.capitalizeFirstLetter(props.item.user_info.user_role)}}
                </div>
            </div>

            <span class='comment_date_container' v-if="props.item.user_info.username != props.user_info.username">
                Commented {{ comment_timeout }}
            </span>

            <span class='comment_date_container' v-else>
                Last change {{ comment_timeout }}
            </span>
        </div>

        <div class="dropdown_btn_container">
            <div v-if="props.item.comment_status != 'deleted'">
                <div v-if="props.item.report_reasons.length == 0">
                    <dropdown
                        @moreFuncOpenMobile="moreFuncSwipeElementOpen"
                        @StartEdit="emit('startEditComment')"
                        @showDeleteAlert="emit('showDeleteAlert')"
                        :isMobile="store.getters.getIsMobileState"
                        :current_user_info="props.user_info"
                        :user_info="props.item.user_info"
                        :isBlock=false
                        :comment_text="props.item.comment_text"
                        :comment_status="props.item.comment_status">
                    </dropdown>
                </div>
                <div v-else>
                    <dropdown
                        @moreFuncOpenMobile="moreFuncSwipeElementOpen"
                        @StartEdit="emit('startEditComment')"
                        @showDeleteAlert="emit('showDeleteAlert')"
                        :isMobile="store.getters.getIsMobileState"
                        :current_user_info="props.user_info"
                        :user_info="props.item.user_info"
                        :isBlock=true
                        :comment_text="props.item.comment_text"
                        :comment_status="props.item.comment_status">
                    </dropdown>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import Dropdown from '@/components/Templates_components/Dropdown/Dropdown.vue';
import { ref, defineProps, defineEmits } from 'vue';
import { useStore } from 'vuex';
import { useTimeAgo } from '@vueuse/core';


const props = defineProps(['item', 'user_info']);
const emit = defineEmits(['startEditComment', 'showDeleteAlert']);
const store = useStore();

let comment_timeout = ref(useTimeAgo(new Date(props.item.date)));

function moreFuncSwipeElementOpen(){console.log('Open modal for mobile')}
</script>

<style lang="scss" scoped>
.user-info_container{
    display: flex;
    flex-direction: row;
    margin-top: 6px;
    padding: 8px 5px 0 5px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    background-color: var(--bg_button_color);

    .profile_img{
        height: 35px;
        width: 35px;
        margin: 0 5px 0 0;
        object-fit: cover;
        border-radius: 5px;
        stroke: var(--text_color_secondary);
        cursor: pointer;
    }

    .header_of_comment_info{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        width: 100%;

        .column_wrapper{
            display: flex;
            flex-direction: column;

            .username_and_role{
                display:flex;
                flex-direction: row;
                justify-content: flex-start;
                align-items: center;
                font-weight: 700;
                font-size: 13px;
                line-height: 13px;
                margin-bottom: 4px;
                text-overflow: ellipsis;
                overflow: hidden; 
                white-space: nowrap;
    
                cursor: pointer;

                .user_role{
                    font-size: 11px;
                    margin-left: 10px;
                    padding: 1px 8px;
                    border-radius: 20px;
                    border: 1px solid var(--bg_button_active_color);
                    font-weight: 300;
                }
            }

            .comment_date_container{
                display: block;
                flex-direction: row;
                align-items: flex-start;
                font-weight: 300;
                margin-bottom: 6px;
                font-size: 11px;
                line-height: 12px;
                text-overflow: ellipsis;
                overflow: hidden; 
                white-space: nowrap;
            }
        }

        .dropdown_btn_continer{
            display: none;
        }

    }

}
</style>