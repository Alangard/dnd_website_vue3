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
            label="Search by post's title/description" 
            append-inner-icon="mdi-magnify"
            single-line
            hide-details
            @click:append-inner="startSearch"
            @keydown.enter.stop="startSearch">
    </v-text-field>

    <v-divider></v-divider>

    <v-card class="filters_blocks" rounded='0' flat="true">
        <div class="filters_tags_block my-3 mx-5">
                <span>Filter by tags</span>
                
                <v-chip-group multiple v-model="selected_tags" selected-class="text-primary">
                        <v-chip v-for="tag in tags" :key="tag">{{ tag }}</v-chip>
                </v-chip-group>
        </div>

        <v-divider></v-divider>

        <div class="filters_author_block my-3 mx-5">
                <span>Filter by author</span>

                <v-text-field
                        class="mt-2"
                        v-model="search_author_query"
                        clearable
                        density="compact" 
                        variant="outlined"
                        label="Search author by username" 
                        append-inner-icon="mdi-magnify"
                        single-line
                        hide-details>
                </v-text-field>
                
                <div class="author_chip_container">
   
                        <div v-if="search_author_query != null && search_author_query.length > 0">

                                        <v-chip class="my-1 mr-4"  v-for="user in filteredUserList" :key="user.id" @click="clickOnChip(user)">
                                                <v-avatar start style="cursor:pointer">
                                                        <v-img v-if="user.avatar != ''" :src="user.avatar" :alt="user.username" size="x-small"></v-img>
                                                        <v-icon icon="mdi-account-circle-outline" size="large" v-else></v-icon>
                                                </v-avatar>
                                                {{user.username}}
                                        </v-chip>
     
                                
                        </div>
                        
                        <div v-else>
                                <v-chip class="my-1 mr-2" v-for="(user, index) in selected_user" :key="user" :class="{'text-primary': user.chosen == true}"  @click="deleteChip(index)">
                                        <v-avatar start style="cursor:pointer">
                                                <v-img v-if="user.avatar != ''" :src="user.avatar" :alt="user.username" size="x-small"></v-img>
                                                <v-icon icon="mdi-account-circle-outline" size="large" v-else></v-icon>
                                        </v-avatar>
                                        {{user.username}}
                                </v-chip>
                        </div>
                 
                </div>



        </div>

        <v-divider></v-divider>

        <div class="filters_postdate_block my-3 mx-5">
                <span>Filter by post date</span>

                <v-row>
                        <v-col cols="12" sm="6">
                                <v-date-picker v-model="dates" range></v-date-picker>
                        </v-col>
                        <v-col cols="12" sm="6">
                                <v-text-field v-model="dateRangeText" label="Date range" prepend-icon="mdi-calendar"></v-text-field>
                        </v-col>
                </v-row>

        </div>

        <v-divider></v-divider>

    </v-card>



    <div class="apply_filters_btn_container" >
            <v-btn block @click.stop="applyFilters">Apply</v-btn>
    </div>


    </v-navigation-drawer>
</template>

<script setup>
import { ref, defineProps, defineEmits, onUpdated, computed} from 'vue'
import { useDisplay } from 'vuetify'
import FilterComponent from './FilterComponent.vue'



const props = defineProps(['isOpenAside'])
const emit = defineEmits([''])

const { width } = useDisplay()
const hasData = ref(true)
let submitForm = ref(false)

// Search field variables
let loading = ref(false)
let loaded = ref(false)
let searchField = ref('')

// Filter by tags
const tags = ref([
        'Work',
        'Home Improvement',
        'Vacation',
        'Food',
        'Drawers',
        'Shopping',
        'Art',
        'Tech',
        'Creative Writing',
])

let selected_tags = ref([])


// Filter by author
const search_author_query = ref('');
const users = ref([
        {
            id: '1',
            username: 'Frozen Yogurt',
            avatar: ''
        },
        {
            id: '2',
            username: 'Alangard',
            avatar: ''
        },
        {
            id: '3',
            username: 'Test',
            avatar: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQAox0pl-j8_QQ2S5XDmXMoi5sK_hinHTG2v6HByW6id9m7lfjKvtvRHGxELUNoOxatn54&usqp=CAU'
        },
])

let selected_user = ref([])

const filteredUserList = computed(() => {
      return users.value.filter(user => user.username.toLowerCase().indexOf(search_author_query.value.toLowerCase()) !== -1)
});

const clickOnChip =(user) => {

        console.log('yes')
        const index = users.value.findIndex((element) => element == user)
        users.value[index]['chosen'] = true;

        search_author_query.value = ''

        user['chosen'] = true
        selected_user.value.push(user);
}

const deleteChip =(index) => {
        selected_user.value.splice(index, 1)
}

// Filter by date

const dates = ref(['2019-09-10', '2019-09-20'])
const dateRangeText = computed(() => {return dates.value.join(' - ')}) 



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

.author_chip_container{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        margin-top: 8px;
}
.apply_filters_btn_container{
    position: fixed;
    width: 100%;
    bottom: 0;
    padding: 12px 8px;

}
</style>