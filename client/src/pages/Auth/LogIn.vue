<template>
<div class='d-flex flex-column align-center justify-center h-100 w-100'>
  <v-card 
    width="98%" 
    max-width="550" 
    :variant="width <= 740 ? 'flat' : 'elevated'">

    <v-card-item class="py-3 px-4">
        <v-card-title>Log In</v-card-title>
    </v-card-item>

    <v-container v-if="validationErrors.state">
        <v-alert 
          density="compact"
          type="error"
          :text="validationErrors.text"
        ></v-alert>
    </v-container>

    <v-container>
        <form>
            <v-text-field
                v-model="formdata.username"
                clearable
                color="primary"
                label="Username"
                variant="underlined"
            ></v-text-field>

            <v-text-field
                v-model="formdata.password"
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
                v-model="formdata.remember"
                label="Remember"
                color="secondary"
                hide-details="true"
            ></v-checkbox>

            <div class='d-flex font-weight-regular text-capitalize text-medium-emphasis text-subtitle-1 text-primary text-decoration-underline'  
              style="margin-top: 14px; cursor: pointer;" 
              @click="router.push({ name: 'reset_password'})">
                Forgot Password?
            </div>
            </div>

            <v-card-actions class="d-flex flex-row justify-center">
            <v-btn width='95%' variant="outlined" color="success" @click="submitForm(formdata)">
                Log In
            </v-btn>
            </v-card-actions>

            <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style="white-space: pre-wrap;">
                Don't have an account? <span class="link text-primary text-decoration-underline" style="cursor: pointer" @click="router.push({ name: 'signup'})" >Sign up</span>  
            </div>
        </form>
    </v-container>

    <!-- <div class='d-flex text_social_media justify-center w-100 font-weight-regular text-medium-emphasis text-subtitle-1' style=" white-space: pre-wrap;">
        Or<span class="text-primary"> Log In </span>with<span class="text-secondary"> Social Media</span>
        
    </div> -->

  </v-card>
</div>
</template>

<script setup>
import {ref, defineProps, watch} from 'vue';
import {useStore} from 'vuex';
import {useDisplay} from 'vuetify'
import router from '@/router/router';

const { width } = useDisplay();
const props = defineProps(['currURLObj'])
const store = useStore();

let showPassword = ref(false);

const formdata = ref({
  'username': '',
  'password': '',
  'remember': true,
})

//Custom validations errors from backend
const validationErrors = ref({
  text: '',
  state: false,
})

// Watch for textfield changes (remove the error display when data is changed in the field)
watch(() => formdata.value, (new_obj) => {
  for(const[key, value] of Object.entries(new_obj)){
    if(new_obj[key] == '' || new_obj[key] === null){
      validationErrors.value.state = false
    }
  }
},{deep: true}
)


const submitForm = (data) => {
  const user_data = {'username': data.username, 'password': data.password}

  store.dispatch("auth/login", user_data)
  .then(
    () => {
      if(!data.remember){store.dispatch("auth/dontRemember")}
      router.push({ name: 'journal'})
    },
    (error) => {
      validationErrors.value.state = true
      validationErrors.value.text = error.response.data.detail
    }
  );
}

</script>

<style lang='scss' scoped></style>