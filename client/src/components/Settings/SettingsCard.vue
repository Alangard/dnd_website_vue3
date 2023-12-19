
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
            <v-text-field class="d-flex flex-row flex-wrap" label="EMAIL ADDRESS" type="email" variant="solo" color="primary"  clearable></v-text-field>

            <v-row>
                <v-col cols="6">
                    <v-select class="text-caption" label="REGION" clearable variant="solo" :items="['Rus', 'Eng']"></v-select>
                </v-col>
                <v-col cols="6">
                    <v-text-field class="d-flex flex-row flex-wrap"
                            v-model="formattedDate"
                            label="DATE OF BIRTH"
                            color="primary"
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
                    <v-text-field class="d-flex flex-row flex-wrap" label="PROFILE NAME" type="text" variant="solo" color="primary" clearable></v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-text-field class="d-flex flex-row flex-wrap" label="TAGNAME" type="text" variant="solo" color="primary" clearable></v-text-field>
                </v-col>
            </v-row>

            <div class="d-flex flex-row-reverse mt-6">
                <v-btn :disabled="!wasEdited">SAVE AND VERIFY</v-btn>
            </div>
        </v-card-text>
    </v-card>

    <v-card class="mb-6 addintional_profile_info"
        :class="{'d-flex flex-row align-start': width >= mobileWidthLimit, 'd-flex flex-column justify-start': width < mobileWidthLimit}"
        :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'" 
        height="auto">
        
        <v-card class="pa-6"
            :style=" width >= mobileWidthLimit ? 'width: 300px; height: 100%' : 'width: 100%; height: auto'"
            variant="tonal"  
            rounded="0"> 
            <v-card-title class="pa-0">Additional profile info</v-card-title>
            <v-card-text class="pa-0">Customize the additional information displayed on your profile.
            </v-card-text>
        </v-card>

        <v-card-text class="pa-6">
            <div class="profile_background" style="position: relative;"  
                @mouseover="editableProfileBackgroundImg = true" 
                @mouseleave="editableProfileBackgroundImg = false">

                <p class="text-h6 mb-2">Profile background image</p>
                <v-img class="background_img" v-if="user_data.background" 
                    max-height='300px' 
                    cover 
                    :src='user_data.background'>
                </v-img>
 
                <v-img class="background_img" v-else 
                    max-height='300px' 
                    cover >
                </v-img>
                
                <v-file-input class="edit_profile_background_img d-flex flex-row flex-wrap mt-3 mb-4"
                    v-if="editProfileBackgroundImg"
                    v-model="user_data.background"
                    :error-messages="validationErrors.background !== ''? validationErrors.background : validator.background.$errors.map(e => e.$message)"
                    @input="validator.background.$touch"
                    :accept="allowedImageExtensions.map(ext => `image/${ext}`).join(', ')"
                    prepend-inner-icon="mdi-image"
                    prepend-icon=""
                    variant="solo"
                    label="Select image">
                </v-file-input>


                <v-btn 
                    v-show="editableProfileBackgroundImg || editProfileBackgroundImg || width < mobileWidthLimit"
                    @click="editProfileBackgroundImg = !editProfileBackgroundImg" 
                    density="comfortable" 
                    icon="mdi-pencil-outline"  
                    style="position: absolute; top: 50px; right: 15px">
                </v-btn>
                <v-btn 
                    v-show="(editableProfileBackgroundImg || width < mobileWidthLimit) && user_data.background" 
                    density="comfortable"
                    icon="mdi-trash-can-outline"  
                    style="position: absolute; top: 95px; right: 15px">
                </v-btn>
            </div>

            <v-card class="profile_avatar mt-3" style="position: relative;" 
                @mouseover="editableProfileBackgroundImg = true" 
                @mouseleave="editableProfileBackgroundImg = false">

                <v-card-title>Profile avatar</v-card-title>
                <v-card-text class="d-flex flex-row align-center justify-space-between w-auto">
                    <v-avatar class="avatar pr-2" v-if="user_data.avatar" 
                        :image="user_data.avatar" 
                        :alt="user_data.username" 
                        size="120">
                    </v-avatar>

                    <v-icon class="account_icon d-flex pr-2" v-else
                        icon="mdi-account-circle" 
                        size="120">
                    </v-icon>

                    <div class="d-flex flex-column justify-center px-2 w-100">
                        <v-file-input class="edit_avatar d-flex flex-row flex-wrap mb-2"
                            v-if="editAvatarImg"
                            v-model="user_data.new_avatar"
                            :error-messages="validationErrors.new_avatar !== ''? validationErrors.new_avatar : validator.new_avatar.$errors.map(e => e.$message)"
                            @input="validator.new_avatar.$touch"
                            :accept="allowedImageExtensions.map(ext => `image/${ext}`).join(', ')"
                            prepend-inner-icon="mdi-image"
                            prepend-icon=""
                            variant="solo"
                            label="Select image">
                        </v-file-input>

                        <v-btn class="delete_avatar"  @click="delete_avatar" :disabled="user_data.avatar == null">Delete avatar</v-btn>
                    </div>
                </v-card-text>
            </v-card>
        
            <v-textarea class="about_info d-flex flex-row flex-wrap"
                v-model="user_data.about_info"
                auto-grow
                clearable
                variant="solo"
                label="About me"
                rows="1"
            ></v-textarea>

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
            <v-text-field class="d-flex flex-row flex-wrap" 
                v-model='user_data.username' 
                label="USERNAME" 
                type="text" 
                variant="solo"
                color="primary" 
                clearable>
            </v-text-field>

            <p class="text-h6 mb-2">Change Password</p>

            <v-text-field
                class="d-flex flex-row flex-wrap"
                v-model="user_data.curr_password"
                :append-inner-icon="showCurrPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showCurrPassword ? 'text' : 'password'"
                @click:append="showCurrPassword = !showCurrPassword"
                clearable
                color="primary"
                label="CURRENT PASSWORD"
                variant="solo"
            ></v-text-field>

            <v-text-field
                class="d-flex flex-row flex-wrap"
                v-model="user_data.new_password"
                :append-inner-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showNewPassword ? 'text' : 'password'"
                @click:append="showNewPassword = !showNewPassword"
                clearable
                color="primary"
                label="NEW PASSWORD"
                variant="solo"
            ></v-text-field>

            <v-text-field
                class="d-flex flex-row flex-wrap"
                v-model="user_data.confirm_new_password"
                :append-inner-icon="showConfirmNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
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

    <!-- <v-dialog v-model="profilePreviewDialog" width="auto">
        <Profile></Profile>
           

  
    </v-dialog> -->
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, computed, onBeforeMount, watchEffect, watch, toRaw } from 'vue';
import { useStore } from 'vuex';
import { useDisplay } from 'vuetify/lib/framework.mjs';
import { useTheme } from 'vuetify/lib/framework.mjs';
import { useVuelidate } from '@vuelidate/core'
import { required, helpers} from '@vuelidate/validators'
import routes from '@/router/router'

