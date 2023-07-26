<template>

<div class='d-flex flex-column align-center justify-center h-100 w-100'>
  <v-card width="98%" max-width="550" :variant="width <= 740 ? 'flat' : 'elevated'" > 
  
    <div class="confirm_code_card" v-if="activationSuccessed === null">
      <v-card-item class="text-subtitle-1">
              <div class="d-flex flex-column">
                  <v-card-title class='mb-2' style="white-space: normal;">Account activation</v-card-title>
                  <v-card-subtitle style="white-space: normal;">We have sent a temporary confirmation code to {{router.currentRoute.value.params.email}}</v-card-subtitle>
                  <v-card-subtitle style="white-space: normal;">Enter the code to confirm account creation</v-card-subtitle>
              </div>
      </v-card-item>

      <v-card-text class="text-subtitle-1 pb-4">
          <form>
            <v-text-field
                v-model="formdata.confirmation_code"
                :error-messages="validationsErrors.confirmation_code !== ''? validationsErrors.confirmation_code : validator.confirmation_code.$errors.map(e => e.$message)"
                @input="validator.confirmation_code.$touch"
                @blur="validator.confirmation_code.$touch"
                clearable
                color="primary"
                label="Confirmation Code"
                variant="underlined"
            ></v-text-field>

            <v-btn class="px-0 mb-2" prepend-icon="mdi-refresh"  variant="text" @click="resendConfirmationCode">Resend Confirmation Code</v-btn>
            <v-card-actions class="d-flex flex-row justify-center pt-2">
              <v-btn width='95%' variant="outlined" color="success" :disabled = 'validator.$errors.length > 0' @click="activateUser">Confirm Account Creation</v-btn>
            </v-card-actions>
          </form>
          
      </v-card-text>
    </div>

    <div class="confirm_result_card" v-else>
      <v-card-item class="text-subtitle-1">
            <div class="d-flex flex-column">
                <div class="d-flex flex-row align-center mb-2">
                  <v-icon class='mr-2' size="40" :color="activationSuccessed ? 'success' : 'error'" :icon="activationSuccessed ? 'mdi-account-check-outline' : 'mdi-account-alert-outline'"></v-icon>
                  <v-card-title style="white-space: normal;">Account status</v-card-title>
                </div>

                <div v-if="activationSuccessed">
                  <v-card-subtitle style="white-space: normal;">Your account has been successfully activated</v-card-subtitle>
                  <v-card-subtitle style="white-space: normal;">You can proceed to LogIn</v-card-subtitle>

                </div>            
            </div>
      </v-card-item>

      <v-card-text class="text-subtitle-1 pb-4">
        <form>
          <v-text-field
              v-if="!activationSuccessed"
              v-model="formdata.email"
              :error-messages="validationsErrors.email !== ''? validationsErrors.email : validator.email.$errors.map(e => e.$message)"
              @input="validator.email.$touch"
              @blur="validator.email.$touch"
              clearable
              color="primary"
              label="Email"
              variant="underlined"
          ></v-text-field>

          <v-card-actions class="d-flex flex-row justify-center pt-2">
            <v-btn v-if="activationSuccessed" width='95%' variant="outlined" color="success" @click="$router.push({ name: 'login'})">Go to LogIn</v-btn>
            <v-btn v-else prepend-icon="mdi-refresh" width='95%' variant="outlined" color="success" @click="resendConfirmationCode">Resend Confirmation Code</v-btn>
          </v-card-actions>
        </form>
      </v-card-text>
    </div>

  </v-card>
</div>
</template>


<script setup>
import { ref, computed, watch } from 'vue';
import { useStore } from 'vuex';
import { useVuelidate } from '@vuelidate/core';
import {useDisplay} from 'vuetify'
import { email, required, maxLength} from '@vuelidate/validators';
import router from '@/router/router';

const { width } = useDisplay();
const store = useStore()


const activationSuccessed = ref(null)

const formdata = ref({'email': '', 'confirmation_code': ''})
const validationsErrors = ref({'email': '', 'confirmation_code': ''})
const validator_rules = computed(() => {
  return {
    email: { required, email },
    confirmation_code: {required,maxLength: maxLength(6)}
  };
});

const validator = useVuelidate(validator_rules, formdata)


// Watch for textfield changes (remove the error display when data is changed in the field)
watch(() => formdata.value, (new_obj) => {
  for(const[key, value] of Object.entries(new_obj)){
    if(new_obj[key] == '' || new_obj[key] === null || new_obj.agree_terms == true){
      validationsErrors.value[key] = ''
    }
  }
},{deep: true}
)

const resendConfirmationCode = () => {
    store.dispatch("auth/send_confirmation_code", router.currentRoute.value.params.email).then(
      () => {},
      (error) => { 
        console.log(error)
      }
    )
}

const activateUser = () => {
  if(validator.$errors == undefined){
    store.dispatch("auth/user_activate", formdata.value.confirmation_code).then(
      () => { activationSuccessed.value = true },
      (error) => {
        validationsErrors.value['confirmation_code'] = error.response.data.message  
      }
    )
  }
}

</script>

<style lang="scss" scoped>
</style>