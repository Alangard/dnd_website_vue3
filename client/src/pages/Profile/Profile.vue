<template>
<div class="d-flex flex-column" :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px; width: inherit;'">
    <v-card class="main-container elevation-8 w-100" style="position: relative;"> 
        <!-- <v-btn class="mobile_edit_trigger"
            v-if="width < mobileWidthLimit"
            @click="allEdit"  
            icon="mdi-dots-vertical"
            style="position: absolute; top: 15px; right: 20px; z-index: 99999;">
        </v-btn> -->

        <div class="user_profile" style="position: relative;">
            <div class="profile_header"
                @mouseover="editableBackground = true" 
                @mouseleave="editableBackground = false" 
                style="position: relative; background-size: 100%;background-repeat: no-repeat; background-position: center;  overflow: hidden;  min-height: 65px;">

                <v-img class="background_img"
                    width="auto" 
                    max-height='300px' 
                    cover 
                    src="https://cdn.vuetifyjs.com/images/parallax/material.jpg" 
                    style="position: relative;">
                </v-img>
                <v-btn  v-show="editableBackground && hasPermissions" density="comfortable" icon="mdi-pencil-outline"  style="position: absolute; top: 25px; right: 25px"></v-btn>
            </div>
            <div class="avatar_container"
                @mouseover="editableAvatar = true" 
                @mouseleave="editableAvatar = false"  
                style="display: inline-block; margin: -45px 10px 0 12px; position: relative;">
                <v-avatar class="avatar" v-if="user_data?.avatar" 
                    :image="user_data?.avatar" 
                    :alt="user_data?.username" 
                    size="120"
                    :style="`border: 4px solid ${theme.current.value.colors.background}; border-radius: 80px; display: inline-block;position: relative; overflow: hidden;`">
                </v-avatar>

                <v-icon class="account_icon d-flex" v-else
                    icon="mdi-account-circle" 
                    size="120"
                    :style="`border: 4px solid ${theme.current.value.colors.background}; border-radius: 80px; display: inline-block;position: relative; overflow: hidden;`">
                </v-icon>
                <v-btn  v-show="editableAvatar && hasPermissions" density="comfortable" icon="mdi-pencil-outline"  style="position: absolute; top: 40px; right: 40px" @click="avatar_change_dialog__opened = true"></v-btn>
                <span class="online_status" 
                    :style="online_status ? `border-color: ${theme.current.value.colors.background}; background: ${theme.current.value.colors.success};` : `border-color: ${theme.current.value.colors.background}; background: #cad0ce;`">
                </span>
            </div>
            <div class="user_title" style="display: inline-block; vertical-align: top;" @mouseover="editableUserTitle = true" @mouseleave="editableUserTitle = false" >
                <div class="px-2" v-show="editableUserTitle == false && userTitleEditField == false">  
                    <div class="username text-h6">{{user_data?.username}}</div>
                    <div class="user_role">{{user_role}}</div>
                </div>
                <div class="px-2 pb-1" v-if="userTitleEditField">
                    <v-text-field class="username"
                        v-model="username" 
                        placeholder="username" 
                        variant="underlined"
                        density="compact" 
                        clearable
                        hide-details 
                        :append-icon="username !== '' && editedUsername == false ? 'mdi-check' : ''"
                        @click:append="sendUsername()">
                    </v-text-field>
                    <v-text-field class="user_role" 
                        v-model="user_role"
                        placeholder="user role" 
                        variant="underlined"
                        density="compact" 
                        clearable
                        hide-details 
                        :append-icon="user_role !== '' && editedUserRole == false ? 'mdi-check' : ''"
                        @click:append="sendUserRole()">
                    </v-text-field>
                </div>
                <v-card class="pl-2 pr-15 pre_edit_container" v-if="editableUserTitle && userTitleEditField == false && hasPermissions" style="position: relative;">
                    <div class="username text-h6">{{user_data?.username}}</div>
                    <div class="user_role">{{ user_role }}</div>
                    <v-btn 
                        v-show="editableUserTitle" 
                        @click="userTitleEditField = true"
                        density="comfortable" 
                        icon="mdi-pencil-outline"  
                        style="position: absolute; top: 0px; right: 10px">
                    </v-btn>
                </v-card>

                <div class="last_visited text-caption px-2" v-if="!online_status">Last visited: {{DateTimeFormat(last_online_date)}}</div>
            </div>
            <div class="about d-flex flex-row user_info mx-3 mt-3" style="min-width: 300px; max-width: 600px; position: relative;" @mouseover="editableAboutInfo = true" @mouseleave="editableAboutInfo = false">
                <div v-if="aboutEditField == false">
                    <v-card class="pa-2" variant="tonal">
                    {{user_data?.about_info}}
                    </v-card>
                    <v-btn 
                        v-show="editableAboutInfo && hasPermissions" 
                        @click="aboutEditField = true"
                        density="comfortable" 
                        icon="mdi-pencil-outline"  
                        style="position: absolute; top: 10px; right: 10px">
                    </v-btn>
                </div>

                <v-textarea class="about_info" 
                    v-else
                    v-model="about_info"
                    placeholder="about me" 
                    variant="filled"
                    density="compact" 
                    clearable
                    hide-details 
                    hide-spin-buttons
                    no-resize
                    :append-icon="about_info !== '' && editedAbout == false ? 'mdi-check' : ''"
                    @click:append="sendAboutInfo()">
                </v-textarea>
            </div>

            <v-card class="stats mt-5 mx-3" style="position: relative;" @mouseover="editableStats = true" @mouseleave="editableStats = false">
                
                    <v-card-title>Stats</v-card-title>
                    <v-card-text>
                        <div class="showcase_container d-flex flex-row align-center pa-2">
                            <DraggableShowcase 
                                :list="stats_info.selected" 
                                :type="'stats'" 
                                :edit="editStats" 
                                @changeStatOption="changeStatOption"
                                @removeStatBlock="removeStatBlock">
                            </DraggableShowcase>

                            <v-btn class="add_stat_block ml-3"
                                v-if="stats_info?.selected?.length < 4 && editStats == true"
                                @click="addStatsBlock"
                                icon="mdi-plus" 
                                width="50px"
                                height="50px">
                            </v-btn>


                        </div>
                    </v-card-text>
                    <v-btn 
                        v-show="editableStats && editStats == false && hasPermissions"
                        @click="editStats = true"
                        density="comfortable" 
                        icon="mdi-pencil-outline"  
                        style="position: absolute; top: 10px; right: 10px">
                    </v-btn>
                    <v-btn class="save_stat"
                        v-if="editStats == true"
                        @click="saveStats"
                        density="comfortable" 
                        icon="mdi-check-outline"  
                        style="position: absolute; top: 10px; right: 10px">
                    </v-btn>
            </v-card>

            <!-- <v-card class="showcases mt-5 mx-3" style="position: relative;" @mouseover="editableShowcases = true" @mouseleave="editableShowcases = false">
                <v-card-title>Showcases</v-card-title>
                <v-expansion-panels v-model="expansionPanelShowcases">
                    <v-expansion-panel class="achievements" value="achievements">
                        <v-expansion-panel-title class="text-h6" expand-icon="mdi-plus" collapse-icon="mdi-minus">Achivements</v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <div class="showcase_container d-flex flex-row align-center pa-2">
                                <DraggableShowcase :list="info.achievements" :type="'achievements'" :edit="editShowcases"></DraggableShowcase>

                                <v-btn class="add_achievement_block ml-3 mt-3"
                                    v-if="info.achievements.length < 4 && editShowcases == true"
                                    @click="addAchievementBlock"
                                    icon="mdi-plus" 
                                    width="50px"
                                    height="50px">
                                </v-btn>
                            </div>
                        </v-expansion-panel-text>
                    </v-expansion-panel>

                    <v-expansion-panel class="active_company" value="active_company">
                        <v-expansion-panel-title class="text-h6" expand-icon="mdi-plus" collapse-icon="mdi-minus">Companies</v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <div class="showcase_container d-flex flex-row align-center pa-2">
                                <DraggableShowcase :list="info.active_company" :type="'active_company'" :edit="editShowcases"></DraggableShowcase>
                                
                                <v-btn class="add_active_company_block ml-3"
                                    v-if="info.active_company.length < 4 && editShowcases == true"
                                    @click="addActiveCompanyBlock"
                                    icon="mdi-plus" 
                                    width="50px"
                                    height="50px">
                                </v-btn>
                            </div>
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                    
                    <v-expansion-panel class="workshop" value="workshop">
                        <v-expansion-panel-title class="text-h6" expand-icon="mdi-plus" collapse-icon="mdi-minus">Workshop</v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <div class="showcase_container d-flex flex-row align-center pa-2">
                                <DraggableShowcase :list="info.workshop" :type="'workshop'" :edit="editShowcases"></DraggableShowcase>
                                
                                <v-btn class="add_workshop_block ml-3"
                                    v-if="info.active_company.length < 4 && editShowcases == true"
                                    @click="addWorkshopBlock"
                                    icon="mdi-plus" 
                                    width="50px"
                                    height="50px">
                                </v-btn>
                            </div>
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                </v-expansion-panels>
       
                <v-btn class="save_showcases"
                    v-if="editShowcases == true"
                    @click="saveShowcases"
                    density="comfortable" 
                    icon="mdi-check-outline"  
                    style="position: absolute; top: 5px; right: 10px">
                </v-btn>

                <v-btn class="edit_showcases"
                    v-show="editableShowcases && editShowcases == false" 
                    @click="editShowcases = true"
                    density="comfortable" 
                    icon="mdi-pencil-outline"  
                    style="position: absolute; top: 5px; right: 10px">
                </v-btn>
            </v-card> -->

            <v-card class="wall mt-5 mx-3">
                <v-card-title>Wall <span class="text-subtitle-1">77</span></v-card-title>
                <v-card-text>Is empty yet</v-card-text>
            </v-card>
        </div>
    </v-card>