import Profile from '@/pages/Profile/Profile.vue'


let theme = useTheme()
const { width } = useDisplay();
const store = useStore();

const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})
let user_data_initial = computed(() => {return store.getters['auth/getUserData']})
let user_data = ref(null)

const wasEdited = ref(false)

const formattedDate = ref('')

let showCurrPassword = ref(false);
let showNewPassword = ref(false);
let showConfirmNewPassword = ref(false);
let expansionPanelShowcases = ref(['achievements'])

let editableProfileBackgroundImg = ref(false)
let editProfileBackgroundImg = ref(false)
let editAvatarImg = ref(true)
const profilePreviewDialog = ref(true)


const allowedImageExtensions = ref(['jpg', 'jpeg', 'png', 'webp']);
const maxImageSize = ref(2000000)

//Custom validations errors from backend
const validationErrors = ref({'avatar': '',})

const validator_rules = computed(() => ({
    new_avatar: {
        required: helpers.withMessage('Please select an image file', required),
        maxSize: helpers.withMessage('Maximum file size must not be greater than 2MB', (value) => {
        if (!value[0]) return true;

        const fileSize = value[0].size;

        return fileSize <= maxImageSize.value;
        }),
        fileExt: helpers.withMessage('The file must have the extension: *.jpg,*.jpeg,*.png,*.webp', (value) => {
        if (!value[0] || !value[0].name) return true;

        const fileExtension = value[0].name.split('.').pop().toLowerCase();

        return allowedImageExtensions.value.includes(fileExtension);
        })
  }
}));

const validator = useVuelidate(validator_rules, user_data)

onBeforeMount(() => {
    const additional_dict = {'curr_password': '','new_password': '','confirm_new_password': '', 'new_background': '', 'new_avatar': ''}
    user_data.value = Object.assign(additional_dict, toRaw(user_data_initial.value));

})

const delete_avatar =() =>{
    if(user_data.value.avatar != null){
        store.dispatch('accounts/changeAccountData', {'avatar': 'null'})
    }

}

const avatar_edit_confirm =()=> {
    avatar_change_dialog__opened.value = false
    let formData = new FormData();

    if(validator?.avatar?.$errors?.length > 0){
        if(formdata.value.avatar== null){formData.append("avatar", formdata.value.avatar)}
        else{formData.append("avatar", formdata.value.avatar[0])}

        store.dispatch('accounts/changeAccountData', formData)
    }
}

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