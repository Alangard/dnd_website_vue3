<!-- <template>
    <v-card class="mt-4">
      <div class="d-flex flex-row">
        
        <v-card class="mr-4" rounded="0" style="width: 350px !important"> 
            <v-tabs 
                v-model="tab"
                direction="vertical"
                color="primary">

                <v-tab value="option-1">
                    <v-icon start> mdi-account</v-icon>
                    Option 1
                </v-tab>
                
                <v-tab value="option-2">
                    <v-icon start>mdi-lock</v-icon>
                    Option 2
                </v-tab>

                <v-tab value="option-3">
                    <v-icon start>mdi-access-point</v-icon>
                    Option 3
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
                <p>
                  Morbi nec metus. Suspendisse faucibus, nunc et pellentesque egestas, lacus ante convallis tellus, vitae iaculis lacus elit id tortor. Sed mollis, eros et ultrices tempus, mauris ipsum aliquam libero, non adipiscing dolor urna a orci. Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo. Nunc sed turpis.
                </p>
  
                <p>
                  Suspendisse feugiat. Suspendisse faucibus, nunc et pellentesque egestas, lacus ante convallis tellus, vitae iaculis lacus elit id tortor. Proin viverra, ligula sit amet ultrices semper, ligula arcu tristique sapien, a accumsan nisi mauris ac eros. In hac habitasse platea dictumst. Fusce ac felis sit amet ligula pharetra condimentum.
                </p>
  
                <p>
                  Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Nam commodo suscipit quam. In consectetuer turpis ut velit. Sed cursus turpis vitae tortor. Aliquam eu nunc.
                </p>
  
                <p>
                  Etiam ut purus mattis mauris sodales aliquam. Ut varius tincidunt libero. Aenean viverra rhoncus pede. Duis leo. Fusce fermentum odio nec arcu.
                </p>
  
                <p class="mb-0">
                  Donec venenatis vulputate lorem. Aenean viverra rhoncus pede. In dui magna, posuere eget, vestibulum et, tempor auctor, justo. Fusce commodo aliquam arcu. Suspendisse enim turpis, dictum sed, iaculis a, condimentum nec, nisi.
                </p>
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
</template> -->

<template>
    <v-card class="pt-4" width="100%">
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


    <v-data-table :items="items"></v-data-table>

  </template>
<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import { useStore } from 'vuex';

const store = useStore();

const notificationsList = computed(() => {return store.getters['accounts/getNotificationsList']});

let page_url = ref(`?page=1&`)
let notifications_count = ref(0)

onBeforeMount(async () => {
    if(store.getters['auth/loginState'] == true){
        notifications_count.value = (await store.dispatch('accounts/getNotificationsList', {'paginate_url': page_url.value, 'request_type': 'initial'})).count 
        
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



const items = ref([
    {
      name: 'African Elephant',
      species: 'Loxodonta africana',
      diet: 'Herbivore',
      habitat: 'Savanna, Forests',
    },
  ]
)

</script>
<style lang="scss" scoped></style>