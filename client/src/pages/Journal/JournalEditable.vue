<template>
    <v-card max-width='750' width="100%" class="mt-4">
        <v-card-title>Editing post</v-card-title>
        <v-card-text>
            <div class="title mb-3">
                <span class="text-subtitle-1">Post title</span>
                <v-textarea
                    class="pt-0"
                    v-model="post_data.title"
                    :error-messages="validator.title.$errors.map(e => e.$message)"
                    @input="validator.title.$touch"
                    @blur="validator.title.$touch" 
                    clearable 
                    placeholder="Title"
                    auto-grow
                    rows="1"
                    counter
                    maxlength="200"
                    persistent-hint
                    hint="Max characters is 200">
                </v-textarea>
            </div>
            
            <div class="description mb-3">
                <span class="text-subtitle-1">Post description</span>

                <v-textarea
                    class="pt-0"
                    v-model="post_data.description"
                    :error-messages="validator.description.$errors.map(e => e.$message)"
                    @input="validator.description.$touch"
                    @blur="validator.description.$touch"  
                    clearable 
                    placeholder="Description" 
                    auto-grow
                    rows="3"
                    counter
                    maxlength="500"
                    persistent-hint
                    hint="Max characters is 500">
                </v-textarea>
            </div>

            <div class="thumbnail mb-3 d-flex flex-column">
                <span class="text-subtitle-1">Post thumbnail</span>

                    <div class="file_input">
                        <v-file-input 
                            v-model="post_data.thumbnail"
                            @change="onFileChange"
                            @click:clear="onFileClear"
                            class="pt-0"
                            prepend-icon=""
                            prepend-inner-icon="mdi-image"
                            clearable 
                            :rules="rules"
                            accept="image/png, image/jpeg, image/bmp"
                            label="Input thumbnail img">
                        </v-file-input>
                    </div>

                    <v-card class="mb-4" variant="tonal" v-if="post_data.thumbnail_source">
                        <v-img
                            
                            :src="post_data.thumbnail_source"
                            :height="300"
                            aspect-ratio="16/9"
                            >                         
                        </v-img>
                    </v-card>


                <!-- <div v-if="showDialogButton">
                    <v-btn color="primary" @click="showPreviewDialog = true">Open Dialog</v-btn>
                </div> -->
            </div>

            <div class="body mb-3">
                <span class="text-subtitle-1">Post body</span>
                <div v-if="route_name == 'journal_edit'">
                    <div v-if="post_data?.body" >
                        <TextEditor :initialContent="post_data?.body" @editor-content="(data) => {post_data.body = data}"></TextEditor>
                    </div>
                    <div v-else></div>
                </div>
                <div v-else>
                    <TextEditor @editor-content="(data) => {post_data.body = data}"></TextEditor>
                </div>
                
                <div class="v-input__details px-4 pt-3" v-if="validator.body.$errors">
                    <v-container class="v-messages__message pa-0 text-error">{{validator.body.$errors.map(e => e.$message)[0]}}</v-container>
                </div>
            </div>


            <div class="tags">
                <span class="text-subtitle-1">Post tags</span>

                <v-combobox
                    v-model="post_data.tags"
                    :items="tagsSlugList"
                    v-model:search="tagSerch"
                    :hide-no-data="false"
                    :error-messages="validator.tags.$errors.map(e => e.$message)"
                    @input="validator.tags.$touch"
                    @blur="validator.tags.$touch" 
                    label="Selected tags"
                    clearable
                    hide-selected
                    multiple
                    chips
                    closable-chips
                    persistent-hint
                    :item-limit="10"
                    hint="Maximum is 10 tags">

                    <template v-slot:no-data>
                        <v-list-item>
                        <v-list-item-title style="white-space: normal; overflow: hidden;">
                            No results matching "<strong>{{ tagSerch }}</strong>". Press <kbd>enter</kbd> to create a new one
                        </v-list-item-title>
                        </v-list-item>
                    </template>
            
                </v-combobox>

            </div>

            <div class="postponed_publication">
                <div class="d-flex flex-column">
                    <v-switch
                        v-model="post_data.publish_option"
                        :label="`Publish: ${post_data.publish_option}`"
                        @update:model-value="changePublishOption"
                        color="info"
                        hide-details
                        true-value="later"
                        false-value="now">
                    </v-switch>
                    
                    <VueDatePicker 
                        class="mb-6"
                        style="max-width: 400px;"
                        v-if="post_data.publish_option == 'later'"
                        v-model="post_data.publish_datetime" 
                        :format="format"
                        :teleport="true"
                        placeholder="Pick the date and time of publication" 
                        :min-date="new Date()" 
                        :enable-time-picker="true"
                        :clearable="true"
                    />
                </div>
            </div>

            <div class="allow_comments">
                <v-switch
                    v-model="post_data.allow_comments"
                    :label="`Allow comments: ${post_data.allow_comments}`"
                    color="info"
                    hide-details
                    true-value="yes"
                    false-value="no">
                </v-switch>
            </div>


        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="d-flex flex-row justify-space-between flex-wrap">
            <v-btn class='my-2 mx-2' variant="outlined" color="error" @click="cancelPostCreation">Cancel</v-btn>
            <div class="save">
                <v-btn class='mx-2' variant="outlined" @click="save_to_draft" :disabled="saveToDraftBtnDisabled">Save to draft</v-btn>
                <v-btn class='mx-2 my-2' v-if="post_data.publish_option == 'later'" variant="outlined" @click="postponed_publish">Postponed publication</v-btn>
                <v-btn class='mx-2 my-2' v-else variant="outlined" @click="publish">{{route_name.value == 'journal_edit' ? 'Publish with changes' : 'Publish'}}</v-btn> 
            </div>
        </v-card-actions>



        
    </v-card>

    <!-- <v-dialog v-model="showPreviewDialog" width="auto">
      <v-card>
        <v-card-text>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" block @click="showPreviewDialog = false">Close Dialog</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog> -->

    <v-dialog v-model="cancelCautionDialog" width="auto">
        <v-card>
            <v-card-title class="text-h5"  style="white-space: normal; overflow: hidden;">Do you really want to cancel a post creation?</v-card-title>
            <v-card-text class="px-4">After confirming the action, all entered data will be deleted. If you want to save the data and continue creating the post later, click the "save to draft" button</v-card-text>

            <v-spacer></v-spacer>
            <v-card-actions class="d-flex flex-wrap">
                <v-btn class='my-2 mr-2' variant="outlined" @click="cancelCautionDialog = false" >Continue editing</v-btn>
                <v-btn class='ml-0' variant="outlined" color="error" @click="routes.go(-1)">Exit without saving data</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>


    <v-dialog v-model="validationErrorAlert" width="auto">
        <v-card>
            <div class="d-flex flex-row align-center">
                <v-icon class='mx-2' color="warning" size="large" icon="mdi-alert-circle-check-outline"></v-icon>
                <v-card-title class="text-h5 px-0"  style="white-space: normal; overflow: hidden;">Field validation error</v-card-title>
            </div>    
            <v-card-text class="px-4" style="white-space: normal; overflow: hidden;">
                You can't submit a post until the errors are fixed
                <v-list-item class="pl-0" v-for="(error, index) in validator.$errors" :key="index">
                    <template v-slot:prepend>
                        <v-icon class='mr-2' icon="mdi-circle-small"></v-icon>
                    </template>
                    <v-list-item-title>{{ `Error of the '${error.$property}' field` }}</v-list-item-title>
                    <v-list-item-subtitle style="white-space: normal; overflow: hidden;">{{error.$message}}</v-list-item-subtitle>
                </v-list-item>
            </v-card-text>
            <v-spacer></v-spacer>
            <v-card-actions class="d-flex flex-wrap justify-end">
                <v-btn class='my-2 mr-2' variant="text" color="success" @click="validationErrorAlert = false" >I got it</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>


