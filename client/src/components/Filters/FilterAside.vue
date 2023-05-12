<template>
    <v-navigation-drawer class="h-a" v-if="width <= 740" v-model="props.isOpenAside"  disable-resize-watcher='false' location="right" width="740" temporary>

    <v-sheet class='d-flex flex-row align-center w-100 justify-space-between pt-1'>
            <v-btn class="close_aside" variant="plain" rounded='lg' size="large" prepend-icon="mdi-arrow-left" @click.stop="changeStateFilterAside">Filters</v-btn>
            <v-btn class="clear_form" v-if='clearable_form' variant="plain" size="large" @click.stop="clearAllFilters">Clear all</v-btn>
    </v-sheet>  

    <v-divider></v-divider>

    <v-text-field class="search_post"
            v-model="output_filters_data.filter__post_search_result"
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

    <v-card class="filters_blocks" rounded='0' flat="true" style="height: max-content;">
        <div class="filters_postdate_block my-3 mx-5">
                <span>Filter by post date</span>

                <VueDatePicker 
                        class="mt-2"
                        v-model="output_filters_data.filter__post_date_result" 
                        :format="format"
                        placeholder="Input date range" 
                        :max-date="new Date()" 
                        :enable-time-picker="false"
                        :clearable="true"
                        :dark="theme.global.name.value == 'dark'? true : false" 
                        range 
                />
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

                                        <v-chip class="my-1 mr-4"  v-for="user in filteredUserList" :key="user.id" @click="selectUser(user)">
                                                <v-avatar start style="cursor:pointer">
                                                        <v-img v-if="user.avatar != ''" :src="user.avatar" :alt="user.username" size="x-small"></v-img>
                                                        <v-icon icon="mdi-account-circle-outline" size="large" v-else></v-icon>
                                                </v-avatar>
                                                {{user.username}}
                                        </v-chip>
     
                                
                        </div>
                        
                        <div v-else>
                                <v-chip class="my-1 mr-2" v-for="(user, index) in  output_filters_data.filter__post_author_result" :key="user" :class="{'text-primary': user.chosen == true}"  @click="unselectUser(index)">
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

        <div class="filters_tags_block my-3 mx-5">
                <span>Filter by tags</span>
                
                <div class="mt-3 d-flex flex-row flex-wrap">
                        <v-chip
                                class="mr-2"
                                @click="selectTag(tag, $event)"
                                v-for="tag in tags" :key="tag">
                                {{ tag.name }}
                        </v-chip>
                </div>
        </div>

        <div class="apply_filters_btn_container" >
                <v-btn block @click.stop="applyFilters">Apply</v-btn>
        </div>
    </v-card>
    </v-navigation-drawer>

</template>

<script setup>
import { ref, defineProps, defineEmits, onUpdated, onMounted, computed, watch} from 'vue'
import { useDisplay } from 'vuetify'
import { useTheme } from 'vuetify/lib/framework.mjs';
import store from '@/store';


let theme = useTheme()
const props = defineProps(['isOpenAside'])
const emit = defineEmits([''])


let output_filters_data = ref({
        'filter__post_search_result':  null,
        'filter__post_date_result': null,
        'filter__post_author_result': [],
        'filter__post_tags_result': [],
})


onMounted(async () => {
        try{
                store.dispatch('fetchUsersData', {'url': 'accounts/'});
                store.dispatch('fetchTagsData', {'url': 'tags/'});
                
        }
        catch(err){console.log(err)}
})

onUpdated(() => {
        //Disable scroll when a aside toolbar is opened
        if(props.isOpenAside){document.documentElement.style.overflow = 'hidden'}
        else{document.documentElement.style.overflow = 'visible'}
})

// Watch for changes in the input fields, if at least one of them changes, change the visibility of the "clear all" button
watch(() => output_filters_data.value, (new_obj) => {
        
        for(const [key, value] of Object.entries(new_obj)){
                if(value == '' || value == [] || value == null){clearable_form.value = false}
                else{
                        clearable_form.value = true
                        break
                }
        }
},{deep: true}
)

const { width } = useDisplay()
let submitForm = ref(false)
let clearable_form = ref(false);


// Search field variables
let loading = ref(false)
let loaded = ref(false)


//output variables obj

const search_author_query = ref('');

const users = computed(() => {return store.getters.getUsersList});
const tags = computed(() => {return store.getters.getTagsList});
const filteredUserList = computed(() => {return users.value.filter(user => user.username.toLowerCase().indexOf(search_author_query.value.toLowerCase()) !== -1)});


/////

const startSearch =() => {
        loading.value = true

        setTimeout(() => {
          loading.value = false
          loaded.value = true
        }, 2000)

        props.isOpenAside = false
        emit('filterToolbarIsOpen')
}

const format = (dates) => {
        let new_date = ''
        dates.forEach(function (date, i) {
                const day = date.getDate();
                const month = date.getMonth() + 1;
                const year = date.getFullYear();
                if(i==0){new_date = `From ${day}/${month}/${year}`}
                else{new_date += ` to ${day}/${month}/${year}`}
        });
        return new_date;
}

const selectUser =(user) => {
        const index = users.value.findIndex((element) => element == user)
        users.value[index]['chosen'] = true;

        search_author_query.value = ''
 
        output_filters_data.value.filter__post_author_result.push({'id': user.id, 'username': user.username, 'avatar': user.avatar, 'chosen': true});
}

const unselectUser =(index) => {
        output_filters_data.value.filter__post_author_result.splice(index, 1)
}

const selectTag = (tag_data, event) => {
        const element = event.target
        element.classList.toggle('text-primary')

        const tag_index = output_filters_data.value.filter__post_tags_result.length ? output_filters_data.value.filter__post_tags_result.indexOf(tag_data) : -1
        if(tag_index >= 0){output_filters_data.value.filter__post_tags_result.splice(tag_index, 1)}
        else{output_filters_data.value.filter__post_tags_result.push(tag_data)}     
}

const applyFilters =() => {

        ////
        `?search=${'perspiciatis.3'}` // template
        `created_datetime_after=${'2023-04-18'}&created_datetime_before=${'2023-04-19'}`// template
        `&username=${Alangard}&username=${TestUser}` // n*template
        `&tags=${tavern}&tags=${mousetrap}` // n*template

 




        submitForm.value = true
        props.isOpenAside = false
        emit('filterToolbarIsOpen')


}

const clearAllFilters =() =>{
        for(const [key, value] of Object.entries(output_filters_data.value)){
                
        }
}

const changeStateFilterAside =() => {
        props.isOpenAside = false
        emit('filterToolbarIsOpen')
}


</script>


<style lang="scss" scoped>

.author_chip_container{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        margin-top: 8px;
}
.apply_filters_btn_container{
    width: 100%;
    bottom: 0;
    padding: 12px 8px;

}
</style>