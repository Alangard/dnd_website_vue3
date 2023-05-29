<template>
    <v-dialog class="auth_dialog" width="auto" max-width="550" min-width="350" >
        <v-card title="Log In" v-if="authOptions == 'log_in'">
          <v-container>

            <v-text-field
                v-model="formdata_logIn.username"
                color="primary"
                label="Username"
                variant="underlined"
            ></v-text-field>

            <v-text-field
                v-model="formdata_logIn.password"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPassword ? 'text' : 'password'"
                @click:append="showPassword = !showPassword"
                :rules="[rules.required, rules.min]"
                hint="At least 8 characters"
                counter
                color="primary"
                label="Password"
                variant="underlined"
            ></v-text-field>

            <div class="d-flex flex-row justify-space-between align-start">
              <v-checkbox
                v-model="formdata_logIn.remember"
                label="Remember"
                color="secondary"
                hide-details="true"
              ></v-checkbox>

              <div class='d-flex font-weight-regular text-capitalize text-medium-emphasis text-subtitle-1 text-primary text-decoration-underline'  style="margin-top: 14px; cursor: pointer;" @click="forgotPasswordClick">
                Forgot Password?
              </div>
            </div>

            <v-card-actions class="d-flex flex-row justify-center">
              <v-btn width='95%' variant="outlined" color="success" @click="submitLoginForm(formdata_logIn)">
                  Log In
              </v-btn>
            </v-card-actions>

            <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style="white-space: pre-wrap;">
                Don't have an account? <span class="link text-primary text-decoration-underline" style="cursor: pointer" @click="authOptions = 'sign_up'" >Sign up</span>  
            </div>
          </v-container>



          <!-- <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style=" white-space: pre-wrap;">
                Or<span class="text-primary"> Log In </span>with<span class="text-secondary"> Social Media</span>
                
          </div> -->



        </v-card>

        <v-card class="mx-auto" title="Create account" v-if="authOptions == 'sign_up'">
            <v-container>
              <form>
                <v-text-field
                    v-model="formdata_singUp.username"
                    :error-messages="v$.username.$errors.map(e => e.$message)"
                    @input="v$.username.$touch"
                    @blur="v$.username.$touch"
                    hint="No more than 30 characters"
                    counter
                    clearable
                    color="primary"
                    label="Username"
                    variant="underlined"
                ></v-text-field>

                <v-text-field
                    v-model="formdata_singUp.email"
                    :error-messages="v$.email.$errors.map(e => e.$message)"
                    @input="v$.email.$touch"
                    @blur="v$.email.$touch"
                    clearable
                    color="primary"
                    label="Email"
                    variant="underlined"
                ></v-text-field>

                <v-text-field
                    v-model="formdata_singUp.password"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword ? 'text' : 'password'"
                    @click:append="showPassword = !showPassword"
                    :error-messages="v$.password.$errors.map(e => e.$message)"
                    @input="v$.password.$touch"
                    @blur="v$.password.$touch"
                    clearable
                    hint="At least 8 characters"
                    counter
                    color="primary"
                    label="Password"
                    variant="underlined"
                ></v-text-field>

                <v-text-field
                    v-model="formdata_singUp.confirm_password"
                    :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showConfirmPassword ? 'text' : 'password'"
                    @click:append="showConfirmPassword = !showConfirmPassword"
                    :error-messages="v$.confirm_password.$errors.map(e => e.$message)"
                    @input="v$.confirm_password.$touch"
                    @blur="v$.confirm_password.$touch"
                    clearable
                    hint="At least 8 characters"
                    counter
                    color="primary"
                    label="Confirm Password"
                    variant="underlined"
                ></v-text-field>

                <v-checkbox 
                  v-model="formdata_singUp.agree_terms"
                  :error-messages="singUpValidationErrors.agree_terms"
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
                            {{separator(index)}}
                          </template>
                        </v-tooltip>
                      </div>
                    </template>
                </v-checkbox>

                <v-card-actions class="d-flex flex-row justify-center">
                  <v-btn width='95%' variant="outlined" color="success" @click="submitSignUpForm(formdata_singUp)">
                      Complete Registration
                  </v-btn>
                </v-card-actions>

                <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style=" white-space: pre-wrap;">
                    Already have an account? <span class="text-primary text-decoration-underline" style="cursor: pointer" @click="authOptions = 'log_in'">Log In</span>  
                </div>
              </form>
            </v-container>
        </v-card>
    </v-dialog>

