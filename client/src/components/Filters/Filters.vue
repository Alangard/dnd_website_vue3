<template>

<v-card class="filters-container  elevation-8" >

                <div class="order_selector" id="order_selector">
                        <v-select
                                active="true"
                                variant="underlined"
                                hide-selected="true"
                                density="comfortable"
                                label="Order by"
                                v-model="curr_order_variant"
                                :items="order_variants"
                                @update:modelValue="onOrderChange"
                        ></v-select>
                </div>

                <v-sheet class='d-flex flex-row align-center w-100 justify-end pb-2'>
                        <v-btn v-if="store.getters.getPostListStyle=='grid'" class='list_style_btn' size="large" variant="plain" icon="mdi-format-list-bulleted" @click.stop="displayPostInListStyle"></v-btn>
                        <v-btn v-if="store.getters.getPostListStyle =='list'" class='grid_style_btn' size="large" variant="plain" icon="mdi-grid-large" @click.stop="displayPostInGridStyle"></v-btn>
                        <v-btn class='filter_btn' size="large" variant="plain" icon="mdi-tune" @click.stop="openFilterAside"></v-btn>
                </v-sheet>  
</v-card>     


</template>

<script setup>
import { ref, defineEmits } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const emit = defineEmits(['filterToolbarIsOpen'])

const curr_order_variant = ref('New first')
const order_variants = ref([
        'New first',
        'Old first',
        'Asc likes',
        'Desc likes',
        'Asc comments',
        'Desc comments',
])

const onOrderChange =() => {
        console.log('change', curr_order_variant.value);
        // make a request for ordering
}

const openFilterAside =() => {emit('filterToolbarIsOpen');}

const displayPostInGridStyle =() => {store.commit('changePostListStyle', 'grid')}

const displayPostInListStyle =() => {store.commit('changePostListStyle', 'list')}








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

        .order_selector{
                width: 300px;
        }
}


// .apply_filters_btn_container{
//         position: fixed;
//         width: 100%;
//         bottom: 0;
//         padding: 12px 8px;

// }



</style>