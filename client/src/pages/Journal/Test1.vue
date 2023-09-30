<script setup>


const save_to_draft=()=>{

    if(Object.entries(post_data.value).toString() != Object.entries(post_data_initial.value).toString()){
        validator.value.$errors = [] 
        const formData = new FormData();

        formData.append('is_draft', true)
        formData.append('id',routes.currentRoute.value.params.post_id)
            
        for (const [key, value] of Object.entries(post_data.value)) {
            if(value != post_data_initial.value[key]){
                if(key=='title' || key=='description' || key=='body'){
                    if(value==''){formData.append(key, `Here could be a ${value} of your post`)}
                    else{formData.append(key, value)}
                }
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

        store.dispatch('journal/partialUpdatePost',  formData)

        routes.go(-1)
    }


}

const test =(type) =>{
    if(Object.entries(post_data.value).toString() != Object.entries(post_data_initial.value).toString()){
        if(type=='postponed_publish'){
            let formData = new FormData();
        }
        else if(type=='save_to_draft'){

        }
    }
}
</script>

 