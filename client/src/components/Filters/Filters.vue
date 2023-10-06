<template>

<v-card class="filters-container  elevation-8" >


        <div class="d-flex flex-row align-center justify-content-start">
                <div class="order_selector" id="order_selector" style="width: 150px;">
                        <v-select
                                active="true"
                                variant="underlined"
                                hide-selected="true"
                                density="comfortable"
                                label="Order by"
                                v-model="curr_order_variant"
                                :items="order_variants"
                                item-title="title"
                                item-value="value"
                                @update:modelValue="onOrderChange"
                        ></v-select>
                </div>

                <v-slide-group class="pa-4" v-model="contentType" selected-class="bg-info">

                        <v-slide-group-item 
                                v-for="variant in contentTypeVariants" :key="variant" 
                                v-slot="{ isSelected, toggle, selectedClass }">

                                        <v-btn :class="['ma-2', selectedClass]" 
                                                :color="isSelected ? 'text-info' : undefined"
                                                @click="() => {toggle(); $emit('clickContentType', variant);}">
                                                {{ variant }}
                                        </v-btn>
                        </v-slide-group-item>
                </v-slide-group>

        </div>

        <v-sheet class='d-flex flex-row align-center w-100 justify-end pb-2' v-if='width < mobileWidthLimit'>
                <v-btn class='filter_btn' size="large" variant="plain" icon="mdi-tune" @click.stop="openFilterAside"></v-btn>
        </v-sheet>  
</v-card>     


</template>

<script setup>
import { ref, defineEmits, computed} from 'vue'
import { useStore } from 'vuex'
import {useDisplay} from 'vuetify'

const { width } = useDisplay();
const store = useStore()
const emit = defineEmits(['filterToolbarIsOpen', 'orderChange', 'clickContentType'])

const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})

const curr_order_variant = ref({title: 'New first', value: '?ordering=-created_datetime'})
const order_variants = ref([
        {title: 'New first', value: 'ordering=-created_datetime'},
        {title: 'Old first', value: 'ordering=created_datetime'},
        // {title: 'Asc likes', value: 'ordering=post_reactions__total_reactions'},
        // {title: 'Desc likes', value: 'ordering=-post_reactions__total_reactions'},
        // {title: 'Asc comments', value: 'ordering=num_comments'},
        // {title: 'Desc comments', value: 'ordering=-num_comments'},
])

const contentType = ref(0)
const contentTypeVariants =ref(['All posts', 'Feed'])

const onOrderChange = async () => {emit('orderChange', curr_order_variant.value)}
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
}


// .apply_filters_btn_container{
//         position: fixed;
//         width: 100%;
//         bottom: 0;
//         padding: 12px 8px;

// }



</style>