</div>

<v-dialog class="avatar_change_dialog"
    v-model="avatar_change_dialog__opened"
    width="auto">

    <v-card>
        <v-card-title>Editing avatar</v-card-title>
        <v-card-text class="d-flex flex-row align-start">
            <v-avatar class="avatar" v-if="user_data?.avatar" 
                :image="user_data?.avatar" 
                :alt="user_data?.username" 
                size="120">
            </v-avatar>

            <v-icon class="account_icon d-flex" v-else
                icon="mdi-account-circle" 
                size="120">
            </v-icon>


            <div class="d-flex flex-column ml-3">
                <v-list class="py-0" lines="one">
                    <v-list-item class="pt-0 pb-2">
                        <v-list-item-title class="pb-2 text-h6">Upload</v-list-item-title>
                        <v-list-item-subtitle class="pb-1">Acceptable formats: {{allowedImageExtensions.map(ext => `*.${ext}`).join(', ')}}</v-list-item-subtitle>
                        <v-list-item-subtitle class="pb-1">Maximum size: {{maxImageSize / 1000000}}MB</v-list-item-subtitle>
                    </v-list-item>
                </v-list>
                
                <v-file-input class="edit_avatar d-flex flex-row flex-wrap mx-4 mb-4" style="width: 290px;"
                    v-model="formdata.avatar"
                    :error-messages="validationErrors.avatar !== ''? validationErrors.avatar : validator.avatar.$errors.map(e => e.$message)"
                    @input="validator.avatar.$touch"
                    :accept="allowedImageExtensions.map(ext => `image/${ext}`).join(', ')"
                    prepend-inner-icon="mdi-image"
                    prepend-icon=""
                    variant="solo"
                    label="Select image">
                </v-file-input>
      
                <v-btn class="delete_avatar mx-4" width="290px" @click="delete_avatar" :disabled="user_data.avatar == null">Delete avatar</v-btn>
            </div>
        </v-card-text>
        <v-card-actions>
            <v-btn color="primary" block :disabled="validator?.avatar?.$errors?.length > 0" @click="avatar_edit_confirm">Confirm</v-btn>
        </v-card-actions>
    </v-card>
