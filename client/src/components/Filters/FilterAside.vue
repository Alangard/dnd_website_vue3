<template>
    <v-navigation-drawer class="h-a" v-if="width <= 740" v-model="props.isOpenAside"  disable-resize-watcher='false' location="right" width="740" temporary>

    <v-sheet class='d-flex flex-row align-center w-100 justify-space-between pt-1'>
            <v-btn class="close_asid" variant="plain" rounded='lg' size="large" prepend-icon="mdi-arrow-left" @click.stop="changeStateFilterAside">Filters</v-btn>
            <v-btn class="clear_form" v-if='hasData' variant="plain" size="large">Clear all</v-btn>
    </v-sheet>  

    <v-divider></v-divider>

    <v-text-field 
            v-model="searchField"
            :loading="loading" 
            clearable
            density="compact" 
            variant="default"
            label="Search by post's title/description" append-inner-icon="mdi-magnify"
            single-line
            hide-details
            @click:append-inner="startSearch"
            @keydown.enter.stop="startSearch">
    </v-text-field>

    <v-divider></v-divider>

    <v-card rounded='0' flat="true">
            <v-row>
                    
                    <v-col :cols="4">
                            <v-tabs v-model="tab" align-tabs="start" direction="vertical">
                                    <v-tab v-for="item in items" :key="item" :value="item">{{ item }}</v-tab>
                            </v-tabs>
                    </v-col>

                    <v-col :cols="8">
                            <v-window v-model="tab">
                                    <v-window-item v-for="item in items" :key="item" :value="item">
                                            <v-card flat><v-card-text v-text="text"></v-card-text></v-card>
                                    </v-window-item>
                            </v-window>
                    </v-col>

            </v-row>
    </v-card>



    <v-card rounded='0' class="apply_filters_btn_container elevation-8" >
            <v-btn block @click.stop="applyFilters">Apply</v-btn>
    </v-card>


    </v-navigation-drawer>
</template>

<script setup>
import { ref, defineProps, defineEmits, onUpdated} from 'vue'
import { useDisplay } from 'vuetify'



const props = defineProps(['isOpenAside'])
const emit = defineEmits([''])

const { width } = useDisplay()
const hasData = ref(true)
let submitForm = ref(false)

// Search field variables
let loading = ref(false)
let loaded = ref(false)
let searchField = ref('')

// Filter tabs variables
let tab = ref(null)
let items = ref(['web', 'shopping', 'videos', 'images', 'news'])
let text = ref('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.')

const startSearch =() => {
        loading.value = true

        setTimeout(() => {
          loading.value = false
          loaded.value = true
        }, 2000)

        props.isOpenAside = false
        emit('filterToolbarIsOpen')
}

const applyFilters =() => {
        submitForm.value = true
        props.isOpenAside = false
        emit('filterToolbarIsOpen')
}

const changeStateFilterAside =() => {
        props.isOpenAside = false
        emit('filterToolbarIsOpen')
}

onUpdated(() => {
        //Disable scroll when a aside toolbar is opened
        if(props.isOpenAside){document.documentElement.style.overflow = 'hidden'}
        else{document.documentElement.style.overflow = 'visible'}
})

</script>


<style lang="scss" scoped>
.apply_filters_btn_container{
    position: fixed;
    width: 100%;
    bottom: 0;
    padding: 12px 8px;

}
</style>