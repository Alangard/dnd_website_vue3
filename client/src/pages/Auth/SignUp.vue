<template>
<div class='d-flex flex-column align-center justify-center h-100 w-100'>
  <v-card width="98%" max-width="550" :variant="width <= 740 ? 'flat' : 'elevated'">
        
      <v-card-item class="py-3 px-4">
          <v-card-title>Create account</v-card-title>
      </v-card-item>

      <v-container>
      <form>
          <v-text-field
              v-model="formdata.username"
              :error-messages="validationErrors.username !== ''? validationErrors.username : validator.username.$errors.map(e => e.$message)"
              @input="validator.username.$touch"
              @blur="validator.username.$touch"
              hint="No more than 30 characters"
              counter
              clearable
              color="primary"
              label="Username"
              variant="underlined"
          ></v-text-field>

          <v-text-field
              v-model="formdata.email"
              :error-messages="validationErrors.email !== ''? validationErrors.email : validator.email.$errors.map(e => e.$message)"
              @input="validator.email.$touch"
              @blur="validator.email.$touch"
              clearable
              color="primary"
              label="Email"
              variant="underlined"
          ></v-text-field>

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

          <v-checkbox 
            v-model="formdata.agree_terms"
            :error-messages="validationErrors.agree_terms"
            required
            color="secondary">

              <template v-slot:label>
              <div>
                  I agree to
                  <v-tooltip location="bottom" v-for="(item, index) in terms_services" :key="index">
                    <template v-slot:activator="{ props }">
                        <a class='text-primary' target="_blank" :href="item.link" v-bind="props" @click.stop>
                        {{item.document_name}}
                        </a>
                        {{helper.Separator(index, terms_services)}}
                    </template>
                  </v-tooltip>
              </div>
              </template>
          </v-checkbox>

          <v-card-actions class="d-flex flex-row justify-center">
          <v-btn width='95%' variant="outlined" color="success" @click="submitForm(formdata)">
              Complete Registration
          </v-btn>
          </v-card-actions>

          <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style=" white-space: pre-wrap;">
              Already have an account? <span class="text-primary text-decoration-underline" style="cursor: pointer" @click="router.push({ name: 'login'})">Log In</span>  
          </div>
      </form>
      </v-container>

  </v-card>
</div>
</template>

<script setup>
import {ref, computed, defineProps, watch} from 'vue';
import {useStore} from 'vuex';
import { useVuelidate } from '@vuelidate/core'
import { email, required, sameAs, minLength, maxLength, numeric, not, helpers} from '@vuelidate/validators'
import {useDisplay} from 'vuetify'
import router from '@/router/router';
import helper from '@/helpers'

const { width } = useDisplay();
const props = defineProps(['currURLObj'])
const store = useStore();

let showPassword = ref(false);
let showConfirmPassword = ref(false);

const formdata = ref({
    'username': '',
    'email': '',
    'password': '',
    'confirm_password': '',
    'agree_terms': false,
})

//Custom validations errors from backend
const validationErrors = ref({
    'username': '',
    'email': '',
    'password': '',
    'agree_terms': ''
})

// Array of website agreement documents
const terms_services = [
  {document_name: 'Terms', link: '#'},
  {document_name: 'Privacy Policy', link: '#'},
]

// Watch for textfield changes (remove the error display when data is changed in the field)
watch(() => formdata.value, (new_obj) => {
  for(const[key, value] of Object.entries(new_obj)){
    if(new_obj[key] == '' || new_obj[key] === null || new_obj.agree_terms == true){
      validationErrors.value[key] = ''
    }
  }
},{deep: true}
)

//Check if the field matches the username or email
const containPersonalData = () => (value) =>  {
  for(const element of [formdata.value.username, formdata.value.email.split('@')[0]]){
    if(value == element){return false}
  }
  return true
}

const validator_rules = computed(() => {
  return {
    username: { 
      required, 
      maxLength: helpers.withMessage('Your username is longer than 30 characters', maxLength(30)),
    },

    email: { required, email },
    password: { 
      required, 
      minLength: minLength(8),
      notOnlyNumeric: helpers.withMessage('Your password can’t be entirely numeric', not(numeric)),
      notIncludePersonalInfo: helpers.withMessage('Your password can’t be your username or email', containPersonalData)
    },
    confirm_password: {
      required, 
      sameAs: helpers.withMessage('Password and Confirm Password must be equal', sameAs(formdata.value.password))
    },
  };
});

const validator = useVuelidate(validator_rules, formdata)


const submitForm =(data) =>{

  const user_data = {'username': data.username, 'email': data.email, 'password': data.password, 're_password': data.confirm_password}

  if(data.agree_terms){
      store.dispatch("auth/register", user_data)
      .then(
        () => {authOptions.value = 'log_in'},
        (error) => {
          for(const [key, value] of Object.entries(error.response.data)){validationErrors.value[key] = value[0]}
        }
      );
  }
  else{validationErrors.value.agree_terms = 'You must agree to the Terms and Privacy Policy'}
}

</script>

<style lang='scss' scoped></style>