</v-dialog>



</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, computed, onBeforeMount, watchEffect, watch, toRaw } from 'vue';
import { useStore } from 'vuex';
import { useDisplay } from 'vuetify/lib/framework.mjs';
import { useTheme } from 'vuetify/lib/framework.mjs';
import { useVuelidate } from '@vuelidate/core'
import { required, helpers} from '@vuelidate/validators'

import {DateTimeFormat} from '@/helpers'
import routes from '@/router/router'

import DraggableShowcase from '@/components/Profile/DraggableShowcase.vue'


// let expansionPanelShowcases = ref(['achievements', 'active_company','workshop' ])

// const info = ref({
//     'stats': [{'name': 'Likes', 'count': 12000}, {'name': 'Comments', 'count': 360}, {'name': 'Post', 'count': 15}],
//     'achievements': [{'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'}, {'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'}, {'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'}],
//     'active_company': [
//         {'company_name': 'Tavern', 'company_role': 'Player', 'player_name': 'John Doe', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
//         {'company_name': 'Mousetrap', 'company_role': 'Player', 'player_name': 'Rem Stonehold', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
//         {'company_name': 'Curse of Strahd', 'company_role': 'Player', 'player_name': 'Mjolnir', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
//         {'company_name': 'Curse of Strahd', 'company_role': 'Player', 'player_name': 'Mjolnir', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
//     ],
//     'workshop': [
//         {'object_name': 'The Ancient Ring', 'object_type': 'Item', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
//         {'object_name': 'John Doe', 'object_type': 'Character', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
//         {'object_name': 'Lily Doe', 'object_type': 'NPC', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
//     ]

