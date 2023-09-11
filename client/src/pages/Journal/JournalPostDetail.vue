<template>
    <div class="main_wrapper">

        <v-card class="post_detail_wrapper">
            <v-img
                class="bg-white"
                :src="postDetail.thumbnail"
                max-height="430"
                aspect-ratio="16/9"
                contain>
            </v-img>
            <v-card-title class="title mb-2">{{postDetail.title}}</v-card-title>
            <v-card-subtitle class="description text-h6 mb-2">{{ postDetail.description }}</v-card-subtitle>
            <v-card-text class="body text-body-1 mb-2" >
                <editor-content class="text-editor w-100" :editor="editor"/>
            </v-card-text>
            <v-card-actions></v-card-actions>
        </v-card>

        <Comments></Comments>
    </div>

</template>

<script setup>
import { ref, defineAsyncComponent, onMounted, onBeforeUnmount, computed} from 'vue';
import { useStore } from 'vuex';
import {useEditor, EditorContent, Editor } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'

const Comments = defineAsyncComponent(() => import('@/components/Comments/Comments.vue'));

let store = useStore();

const postDetail = computed(() => store.getters['journal/getPostDetail'])
let editor = ref()



onMounted(async () => {
    const post_id = 38
    await store.dispatch('journal/getPostDetail', post_id)

    editor.value = new Editor({
        content: postDetail.value.body,
        extensions: [
        StarterKit,
        ],
        editable: false,
    });
})

onBeforeUnmount(() => {
    editor.value.destroy();
});



    
</script>

<style lang="scss" scoped>
    .main_wrapper{
        width: 100%;
        max-width: 750px;
        padding: 0;
        margin: 0;
        margin-top: 20px;
        position: relative;

        .image_container{
            position: relative;


            .title_container{
                position: absolute;
                display: flex;
                bottom: 0;
                overflow-wrap: normal;
                overflow: hidden;
                /* white-space: nowrap; */
                word-break: normal;
                word-wrap: break-word;
                padding: 20px 20px;
                z-index: 999;
            }
        }
    }
</style>