</template>

<script setup>
import {ref, computed, defineProps, defineEmits, watch} from 'vue';
import {useStore} from 'vuex';
import axios from 'axios';
import { useVuelidate } from '@vuelidate/core'
import { email, required, sameAs, minLength, maxLength, numeric, not, helpers} from '@vuelidate/validators'

const props = defineProps(['authDialog'])
const emit = defineEmits(['closeAuthDialog'])
const store = useStore();

let showPassword = ref(false);
let showConfirmPassword = ref(false);
let authOptions = ref('log_in')

const formdata_singUp = ref({
    'username': '',
    'email': '',
    'password': '',
    'confirm_password': '',
    'agree_terms': false,
})

const singUpValidationErrors = ref({
    'username': '',
    'email': '',
    'password': '',
    'agree_terms': ''
})

const formdata_logIn = ref({
  'username': '',
  'password': '',
  'remember': false,
})


watch(() => formdata_singUp.value, (new_obj) => {
  if(new_obj.agree_terms) singUpValidationErrors.value = ''
},{deep: true}
)

const terms_services = [
  {document_name: 'Terms', link: '#'},
  {document_name: 'Privacy Policy', link: '#'},
]

const separator = (index, array_of_objects = terms_services) => {
  if(array_of_objects.length > 2){
    if(index == array_of_objects.length - 2){return ' and '}
    else if(index < array_of_objects.length - 1){return ', '}
    else{return ''}
  }
  else if(array_of_objects.length == 2){
    if(index < 1){return ' and '}
  }
}

const containPersonalData = () => (value) =>  {
  for(const element of [formdata_singUp.value.username, formdata_singUp.value.email.split('@')[0]]){
    if(value == element){return false}
  }
  return true
}

const rules_signup = computed(() => {
  return {
    username: { 
      required, 
      maxLength: helpers.withMessage('Your username is longer than 30 characters', maxLength(5)),
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
      sameAs: helpers.withMessage('Password and Confirm Password must be equal', sameAs(formdata_singUp.value.password))
    },
  };
});

const v$ = useVuelidate(rules_signup, formdata_singUp)


const rules = ref( {
    required: value => !!value || 'Required.',
    min: v => v.length >= 8 || 'Min 8 characters',
    emailMatch: () => (`The email and password you entered don't match`),
})


const submitLoginForm =(data) => {
    const user_data = {'username': data.username, 'password': data.password}

    store.dispatch('auth_login',{'url': 'auth/token/create/', 'userdata': user_data})
    .then(() => {
      const status = store.getters.getCurrUserResponseStatus
      if(status == 200){
        emit('closeAuthDialog');
      }
    }) 
}

const submitSignUpForm =async (data) =>{

  const user_data = {'username': data.username, 'email': data.email, 'password': data.password}

  if(data.agree_terms){
    
    store.dispatch('create_account', {'url': 'account/create/', 'userdata': user_data}).then(()=>{
    const status = store.getters.getCurrUserResponseStatus
    const error_info = store.getters.getCurrUserError

    if(status == 200 || status == 201){
        store.dispatch('auth_login', {'url': 'auth/token/create/', 'userdata': {'username': user_data.username, 'password': user_data.password}})
        emit('closeAuthDialog');
      }
    else{
      console.log(error_info.response.data)
    }
  })
  }
  else{
    singUpValidationErrors.value.agree_terms = 'You must agree to the Terms and Privacy Policy'
  }



 





  
  

}


</script>

<style lang="scss" scoped>
</style>
