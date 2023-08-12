<template>
    <v-list density="compact">
        <v-list-item v-for="(option, index) in options" :key="index" :value="option" color="primary" @click="commentActionPressed(option.value)">
            <template v-slot:prepend>
                <v-icon :icon="option.icon" :color="option.color" class="mr-3"></v-icon>
            </template>
        <v-list-item-title v-text="option.text"></v-list-item-title>
      </v-list-item>
    </v-list>



</template>


<script setup>
import { ref, defineEmits } from 'vue'

const emit = defineEmits(['commentAction', 'confirmedAction'])

const options = ref([
    {text: 'Edit', value: 'edit', icon: 'mdi-pencil-outline', color: ''},
    {text: 'Share', value: 'share', icon: 'mdi-share-variant-outline', color: ''},
    {text: 'Report', value: 'report', icon: 'mdi-cancel', color: 'error'},
    {text: 'Delete', value: 'delete', icon: 'mdi-delete-outline', color: 'error'}]
)


const commentActionPressed = (action) => {
    emit('commentAction', action)
}
    

</script>


<style lang="scss" scoped>
</style>