// })


let theme = useTheme()
const { width } = useDisplay();
const store = useStore();



const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})
const stats_info = computed(() => {return store.getters['accounts/getShowcaseStats']})
const last_online_date = computed(() => {return store.getters['getLastOnlineDate']})
const online_status = computed(() => store.getters['getOnlineStatus'])
let user_data = ref(null) 

const hasPermissions = ref(false)

let editableBackground = ref(false)
let editableAvatar = ref(false)
let editableUserTitle = ref(false)
let editableAboutInfo = ref(false)
let editableStats = ref(false)
let editableShowcases = ref(false)

let userTitleEditField = ref(false)
let aboutEditField = ref(false)
let editedUsername = ref(false)
let editedUserRole = ref(false)
let editedAbout = ref(false)
let editStats = ref(false)
let editShowcases = ref(false)

// let username = ref('Alangard')
let user_role = ref('user')
let about_info = ref('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation')

let addStat = ref(false)
let statType = ref(false)

const avatar_change_dialog__opened = ref(false)


onBeforeMount(async() => {

   
    user_data = computed(() => {return store.getters['auth/getUserData']})
        hasPermissions.value = true
    // const route_username = routes.currentRoute.value.params['username']
    // if(route_username != store.getters['auth/getUserData'].username){
    //     user_data.value = await store.dispatch('accounts/getUserInfo', route_username)
    //     hasPermissions.value = false
    // }
    // else{
    //     user_data = computed(() => {return store.getters['auth/getUserData']})
    //     hasPermissions.value = true
    // }


   
    

})


const sendUsername =() => {
    // checkUsername;
    editedUsername.value = true
    if(editedUserRole.value == true){
        console.log('username')
        userTitleEditField.value = false
        editableUserTitle.value = false
        editedUsername.value = false
        editedUserRole.value = false
    }

}

const sendUserRole =() =>{
     // checkUserRole;
     editedUserRole.value = true
    if(editedUsername.value == true){
        console.log('user_role')
        userTitleEditField.value = false
        editableUserTitle.value = false
        editedUsername.value = false
        editedUserRole.value = false
    }
}

const allEdit =() =>{
    editableBackground.value = !editableBackground.value 
    editableAvatar.value = !editableAvatar.value
    editableUserTitle.value = !editableUserTitle.value
    editableAboutInfo.value = ! editableAboutInfo.value
    editableStats.value = !editableStats.value
}

const sendAboutInfo =() =>{aboutEditField.value = false;}



const saveShowcases =() =>{
    //save showcases
    editShowcases.value = false
}

const addStatsBlock =() => { 
    addStat.value = true;
    store.commit('accounts/addStatBlock')
}

const removeStatBlock =(order) => {
    store.commit('accounts/removeStatBlock', order)
}

const changeStatOption =(type) =>{
    statType.value = type
    store.commit('accounts/updateCountStats', type)
}

const saveStats =() =>{
    if(statType.value !== ''){
        store.commit('accounts/saveLastStatBlock', statType.value)
        statType.value = ''
    }
    editStats.value = false

}



const addAchievementBlock = () =>{ console.log('add achievement') }
const addActiveCompanyBlock =() =>{ console.log('add company') }
const addWorkshopBlock =() =>{ console.log('add workshop') }



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