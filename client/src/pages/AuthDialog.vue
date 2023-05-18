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

              <div class='d-flex font-weight-regular text-capitalize text-medium-emphasis text-subtitle-1'  style="margin-top: 14px;" @click="forgotPasswordClick">
                Forgot Password?
              </div>
            </div>

            <v-card-actions class="d-flex flex-row justify-center">
              <v-btn width='95%' variant="outlined" color="success" @click="submitForm(formdata_logIn)">
                  Log In
              </v-btn>
            </v-card-actions>

            <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style=" white-space: pre-wrap;">
                Don't have an account? <span class="text-primary text-decoration-underline" @click="authOptions = 'sign_up'">Sign up</span>  
            </div>
          </v-container>



          <!-- <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style=" white-space: pre-wrap;">
                Or<span class="text-primary"> Log In </span>with<span class="text-secondary"> Social Media</span>
                
          </div> -->



        </v-card>

        <v-card class="mx-auto" title="Create account" v-if="authOptions == 'sign_up'">
            <v-container>
              <v-text-field
                  v-model="formdata_singUp.username"
                  color="primary"
                  label="Username"
                  variant="underlined"
              ></v-text-field>

              <v-text-field
                  v-model="formdata_singUp.email"
                  color="primary"
                  label="Email"
                  variant="underlined"
              ></v-text-field>

              <v-text-field
                  v-model="formdata_singUp.password"
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

              <v-text-field
                  v-model="formdata_singUp.confirm_password"
                  :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  @click:append="showConfirmPassword = !showConfirmPassword"
                  :rules="[rules.required, rules.min]"
                  hint="At least 8 characters"
                  counter
                  color="primary"
                  label="Confirm Password"
                  variant="underlined"
              ></v-text-field>

              <v-checkbox v-model="formdata_singUp.agree_terms" hide-details="true" color="secondary">
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
                <v-btn width='95%' variant="outlined" color="success" @click="submitForm(formdata_singUp)">
                    Complete Registration
                </v-btn>
              </v-card-actions>

              <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style=" white-space: pre-wrap;">
                  Already have an account? <span class="text-primary text-decoration-underline" @click="authOptions = 'log_in'">Log In</span>  
              </div>
            </v-container>
        </v-card>
    </v-dialog>

</template>

<script setup>
import {ref, computed, onBeforeMount, defineProps, defineEmits} from 'vue';
import {useStore} from 'vuex';

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

const formdata_logIn = ref({
  'username': '',
  'password': '',
  'remember': false,
})


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

const rules = ref( {
    required: value => !!value || 'Required.',
    min: v => v.length >= 8 || 'Min 8 characters',
    emailMatch: () => (`The email and password you entered don't match`),
})

// const getJWTTokens = computed(() => {return {
//   'access': store.getters.getCurrUserData.access, 
//   'refresh': store.getters.getCurrUserData.refresh
// }})

const submitForm =(data) => {
  store.dispatch('auth_login',{'url': 'auth/token/create/', 'userdata': data});
  const jwtTokens = store.getters.getCurrUserData;
  localStorage.setItem('access_token', jwtTokens.access);
  localStorage.setItem('refresh_token', jwtTokens.refresh);
  emit('closeAuthDialog');
}

const authManager = () => {
  if(localStorage.getItem('access_token') && localStorage.getItem('refresh_token')){

    const log_in = () =>{

    }

    const userData = {
      'username': 'admin',
      'password': '1234',
    }

   
  }

  // store.dispatch('auth_login',{'url': 'auth/token/create/', 'userdata': formdata_logIn.value})

  
}

onBeforeMount(() => {
    authManager();
})
</script>

<style lang="scss" scoped>
  
</style>
