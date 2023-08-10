<template>
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

</template>

<script setup>
import {ref} from 'vue'

const emoticonTab = ref(null)
</script>


<style lang="scss" scoped></style>