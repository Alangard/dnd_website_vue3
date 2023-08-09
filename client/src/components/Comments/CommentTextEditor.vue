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


{/* <div class="rounded-editor mb-5 ql-container ql-snow">
    <div class="ql-editor" data-gramm="false" contenteditable="true" data-placeholder="Enter a comment...">
        <p>dasdad</p>
    </div>
    <div class="ql-clipboard" contenteditable="true" tabindex="-1"></div>
    <div class="ql-tooltip ql-editing" data-mode="link" style="left: -116.172px; top: 28px;">
        <a class="ql-preview" rel="noopener noreferrer" target="_blank" href="about:blank"></a>
        <input type="text" data-formula="e=mc^2" data-link="https://quilljs.com" data-video="Embed URL" placeholder="https://quilljs.com">
        <a class="ql-action"></a>
        <a class="ql-remove"></a>
    </div>
</div> */}



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