</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeMount, onUpdated } from 'vue'
import { useTheme } from 'vuetify/lib/framework.mjs';
import { useStore } from 'vuex';
import { useVuelidate } from '@vuelidate/core'
import { required, helpers, maxLength } from '@vuelidate/validators'
import routes from '@/router/router' 

import TextEditor from '@/components/TextEditor/TextEditor.vue'

let theme = useTheme();
let store = useStore();


const tagList = computed(() => store.getters['journal/getTagsList'])
const tagsSlugList = computed(() => tagList.value.map(tag => tag.slug));
const tagSerch = ref(null)
const route_name = ref(routes.currentRoute.value.name)
const previous_page = ref(routes.options.history.state)


let showDialogButton = ref(false)
let showPreviewDialog = ref(false)
let cancelCautionDialog = ref(false)
let validationErrorAlert = ref(false)

let saveToDraftBtnDisabled = ref(true)
let mountedComplete = ref(false)


const save_to_draft=()=>{

    if(Object.entries(post_data.value).toString() != Object.entries(post_data_initial.value).toString()){
        validator.value.$errors = [] 
        const formData = new FormData();

        formData.append('is_draft', true)
        if(route_name.value=='journal_edit'){formData.append('id',routes.currentRoute.value.params.post_id)}
        
        for (const [key, value] of Object.entries(post_data.value)) {
            if(key=='title' || key=='description' || key=='body'){
                    if(value==''){formData.append(key, `Here could be a ${value} of your post`)}
                    else{formData.append(key, value)}
            }
            if(value != post_data_initial.value[key]){
                if(key=='title' || key=='description' || key=='body'){}
                else if(key=='thumbnail'){
                    if(value == null){formData.append("thumbnail", value)}
                    else{formData.append("thumbnail", value[0])}
                }
                else if(key=='tags'){formData.append('tags', JSON.stringify(value));}
                else if(key=='allow_comments'){formData.append('allow_comments', value =='yes' ? JSON.stringify(true) : JSON.stringify(false))}
                else if(key=='publish_option'){
                    if(value=='now'){
                        formData.append('is_publish', true)
                        formData.append('publish_datetime', null)
                    }
                    else{
                        if(post_data.value['publish_datetime']){
                            const date = new Date(post_data.value['publish_datetime']);
                            const utcDateTime = date.toISOString();
                            formData.append('publish_datetime', utcDateTime)
                            formData.append('is_publish', false)
                        }
                    }
                }
                else if(key=='publish_datetime'){}
                else{formData.append(key, value)}
                
            }   
        }

        if(route_name.value=='journal_edit'){
            store.dispatch('journal/partialUpdatePost',  formData)
        }
        else if(route_name.value=='journal_create'){
            store.dispatch('journal/createPost',  formData)
        }


        previous_page.value ? routes.go(-1) : routes.push({name: 'journal'})
    }


}

