<template>
    <v-combobox
        v-model="chips"
        :items="items"
        chips
        clearable
        label="Your favorite hobbies"
        multiple
        variant="solo">

        <template v-slot:selection="{ attrs, item, select, selected }">
            <v-chip
                v-bind="attrs"
                :model-value="selected"
                closable
                @click="select"
                @click:close="remove(item)">

                <strong>{{ item }}</strong>&nbsp;
                <span>(interest)</span>
            </v-chip>
        </template>
    </v-combobox>
</template>

<script setup> 

import { ref, computed, watch } from 'vue'
const chips = ref(['Programming', 'Playing video games', 'Watching movies', 'Sleeping'])
const items = ref(['Streaming', 'Eating'])

const remove = (item) => {
    chips.value.splice(chips.value.indexOf(item), 1)
}


</script>

<style lang="scss" scoped>
</style>