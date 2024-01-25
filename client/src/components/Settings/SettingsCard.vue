
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
            <v-text-field class="d-flex flex-row flex-wrap" 
                v-model="user_data.personal_info.email"
                :error-messages="user_data.personal_info.backend_errors.email"
                @update:model-value="resetFields(user_data.personal_info, 'personal_info')"
                label="EMAIL ADDRESS" type="email" variant="solo" color="primary" clearable>

                    <template v-slot:append-inner>
                        <v-fade-transition leave-absolute>
                            <v-progress-circular v-if="user_data.personal_info.loading == true" color="info" indeterminate size="24"></v-progress-circular>
                            <v-icon v-else-if="user_data.personal_info.loading == false && user_data.personal_info.verify_success != null"
                                height="24" width="24" 
                                :icon="user_data.personal_info.verify_success == true ? 'mdi-checkbox-marked-circle-outline' : 'mdi-close-circle-outline'" 
                                :color="user_data.personal_info.verify_success == true ? 'success': 'error'">
                            </v-icon>
                        </v-fade-transition>
                    </template>
            </v-text-field>
<!--          <v-select class="d-flex flex-row flex-wrap text-caption" 
                v-model="user_data.personal_info.region" 
                label="REGION" clearable variant="solo" :items="['Rus', 'Eng']"
                @update:model-value="resetFields(user_data.personal_info, 'personal_info')">
            </v-select>
