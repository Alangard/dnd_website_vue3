
import LogInVue from '@/pages/Auth/LogIn.vue';
<template>  
    <v-card class="mt-8 mb-6 personal_information"
        :class="{'d-flex flex-row align-start': width >= mobileWidthLimit, 'd-flex flex-column justify-start': width < mobileWidthLimit}"
        :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'" 
        height="auto">
        
        <v-card class="pa-6"
            :style=" width >= mobileWidthLimit ? 'width: 300px; height: 100%' : 'width: 100%; height: auto'"
            variant="tonal"  
            rounded="0"> 
            <v-card-title class="pa-0">Personal Information</v-card-title>
            <v-card-text class="pa-0">
                This information is private and will not be shared with other players. Read the
                <a class='text-info font-weight-bold clickable' target="_blank" href="#" @click.stop>Privacy Notice</a> anytime!
            </v-card-text>
        </v-card>

        <v-card-text class="pa-6">
            <v-text-field label="EMAIL ADDRESS" type="email" variant="solo" clearable></v-text-field>

            <v-row>
                <v-col cols="6">
                    <v-select class="text-caption" label="REGION" clearable variant="solo" :items="['Rus', 'Eng']"></v-select>
                </v-col>
                <v-col cols="6">
                    <v-text-field
                            v-model="formattedDate"
                            label="DATE OF BIRTH"
                            variant="solo">
                    </v-text-field>
                </v-col>
            </v-row>

            <div class="d-flex flex-row-reverse mt-6">
                <v-btn :disabled="!wasEdited">SAVE AND VERIFY</v-btn>
            </div>
        </v-card-text>
    </v-card>

    <v-card class="mb-6 profile_id"
        :class="{'d-flex flex-row align-start': width >= mobileWidthLimit, 'd-flex flex-column justify-start': width < mobileWidthLimit}"
        :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'" 
        height="auto">
        
        <v-card class="pa-6"
            :style=" width >= mobileWidthLimit ? 'width: 300px; height: 100%' : 'width: 100%; height: auto'"
            variant="tonal"  
            rounded="0"> 
            <v-card-title class="pa-0">Profile ID</v-card-title>
            <v-card-text class="pa-0">Your Profile ID and Profile Name is used by players to find you through the social panel.</v-card-text>
        </v-card>

        <v-card-text class="pa-6">
            <v-row>
                <v-col cols="6">
                    <v-text-field label="PROFILE NAME" type="text" variant="solo" clearable></v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-text-field label="TAGNAME" type="text" variant="solo" clearable></v-text-field>
                </v-col>
            </v-row>

            <div class="d-flex flex-row-reverse mt-6">
                <v-btn :disabled="!wasEdited">SAVE AND VERIFY</v-btn>
            </div>
        </v-card-text>
    </v-card>

    <v-card class="mb-6 account__sign_in"
        :class="{'d-flex flex-row align-start': width >= mobileWidthLimit, 'd-flex flex-column justify-start': width < mobileWidthLimit}"
        :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'" 
        height="auto">
        
        <v-card class="pa-6"
            :style=" width >= mobileWidthLimit ? 'width: 300px; height: 100%' : 'width: 100%; height: auto'"
            variant="tonal"  
            rounded="0"> 
            <v-card-title class="pa-0">Account Sign-In</v-card-title>
            <v-card-text class="pa-0">We recommend that you periodically update your password to help prevent unauthorized access to your account.</v-card-text>
        </v-card>

        <v-card-text class="pa-6">
            <v-text-field label="USERNAME" type="text" variant="solo" clearable></v-text-field>
            <p class="text-h6 mb-2">Change Password</p>

            <v-text-field
                v-model="formdata.curr_password"
                :append-icon="showCurrPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showCurrPassword ? 'text' : 'password'"
                @click:append="showCurrPassword = !showCurrPassword"
                clearable
                color="primary"
                label="CURRENT PASSWORD"
                variant="solo"
            ></v-text-field>

            <v-text-field
                v-model="formdata.new_password"
                :append-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showNewPassword ? 'text' : 'password'"
                @click:append="showNewPassword = !showNewPassword"
                clearable
                color="primary"
                label="NEW PASSWORD"
                variant="solo"
            ></v-text-field>

            <v-text-field
                v-model="formdata.confirm_new_password"
                :append-icon="showConfirmNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showConfirmNewPassword ? 'text' : 'password'"
                @click:append="showConfirmNewPassword = !showConfirmNewPassword"
                clearable
                color="primary"
                label="CONFIRM NEW PASSWORD"
                variant="solo"
            ></v-text-field>

            <div class="d-flex flex-row-reverse mt-6">
                <v-btn :disabled="!wasEdited">SAVE AND VERIFY</v-btn>
            </div>
        </v-card-text>
    </v-card>

    <v-card class="mb-6 login_management"
        :class="{'d-flex flex-row align-start': width >= mobileWidthLimit, 'd-flex flex-column justify-start': width < mobileWidthLimit}"
        :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'" 
        height="auto">
        
        <v-card class="pa-6"
            :style=" width >= mobileWidthLimit ? 'width: 300px; height: 100%' : 'width: 100%; height: auto'"
            variant="tonal"  
            rounded="0"> 
            <v-card-title class="pa-0">Login Management</v-card-title>
            <v-card-text class="pa-0">Worried that your account or password has been compromised? You can forcibly log out from site.</v-card-text>
        </v-card>

        <v-card-text class="d-flex flex-row-reverse align-center pa-6" :style="width >= mobileWidthLimit ? 'height: 100%;' : ''">
            <v-btn :disabled="!wasEdited" width="100%">LOG OUT</v-btn>
        </v-card-text>
    </v-card>

    <v-card class="profile_view"
        :class="{'d-flex flex-row align-start': width >= mobileWidthLimit, 'd-flex flex-column justify-start': width < mobileWidthLimit}"
        :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'" 
        height="auto">
        
        <v-card class="pa-6"
            :style=" width >= mobileWidthLimit ? 'width: 300px; height: 100%' : 'width: 100%; height: auto'"
            variant="tonal"  
            rounded="0"> 
            <v-card-title class="pa-0">Profile View</v-card-title>
            <v-card-text class="pa-0">Create or edit your profile for others to see.</v-card-text>
        </v-card>

        <v-card-text class="d-flex flex-row-reverse align-center pa-6" :style="width >= mobileWidthLimit ? 'height: 100%;' : ''">
            <v-btn width="100%" @click="profilePreviewDialog = true">PREVIEW PROFILE</v-btn>
        </v-card-text>

    </v-card>

    <v-dialog v-model="profilePreviewDialog" width="auto">
        <v-card style="min-height: 380px; max-height: 450px;">

        
            <div class="background_container" style="position: relative;" >
                <v-img width="auto" max-height='300px' cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg" style="position: relative;"></v-img>

                

                <div class="d-flex flex-row align-end" style="position: absolute; bottom: -60px; left: 20px;" >

                    <div style="position: relative;">
                        <v-avatar class="avatar" 
                            image="https://cdn.vuetifyjs.com/images/parallax/material.jpg" 
                            alt="username" 
                            size="120"
                            
                            @click="routes.push({name: 'user_profile', params: { username: post.author.username }})">
                            <v-icon icon="mdi-account-circle" size="120"></v-icon>
                        </v-avatar>
                        <span class="text-success" style=" position: absolute; bottom: -25px; border-radius: 50%;"></span>
                    </div>
                    <div class="d-flex flex-column ml-4">
                        <span class="text-h6">Username</span>
                        <span class="">User role</span>
                    </div>
            
                </div>
            </div>
                
        </v-card>
           

  
    </v-dialog>
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
const wasEdited = ref(false)

