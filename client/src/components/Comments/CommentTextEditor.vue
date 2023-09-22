<template>
    <QuillEditor :options="options" class="rounded-editor"/>
</template>


<script setup>
import { ref } from 'vue'

const options = ref({
    modules: {
        toolbar: [
            [{ 'font': [] }, { 'size': ['small', false, 'large', 'huge'] }],
            ['bold', 'italic', 'underline', 'strike'],
            ['link', 'blockquote', { 'color': [] }],
            [{ 'align': [] }, { 'list': 'ordered'}, { 'list': 'bullet' }],
            ['clean']  

        ]
    },
    placeholder: 'Enter a comment...',
    readOnly: false,
    theme: 'snow'
})


</script>


<style lang='scss' scoped>
.rounded-editor {
  .ql-tooltip.ql-editing[data-mode="link"] {
    /* Добавьте стили для элемента ввода ссылки */
    background-color: red;
    border-radius: 5px;
    padding: 5px;
  }
}

</style>
<!-- 
.rounded_editor .ql-toolbar{
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
}
.rounded_editor{
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
} -->