-->  
            <div class="d-flex flex-row-reverse mt-6">
                <v-btn :disabled="user_data.personal_info.backend_errors.length > 0" 
                    @click="updateSettingPart(user_data.personal_info, 'personal_info')">
                    VERIFY AND SAVE
                </v-btn>
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

        <v-card-text class="pa-6" style="width: min-content;">
            <v-row>
                <v-col cols="6">
                    <v-text-field class="d-flex flex-row flex-wrap"
                        v-model="user_data.profile_id.profile_name"
                        :error-messages="user_data.profile_id.backend_errors.profile_name" 
                        @update:model-value="resetFields(user_data.profile_id, 'profile_id')"
                        label="PROFILE NAME" type="text" variant="solo" color="primary" clearable>

                        <template v-slot:append-inner>
                            <v-fade-transition leave-absolute>
                                <v-progress-circular v-if="user_data.profile_id.loading == true" color="info" indeterminate size="24"></v-progress-circular>
                                <v-icon v-else-if="user_data.profile_id.loading == false && user_data.profile_id.verify_success != null"
                                    height="24" width="24" 
                                    :icon="user_data.profile_id.backend_errors['profile_name'] ? 'mdi-close-circle-outline' : 'mdi-checkbox-marked-circle-outline'" 
                                    :color="user_data.profile_id.backend_errors['profile_name'] ? 'error' : 'success'">
                                </v-icon>
                            </v-fade-transition>
                        </template>
                    </v-text-field>
                </v-col>
                <v-col cols="6">
                    <v-text-field class="d-flex flex-row flex-wrap"
                        v-model="user_data.profile_id.tagname"
                        :error-messages="user_data.profile_id.backend_errors.tagname" 
                        @update:model-value="resetFields(user_data.profile_id, 'profile_id')"  
                        label="TAGNAME" type="text" variant="solo" color="primary" clearable prepend-inner-icon="mdi-pound">

                        <template v-slot:append-inner>
                            <v-fade-transition leave-absolute>
                                <v-progress-circular v-if="user_data.profile_id.loading == true" color="info" indeterminate size="24"></v-progress-circular>
                                <v-icon v-else-if="user_data.profile_id.loading == false && user_data.profile_id.verify_success != null && user_data.profile_id.tagname !== null"
                                    height="24" width="24" 
                                    :icon="user_data.profile_id.backend_errors['tagname'] ? 'mdi-close-circle-outline' : 'mdi-checkbox-marked-circle-outline'" 
                                    :color="user_data.profile_id.backend_errors['tagname'] ? 'error' : 'success'">
                                </v-icon>
                            </v-fade-transition>
                        </template>
                    </v-text-field>
                </v-col>
            </v-row>

            <div class="d-flex flex-row-reverse mt-6">
                <v-btn :disabled="user_data.profile_id.backend_errors.length > 0" 
                    @click="updateSettingPart(user_data.profile_id, 'profile_id')">
                    VERIFY AND SAVE
                </v-btn>
            </div>
        </v-card-text>
    </v-card>

    <v-card class="mb-6 notifications_settings"
        :class="{'d-flex flex-row align-start': width >= mobileWidthLimit, 'd-flex flex-column justify-start': width < mobileWidthLimit}"
        :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'" 
        height="auto">
        
        <v-card class="pa-6"
            :style=" width >= mobileWidthLimit ? 'width: 300px; height: 100%' : 'width: 100%; height: auto'"
            variant="tonal"  
            rounded="0"> 
            <v-card-title class="pa-0">Notifications Settings</v-card-title>
            <v-card-text class="pa-0">You can customize your alerts by selecting the users and the activities you want to be notified about on the site.</v-card-text>
        </v-card>

        <v-card-text class="pa-6">
            

            <div class="d-flex flex-row-reverse mt-6">
                <v-btn :disabled="!wasEdited" @click="updateSettingPart(1, 'notifications_settings')">SAVE AND VERIFY</v-btn>
            </div>
        </v-card-text>
    </v-card>

    <v-card class="mb-6 addintional_profile_info"
        :class="{'d-flex flex-row align-start': width >= mobileWidthLimit, 'd-flex flex-column justify-start': width < mobileWidthLimit}"
        :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px; width: inherit;'"
        height="auto">
        
        <v-card class="pa-6"
            :style=" width >= mobileWidthLimit ? 'width: 300px; height: 100%' : 'width: 100%; height: auto'"
            variant="tonal"  
            rounded="0"> 
            <v-card-title class="pa-0">Additional profile info</v-card-title>
            <v-card-text class="pa-0">Customize the additional information displayed on your profile.
            </v-card-text>
        </v-card>


        <v-card-text class="pa-6 w-100" style="position: relative; max-width: 450px;">
            <div class="profile_background" style="position: relative;">

                <p class="text-h6 mb-2">Profile background image</p>
                <v-img class="background_img" v-if="user_data.additional_profile_info.profile_background_img" 
                    max-height='300px' 
                    cover 
                    :src='user_data.additional_profile_info.profile_background_img'>
                </v-img>
 
                <v-img class="background_img" v-else 
                    max-height='300px' 
                    cover 
                    src="https://cdn.vuetifyjs.com/images/parallax/material.jpg" >
                </v-img>
                
                <v-file-input class="edit_profile_background_img d-flex flex-row flex-wrap mt-3 mb-4"
                    v-if="editProfileBackgroundImg"
                    v-model="user_data.additional_profile_info.profile_background_img_new"
                    :error-messages="validator.additional_profile_info.profile_background_img_new.$errors.map(e => e.$message)"
                    @input="validator.additional_profile_info.profile_background_img_new.$touch"
                    :accept="allowedImageExtensions.map(ext => `image/${ext}`).join(', ')"
                    @update:model-value="user_data.additional_profile_info.saved = false"
                    prepend-inner-icon="mdi-image"
                    prepend-icon=""
                    variant="solo"
                    label="Select image">
                </v-file-input>


                <v-btn
                    @click="editProfileBackgroundImg = !editProfileBackgroundImg" 
                    density="comfortable" 
                    icon="mdi-pencil-outline"  
                    style="position: absolute; top: 50px; right: 15px">
                </v-btn>
                <v-btn 
                    v-show="user_data.additional_profile_info.profile_background_img"
                    @click="deleteBackgroundImg" 
                    density="comfortable"
                    icon="mdi-trash-can-outline"  
                    style="position: absolute; top: 95px; right: 15px">
                </v-btn>
            </div>

            <v-card class="profile_avatar mt-3" style="position: relative;">

                <v-card-title>Profile avatar</v-card-title>
                <v-card-text class="d-flex flex-row align-center justify-space-between w-auto">
                    <v-avatar class="avatar pr-2" 
                        v-if="user_data.additional_profile_info.profile_avatar_img" 
                        :image="user_data.additional_profile_info.profile_avatar_img" 
                        :alt="user_data.sign_in.username" 
                        size="120">
                    </v-avatar>

                    <v-icon class="account_icon d-flex pr-2" v-else
                        icon="mdi-account-circle" 
                        size="120">
                    </v-icon>

                    <div class="d-flex flex-column justify-center px-2 w-100">
                        <v-file-input class="edit_avatar d-flex flex-row flex-wrap mb-2"
                            v-if="editAvatarImg"
                            v-model="user_data.additional_profile_info.profile_avatar_img_new"
                            :error-messages="validator.additional_profile_info.profile_avatar_img_new.$errors.map(e => e.$message)"
                            @input="validator.additional_profile_info.profile_avatar_img_new.$touch"
                            :accept="allowedImageExtensions.map(ext => `image/${ext}`).join(', ')"
                            @update:model-value="user_data.additional_profile_info.saved = false"
                            prepend-inner-icon="mdi-image"
                            prepend-icon=""
                            variant="solo"
                            label="Select image">
                        </v-file-input>

                        <v-btn class="delete_avatar"  @click="delete_avatar" :disabled="user_data.additional_profile_info.profile_avatar_img_new == null">Delete avatar</v-btn>
                    </div>
                </v-card-text>
            </v-card>
        
            <v-textarea class="about_info d-flex flex-row flex-wrap"
                v-model="user_data.additional_profile_info.about_info"
                @update:model-value="user_data.additional_profile_info.saved = false"
                auto-grow
                clearable
                variant="solo"
                label="About me"
                rows="1"
            ></v-textarea>

            <v-card class="stats" style="position: relative;">
                
                <v-card-title>Stats</v-card-title>
                <v-card-text>
                    <div class="showcase_container d-flex flex-row align-center pa-2" style="overflow-x: auto;">
                        <DraggableShowcase 
                            :list="user_data.additional_profile_info.statistics.selected"
                            :all_elements_list="user_data.additional_profile_info.statistics.all" 
                            :type="'stats'" 
                            :edit="true"
                            @startDrag="user_data.additional_profile_info.saved = false" 
                            @changeStatOption="changeStatOption"
                            @removeStatBlock="removeStatBlock">
                        </DraggableShowcase>

                        <v-btn class="add_stat_block ml-3"
                            v-if="user_data.additional_profile_info.statistics?.selected?.length < 4"
                            @click="addStatsBlock"
                            icon="mdi-plus" 
                            width="50px"
                            height="50px">
                        </v-btn>
                    </div>
                </v-card-text>
            </v-card>

            <div class="d-flex flex-row-reverse mt-6">
                <v-btn :disabled="validator.additional_profile_info.$errors.length > 0 || user_data.additional_profile_info.backend_errors.length > 0" 
                    @click="updateSettingPart(user_data.additional_profile_info, 'additional_profile_info')">
                    VERIFY AND SAVE
                </v-btn>
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
                v-model='user_data.sign_in.username' 
                :error-messages="user_data.sign_in.backend_errors.username" 
                @update:model-value="resetFields(user_data.sign_in, 'sign_in')" 
                label="USERNAME" 
                type="text" 
                variant="solo"
                color="primary" 
                clearable>

                <template v-slot:append-inner>
                    <v-fade-transition leave-absolute>
                        <v-progress-circular v-if="user_data.sign_in.loading == true" color="info" indeterminate size="24"></v-progress-circular>
                        <v-icon v-else-if="user_data.sign_in.loading == false && user_data.sign_in.verify_success != null"
                            height="24" width="24" 
                            :icon="user_data.sign_in.backend_errors['username'] ? 'mdi-close-circle-outline' : 'mdi-checkbox-marked-circle-outline'" 
                            :color="user_data.sign_in.backend_errors['username'] ? 'error' : 'success'">
                        </v-icon>
                    </v-fade-transition>
                </template>
            </v-text-field>

            <p class="text-h6 mb-2">Change Password</p>

            <v-text-field
                class="d-flex flex-row flex-wrap"
                :model-value="'*'.repeat(minPasswordLength)"
                :type="showCurrPassword ? 'text' : 'password'"
                readonly
                color="primary"
                label="CURRENT PASSWORD"
                variant="solo">
            
                <template v-slot:append-inner>
                    <v-fade-transition leave-absolute>
                        <v-progress-circular v-if="user_data.sign_in.loading == true" color="info" indeterminate size="24"></v-progress-circular>
                        <v-icon v-else-if="user_data.sign_in.loading == false && user_data.sign_in.verify_success != null && user_data.sign_in.current_password != ''"
                            height="24" width="24" 
                            :icon="user_data.sign_in.backend_errors['current_password'] ? 'mdi-close-circle-outline' : 'mdi-checkbox-marked-circle-outline'" 
                            :color="user_data.sign_in.backend_errors['current_password'] ? 'error' : 'success'">
                        </v-icon>
                    </v-fade-transition>
                </template>
            </v-text-field>

            <v-text-field
                class="d-flex flex-row flex-wrap"
                v-model="user_data.sign_in.new_password"
                :append-inner-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showNewPassword ? 'text' : 'password'"
                :error-messages="validator.sign_in.new_password.$errors.map(e => e.$message)"
                @input="validator.sign_in.new_password.$touch" 
                @update:model-value="resetFields(user_data.sign_in, 'sign_in')" 
                @click:append-inner="showNewPassword = !showNewPassword"
                clearable
                color="primary"
                label="NEW PASSWORD"
                variant="solo">


                <template v-slot:append-inner>
                    <v-fade-transition leave-absolute>
                        <v-progress-circular v-if="user_data.sign_in.loading == true" color="info" indeterminate size="24"></v-progress-circular>
                        <v-icon v-else-if="user_data.sign_in.loading == false && user_data.sign_in.verify_success != null && user_data.sign_in.new_password != ''"
                            height="24" width="24" 
                            :icon="user_data.sign_in.backend_errors['new_password'] ? 'mdi-close-circle-outline' : 'mdi-checkbox-marked-circle-outline'" 
                            :color="user_data.sign_in.backend_errors['new_password'] ? 'error' : 'success'">
                        </v-icon>
                    </v-fade-transition>
                </template>
            
            </v-text-field>




            <v-text-field
                class="d-flex flex-row flex-wrap"
                v-model="user_data.sign_in.confirm_new_password"
                :append-inner-icon="showConfirmNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showConfirmNewPassword ? 'text' : 'password'"
                :error-messages="validator.sign_in.confirm_new_password.$errors.map(e => e.$message)"
                @input="validator.sign_in.confirm_new_password.$touch" 
                @update:model-value="resetFields(user_data.sign_in, 'sign_in')" 
                @click:append-inner="showConfirmNewPassword = !showConfirmNewPassword"
                clearable
                color="primary"
                label="CONFIRM NEW PASSWORD"
                variant="solo">

                <template v-slot:append-inner>
                    <v-fade-transition leave-absolute>
                        <v-progress-circular v-if="user_data.sign_in.loading == true" color="info" indeterminate size="24"></v-progress-circular>
                        <v-icon v-else-if="user_data.sign_in.loading == false && user_data.sign_in.verify_success != null && user_data.sign_in.confirm_new_password != ''"
                            height="24" width="24" 
                            :icon="user_data.sign_in.backend_errors['confirm_new_password'] ? 'mdi-close-circle-outline' : 'mdi-checkbox-marked-circle-outline'" 
                            :color="user_data.sign_in.backend_errors['confirm_new_password'] ? 'error' : 'success'">
                        </v-icon>
                    </v-fade-transition>
                </template>
            
            </v-text-field>

            <div class="d-flex flex-row-reverse mt-6">
                <v-btn :disabled="validator.sign_in.$errors.length > 0 || user_data.sign_in.backend_errors.length > 0" 
                    @click="updateSettingPart(user_data.sign_in, 'sign_in')">
                    VERIFY AND SAVE
                </v-btn>
                <!-- <v-btn v-if="user_data.sign_in.verify_success == true  && !user_data.sign_in.saved == true " @click="updateSettingPart(user_data.sign_in, 'sign_in')">VERIFY DATA AND SAVE CHANGES</v-btn> -->
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
 
    <v-card class="mb-6 profile_preview"
        :class="{'d-flex flex-row align-start': width >= mobileWidthLimit, 'd-flex flex-column justify-start': width < mobileWidthLimit}"
        :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'" 
        height="auto">
        
        <v-card class="pa-6"
            :style=" width >= mobileWidthLimit ? 'width: 300px; height: 100%' : 'width: 100%; height: auto'"
            variant="tonal"  
            rounded="0"> 
            <v-card-title class="pa-0">Profile Preview</v-card-title>
            <v-card-text class="pa-0">See how your changes have affected the appearance of the profile.</v-card-text>
        </v-card>

        <v-card-text class="d-flex flex-row-reverse align-center pa-6" :style="width >= mobileWidthLimit ? 'height: 100%;' : ''">
            <v-btn width="100%" @click="profilePreviewDialog = true">PREVIEW PROFILE</v-btn>
        </v-card-text>
    </v-card>

 
    <v-dialog class="ma-0" v-model="profilePreviewDialog" width="auto" scrollable >
        <Profile :user_info="user_data"></Profile>
    </v-dialog>
  
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, computed, onBeforeMount, watchEffect, watch, toRaw } from 'vue';
import { useStore } from 'vuex';
import { useDisplay } from 'vuetify/lib/framework.mjs';
import { useTheme } from 'vuetify/lib/framework.mjs';
import { useVuelidate } from '@vuelidate/core'
import { required, sameAs, minLength, numeric, not, helpers } from '@vuelidate/validators'
import routes from '@/router/router'

