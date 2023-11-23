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
            <div class="user_title" style="display: inline-block; vertical-align: top;" @mouseover="editablUserTitle = true" @mouseleave="editablUserTitle = false" >
                <div class="px-2" v-show="editablUserTitle == false && userTitleEditField == false">  
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
                <v-card class="px-2 pre_edit_container" v-if="editablUserTitle && userTitleEditField == false" style="position: relative;">
                    <div class="username text-h6">{{username}}</div>
                    <div class="user_role">{{ user_role }}</div>
                    <v-btn 
                        v-show="editablUserTitle" 
                        @click="userTitleEditField = true"
                        density="comfortable" 
                        icon="mdi-pencil-outline"  
                        style="position: absolute; top: 0px; right: 10px">
                    </v-btn>
                </v-card>
                <div class="last_visited text-caption px-2">Last visited: 23 November 2023</div>
            </div>
            <div class="about d-flex flex-row user_info mx-3 mt-3">
                <v-card class="pa-2" variant="tonal" min-width="300px" max-width="600px">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
                </v-card>
            </div>

            <v-card class="stats mt-5 mx-3">
                <v-card-title>Stats</v-card-title>
                <v-card-text class="d-flex flex-row flex-wrap">
                    <v-card class="d-flex flex-column align-center" rounded="0">
                        <v-card-title>Likes</v-card-title>
                        <v-card-text>12000</v-card-text>
                    </v-card>

                    <v-card class="d-flex flex-column align-center" rounded="0">
                        <v-card-title>Comments</v-card-title>
                        <v-card-text>360</v-card-text>
                    </v-card>

                    <v-card class="d-flex flex-column align-center" rounded="0">
                        <v-card-title>Posts</v-card-title>
                        <v-card-text>15</v-card-text>
                    </v-card>

                    <v-card class="d-flex flex-column align-center" rounded="0">
                        <v-card-title>Longest stay in the top</v-card-title>
                        <v-card-text>5 days</v-card-text>
                    </v-card>
                </v-card-text>
            </v-card>

            <div class="showcase mt-5 mx-3">
                    <v-expansion-panels v-model="expansionPanelShowcases">
                        <v-expansion-panel class="achievements" value="achievements">
                            <v-expansion-panel-title class="text-h6" expand-icon="mdi-plus" collapse-icon="mdi-minus">Achivements showcase</v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div class="d-flex flex-row flex-wrap">
                                    <!-- <v-card class="mr-3" width="90px" height="90px" v-for="achievement in achievements" :key="achievement.id">
                                        <v-img height="100%" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                    </v-card> -->
                                    <v-card class="mr-3 mt-3" width="90px" height="90px">
                                        <v-img height="100%" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                    </v-card>
                                    <v-card class="mr-3 mt-3" width="90px" height="90px">
                                        <v-img height="100%" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                    </v-card>
                                    <v-card class="mr-3 mt-3" width="90px" height="90px">
                                        <v-img height="100%" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img>
                                    </v-card>
                                </div>
                            </v-expansion-panel-text>
                        </v-expansion-panel>

                        <v-expansion-panel class="active_company" value="active_company">
                            <v-expansion-panel-title class="text-h6" expand-icon="mdi-plus" collapse-icon="mdi-minus">Company showcase</v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div class="d-flex flex-row flex-wrap">
                                    <v-card class="d-flex flex-column align-center mr-3 mt-3 pt-3">
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
                                    </v-card>
                                </div>
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                        
                        <v-expansion-panel class="workshop" value="workshop">
                            <v-expansion-panel-title class="text-h6" expand-icon="mdi-plus" collapse-icon="mdi-minus">Workshop</v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div class="d-flex flex-row flex-wrap">
                                    <v-card class="d-flex flex-column align-center mr-3 mt-3 pt-3">
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
                                    </v-card>
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

let theme = useTheme()
const { width } = useDisplay();
const store = useStore();

const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})

let expansionPanelShowcases = ref(['achievements', 'active_company','workshop' ])
let editableBackground = ref(false)
let editableAvatar = ref(false)
let editablUserTitle = ref(false)

let userTitleEditField = ref(false)
let editedUsername = ref(false)
let editedUserRole = ref(false)

let username = ref('Alangard')
let user_role = ref('user')

const sendUsername =() => {
    // checkUsername;
    editedUsername.value = true
    if(editedUserRole.value == true){
        console.log('username')
        userTitleEditField.value = false
        editablUserTitle.value = false
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
        editablUserTitle.value = false
        editedUsername.value = false
        editedUserRole.value = false
    }
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