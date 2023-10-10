<template>
        <v-navigation-drawer 
                class="d-flex flex-column align-baseline" 
                v-if="props.type == 'mobile'" 
                v-model="props.isOpenAside"  
                disable-resize-watcher='false' 
                location="right"
                permanent="true"
                width="750"
                temporary>

                <div class='d-flex flex-row align-center justify-space-between pt-1' style="width: 100vw;">
                        <v-btn class="close_aside" variant="plain" rounded='lg' size="large" prepend-icon="mdi-arrow-left" @click.stop="changeStateFilterAside">Filters</v-btn>
                        <v-btn class="clear_form" v-if='clearable_form' variant="plain" size="large" @click.stop="clearAllFilters">Clear all</v-btn>
                </div>  

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

                <v-card class="filters_blocks" rounded='0' flat="true" style="height: 100%; width: 100vw;">
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
                                <v-combobox
                                        v-model="output_filters_data.filter__post_author_result"
                                        :items="usernameList"
                                        v-model:search="userSerch"
                                        :hide-no-data="false"
                                        variant="outlined"
                                        density="compact"
                                        clearable
                                        hide-selected
                                        multiple
                                        chips
                                        closable-chips
                                        persistent-hint>

                                        <template v-slot:no-data>
                                                <v-list-item>
                                                <v-list-item-title style="white-space: normal; overflow: hidden;">
                                                No results matching "<strong>{{ userSerch }}</strong>". Press <kbd>enter</kbd> to create a new one
                                                </v-list-item-title>
                                                </v-list-item>
                                        </template>
                                </v-combobox>
                                
                        </div>
                        <v-divider></v-divider>

                        <div class="filters_tags_block my-3 mx-5">
                                <span>Filter by tags</span>
                                <v-combobox
                                        v-model="output_filters_data.filter__post_tags_result"
                                        :items="tagsSlugList"
                                        v-model:search="tagSerch"
                                        :hide-no-data="false"
                                        variant="outlined"
                                        density="compact"
                                        clearable
                                        hide-selected
                                        multiple
                                        chips
                                        closable-chips
                                        persistent-hint>

                                        <template v-slot:no-data>
                                                <v-list-item>
                                                <v-list-item-title style="white-space: normal; overflow: hidden;">
                                                No results matching "<strong>{{ tagSerch }}</strong>". Press <kbd>enter</kbd> to create a new one
                                                </v-list-item-title>
                                                </v-list-item>
                                        </template>
                                </v-combobox>

                        </div>
                        <v-divider></v-divider>
                        <v-card-actions>
                                <v-btn block variant="elevated" @click.stop="applyFilters" :disabled="applyFilterBtnDisabled">Apply filters</v-btn>
                        </v-card-actions>
                </v-card>

        </v-navigation-drawer>

        <div class="filters-container mt-5 mb-4 pr-4" v-if="props.type == 'desktop'" rounded='0' flat="true" style="max-width: 350px; min-width: 300px">

                <v-text-field class="search_post"
                        v-model="output_filters_data.filter__post_search_result"
                        :loading="loading" 
                        clearable
                        density="compact" 
                        variant="solo"
                        label="Search by post's title/description" 
                        append-inner-icon="mdi-magnify"
                        hide-details
                        @click:append-inner="startSearch"
                        @keydown.enter.stop="startSearch">
                </v-text-field>

                <v-card class="my-2 px-2 d-flex flex-column justify-space-between" style="height: 450px;">
                        <div class="d-flex flex-column justify-start">
                                <div class="filters_postdate_block my-3 mb-1">
                                        <span>Filter by post date</span>

                                        <VueDatePicker 
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

                                <div class="filters_author_block my-5 mb-1">
                                        <span>Filter by author</span>
                                        <v-combobox
                                                v-model="output_filters_data.filter__post_author_result"
                                                :items="usernameList"
                                                v-model:search="userSerch"
                                                :hide-no-data="false"
                                                variant="solo"
                                                density="compact"
                                                clearable
                                                hide-selected
                                                multiple
                                                chips
                                                closable-chips
                                                persistent-hint>

                                                <template v-slot:no-data>
                                                        <v-list-item>
                                                        <v-list-item-title style="white-space: normal; overflow: hidden;">
                                                        No results matching "<strong>{{ userSerch }}</strong>". Press <kbd>enter</kbd> to create a new one
                                                        </v-list-item-title>
                                                        </v-list-item>
                                                </template>
                                        </v-combobox>
                                        
                                </div>

                                <div class="filters_tags_block my-3 mb-1">
                                        <span>Filter by tags</span>
                                        <v-combobox
                                                v-model="output_filters_data.filter__post_tags_result"
                                                :items="tagsSlugList"
                                                v-model:search="tagSerch"
                                                :hide-no-data="false"
                                                variant="solo"
                                                density="compact"
                                                clearable
                                                hide-selected
                                                multiple
                                                chips
                                                closable-chips
                                                persistent-hint>

                                                <template v-slot:no-data>
                                                        <v-list-item>
                                                        <v-list-item-title style="white-space: normal; overflow: hidden;">
                                                        No results matching "<strong>{{ tagSerch }}</strong>". Press <kbd>enter</kbd> to create a new one
                                                        </v-list-item-title>
                                                        </v-list-item>
                                                </template>
                                        </v-combobox>

                                </div> 
                        </div>
                        
                        <v-card-actions class="d-flex flex-column px-0">
                                <v-btn class="apply_form mb-2 mx-0" @click.stop="applyFilters" color="text-info" block variant="elevated" size="large" density="default" >Apply filter</v-btn>
                                <v-btn class="clear_form mx-0" @click.stop="clearAllFilters"  block variant="elevated" size="large" density="default" >Clear filter</v-btn>
                        </v-card-actions>
                </v-card>
        </div>