import Profile from '@/pages/Profile/Profile.vue'
import DraggableShowcase from '@/components/Profile/DraggableShowcase.vue'

const minPasswordLength = 8
let user_data = ref({
    'personal_info': {'email': '','region': '', 'verify_success': null, 'saved': false, 'loading': false, 'backend_errors': {}},
    'profile_id': {'profile_name': '', 'tagname': '', 'verify_success': null, 'saved': false, 'loading': false, 'backend_errors': {}},
    'additional_profile_info': {
        'profile_background_img': '',
        'profile_background_img_new': '',
        'profile_avatar_img': '',
        'profile_avatar_img_new': '',
        'about_info': '',
        'statistics': {
            'selected':[],
            'all':[]
        },
        'verify_success': null, 'saved': false, 'loading': false, 'backend_errors': {}
    },
    'sign_in': {
        'username': '',
        'current_password': '',
        'new_password': '',
        'confirm_new_password': '',
        'verify_success': null, 'saved': false, 'loading': false, 'backend_errors': {}
    },
})

let initial__user_data = ref(null)

const resetFields = async(current_data, type) => {
    user_data.value[type].verify_success = null
    user_data.value[type].backend_errors = {}
}

const updateSettingPart = async(current_data, type) => {
    let formData = new FormData();
    const data = {}
    // Избавиться от отдельного метода verify и если есть ошибка при изменении данных, то выводить, а если нет, то сразу сохранять

    for(const [key, value] of Object.entries(initial__user_data.value[type])) {
        //Проверяем и отправляем объект только с теми полями, которые были изменены
        if(JSON.stringify(current_data[key]) != JSON.stringify(value)){
            if(key == 'statistics' && 'selected' in value){data[key] = JSON.stringify(current_data[key]['selected'])}
            else if(key == 'profile_background_img_new'){data[key]  = current_data[key][0]}
            else if(key == 'profile_avatar_img_new'){data[key] = current_data[key][0]}
            else{data[key]  = current_data[key]}
        }
    }

    if(Object.entries(data).length !== 0){
        for (var key in data) {formData.append(key, data[key])}

        user_data.value[type].loading = true

        const response = await store.dispatch('accounts/updateUserSettings', formData)
        if(response.status == 200){

            user_data.value[type].verify_success = true
            user_data.value[type].loading = false

            if(type == 'additional_profile_info'){
                if(response.data['background_image']){
                    user_data.value.additional_profile_info.profile_background_img = response.data['background_image']
                    user_data.value.additional_profile_info.profile_background_img_new = ''
                    validator.value.additional_profile_info.profile_background_img_new.$reset()
                    editProfileBackgroundImg.value = false
                }
                else if(response.data['avatar']){
                    user_data.value.additional_profile_info.profile_avatar_img = response.data['avatar']
                    user_data.value.additional_profile_info.profile_avatar_img_new = ''
                    validator.value.additional_profile_info.profile_avatar_img_new.$reset()
                }
                user_data.value.additional_profile_info.saved = true
            }
            else if('new_password' in data){store.commit('auth/logout')}
        }
        else{
            user_data.value[type].verify_success = false
            user_data.value[type].backend_errors = response.data.errors // errors = {'field_name': [error1, error2...]}
            user_data.value[type].loading = false
        }
    }
}

