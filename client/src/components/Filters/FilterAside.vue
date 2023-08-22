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

        <v-card class="filters_blocks" rounded='0' flat="true" style="height: 100%;">
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
                                        selected-class="text-primary"
                                        v-for="tag in tags" :key="tag">
                                        {{ tag.name }}
                                </v-chip>
                        </div>
                </div>
                <v-divider></v-divider>
        </v-card>

        <div class="apply_filters_btn_container" >
                <v-btn block @click.stop="applyFilters">Apply</v-btn>
        </div>
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



const filters_data_initial = {
        'filter__post_search_result':  null,
        'filter__post_date_result': null,
        'filter__post_author_result': [],
        'filter__post_tags_result': [],
}

//explore deepCopy
//let output_filters_data = ref({...filters_data_initial}) doesnt work

let output_filters_data = ref({
        'filter__post_search_result':  null,
        'filter__post_date_result': null,
        'filter__post_author_result': [],
        'filter__post_tags_result': [],
})


onMounted(async () => {
       if(store.getters.getUsersList.length == 0){store.dispatch('fetchUsersData', {'url': 'accounts/'});}
       store.dispatch('journal/getTagsList')          
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
const tags = computed(() => {return store.getters['journal/getTagsList']});
const filteredUserList = computed(() => {return users.value.filter(user => user.username.toLowerCase().indexOf(search_author_query.value.toLowerCase()) !== -1)});


/////

function copyObject(obj) {
  let copy = {};
  for (let prop in obj) {
    if (obj.hasOwnProperty(prop)) {
      copy[prop] = obj[prop];
    }
  }
  return copy;
}

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
 
        output_filters_data.value['filter__post_author_result'].push({'id': user.id, 'username': user.username, 'avatar': user.avatar, 'chosen': true});
        store.commit('spliceUserList', index)
}

const unselectUser =(index) => {
        store.commit('pushUserList', output_filters_data.value['filter__post_author_result'][index])
        output_filters_data.value['filter__post_author_result'].splice(index, 1)
        
}

const selectTag = (tag_data, event) => {
        const element = event.target
        element.classList.toggle('selected')

        const tag_index = output_filters_data.value.filter__post_tags_result.length ? output_filters_data.value.filter__post_tags_result.indexOf(tag_data) : -1
        if(tag_index >= 0){output_filters_data.value.filter__post_tags_result.splice(tag_index, 1)}
        else{output_filters_data.value.filter__post_tags_result.push(tag_data)}     
}

const applyFilters =() => {

        let queryset = ''
        for(const [key, value] of Object.entries(output_filters_data.value)){

                switch(key){
                        case 'filter__post_search_result':
                                if(value != null){queryset += `&search=${value}`}
                                break
                        
                        case 'filter__post_date_result':

                                let new_date = ''
                                if(value != null){
                                        value.forEach(function (date, i) {
                                                const day = date.getDate();
                                                const month = date.getMonth() + 1;
                                                const year = date.getFullYear();
                                                if(i==0){new_date = `&end_dater=${year}-${month}-${day}`}
                                                else{new_date += `&start_date=${year}-${month}-${day}`}
                                        });
                                        queryset += new_date
                                }

                                break

                        case 'filter__post_author_result':
                                let users_str = '' 
                                for(const user_data of value){users_str += `&username=${user_data.username}`}
                                queryset += users_str
                                break
                        
                        case 'filter__post_tags_result':
                                let tags_str = '' 
                                for(const tag_data of value){tags_str += `&tags=${tag_data.slug}`}
                                queryset += tags_str
                                break
                }
                
        }

        const url = 'posts/?' + queryset.slice(1);
        store.dispatch('fetchPostData',{'url': url, 'setVariable': true})



        submitForm.value = true
        props.isOpenAside = false
        emit('filterToolbarIsOpen')


}

const clearAllFilters =() =>{
        for(const [key, value] of Object.entries(filters_data_initial)){

                if(key == 'filter__post_tags_result'){
                        const elements = document.querySelectorAll('.filters_tags_block div> .v-chip')
                        try{for (const element of elements){element.classList.toggle('selected')}}
                        catch(err){console.log(err)}
                }

                output_filters_data.value[key] = value
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
        position: fixed;
        width: 100%;
        bottom: 0px;
        margin-bottom: 10px;
        padding: 12px 8px;

}

.selected{
        color: rgb(var(--v-theme-primary));
}
</style>