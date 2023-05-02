<template>

<v-card class="filters-container  elevation-8" >

                <div class="selector">
                        <v-select
                                variant="underlined"
                                hide-selected="true"
                                density="comfortable"
                                label="Order by"
                                v-model="curr_filter"
                                :items="filters"
                                @update:modelValue="onOrderChange"
                        ></v-select>
                </div>

                <v-sheet class='d-flex flex-row align-center w-100 justify-end pb-2'>
                        <v-btn class='' size="large" variant="plain" icon="mdi-filter-menu-outline" @click.stop="drawer = !drawer">
                        </v-btn>
                </v-sheet>  
</v-card>     

<v-navigation-drawer
                v-model="drawer"
                location="right"
                width="740"
                temporary>

        <v-btn class='' variant="plain" rounded='lg' size="large" icon="mdi-arrow-left" @click.stop="drawer = !drawer">                    
        </v-btn>
</v-navigation-drawer>

</template>

<script setup>
import { ref } from 'vue'

const drawer = ref(null)
const curr_filter = ref('The popular')
const filters = ref([
        'The popular',
        'The unpopular',
        'Asc likes',
        'Desc likes',
        'Asc comments',
        'Desc comments',
      ])

const onOrderChange =() => {
        console.log('change', curr_filter.value);
        // make a request for ordering

}

</script>

<style lang="scss" scoped>

.filters-container{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        margin: 20px 0 15px 0;
        padding: 25px 5px 10px 15px;
        width: inherit;
        border-radius: 5px;
        caret-color: transparent;

        .selector{
                width: 300px;
        }
}

// d-flex flex-row align-center justify-space-between pt-5 px-4 w-100 mt-8 mb-4

</style>