let theme = useTheme()
const { width } = useDisplay();
const store = useStore();

const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})
// let user_data_initial = computed(() => {return store.getters['auth/getUserData']})
// const stats_info = computed(() => {return store.getters['accounts/getShowcaseStats']})

const wasEdited = ref(true)

let showCurrPassword = ref(false);
let showNewPassword = ref(false);
let showConfirmNewPassword = ref(false);

let editableProfileBackgroundImg = ref(false)
let editProfileBackgroundImg = ref(false)
let editAvatarImg = ref(true)
const profilePreviewDialog = ref(false)

let addStat = ref(false)
let statType = ref(false)

const allowedImageExtensions = ref(['jpg', 'jpeg', 'png', 'webp']);
const maxImageSize = ref({'background': 6000000, 'avatar': 2000000})

const validator_rules = computed(() => ({
    additional_profile_info: {
        profile_background_img_new: {
            required: helpers.withMessage('Please select an image file', required),
            maxSize: helpers.withMessage('Maximum file size must not be greater than 2MB', (value) => {
                if (!value[0]) return true;
                const fileSize = value[0].size;
                return fileSize <= maxImageSize.value.background;
            }),
            fileExt: helpers.withMessage('The file must have the extension: *.jpg,*.jpeg,*.png,*.webp', (value) => {
                if (!value[0] || !value[0].name) return true;
                const fileExtension = value[0].name.split('.').pop().toLowerCase();
                return allowedImageExtensions.value.includes(fileExtension);
            })
        },
        profile_avatar_img_new: {
            required: helpers.withMessage('Please select an image file', required),
            maxSize: helpers.withMessage('Maximum file size must not be greater than 2MB', (value) => {
                if (!value[0]) return true;
                const fileSize = value[0].size;
                return fileSize <= maxImageSize.value.avatar;
            }),
            fileExt: helpers.withMessage('The file must have the extension: *.jpg,*.jpeg,*.png,*.webp', (value) => {
                if (!value[0] || !value[0].name) return true;
                const fileExtension = value[0].name.split('.').pop().toLowerCase();
                return allowedImageExtensions.value.includes(fileExtension);
            })
        },
    },
    sign_in: {
        new_password: { 
            required, 
            minLength: minLength(minPasswordLength),
            notOnlyNumeric: helpers.withMessage('Your password can’t be entirely numeric', not(numeric)),
        },
        confirm_new_password: {
            required, 
            sameAs: helpers.withMessage('Password and Confirm Password must be equal', sameAs(user_data.value.sign_in.new_password))
        },
    }
    
}));