const formattedDate = ref('')

let showCurrPassword = ref(false);
let showNewPassword = ref(false);
let showConfirmNewPassword = ref(false);

const formdata = ref({
    'curr_password': '',
    'new_password': '',
    'confirm_new_password': ''
})

const profilePreviewDialog = ref(true)

</script>

<style lang="scss" scoped>
    .clickable{
        &:hover{cursor: pointer;}
    }
</style>


<!-- <template> 
    <v-container> 
        <v-form id="form" @submit.prevent="checkDate"> 
        <v-text-field label="Date" id="date" v-model="date"></v-text-field> 
        <small>Enter date as Month / Day / Year</small> 
        <v-btn type="submit">Submit</v-btn> </v-form> <p id="result">{{ result }}</p> 
    </v-container> 
</template> 
<script> import { ref } from 'vue'; export default { 
    setup() { 
        const date = ref(''); 
        const result = ref(''); 
        function checkValue(str, max) { 
            if (/^\D|^0\d/.test(str)) { 
                var num = parseInt(str); 
                if (isNaN(num) || num <= 0 || num > max) num = 1; 
                str = num > parseInt(max.toString().charAt(0)) && num.toString().length == 1 ? '0' + num : num.toString(); 
            } 
            return str; 
        } 
        
        function checkDate() { 
            let input = date.value; 
            if (/\D\D\D$/.test(input)) input = input.substr(0, input.length - 3); 
            let values = input.split('/').map((v) => v.replace(/\D/g, '')); 
            if (values[0]) values[0] = checkValue(values[0], 12); 
            if (values[1]) values[1] = checkValue(values[1], 31); 
            let output = values.map((v, i) => (v.length == 2 && i < 2 ? v + ' / ' : v)); 
            date.value = output.join('').substr(0, 14); 
            if (values.length == 3) { 
                    let year = values[2].length !== 4 ? parseInt(values[2]) + 2000 : parseInt(values[2]); 
                let month = parseInt(values[0]) - 1; 
                let day = parseInt(values[1]); 
                let d = new Date(year, month, day); 
                if (!isNaN(d)) { 
                    result.value = d.toString(); 
                    let dates = [d.getMonth() + 1, d.getDate(), d.getFullYear()]; 
                    output = dates.map((v) => { v = v.toString(); return v.length == 1 ? '0' + v : v; }).join(' / '); 
                } 
            } 
            date.value = output; 
        } 
        return { date, result, checkDate }; 
    }, 
}; 
</script> 
<style> </style> -->