</template>

<script setup>
import { ref, defineProps, defineEmits, onUpdated, onMounted, onBeforeMount, computed, watch, toRaw} from 'vue'
import { useDisplay } from 'vuetify'
import { useTheme } from 'vuetify/lib/framework.mjs';
import store from '@/store';
import routes from '@/router/router' 


let theme = useTheme()
const props = defineProps(['isOpenAside', 'type'])
const emit = defineEmits(['setFilter', 'filterToolbarIsOpen'])

const mobileWidthLimit = computed(() => {return store.getters['getMobileWidthLimit']})
const userList = computed(() => store.getters['accounts/getUsersList'])
const tagList = computed(() => store.getters['journal/getTagsList'])

const usernameList = computed(() => userList?.value?.map(user => user.username));
const tagsSlugList = computed(() => tagList?.value?.map(tag => tag.slug));

const userSerch = ref(null)
const tagSerch = ref(null)


let filters_data_initial = ref({
        'filter__post_search_result':  null,
        'filter__post_date_result': null,
        'filter__post_author_result': null,
        'filter__post_tags_result': null,
})

let output_filters_data = ref({
        'filter__post_search_result':  null,
        'filter__post_date_result': null,
        'filter__post_author_result': null,
        'filter__post_tags_result': null,
})


const { width } = useDisplay()
let clearable_form = ref(false);
let applyFilterBtnDisabled = ref(true)


const format = (dates) => {
        let new_date = ''
        // console.log(dates)
        dates.forEach(function (date, i) {
                const day = date?.getDate().toString().padStart(2, '0');
                const month = (date?.getMonth() + 1).toString().padStart(2, '0');
                const year = date?.getFullYear().toString().padStart(4, '0');
                if(i==0){new_date = `From ${day}/${month}/${year}`}
                else if(i==1 && date !== null){new_date += ` to ${day}/${month}/${year}`}
        });
        return new_date;
}

onBeforeMount(async () => {
        await store.dispatch('accounts/getUsersList')
        await store.dispatch('journal/getTagsList')  
})

onUpdated(() => {
        //Disable scroll when a aside toolbar is opened
        if(props.isOpenAside){document.documentElement.style.overflow = 'hidden'}
        else{document.documentElement.style.overflow = 'visible'}
})

