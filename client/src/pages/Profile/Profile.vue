<template>
<div class="d-flex flex-column"
    :class="{'mt-3': width >= mobileWidthLimit, '': width < mobileWidthLimit}"   
    :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px; width: inherit; overflow-y: auto'">
    <v-card v-if="user_data != null" class="main-container elevation-8 w-100 px-2" style="position: relative; overflow-y: auto;"> 
        <div class="user_profile" style="position: relative;">
            <div class="profile_header"
                style="position: relative; background-size: 100%;background-repeat: no-repeat; background-position: center;  overflow: hidden;  min-height: 65px;">

                <v-img class="background_img"
                    width="auto" 
                    max-height='300px' 
                    cover 
                    :src="
                        user_data?.additional_profile_info?.profile_background_img_new != '' 
                        ? user_data?.additional_profile_info?.profile_background_img_new 
                        :'https://cdn.vuetifyjs.com/images/parallax/material.jpg'
                    "
                    style="position: relative;">
                </v-img>
            </div>
            <div class="avatar_container"
                style="display: inline-block; margin: -45px 10px 0 12px; position: relative;">
                <v-avatar class="avatar" v-if="user_data?.additional_profile_info?.profile_avatar_img_new" 
                    :image="user_data?.additional_profile_info?.profile_avatar_img_new" 
                    :alt="user_data?.sign_in.username" 
                    size="120"
                    :style="`border: 4px solid ${theme.current.value.colors.background}; border-radius: 80px; display: inline-block;position: relative; overflow: hidden;`">
                </v-avatar>

                <v-icon class="account_icon d-flex" v-else
                    icon="mdi-account-circle" 
                    size="120"
                    :style="`border: 4px solid ${theme.current.value.colors.background}; border-radius: 80px; display: inline-block;position: relative; overflow: hidden;`">
                </v-icon>
                <span class="online_status" 
                    :style="online_status ? `border-color: ${theme.current.value.colors.background}; background: ${theme.current.value.colors.success};` : `border-color: ${theme.current.value.colors.background}; background: #cad0ce;`">
                </span>
            </div>
            <div class="user_title" style="display: inline-block; vertical-align: top;">
                <div class="px-2">  
                    <div class="profile_name text-h6">{{user_data?.profile_id?.profile_name}}</div>
                    <!-- <div class="user_role">{{user_role}}</div> -->
                </div>      
                <div class="last_visited text-caption px-2" v-if="!online_status">Last visited: {{DateTimeFormat(last_online_date)}}</div>
            </div>
            <div class="about d-flex flex-row user_info mx-3 mt-3" :style=" width >= mobileWidthLimit ? 'max-width: 600px; position: relative;' : 'position: relative; max-width: 300px;'">
                <v-card class="pa-2" variant="tonal">{{user_data?.additional_profile_info?.about_info}}</v-card>
            </div>
            <v-card class="stats mt-5 mx-3" style="position: relative;">
                <v-card-title>Stats</v-card-title>
                <v-card-text>
                    <div class="showcase_container d-flex flex-row align-center pa-2" style="overflow-x: auto;">
                        <DraggableShowcase 
                            :list="user_data?.additional_profile_info?.statistics?.selected" 
                            :type="'stats'" 
                            :edit="false">
                        </DraggableShowcase>
                    </div>
                </v-card-text>
            </v-card>
            <v-card class="wall mt-5 mx-3">
                <v-card-title>Wall <span class="text-subtitle-1">77</span></v-card-title>
                <v-card-text>Is empty yet</v-card-text>
            </v-card>
        </div>
    </v-card>
    <div class="d-flex flex-row align-center justify-center w-100 h-100" v-else>This user is not exist</div>
</div>


</template>

<script setup>
import { ref, computed, onBeforeMount, defineProps } from 'vue';
import { useStore } from 'vuex';
import { useDisplay } from 'vuetify/lib/framework.mjs';
import { useTheme } from 'vuetify/lib/framework.mjs';
import { DateTimeFormat } from '@/helpers'
import routes from '@/router/router' 

import DraggableShowcase from '@/components/Profile/DraggableShowcase.vue'

let theme = useTheme()
const { width } = useDisplay();
const store = useStore();
const props = defineProps(['user_info',])


const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})
const last_online_date = computed(() => {return store.getters['getLastOnlineDate']})
const online_status = computed(() => {return store.getters['getOnlineStatus']})

let user_data = ref({
    'profile_id': {'profile_name': '', 'tagname': ''},
    'additional_profile_info': {'profile_background_img': '', 'profile_avatar_img': '', 'about_info': '','statistics': {}},
})





onBeforeMount(async() => {
    if(props.user_info !== undefined){user_data.value = props.user_info}
    else{
        const response = await store.dispatch('accounts/getUserInfo', routes.currentRoute.value.params.profile_name)

        if(response !== null){
            user_data.value['profile_id']['profile_name'] = response.profile_name
            user_data.value['profile_id']['tagname'] = response.tagname
            user_data.value['additional_profile_info']['profile_background_img'] = response.background_image
            user_data.value['additional_profile_info']['profile_avatar_img'] = response.avatar
            user_data.value['additional_profile_info']['about_info'] = response.about_info
            user_data.value['additional_profile_info']['statistics'] = response.statistics
        }
        else{user_data.value = response}
    }

})

</script>

<style lang="scss" scoped>
    .main-container{
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: auto;
        margin: 2px 0 15px 0;
        padding: 10px 15px 10px 10px;
        border-radius: 5px;
        caret-color: transparent;
    }

    .showcase_container:hover{overflow-x: auto;}

    .online_status{
        position: absolute; 
        padding: 5px; 
        bottom: 17px; 
        right: 4px;
        border: 4px solid; 
        border-radius: 10px;
    }   
   

</style>