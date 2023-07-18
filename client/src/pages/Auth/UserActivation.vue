<template>

<div class='d-flex flex-column align-center justify-center h-100 w-100'>
  <v-card width="98%" max-width="550" :variant="width <= 740 ? 'flat' : 'elevated'" > 
    
    <v-card-item class="text-subtitle-1">
        <div class="d-flex flex-row align-center"> 
            <v-icon class='mr-2' size="40" :color="activationSuccessed ? 'success' : 'error'" :icon="activationSuccessed ? 'mdi-account-check-outline' : 'mdi-account-alert-outline'"></v-icon>
        
            <div class="d-flex flex-column" v-if="activationSuccessed">
                <v-card-title style="white-space: normal;" >Your account has been successfully activated</v-card-title>
            </div>

            <div class="d-flex flex-column" v-else>
                <v-card-title style="white-space: normal;" >Some error occurred during account activation</v-card-title>
            </div>
        
        </div>
    </v-card-item>

    <v-card-text class="text-subtitle-1 text-center py-4">
        <div v-if="activationSuccessed" style="white-space: normal;" >
            You can proceed to LogIn
        </div>
        <div v-else style="white-space: normal;" >
            Please enter the e-mail address to which you want to send a new activation code and click the "retry activation message" button
        </div>
    </v-card-text>

    <v-divider class="mx-4 mb-1" v-if="!activationSuccessed"></v-divider>

    <v-container class="pt-1">  
      <form>
        <v-text-field
            v-if="!activationSuccessed"
            v-model="formdata.email"
            :error-messages="validationsErrors.email !== ''? validationsErrors.email : actvation_form_validator.email.$errors.map(e => e.$message)"
            @input="actvation_form_validator.email.$touch"
            @blur="actvation_form_validator.email.$touch"
            clearable
            color="primary"
            label="Email"
            variant="underlined"
        ></v-text-field>

        <v-card-actions class="d-flex flex-row justify-center pt-2">
          <v-btn v-if="activationSuccessed" width='95%' variant="outlined" color="success" @click="$router.push({ name: 'login'})">Go to LogIn</v-btn>
          <v-btn v-else width='95%' variant="outlined" color="success" @click="retryActiovationMessage">Retry activation message</v-btn>
        </v-card-actions>
      </form>
    </v-container>

  </v-card>
</div>
</template>


<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import { useStore } from 'vuex';
import { useVuelidate } from '@vuelidate/core';
import {useDisplay} from 'vuetify'
import { email, required} from '@vuelidate/validators';

import router from '@/router/router';

const { width } = useDisplay();
const store = useStore()

const {uid, token} = router.currentRoute.value.query
const activationSuccessed = ref(true)

const formdata = ref({'email': ''})
const validationsErrors = ref({'email': '',})
const validator_rules = computed(() => {
  return {
    email: { required, email }
  };
});

const actvation_form_validator = useVuelidate(validator_rules, formdata)


const activateUser = () => {
    store.dispatch("auth/user_activate", {uid: uid, token:token}).then(
      () => { activationSuccessed.value = true },
      (error) => { activationSuccessed.value = true }
    )
}

onBeforeMount(() => {
    activateUser();
})

const retryActiovationMessage = () => {
    store.dispatch("auth/resend_activation_email", formdata.value.email).then(
      () => { activationSuccessed.value = true },
      (error) => { activationSuccessed.value = false }
    )
}
</script>

<style lang="scss" scoped>
</style>