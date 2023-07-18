<template>
<div class='d-flex flex-column align-center justify-center h-100 w-100'>
  <v-card width="98%" max-width="550" :variant="width <= 740 ? 'flat' : 'elevated'">
        
      <v-card-item class="py-3 px-4">
          <v-card-title>Reset your Password</v-card-title>
      </v-card-item>

      <v-container>
      <form>
          <v-text-field
              v-model="formdata.password"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
              :error-messages="validationErrors.password !== ''? validationErrors.password : validator.password.$errors.map(e => e.$message)"
              @input="validator.password.$touch"
              @blur="validator.password.$touch"
              clearable
              hint="At least 8 characters"
              counter
              color="primary"
              label="Password"
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


          <v-card-actions class="d-flex flex-row justify-center">
            <v-btn width='95%' variant="outlined" color="success" @click="submitForm(formdata)">
                Complete reset password
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
import { ref, computed, watch } from 'vue';
import { useStore } from 'vuex';
import { useVuelidate } from '@vuelidate/core'
import { required, sameAs, minLength, numeric, not, helpers} from '@vuelidate/validators'
import {useDisplay} from 'vuetify'
import router from '@/router/router';

const { width } = useDisplay();
const store = useStore();

const {uid, token} = router.currentRoute.value.query
let showPassword = ref(false);
let showConfirmPassword = ref(false);

const formdata = ref({
    'password': '',
    'confirm_password': '',
})

//Custom validations errors from backend
const validationErrors = ref({
    'password': '',
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
    password: { 
      required, 
      minLength: minLength(8),
      notOnlyNumeric: helpers.withMessage('Your password can’t be entirely numeric', not(numeric)),
    },
    confirm_password: {
      required, 
      sameAs: helpers.withMessage('Password and Confirm Password must be equal', sameAs(formdata.value.password))
    },
  };
});

const validator = useVuelidate(validator_rules, formdata)


const submitForm =(data) =>{

  store.dispatch("auth/reset_password_confirm", {uid: currURLObj.value.uid, token: currURLObj.value.token, new_password:data.password, re_new_password: data.confirm_password}).then(
      () => {router.push({ name: 'login'})},
      (error) => {console.log(error)}
  )

}

</script>