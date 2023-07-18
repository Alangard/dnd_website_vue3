<template>
<div class='d-flex flex-column align-center justify-center h-100 w-100'>
  <v-card width="98%" max-width="550" :variant="width <= 740 ? 'flat' : 'elevated'"> 

    <v-card-item class="py-3 px-4">
      <v-card-title>Reset your Password</v-card-title>
      <v-card-subtitle>The verification email will be sent to the mailbox.</v-card-subtitle>
      <v-card-subtitle>Please check it.</v-card-subtitle>
    </v-card-item>

    <v-container>
      <form>
        <v-text-field
            v-model="formdata.email"
            :error-messages="validationsErrors.email !== ''? validationsErrors.email : reset_pass_validator.email.$errors.map(e => e.$message)"
            @input="reset_pass_validator.email.$touch"
            @blur="reset_pass_validator.email.$touch"
            clearable
            color="primary"
            label="Email"
            variant="underlined"
        ></v-text-field>

        <v-card-actions class="d-flex flex-row justify-center">
          <v-btn width='95%' variant="outlined" color="success" @click="submitResetForm(formdata)">
              Send
          </v-btn>
        </v-card-actions>

        <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style="white-space: pre-wrap;">
          <span class="link text-info font-weight-bold" style="cursor: pointer" @click="$router.push({ name: 'login'})" >Back to Login</span>  
        </div>
      </form>
    </v-container>


  </v-card>
</div>
</template>

<script setup>
import {ref, computed, defineProps} from 'vue';
import {useStore} from 'vuex';
import { useVuelidate } from '@vuelidate/core'
import { email, required} from '@vuelidate/validators'
import router from '@/router/router';
import {useDisplay} from 'vuetify'

const { width } = useDisplay();
const props = defineProps(['currURLObj'])
const store = useStore();

const formdata = ref({'email': ''})

const validationsErrors = ref({'email': '',})

const validator_rules = computed(() => {
  return {
    email: { required, email }
  };
});

const reset_pass_validator = useVuelidate(validator_rules, formdata)

const submitResetForm = () => {
  store.dispatch("auth/reset_password", formdata.value.email).then(
      () => {},
      (error) => {}
  )
  router.push({ name: 'reset_pass_confirm'})
}
</script>

<style lang='scss' scoped></style>