<template>
<div class='d-flex flex-column align-center justify-center h-100 w-100'>
  <v-card width="98%" max-width="550" :variant="width <= mobileWidthLimit ? 'flat' : 'elevated'">
        
      <v-card-item class="py-3 px-4">
          <v-card-title class="mb-2">Reset your Password</v-card-title>
          <v-card-subtitle style="white-space: normal;">Enter a new password and confirm it</v-card-subtitle>
          <v-card-subtitle style="white-space: normal;">Insert the confirmation code sent to the e-mail from the previous step</v-card-subtitle>
      </v-card-item>

      <v-card-text class="text-subtitle-1 pb-4">
        <form>
          <v-text-field
              v-model="formdata.new_password"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
              :error-messages="validationErrors.new_password !== ''? validationErrors.new_password : validator.new_password.$errors.map(e => e.$message)"
              @input="validator.new_password.$touch"
              @blur="validator.new_password.$touch"
              clearable
              hint="At least 8 characters"
              counter
              color="primary"
              label="New Password"
              variant="underlined"
          ></v-text-field>

          <v-text-field
              v-model="formdata.confirm_password"
              :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showConfirmPassword ? 'text' : 'password'"
              @click:append="showConfirmPassword = !showConfirmPassword"
              :error-messages="validator.confirm_password.$errors.map(e => e.$message)"
              @input="validator.confirm_password.$touch"
              @blur="validator.confirm_password.$touch"
              clearable
              hint="At least 8 characters"
              counter
              color="primary"
              label="Confirm Password"
              variant="underlined"
          ></v-text-field>

          <v-text-field
                v-model="formdata.confirmation_code"
                :error-messages="validationErrors.confirmation_code !== ''? validationErrors.confirmation_code : validator.confirmation_code.$errors.map(e => e.$message)"
                @input="validator.confirmation_code.$touch"
                @blur="validator.confirmation_code.$touch"
                clearable
                color="primary"
                label="Confirmation Code"
                variant="underlined"
            ></v-text-field>

          <v-card-actions class="d-flex flex-row justify-center">
            <v-btn width='95%' variant="outlined" color="success" :disabled = 'validator.$errors.length > 0' @click="submitForm(formdata)">
                Complete reset password
            </v-btn>
          </v-card-actions>

          <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style="white-space: pre-wrap;">
            <span class="link text-info font-weight-bold" style="cursor: pointer" @click="$router.push({ name: 'login'})" >Back to LogIn</span>  
          </div>
        </form>
      </v-card-text>

  </v-card>
</div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useStore } from 'vuex';
import { useVuelidate } from '@vuelidate/core'
import { required, sameAs, minLength, maxLength, numeric, not, helpers} from '@vuelidate/validators'
import {useDisplay} from 'vuetify'
import router from '@/router/router';

const { width } = useDisplay();
const store = useStore();

let showPassword = ref(false);
let showConfirmPassword = ref(false);
const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})

const formdata = ref({
    'new_password': '',
    'confirm_password': '',
    'confirmation_code': '',
})

//Custom validations errors from backend
const validationErrors = ref({
    'new_password': '',
    'confirmation_code': '',
})

// Watch for textfield changes (remove the error display when data is changed in the field)
watch(() => formdata.value, (new_obj) => {
  for(const[key, value] of Object.entries(new_obj)){
    if(new_obj[key] == '' || new_obj[key] === null || new_obj.agree_terms == true){
      validationErrors.value[key] = ''
    }
  }
},{deep: true}
)

const validator_rules = computed(() => {
  return {
    new_password: { 
      required, 
      minLength: minLength(8),
      notOnlyNumeric: helpers.withMessage('Your password can’t be entirely numeric', not(numeric)),
    },
    confirm_password: {
      required, 
      sameAs: helpers.withMessage('Password and Confirm Password must be equal', sameAs(formdata.value.new_password))
    },
    confirmation_code: {required, maxLength: maxLength(6)}
  };
});

const validator = useVuelidate(validator_rules, formdata)

const submitForm =(data) =>{
  if(validator.$errors == undefined){
    store.dispatch("auth/reset_password_confirm", {new_password:data.new_password, confirmation_code: data.confirmation_code}).then(
        () => {
          store.commit('auth/logout')
          router.push({ name: 'login'})},
        (error) => {
          if(!error.response.data.message.isArray){
              validationErrors.value['confirmation_code'] = error.response.data.message
          }
          else{
            for(const [key, value] of Object.entries(error.response.data.message)){
              validationErrors.value[key] = value[0]
            }
          }   
        }
    )
  }

}

</script>