const validator = useVuelidate(validator_rules, user_data)


onBeforeMount(async() => {
    const response = await store.dispatch('accounts/getUserSettings')

        user_data.value.personal_info.email = response?.email
        user_data.value.personal_info.region = response?.region
        user_data.value.profile_id.profile_name = response.profile_name
        user_data.value.profile_id.tagname = response.tagname.slice(1)
        user_data.value.additional_profile_info.profile_background_img = response.background_image
        user_data.value.additional_profile_info.profile_avatar_img = response.avatar
        user_data.value.additional_profile_info.about_info = response.about_info
        user_data.value.sign_in.username = response.username
        user_data.value.additional_profile_info.statistics = response.statistics
      

        Object.assign(initial__user_data, JSON.parse(JSON.stringify(user_data)))

   
    

})

const delete_avatar =async() =>{
    if(user_data.value.additional_profile_info.profile_avatar_img != null){
        user_data.value.additional_profile_info.profile_avatar_img = ''
        const formData = new FormData();
        formData.append('profile_avatar_img_new', null)

        await store.dispatch('accounts/updateUserSettings', formData)
    }
}

const deleteBackgroundImg =async() =>{
    if(user_data.value.additional_profile_info.profile_background_img != null){
        user_data.value.additional_profile_info.profile_background_img = ''
        const formData = new FormData();
        formData.append('profile_avatar_img_new', null)

        await store.dispatch('accounts/updateUserSettings', formData)
    }
}


const addStatsBlock =() => { 
    addStat.value = true;
    user_data.value.additional_profile_info.saved = false
    store.commit('accounts/addStatBlock')
}

const removeStatBlock =(order) => {
    user_data.value.additional_profile_info.saved = false
    store.commit('accounts/removeStatBlock', order)
}

const changeStatOption =(type) =>{
    statType.value = type
    store.commit('accounts/updateCountStats', type)
}


</script>

<style lang="scss" scoped>
    .clickable{
        &:hover{cursor: pointer;}
    }
</style>

