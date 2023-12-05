<template>
<div class="d-flex flex-column" :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'">
    <v-card class="main-container elevation-8 w-100">  
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
                <v-btn  v-show="editableBackground" density="comfortable" icon="mdi-pencil-outline"  style="position: absolute; top: 25px; right: 25px"></v-btn>
            </div>
            <div class="avatar_container"
                @mouseover="editableAvatar = true" 
                @mouseleave="editableAvatar = false"  
                style="display: inline-block; margin: -45px 10px 0 12px; position: relative;">
                <v-avatar class="avatar" 
                    image="https://cdn.vuetifyjs.com/images/parallax/material.jpg" 
                    alt="username" 
                    size="120"
                    :style="`border: 4px solid ${theme.current.value.colors.background}; border-radius: 80px; display: inline-block;position: relative; overflow: hidden;`"
                    @click="routes.push({name: 'user_profile', params: { username: post.author.username }})">
                    <v-icon 
                        icon="mdi-account-circle" 
                        size="120" 
                        :style="`border: 4px solid ${theme.current.value.colors.background}; border-radius: 80px; display: inline-block;position: relative; overflow: hidden;`">
                    </v-icon>
                </v-avatar>
                <v-btn  v-show="editableAvatar" density="comfortable" icon="mdi-pencil-outline"  style="position: absolute; top: 40px; right: 40px"></v-btn>
                <span class="online_status" 
                    :style="`position: absolute; padding: 5px; bottom: 17px; right: 4px; border: 4px solid ${theme.current.value.colors.background}; border-radius: 10px; background: ${theme.current.value.colors.success};`">
                </span>
            </div>
            <div class="user_title" style="display: inline-block; vertical-align: top;" @mouseover="editableUserTitle = true" @mouseleave="editableUserTitle = false" >
                <div class="px-2" v-show="editableUserTitle == false && userTitleEditField == false">  
                    <div class="username text-h6">{{username}}</div>
                    <div class="user_role">{{ user_role }}</div>
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
                <v-card class="px-2 pre_edit_container" v-if="editableUserTitle && userTitleEditField == false" style="position: relative;">
                    <div class="username text-h6">{{username}}</div>
                    <div class="user_role">{{ user_role }}</div>
                    <v-btn 
                        v-show="editableUserTitle" 
                        @click="userTitleEditField = true"
                        density="comfortable" 
                        icon="mdi-pencil-outline"  
                        style="position: absolute; top: 0px; right: 10px">
                    </v-btn>
                </v-card>

                <div class="last_visited text-caption px-2">Last visited: 23 November 2023</div>
            </div>
            <div class="about d-flex flex-row user_info mx-3 mt-3" style="min-width: 300px; max-width: 600px; position: relative;" @mouseover="editableAboutInfo = true" @mouseleave="editableAboutInfo = false">
                <div v-if="aboutEditField == false">
                    <v-card class="pa-2" variant="tonal">
                    {{about_info}}
                    </v-card>
                    <v-btn 
                        v-show="editableAboutInfo" 
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
                <div v-if="editStats == false">
                    <v-card-title>Stats</v-card-title>
                    <v-card-text class="d-flex flex-row flex-wrap">
                        <v-card class="d-flex flex-column align-center" rounded="0" v-for="stat in stats_info_list" :key="stat">
                            <v-card-title>{{ stat.name }}</v-card-title>
                            <v-card-text>{{ stat.count }}</v-card-text>
                        </v-card>
                    </v-card-text>
                    <v-btn 
                        v-show="editableStats" 
                        @click="editStats = true"
                        density="comfortable" 
                        icon="mdi-pencil-outline"  
                        style="position: absolute; top: 10px; right: 10px">
                    </v-btn>
                </div>
                <div v-else>
                    <v-card-title>Stats</v-card-title>
                    <v-card-text class="d-flex flex-row align-center flex-wrap">

                        <DraggableShowcase :list="stats_info_list" :type="'stats'"></DraggableShowcase>

                        <v-btn class="add_stat_block ml-3"
                            v-if="stats_info_list.length < 4"
                            icon="mdi-plus" 
                            width="50px"
                            height="50px">
                        </v-btn>
                    </v-card-text>
                    <v-btn class="save_stat"
                        @click="saveStats"
                        density="comfortable" 
                        icon="mdi-check-outline"  
                        style="position: absolute; top: 10px; right: 10px">
                    </v-btn>

                </div>
            </v-card>

            <div class="showcase mt-5 mx-3">
                    <v-expansion-panels v-model="expansionPanelShowcases">
                        <v-expansion-panel class="achievements" value="achievements">
                            <v-expansion-panel-title class="text-h6" expand-icon="mdi-plus" collapse-icon="mdi-minus">Achivements showcase</v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div class="d-flex flex-row flex-wrap">

                                    <DraggableShowcase :list="info.achievements" :type="'achievements'"></DraggableShowcase>
                                    <!-- <v-card class="mr-3 mt-3" width="90px" height="90px">
                                        <v-img height="100%" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                    </v-card>
                                    <v-card class="mr-3 mt-3" width="90px" height="90px">
                                        <v-img height="100%" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                    </v-card>
                                    <v-card class="mr-3 mt-3" width="90px" height="90px">
                                        <v-img height="100%" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                    </v-card> -->
                                </div>
                            </v-expansion-panel-text>
                        </v-expansion-panel>

                        <v-expansion-panel class="active_company" value="active_company">
                            <v-expansion-panel-title class="text-h6" expand-icon="mdi-plus" collapse-icon="mdi-minus">Company showcase</v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div class="d-flex flex-row flex-wrap">
                                    <DraggableShowcase :list="info.active_company" :type="'active_company'"></DraggableShowcase>
                                    <!-- <v-card class="d-flex flex-column align-center mr-3 mt-3 pt-3">
                                        <v-img width="90px" height="90px" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                        <v-card-title class="pb-0">Tavern</v-card-title>
                                        <v-card-subtitle>
                                            <span class="role">Player</span>/<span class="player_name">John Doe</span>
                                        </v-card-subtitle>
                                    </v-card>
                                    <v-card class="d-flex flex-column align-center mr-3 mt-3 pt-3">
                                        <v-img width="90px" height="90px" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                        <v-card-title class="pb-0">Mousetrap</v-card-title>
                                        <v-card-subtitle>
                                            <span class="role">Player</span>/<span class="player_name">Rem Stonehold</span>
                                        </v-card-subtitle>
                                    </v-card>
                                    <v-card class="d-flex flex-column align-center mr-3 mt-3 pt-3">
                                        <v-img width="90px" height="90px" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                        <v-card-title class="pb-0">Curse of Strahd</v-card-title>
                                        <v-card-subtitle>
                                            <span class="role">Player</span>/<span class="player_name">Mjolnir</span>
                                        </v-card-subtitle>
                                    </v-card> -->
                                </div>
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                        
                        <v-expansion-panel class="workshop" value="workshop">
                            <v-expansion-panel-title class="text-h6" expand-icon="mdi-plus" collapse-icon="mdi-minus">Workshop</v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div class="d-flex flex-row flex-wrap">
                                    <DraggableShowcase :list="info.workshop" :type="'workshop'"></DraggableShowcase>
                                    <!-- <v-card class="d-flex flex-column align-center mr-3 mt-3 pt-3">
                                        <v-img width="90px" height="90px" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                        <v-card-title class="pb-0">The Ancient Ring</v-card-title>
                                        <v-card-subtitle>
                                            <span class="type">Item</span>
                                        </v-card-subtitle>
                                    </v-card>
                                    <v-card class="d-flex flex-column align-center mr-3 mt-3 pt-3">
                                        <v-img width="90px" height="90px" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                        <v-card-title class="pb-0">John Doe</v-card-title>
                                        <v-card-subtitle>
                                            <span class="type">Character</span>
                                        </v-card-subtitle>
                                    </v-card>
                                    <v-card class="d-flex flex-column align-center mr-3 mt-3 pt-3">
                                        <v-img width="90px" height="90px" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                        <v-card-title class="pb-0">Lily Doe</v-card-title>
                                        <v-card-subtitle>
                                            <span class="role">NPC</span>
                                        </v-card-subtitle>
                                    </v-card> -->
                                </div>
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                    </v-expansion-panels>
            </div>

            <v-card class="wall mt-5 mx-3">
                <v-card-title>Wall <span class="text-subtitle-1">77</span></v-card-title>
                <v-card-text>Is empty yet</v-card-text>
            </v-card>
        </div>
    </v-card>

    


