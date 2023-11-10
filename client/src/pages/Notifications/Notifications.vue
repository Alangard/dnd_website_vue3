<template>
    <!-- <v-card class="pt-4" width="100%">
      <div class="d-flex flex-row">
        <v-card class="mr-4" rounded="0">
            <v-tabs
            v-model="tab"
            direction="vertical"
            >
                <v-tab value="option-1">
                    <v-icon start>mdi-account</v-icon>
                    Account
                </v-tab>
                <v-tab value="option-2">
                    <v-icon start>mdi-bell-outline</v-icon>
                    Notifications
                </v-tab>
            </v-tabs>
        </v-card>
        
        <v-window v-model="tab">
          <v-window-item value="option-1">
            <v-card flat>
              <v-card-text>
                <p>
                  Sed aliquam ultrices mauris. Donec posuere vulputate arcu. Morbi ac felis. Etiam feugiat lorem non metus. Sed a libero.
                </p>
  
                <p>
                  Nam ipsum risus, rutrum vitae, vestibulum eu, molestie vel, lacus. Aenean tellus metus, bibendum sed, posuere ac, mattis non, nunc. Aliquam lobortis. Aliquam lobortis. Suspendisse non nisl sit amet velit hendrerit rutrum.
                </p>
  
                <p class="mb-0">
                  Phasellus dolor. Fusce neque. Fusce fermentum odio nec arcu. Pellentesque libero tortor, tincidunt et, tincidunt eget, semper nec, quam. Phasellus blandit leo ut odio.
                </p>
              </v-card-text>
            </v-card>
          </v-window-item>
          <v-window-item value="option-2">
            <v-card flat>
              <v-card-text>
                <span class="text-h6">Notifications settings</span> 
                <v-card class="mt-2 pa-6" >
                    <v-card class="d-flex flex-row align-start mb-2" 
                            v-for="setting in notificationSettings" :key="setting">
                            <div class="d-flex flex-column">
                                <v-card-title class="pt-1 pb-0" style="word-break: normal">{{ setting.title }}</v-card-title>
                                <v-card-text class="pt-2 pb-1">{{ setting.text }}</v-card-text>
                            </div>

                            <v-switch class="d-flex flex-row justify-end px-2"
                                v-model="setting.value"
                                hide-details
                                color="info"
                                inset
                            ></v-switch>
                    </v-card>
                </v-card>

              </v-card-text>
            </v-card>
          </v-window-item>
          <v-window-item value="option-3">
            <v-card flat>
              <v-card-text>
                <p>
                  Fusce a quam. Phasellus nec sem in justo pellentesque facilisis. Nam eget dui. Proin viverra, ligula sit amet ultrices semper, ligula arcu tristique sapien, a accumsan nisi mauris ac eros. In dui magna, posuere eget, vestibulum et, tempor auctor, justo.
                </p>
  
                <p class="mb-0">
                  Cras sagittis. Phasellus nec sem in justo pellentesque facilisis. Proin sapien ipsum, porta a, auctor quis, euismod ut, mi. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nam at tortor in tellus interdum sagittis.
                </p>
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </div>
    </v-card>


    <v-data-table :items="items"></v-data-table> -->

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
            @click="console.log('notifications_settings')">
          </v-btn>
        </div>

        <div class="d-flex flex-row align-center justify-space-between w-100"> 
          <v-select
            class="filter_seen_notifications__select tm-2"
            style="max-width: 120px"
            v-model="seenNotificationSelect"
            :items="['Unseen', 'Seen']"
            @update:model-value="handleFilterChange()"
            density="compact"
            variant="solo"
            hide-details
          ></v-select>

          <v-checkbox-btn class="seen_all__checkbox"
            style="flex: 0 0;"
            v-model="seenAllNotificationOnPage"
            :hide-details="false"
            density="compat" 
            true-icon="mdi-eye" 
            false-icon="mdi-eye-off">
          </v-checkbox-btn>
        </div>
      </v-card-title>

      <v-divider></v-divider> 

      <v-card class="my-1" v-for="notification in notificationsList" :key="notification?.notification_id"
        rounded="0" 
        :variant="notification?.seen ? 'default' : 'tonal'" 
        color="indigo">   

        <Notification :notification="notification"></Notification>

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

const seenNotificationSelect = ref('Unseen')
const seenAllNotificationOnPage = ref(false)

onBeforeMount(async () => {
  if(store.getters['auth/loginState'] == true){  
    const response = await store.dispatch('accounts/getNotificationsList', {'paginate_url': page_url.value, 'request_type': 'all_notifications'})

    notifications_count.value = response.count
    notificationsList.value = response.results
    page_count.value = Math.ceil(notifications_count.value / page_size)          
  }
})

const tab = ref('option-1')
const notificationSettings = ref(
    {
        'new_follower': {'title': 'New follower', 'text': 'Someone starts following you', 'value': false},
        'new_comment': {'title': 'New comment', 'text': 'Someone wrote comment to your post', 'value': false},
        'new_reply': {'title': 'New reply', 'text': 'Someone wrote a reply to your comment', 'value': false},
        'new__post_reaction': {'title': 'New reaction yo your post', 'text': 'Someone reacts to your post', 'value': false},
        'new__comment_reaction': {'title': 'New reaction on comment', 'text': 'Someone reacts to your comment', 'value': false},
        'new__feed_post': {'title': 'New feed post', 'text': "Someone you're following posted something", 'value': false},
        'new__feed_reaction': {'title': 'New feed reaction', 'text': "Someone you're following left a reaction.", 'value': false},
    }   
)

const seenNotificationOnPage =() => {
  console.log('seen all notifications')
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
  filters.value = `seen=${seenNotificationSelect.value == 'Seen' ? "True" : "False"}`
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