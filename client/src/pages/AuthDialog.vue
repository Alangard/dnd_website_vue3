<template>
    <v-dialog class="auth_dialog" width="auto" max-width="550" min-width="350" >
        <v-card v-if="authOptions == 'log_in'">

          <v-card-item class="py-3 px-4">
            <v-card-title>Log In</v-card-title>
          </v-card-item>

          <v-container v-if="login_error.state">
              <v-alert 
                density="compact"
                type="error"
                :text="login_error.text"
              ></v-alert>
          </v-container>

          <v-container>
            <form>
              <v-text-field
                  v-model="formdata_logIn.username"
                  clearable
                  color="primary"
                  label="Username"
                  variant="underlined"
              ></v-text-field>

              <v-text-field
                  v-model="formdata_logIn.password"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showPassword ? 'text' : 'password'"
                  @click:append="showPassword = !showPassword"
                  clearable
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
            </form>
          </v-container>

          <!-- <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style=" white-space: pre-wrap;">
                Or<span class="text-primary"> Log In </span>with<span class="text-secondary"> Social Media</span>
                
          </div> -->

        </v-card>

        <v-card v-if="authOptions == 'sign_up'">
          
          <v-card-item class="py-3 px-4">
            <v-card-title>Create account</v-card-title>
          </v-card-item>
    
          <v-container>
            <form>
              <v-text-field
                  v-model="formdata_singUp.username"
                  :error-messages="singUpValidationErrors.username !== ''? singUpValidationErrors.username : signup_validator.username.$errors.map(e => e.$message)"
                  @input="signup_validator.username.$touch"
                  @blur="signup_validator.username.$touch"
                  hint="No more than 30 characters"
                  counter
                  clearable
                  color="primary"
                  label="Username"
                  variant="underlined"
              ></v-text-field>

              <v-text-field
                  v-model="formdata_singUp.email"
                  :error-messages="singUpValidationErrors.email !== ''? singUpValidationErrors.email : signup_validator.email.$errors.map(e => e.$message)"
                  @input="signup_validator.email.$touch"
                  @blur="signup_validator.email.$touch"
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
                  :error-messages="singUpValidationErrors.password !== ''? singUpValidationErrors.password : signup_validator.password.$errors.map(e => e.$message)"
                  @input="signup_validator.password.$touch"
                  @blur="signup_validator.password.$touch"
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
                  :error-messages="signup_validator.confirm_password.$errors.map(e => e.$message)"
                  @input="signup_validator.confirm_password.$touch"
                  @blur="signup_validator.confirm_password.$touch"
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

        <v-card v-if="authOptions == 'reset_pass'">

          <v-card-item class="py-3 px-4">
            <v-card-title>Reset your Password</v-card-title>
            <v-card-subtitle>The verification email will be sent to the mailbox.</v-card-subtitle>
            <v-card-subtitle>Please check it.</v-card-subtitle>
          </v-card-item>

          <v-container>
            <form>
              <v-text-field
                  v-model="formdata_reset_pass.username"
                  :error-messages="resetPasswordValidationErrors.username !== ''? resetPasswordValidationErrors.username : reset_pass_validator.username.$errors.map(e => e.$message)"
                  @input="reset_pass_validator.username.$touch"
                  @blur="reset_pass_validator.username.$touch"
                  clearable
                  color="primary"
                  label="Username"
                  variant="underlined"
              ></v-text-field>

              <v-text-field
                  v-model="formdata_reset_pass.verification_code"
                  :error-messages="resetPasswordValidationErrors.verification_code !== ''? resetPasswordValidationErrors.verification_code : reset_pass_validator.verification_code.$errors.map(e => e.$message)"
                  @input="reset_pass_validator.verification_code.$touch"
                  @blur="reset_pass_validator.verification_code.$touch"
                  clearable
                  color="primary"
                  label="Verification code"
                  variant="underlined"
              ></v-text-field>

              <v-card-actions class="d-flex flex-row justify-center">
                <v-btn width='95%' variant="outlined" color="success" @click="submitResetForm(formdata_reset_pass)">
                    Send
                </v-btn>
              </v-card-actions>

              <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style="white-space: pre-wrap;">
                <span class="link text-primary text-decoration-underline" style="cursor: pointer" @click="authOptions = 'log_in'" >Back to Login</span>  
              </div>
            </form>
          </v-container>


        </v-card>

        
    </v-dialog>

</template>

<script setup>
import {ref, computed, defineProps, defineEmits, watch, toRaw} from 'vue';
import {useStore} from 'vuex';
import { useVuelidate } from '@vuelidate/core'
import { email, required, sameAs, minLength, maxLength, numeric, not, helpers} from '@vuelidate/validators'

const props = defineProps(['authDialog', 'currURLObj'])
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

const resetPasswordValidationErrors = ref({
  'email': '',
  'verification_code': ''
})

const formdata_logIn = ref({
  'username': '',
  'password': '',
  'remember': true,
})

const formdata_reset_pass = ref({
  'username': '',
  'verification_code': ''
})

const login_error = ref({
  text: '',
  state: false,
})


watch(() => formdata_singUp.value, (new_obj) => {
  for(const[key, value] of Object.entries(new_obj)){
    if(new_obj[key] == '' || new_obj[key] === null || new_obj.agree_terms == true){
      singUpValidationErrors.value[key] = ''
    }
  }
},{deep: true}
)

watch(() => formdata_logIn.value, (new_obj) => {
  for(const[key, value] of Object.entries(new_obj)){
    if(new_obj[key] == '' || new_obj[key] === null){
      login_error.value.state = false
    }
  }
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

const signup_rules = computed(() => {
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
      sameAs: helpers.withMessage('Password and Confirm Password must be equal', sameAs(formdata_singUp.value.password))
    },
  };
});

const reset_pass_rules_ = computed(() => {
  return {
    username: { required },
    verification_code: { 
      required, 
      maxLength: maxLength(6),  
    },
  };
});

const signup_validator = useVuelidate(signup_rules, formdata_singUp)
const reset_pass_validator = useVuelidate(reset_pass_rules_, formdata_reset_pass)

const forgotPasswordClick =() => {authOptions.value = 'reset_pass'}

const submitLoginForm =(data) => {
    const user_data = {'username': data.username, 'password': data.password}

    store.dispatch("auth/login", user_data)
    .then(
      () => {
        if(!data.remember){store.dispatch("auth/dontRemember")}
        emit('closeAuthDialog');
      },
      (error) => {
        login_error.value.state = true
        login_error.value.text = error.response.data.detail
      }
    );
}

const submitSignUpForm =(data) =>{

  const user_data = {'username': data.username, 'email': data.email, 'password': data.password, 're_password': data.confirm_password}

  if(data.agree_terms){
      store.dispatch("auth/register", user_data)
      .then(
        () => {authOptions.value = 'log_in'},
        (error) => {
          for(const [key, value] of Object.entries(error.response.data)){singUpValidationErrors.value[key] = value[0]}
        }
      );
  }
  else{singUpValidationErrors.value.agree_terms = 'You must agree to the Terms and Privacy Policy'}
}


</script>

<style lang="scss" scoped>
</style>