// Watch for changes in the input fields, if at least one of them changes, change the visibility of the "clear all" button
watch(() => output_filters_data.value, (new_obj) => {
        if(Object.entries(new_obj).toString() != Object.entries(filters_data_initial.value).toString()){
                for(const [key, value] of Object.entries(new_obj)){
                        if(value != filters_data_initial.value[key]){
                                clearable_form.value = true
                                applyFilterBtnDisabled.value = false
                                break
                        }
                }
        }
        else{ applyFilterBtnDisabled.value = true}
},{deep: true}
)

watch(() => routes.currentRoute.value?.params?.filter_params, async (new_obj) => {
        const current_filter_params = new_obj
        const filter_group = current_filter_params[0] == '?' 
                ? current_filter_params.slice(1).split('&') 
                : current_filter_params.split('?')[1].split('&')
        filter_group?.forEach(filter_param => {
                // Разделяем ключ и значение фильтра
                const [key, value] = filter_param.split('=');
                switch(key){
                        case 'username':
                                filters_data_initial.value.filter__post_author_result = value.split(',')
                                output_filters_data.value.filter__post_author_result = value.split(',')
                                clearable_form.value = true
                                break
                        case 'tags':
                                filters_data_initial.value.filter__post_tags_result = value.split(',')
                                output_filters_data.value.filter__post_tags_result = value.split(',')
                                clearable_form.value = true
                                break
                        case 'search':
                                filters_data_initial.value.filter__post_search_result = value
                                output_filters_data.value.filter__post_search_result = value
                                clearable_form.value = true
                                break
                        case 'start_date':
                                const start_date_parts = value.split("/")
                                const start_formatted_date = new Date(start_date_parts[2], start_date_parts[1] - 1, start_date_parts[0])
                                filters_data_initial.value.filter__post_date_result = [start_formatted_date]
                                output_filters_data.value.filter__post_date_result = [start_formatted_date]
                                clearable_form.value = true
                                break
                        case 'end_date':
                                const end_date_parts = value.split("/")
                                const end_formatted_date = new Date(end_date_parts[2], end_date_parts[1] - 1, end_date_parts[0])
                                filters_data_initial.value.filter__post_date_result.push(end_formatted_date)
                                output_filters_data.value.filter__post_date_result.push(end_formatted_date)
                                clearable_form.value = true
                                break
                }
        });
        
})

const applyFilters =() => {

                let queryset = []

                for(const [key, value] of Object.entries(output_filters_data.value)){
                        if(value !== null && value.length > 0){
                                switch(key){
                                        
                                        case 'filter__post_search_result':
                                                queryset.push(`search=${value}`)
                                                break
                                        
                                        case 'filter__post_date_result':
                                                for(const [index, element] of toRaw(value).entries()){
                                                        if(element !== null){
                                                                const day = element?.getDate().toString().padStart(2, '0');
                                                                const month = (element?.getMonth() + 1).toString().padStart(2, '0');
                                                                const year = element?.getFullYear().toString().padStart(4, '0');
                                                                queryset.push(index == 0 ? `start_date=${day}/${month}/${year}` : `end_date=${day}/${month}/${year}`)
                                                        }
                                                }

                                                break

                                        case 'filter__post_author_result':
                                                let users_str = 'username='
                            
                                                for(const username of value){users_str += `${username},` }
                                                if (users_str.endsWith(',')) {users_str = users_str.slice(0, -1);}
                                                queryset.push(`${users_str}`)
                                                
                                                break
                                        
                                        case 'filter__post_tags_result':
                                                let tags_str = 'tags='
                                                
                                                for(const tag_slug of value){tags_str += `${tag_slug},`}
                                                if (tags_str.endsWith(',')) {tags_str = tags_str.slice(0, -1);}
                                                queryset.push(`${tags_str}`)
                                                
                                                break
                                }
                        }
                        
                }

                emit('setFilter', queryset)
                changeStateFilterAside()
}

const clearAllFilters =() =>{
        for(const [key, value] of Object.entries(output_filters_data.value)){
                output_filters_data.value[key] = null
                filters_data_initial.value[key] = null
        }
        clearable_form.value = false
        emit('setFilter', null)
        changeStateFilterAside()

}

const changeStateFilterAside =() => {
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