<template>

    <v-card class="notifications_container mt-8" 
      height="100%" 
      :style=" width >= mobileWidthLimit ? 'width: 750px;' : 'max-width: 750px; min-width: 300px'">
      
      <v-card-title class="d-flex flex-column align-start">
        <div class="d-flex flex-row align-center justify-space-between w-100">
          <span> Notifications </span>
          <v-btn class="notifications_settings_btn" 
            icon="mdi-cog-outline" 
            density="compat" 
            variant="text" 
            rounded="sm" 
            @click="routes.push({name: 'notifications_settings'})">
          </v-btn>
        </div>

        <div class="d-flex flex-row align-center justify-space-between w-100 mt-4"> 
          <v-select class="filter_seen_notifications__select"
            style="max-width: 150px"
            v-model="seenNotificationFilterSelect"
            :items="notificationFilterList"
            return-object
            @update:model-value="handleFilterChange()"
            density="compact"
            variant="solo"
            prepend-inner-icon="mdi-filter-outline"
          ></v-select>

          <div class="notifications__actions_container d-flex flex-row align-start" v-if="checkedNotificationList.length > 0">
            <v-select class="notifications_actions mr-2" 
              :style="width >= mobileWidthLimit ? '' : 'max-width: 100px'"
              v-model="notificationActionSelect"
              :items="notificationActionList"
              return-object
              density="compact"
              variant="solo"
              persistent-hint
              :hint="`Selected notifications ${checkedNotificationList.length}`"
            ></v-select>

            <v-btn class="notifications__action_submit" 
              icon="mdi-check-outline" 
              density="comfortable" 
              rounded="sm" 
              @click="submitNotificationAction()">
            </v-btn>
          </div>
        </div>
      </v-card-title>

      <v-divider></v-divider> 

      <v-card class="my-1 notifications_element" v-for="notification in notificationsList" :key="notification?.notification_id"
        rounded="0" 
        :variant="notification?.seen ? 'default' : 'tonal'" 
        color="indigo">   

        <Notification 
          :notification="notification" 
          :checkbox_with_icon="false"
          :checkedNotificationList="checkedNotificationList" 
          @selectCheckbox="selectCheckbox" ></Notification>

        <v-divider></v-divider>
      </v-card>

      <div class="pagination text-center">
        <v-pagination
            v-model="current_page"
            @update:model-value="handlePageChange"
            :length="page_count"
            :total-visible="7"
            size="small"
        ></v-pagination>
      </div>

    </v-card>

  </template>
<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import { useStore } from 'vuex';
import {useDisplay } from 'vuetify/lib/framework.mjs';
import routes from '@/router/router' 

import Notification from '@/components/Notifications/Notification.vue'

const store = useStore();
const { width } = useDisplay();

const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})
const notificationsList = ref(null)

let notifications_count = ref(0)
let filters = ref(null)
const current_page = ref(1)
const page_count = ref(1)
const page_size = 2
let page_url = ref(`?page=1&page_size=${page_size}&seen=False`)

const checkedNotificationList = ref([])
const notificationFilterList = [{'value': 'unseen', 'title': 'Unseen'}, {'value': 'seen', 'title': 'Seen'}] 
const notificationActionList = [{'value': 'seen', 'title': 'Mark as seen'}, {'value': 'unseen', 'title': 'Mark as unseen'}, {'value': 'delete', 'title': 'Delete'}]

const seenNotificationFilterSelect = ref({'value': 'unseen', 'title': 'Unseen'})
const notificationActionSelect = ref({'value': 'seen', 'title': 'Mark as seen'})


onBeforeMount(async () => {
  if(store.getters['auth/loginState'] == true){  
    const response = await store.dispatch('accounts/getNotificationsList', {'paginate_url': page_url.value, 'request_type': 'all_notifications'})

    notifications_count.value = response.count
    notificationsList.value = response.results
    page_count.value = Math.ceil(notifications_count.value / page_size)          
  }

  filters.value = `seen=${seenNotificationFilterSelect.value['value'] == 'seen' ? "True" : "False"}`
})

const selectCheckbox =(notification_id, notification_state) =>{
  const notification_index = checkedNotificationList.value.indexOf(notification_id)
  if(notification_index == -1){checkedNotificationList.value.push(notification_id)}
  else{checkedNotificationList.value.splice(notification_index, 1)}
}

const submitNotificationAction =() =>{
  const data = {
    'page_size': page_size,
    'action': notificationActionSelect.value,
    'notifications_ids': checkedNotificationList.value
  }

  store.dispatch('accounts/submitNotificationsAction', data)
  alert(`Submit action ${notificationActionSelect.value['value']}`)
}

const handlePageChange = async(newPage) => {
    current_page.value = newPage
    page_url.value = `?page=${newPage}&page_size=${page_size}` + `&${filters.value}`

    const response = await store.dispatch('accounts/getNotificationsList', {'paginate_url': page_url.value, 'request_type': 'all_notifications'})
    notifications_count.value = response.count
    notificationsList.value = response.results
    page_count.value = Math.ceil(notifications_count.value / page_size)   

    window.scrollTo({top: 0,behavior: "smooth"});
}

const handleFilterChange = async() =>{
  filters.value = `seen=${seenNotificationFilterSelect.value['value'] == 'seen' ? "True" : "False"}`
  page_url.value =`?page=1&page_size=${page_size}&${filters.value}`
  current_page.value = 1

  const response = await store.dispatch('accounts/getNotificationsList', {'paginate_url': page_url.value, 'request_type': 'all_notifications'})
  notifications_count.value = response.count
  notificationsList.value = response.results
  page_count.value = Math.ceil(notifications_count.value / page_size) 

  window.scrollTo({top: 0,behavior: "smooth"}); 
}

</script>
<style lang="scss" scoped></style>