<template>

<!-- <v-card class="notifications_container mt-8" 
    height="100%" 
    :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'">

    <v-card-title>Account</v-card-title>

    <v-card-text class="pa-0">
  
        <v-card class="profile_background">
            <v-card-text class="pa-0">
                <v-img cover height="250" src="https://cdn.vuetifyjs.com/images/cards/cooking.png">
                    <div class="d-flex flex-column justify-space-between align-center w-100" >
                        <v-card class="pa-2" width="max-content" style="backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.5) !important;" theme="dark">
                            <div class="avatar_card d-flex flex-column justify-center">
                                <v-avatar :image="userData?.avatar" size="80" >
                                    <v-icon icon="mdi-account-circle" size="80"></v-icon>
                                </v-avatar>

                                <div class="d-flex flex-column">
                                    <span class="username text-h6">{{ userData?.username }}#{{ userData?.id }}</span>
                                    <span class="user_status text-body-2">{{ userData?.user_role }}</span>
                                </div>
                            </div>
                        </v-card>
                    </div>
                </v-img>
            </v-card-text>
        </v-card>




        <v-container fluid class="username_and_role__field mt-2"> 
            <v-row>
                <v-col class="username_field" cols="6">
                    <span class="label text-h6">Username</span>
                    <v-text-field 
                        :model-value="userData?.username"
                        placeholder="write username"
                        variant="solo"
                        readonly
                        clearable
                    ></v-text-field>
                </v-col>

                <v-col class="user_status__field" cols="6">
                    <span class="label text-h6">User role</span>
                    <v-text-field 
                        :model-value="userData?.user_role"
                        placeholder="write status/role"
                        variant="solo"
                        readonly
                        clearable
                    ></v-text-field>
                </v-col>
            </v-row>  
        </v-container>

        <v-divider></v-divider>

        <v-row>
            <v-col class="email" cols="6">
                <span class="label text-h6">Email</span>
                <div>
                    <v-text-field 
                    model-value="ad.de2013@yandex.ru"
                    placeholder="your email"
                    variant="solo"
                    readonly
                    clearable
                ></v-text-field>
                </div>
 
            </v-col>
        </v-row>


    </v-card-text>
</v-card> -->

<SettingsCard></SettingsCard>

</template>





<script setup>
import { onMounted, onBeforeUnmount, ref, computed, onBeforeMount } from 'vue';
import { useStore } from 'vuex';
import {useDisplay } from 'vuetify/lib/framework.mjs';
import routes from '@/router/router'

import SettingsCard from '@/components/Settings/SettingsCard.vue'

const { width } = useDisplay();
const store = useStore();

const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})
const userData = computed(() => {return store.getters['auth/getUserData']})

</script>

<style lang='scss' scoped>
</style>