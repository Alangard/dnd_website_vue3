<template>
  <v-menu transition="slide-x-reverse-transition" location="start" :close-on-content-click="false" >

    
    
    
  

    <v-card width="300">
      <v-tabs v-model="emoticonTab" background="primary" fixed-tabs>
        <v-tab value="emoji">Emoji</v-tab>
        <v-tab value="stickers">Stickers</v-tab>
      </v-tabs>

      <v-card-text>
        <v-window class="mt-2" v-model="emoticonTab" color="primary" background="primary">
          <v-window-item value="emoji">
            Elements emoji...
            dasdasdasdasd
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasda
          </v-window-item>

          <v-window-item value="stickers">
            Elements stickers...
            DAsdasdasdasdaddasdasdasdasd
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasdaasdad
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasdaasdaddasd
          </v-window-item>

        </v-window>
      </v-card-text>
    </v-card>
  </v-menu>

  <v-navigation-drawer v-if="width < 600" class="mobile_emoticon h-50" v-model="mobileEmoticonDrawer" location="bottom" temporary>
    <v-card class="h-100">
      <v-tabs v-model="emoticonTab" background="primary" fixed-tabs>
        <v-tab value="emoji">Emoji</v-tab>
        <v-tab value="stickers">Stickers</v-tab>
      </v-tabs>

      <v-card-text>
        <v-window class="mt-2" v-model="emoticonTab" color="primary" background="primary">
          <v-window-item value="emoji">
            Elements emoji...
            dasdasdasdasd
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasda
          </v-window-item>

          <v-window-item value="stickers">
            Elements stickers...
            DAsdasdasdasdaddasdasdasdasd
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasdaasdad
            asdasdasdadasdasdadasdasdasdasdasdasdasdasdasdaasdaddasd
          </v-window-item>

        </v-window>
      </v-card-text>
    </v-card>  
  </v-navigation-drawer>
</template>


<script setup>
import {ref, defineProps} from 'vue'

const prop = defineProps(['activator', 'id'])

const menu = ref()

</script>

<style lang="scss" scoped>
</style>