</div>



</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, computed, onBeforeMount, watchEffect, watch } from 'vue';
import { useStore } from 'vuex';
import { useDisplay } from 'vuetify/lib/framework.mjs';
import { useTheme } from 'vuetify/lib/framework.mjs';
import routes from '@/router/router'

import DraggableShowcase from '@/components/Profile/DraggableShowcase.vue'

const stats_info_list = ref([{'name': 'Likes', 'count': 12000}, {'name': 'Comments', 'count': 360}, {'name': 'Post', 'count': 15}, {'name': '"Hot" streak', 'count': '5 days'}])

let expansionPanelShowcases = ref(['achievements', 'active_company','workshop' ])
const info = ref({
    'achievements': [{'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'}, {'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'}, {'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'}],
    'active_company': [
        {'company_name': 'Tavern', 'company_role': 'Player', 'player_name': 'John Doe', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
        {'company_name': 'Mousetrap', 'company_role': 'Player', 'player_name': 'Rem Stonehold', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
        {'company_name': 'Curse of Strahd', 'company_role': 'Player', 'player_name': 'Mjolnir', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
    ],
    'workshop': [
        {'object_name': 'The Ancient Ring', 'object_type': 'Item', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
        {'object_name': 'John Doe', 'object_type': 'Character', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
        {'object_name': 'Lily Doe', 'object_type': 'NPC', 'img_link': 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'},
    ]

})





let theme = useTheme()
const { width } = useDisplay();
const store = useStore();

const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})



let editableBackground = ref(false)
let editableAvatar = ref(false)
let editableUserTitle = ref(false)
let editableAboutInfo = ref(false)
let editableStats = ref(false)

let userTitleEditField = ref(false)
let aboutEditField = ref(false)
let editedUsername = ref(false)
let editedUserRole = ref(false)
let editedAbout = ref(false)
let editStats = ref(false)

let username = ref('Alangard')
let user_role = ref('user')
let about_info = ref('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation')

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

const sendAboutInfo =() =>{aboutEditField.value = false;}

const saveStats =() =>{
    //send stats
    editStats.value = false
}

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
</style>