const postponed_publish=async()=>{
    
    const validation_result = await validator.value.$validate()
    if(validation_result == false){validationErrorAlert.value = true}
    else{ 
        let formData = new FormData();
        if(Object.entries(post_data.value).toString() != Object.entries(post_data_initial.value).toString()){

            formData.append('is_draft', false)
            if(route_name.value=='journal_edit'){formData.append('id',routes.currentRoute.value.params.post_id)}
                
            for (const [key, value] of Object.entries(post_data.value)) {
                if(value != post_data_initial.value[key]){
                    if(key=='title' || key=='description' || key=='body'){formData.append(key, value)}
                    else if(key=='thumbnail'){
                        console.log(key, 'thumbnail', `Initial: ${post_data_initial.value[key]}, post_data: ${value}`)
                        if(value == null){formData.append("thumbnail", value)}
                        else{formData.append("thumbnail", value[0])}
                    }
                    else if(key=='tags'){formData.append('tags', JSON.stringify(value));}
                    else if(key=='allow_comments'){formData.append('allow_comments', value =='yes' ? JSON.stringify(true) : JSON.stringify(false))}
                    else if(key=='publish_option'){formData.append('is_publish', false)}
                    else if(key=='publish_datetime'){
                        const date = new Date(value);
                        const utcDateTime = date.toISOString();
                        formData.append('publish_datetime', utcDateTime)
                    }
                }
            }           
        }
        else{
            const date = new Date(post_data.value['publish_datetime']);
            const utcDateTime = date.toISOString();

            formData.append('is_draft', false)
            formData.append('is_publish', false)
            formData.append('publish_datetime', utcDateTime)
            formData.append('id',routes.currentRoute.value.params.post_id) 
        }

        if(route_name.value=='journal_edit'){
            store.dispatch('journal/partialUpdatePost',  formData)
        }
        else if(route_name.value=='journal_create'){
            store.dispatch('journal/createPost',  formData)
        }

        previous_page.value ? routes.go(-1) : routes.push({name: 'journal'})
    }
}

const publish = async()=>{
    const validation_result = await validator.value.$validate()
    if(validation_result == false){validationErrorAlert.value = true}
    else{
        let formData = new FormData();
        if(Object.entries(post_data.value).toString() != Object.entries(post_data_initial.value).toString()){
            formData.append('is_draft', false)
            if(route_name.value=='journal_edit'){formData.append('id',routes.currentRoute.value.params.post_id)}
                
            for (const [key, value] of Object.entries(post_data.value)) {
                if(value != post_data_initial.value[key]){
                    if(key=='title' || key=='description' || key=='body'){formData.append(key, value)}
                    else if(key=='thumbnail'){
                        console.log(key, 'thumbnail', `Initial: ${post_data_initial.value[key]}, post_data: ${value}`)
                        if(value == null){formData.append("thumbnail", value)}
                        else{formData.append("thumbnail", value[0])}
                    }
                    else if(key=='tags'){formData.append('tags', JSON.stringify(value));}
                    else if(key=='allow_comments'){formData.append('allow_comments', value =='yes' ? JSON.stringify(true) : JSON.stringify(false))}
                    else if(key=='publish_option'){formData.append('is_publish', true)}
                    else if(key=='publish_datetime'){formData.append('publish_datetime', null)}
                }
               
            }
             
        }
        else{
            formData.append('is_draft', false)
            formData.append('is_publish', true)
            formData.append('publish_datetime', null)
            formData.append('id',routes.currentRoute.value.params.post_id) 
        }
        if(route_name.value=='journal_edit'){
            store.dispatch('journal/partialUpdatePost',  formData)
        }
        else if(route_name.value=='journal_create'){
            store.dispatch('journal/createPost',  formData)
        }
        
        previous_page.value ? routes.go(-1) : routes.push({name: 'journal'})
    }    
}


