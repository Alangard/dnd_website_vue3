<template>
<div class='d-flex flex-column align-center justify-center h-100 w-100'>
  <v-card width="98%" max-width="550" :variant="width <= 740 ? 'flat' : 'elevated'"> 

  <div class="confirm_code_card">
      <v-card-item class="text-subtitle-1">
              <div class="d-flex flex-column">
                  <v-card-title class='mb-2' style="white-space: normal;">Reset your Password</v-card-title>
                  <v-card-subtitle style="white-space: normal;">The confirmation code will be sent to the mailbox</v-card-subtitle>
                  <v-card-subtitle style="white-space: normal;">Please enter your email</v-card-subtitle>
              </div>
      </v-card-item>

      <v-card-text class="text-subtitle-1 pb-4">
          <form>
            <v-text-field
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
              <v-btn width='95%' variant="outlined" color="success" :disabled = 'validator.$errors.length > 0' @click="sendConfirmationCode">Send Confirmation Code</v-btn>
            </v-card-actions>
          </form>
      </v-card-text>
    </div>
  </v-card>
</div>
</template>

<script setup>
import {ref, computed, watch} from 'vue';
import {useStore} from 'vuex';
import { useVuelidate } from '@vuelidate/core'
import { email, required, maxLength} from '@vuelidate/validators'
import router from '@/router/router';
import {useDisplay} from 'vuetify'

const { width } = useDisplay();
const store = useStore();

const formdata = ref({'email': ''})
const validationsErrors = ref({'email': ''})
const validator_rules = computed(() => {
  return {
    email: { required, email },
  };
});

const validator = useVuelidate(validator_rules, formdata)


// Watch for textfield changes (remove the error display when data is changed in the field)
watch(() => formdata.value, (new_obj) => {
  for(const[key, value] of Object.entries(new_obj)){
    if(new_obj[key] == ''){
      validationsErrors.value[key] = ''
    }
  }
},{deep: true}
)

const sendConfirmationCode = () => {
  if(validator.$errors == undefined){
    store.dispatch("auth/send_confirmation_code", formdata.value.email).then(
      () => { 
        router.push({ name: 'reset_password_confirmation', params: {'email' : formdata.value.email }}) 
      },
      (error) => {
        validationsErrors.value['email'] = error.response.data.message  
      }
    )
  }
}

</script>

<style lang='scss' scoped></style>