let post_data_initial = ref({
        'title':  '',
        'description': '',
        'thumbnail': null,
        'thumbnail_source': null,
        'body': '',
        'tags': [],
        'publish_option': 'now',
        'publish_datetime': null,
        'allow_comments': 'yes'
})

let post_data = ref({
        'title':  '',
        'description': '',
        'thumbnail': null,
        'thumbnail_source': null,
        'body': '',
        'tags': [],
        'publish_option': 'now',
        'publish_datetime': null,
        'allow_comments': 'yes'
})

const validator_rules = computed(() => {
  return {
    title: { is_required: helpers.withMessage("This field is required to the post", required) },
    description: { is_required: helpers.withMessage("This field is required to the post", required) },
    body: {is_required: helpers.withMessage("This field is required to the post", required)},
    tags: { maxItems: helpers.withMessage("You can select a maximum of 10 tags to a post", maxLength(10))}
  };
});

const validator = useVuelidate(validator_rules, post_data)



watch(post_data, (newValues, oldValues) => {
        if(mountedComplete.value == true){saveToDraftBtnDisabled.value = false}
        else{mountedComplete.value = true}
    }, {deep: true }
)


onMounted(async () => {
    await store.dispatch('journal/getTagsList')

    if(route_name.value=='journal_edit'){
        const post_id = routes.currentRoute.value.params.post_id
        await store.dispatch('journal/getPostDetail', post_id)

        const postDetail = store.getters['journal/getPostDetail']

        for(const [key, value] of Object.entries(postDetail)){
            switch (key){
                case 'title': 
                    post_data_initial.value[key] = value
                    break
                case 'description': 
                    post_data_initial.value[key] = value
                    break
                case 'thumbnail':
                    if(value != null){
                        const thumbnail_name = value.split("/").pop(); 
                        const file_obj = new File([""], thumbnail_name)
                        post_data_initial.value['thumbnail'] = [file_obj]
                        post_data_initial.value['thumbnail_source'] = value
                    }
                    break
                case 'body': 
                    post_data_initial.value[key] = value
                    break
                case 'tags':
                    const tags = value.map(item => item.slug)
                    post_data_initial.value[key] = tags
                    break
                case 'publish_datetime':
                    if(value){
                        post_data_initial.value[key] = format(value)
                        post_data_initial.value['publish_option'] = 'later'
                    }
                    break
                case 'allow_comments':
                    value == true ? post_data_initial.value[key] = 'yes' :  post_data_initial.value[key] = 'no'
                    break
                default:
                    break
            }
        }

        post_data.value = Object.assign({}, post_data_initial.value);
    }
    mountedComplete.value == true

})


const onFileChange = () => {
    const file = post_data.value.thumbnail[0];
    if (file) {
        post_data.value.thumbnail_source = URL.createObjectURL(file)
        // showDialogButton.value = true
    }
}

const onFileClear = () => {
    post_data.value.thumbnail_source = null
    // showDialogButton.value = false
}


const changePublishOption = () => {
    if(post_data.value.publish_datetime != ''){
        post_data.value.publish_datetime = null
    }
}

const format = (datetime) => {
        const date = new Date(datetime)

        const day = date.getDate().toString().padStart(2, '0');;
        const month = (date.getMonth() + 1).toString().padStart(2, '0');;
        const year = date.getFullYear().toString().padStart(4, '0');;
        const hours = date.getHours().toString().padStart(2, '0');;
        const minutes = date.getMinutes().toString().padStart(2, '0');

        const new_date = `${day}/${month}/${year} ${hours}:${minutes}`;

        return new_date
}

const cancelPostCreation = () => {
    for (const [key, value] of Object.entries(post_data.value)) {
        if(post_data_initial[key] != value){
            cancelCautionDialog.value = true
            return
        }
    }
    const lastPath = routes.options.history.state.back
    lastPath ? lastPath : '/journal'
    routes.go(-1)
}



</script>

<style lang="scss" scoped>
.delete_thumbnail{
    position: absolute;
    top: 10px;
    right: 10px;
}
.drag_n_drop_templte{border: 1px dashed;}

.v-field__field >>> .v-input__details {
  padding-left: 0 !important;
}

</style>