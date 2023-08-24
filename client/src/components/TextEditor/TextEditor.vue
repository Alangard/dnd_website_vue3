<template>
  <div class="text-edtor_toolbar" v-if="editor">
        <v-btn class="bold pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text" 
            @click="editor.chain().focus().toggleBold().run()" 
            :disabled="!editor.can().chain().focus().toggleBold().run()" 
            :class="{ 'is-active text-info v-btn--variant-tonal': editor.isActive('bold') }">
            <v-icon icon="mdi-format-bold" size="large" ></v-icon>
        </v-btn>


        <v-btn class="italic pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text" 
            @click="editor.chain().focus().toggleItalic().run()" 
            :disabled="!editor.can().chain().focus().toggleItalic().run()"
            :class="{ 'is-active text-info v-btn--variant-tonal': editor.isActive('italic') }">
            <v-icon icon="mdi-format-italic" size="large" ></v-icon>
        </v-btn>


        <v-btn class="strike pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text" 
            @click="editor.chain().focus().toggleStrike().run()" 
            :disabled="!editor.can().chain().focus().toggleStrike().run()"
            :class="{ 'is-active text-info v-btn--variant-tonal': editor.isActive('strike') }">
            <v-icon icon="mdi-format-strikethrough" size="large" ></v-icon>
        </v-btn>

        
        <v-btn class="underline pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text" 
            @click="editor.chain().focus().toggleUnderline().run()" 
            :class="{ 'is-active text-info v-btn--variant-tonal': editor.isActive('underline') }">
            <v-icon icon="mdi-format-underline" size="large" ></v-icon>
        </v-btn>


        <v-btn class="clear pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text"
            @click="($event) => { editor.chain().focus().unsetAllMarks().run(); toggleBtn($event) }"
            :class="{ 'is-active text-info v-btn--variant-tonal': editor.isActive('clear') }">
            <v-icon icon="mdi-format-clear" size="large" ></v-icon>
        </v-btn>


        <v-menu class="heading">
            <template v-slot:activator="{ props }">
                <v-btn
                    v-bind="props"
                    class="headers_levels pa-0 mr-1" 
                    height="1.5rem"
                    min-width="25px" 
                    width="25px" 
                    variant="text">
                        <v-icon icon="mdi-format-header-pound" size="large" ></v-icon>
                </v-btn>
            </template>
            <v-list>
                <v-list-item 
                    v-for="index in 6" :key="index"
                    @click="editor.chain().focus().toggleHeading({ level: index }).run()" 
                    :class="{ 'is-active': editor.isActive('heading', { level: index }) }">
                        <v-list-item-title class="font-weight-bold" :style="'font-size:' + ((7-index)*2 + 13) + 'px'">Heading {{ index }}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>


        <v-btn class="bullet_list pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text"
            @click="editor.chain().focus().toggleBulletList().run()"
            :class="{ 'is-active text-info v-btn--variant-tonal': editor.isActive('bulletList') }">
            <v-icon icon="mdi-format-list-bulleted" size="large" ></v-icon>
        </v-btn>


        <v-btn class="ordered_list  pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text"
            @click="editor.chain().focus().toggleOrderedList().run()"
            :class="{ 'is-active text-info v-btn--variant-tonal': editor.isActive('orderedList') }">
            <v-icon icon="mdi-format-list-numbered" size="large" ></v-icon>
        </v-btn>


        <v-btn class="blockquote pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text"
            @click="editor.chain().focus().toggleBlockquote().run()"
            :class="{ 'is-active text-info v-btn--variant-tonal': editor.isActive('blockquote') }">
            <v-icon icon="mdi-format-quote-close" size="large" ></v-icon>
        </v-btn>


        <v-btn class="horizontal_divider pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text"
            @click="($event) => {editor.chain().focus().setHorizontalRule().run(); toggleBtn($event)}">
            <v-icon icon="mdi-minus" size="large" ></v-icon>
        </v-btn>


        <v-btn class="undo pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text"
            @click="($event) => {editor.chain().focus().undo().run(); toggleBtn($event)}"
            :disabled="!editor.can().chain().focus().undo().run()">
            <v-icon icon="mdi-undo" size="large" ></v-icon>
        </v-btn>


        <v-btn class="redo pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text"
            @click="($event) => {editor.chain().focus().redo().run(); toggleBtn($event)}"
            :disabled="!editor.can().chain().focus().redo().run()">
            <v-icon icon="mdi-redo" size="large" ></v-icon>
        </v-btn>

   
        <v-menu class="alignment">
            <template v-slot:activator="{ props }">
                <v-btn
                    v-bind="props"
                    class="alignment pa-0 mr-1" 
                    height="1.5rem"
                    min-width="25px" 
                    width="25px" 
                    variant="text">
                        <v-icon icon="mdi-format-align-center" size="large" ></v-icon>
                </v-btn>
            </template>
            <v-list class="py-1">
                <v-list-item class="left_align py-0 px-2" min-height="30px"
                  @click="editor.chain().focus().setTextAlign('left').run()" 
                  :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }">

                  <template v-slot:prepend>
                    <v-icon class="ma-0" icon="mdi-format-align-left" size="small"></v-icon>
                  </template>
                </v-list-item>
                <v-list-item class="right_align py-0 px-2" min-height="30px"
                  @click="editor.chain().focus().setTextAlign('right').run()" 
                  :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }">

                  <template v-slot:prepend>
                    <v-icon class="ma-0" icon="mdi-format-align-right" size="small"></v-icon>
                  </template>
                </v-list-item>
                <v-list-item class="center_align py-0 px-2" min-height="30px"
                  @click="editor.chain().focus().setTextAlign('center').run()" 
                  :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }">

                  <template v-slot:prepend>
                    <v-icon class="ma-0" icon="mdi-format-align-center" size="small"></v-icon>
                  </template>
                </v-list-item>
                <v-list-item class="justify_align py-0 px-2" min-height="30px"
                  @click="editor.chain().focus().setTextAlign('justify').run()" 
                  :class="{ 'is-active': editor.isActive({ textAlign: 'justify' }) }">

                  <template v-slot:prepend>
                    <v-icon class="ma-0" icon="mdi-format-align-justify" size="small"></v-icon>
                  </template>
                </v-list-item>
            </v-list>
        </v-menu>


        <v-btn class="set_link pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text"
            @click="setLink()"
            :class="{ 'is-active text-info v-btn--variant-tonal': editor.isActive('link') }">
            <v-icon icon="mdi-link-variant-plus" size="large" ></v-icon>
        </v-btn>


        <v-btn class="remove_link pa-0 mr-1" 
            height="1.5rem"
            min-width="25px" 
            width="25px" 
            variant="text"
            @click="($event) => {editor.chain().focus().unsetLink().run(); toggleBtn($event)}"
            :disabled="!editor.isActive('link')">
            <v-icon icon="mdi-link-variant-remove" size="large" ></v-icon>
        </v-btn>


        <v-menu class="text-color">
            <template v-slot:activator="{ props }">
                <v-btn
                    v-bind="props"
                    class="text-color pa-0 mr-1" 
                    height="1.5rem"
                    min-width="25px" 
                    width="25px" 
                    variant="text">
                      <v-icon icon="mdi-palette" size="large" ></v-icon>
                </v-btn>
            </template>
            <div class="d-flex flex-column">
              <v-color-picker v-model="textColor" mode='hex' @update:model-value="editor.chain().focus().setColor(textColor).run()"></v-color-picker>
            </div>
        </v-menu>


        <v-menu class="text-highlight">
            <template v-slot:activator="{ props }">
                <v-btn
                    v-bind="props"
                    class="text-highlight pa-0 mr-1" 
                    height="1.5rem"
                    min-width="25px" 
                    width="25px" 
                    variant="text">
                      <v-icon icon="mdi-marker" size="large" ></v-icon>
                </v-btn>
            </template>
            <div class="d-flex flex-column">
              <v-color-picker v-model="textHighlight" mode='hex' @update:model-value="editor.chain().focus().toggleHighlight({ color: textHighlight }).run()"></v-color-picker>
            </div>
        </v-menu>


        <v-combobox class="font_family"
          v-model="fontFamily"
          :items="['Comic Sans', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']"
          :style="'font-family:'+ fontFamily"
          @update:model-value="editor.chain().focus().setFontFamily(fontFamily).run()" 
          style="width:170px"
          placeholder="Choose font family"
          persistent-placeholder
          hide-no-data
          hide-details
          density="compact"  
          variant="underlined">
            <template v-slot:item="{ item }">
              <div :style="{ fontFamily: item.title}">{{ item.title }}</div>
            </template>
        </v-combobox>




        img, youtube, table, placeholder, mantion?





    </div>
    <editor-content class="text-editor" :editor="editor"/>
  </template>
  
<script setup>
import {ref, onBeforeMount, onBeforeUnmount} from 'vue'
import StarterKit from '@tiptap/starter-kit'
import Underline from '@tiptap/extension-underline'
import TextAlign from '@tiptap/extension-text-align'
import Link from '@tiptap/extension-link'
import TextStyle from '@tiptap/extension-text-style'
import { Color } from '@tiptap/extension-color'
import Highlight from '@tiptap/extension-highlight'
import FontFamily from '@tiptap/extension-font-family'
import { Editor, EditorContent } from '@tiptap/vue-3'

  
const editor = ref(null);
const textColor = ref('#000000')
const textHighlight = ref('#000000')
const fontFamily = ref('Roboto')

onBeforeUnmount(() => {
  editor.value.destroy();
});


const content = `
  <h2>
    Hi there,
  </h2>
  <p>
    this is a <em>basic</em> example of <strong>tiptap</strong>. Sure, there are all kind of basic text styles you’d probably expect from a text editor. But wait until you see the lists:
  </p>
  <ul>
    <li>
      That’s a bullet list with one …
    </li>
    <li>
      … or two list items.
    </li>
  </ul>
  <p>
    Isn’t that great? And all of that is editable. But wait, there’s more. Let’s try a code block:
  </p>
  <pre><code class="language-css">body {
    display: none;
  }</code></pre>
  <p>
    I know, I know, this is impressive. It’s only the tip of the iceberg though. Give it a try and click a little bit around. Don’t forget to check the other examples too.
  </p>
  <blockquote>
    Wow, that’s amazing. Good work, boy! 👏
    <br />
    — Mom
  </blockquote>
`;

onBeforeMount(() => {
  editor.value = new Editor({
    extensions: [
      StarterKit,
      Underline,
      TextAlign.configure({
          types: ['heading', 'paragraph'],
        }),
       Link.configure({
          openOnClick: true,
        }),
      TextStyle,
      FontFamily,
      Color,
      Highlight.configure({ multicolor: true }),
    ],
    content,
  });
});

const toggleBtn = (e) => {
        const element_obj = e.currentTarget.classList
        element_obj.toggle('is-active')
        element_obj.toggle('text-info')
        element_obj.toggle('v-btn--variant-tonal')
}


const setLink = () => {
      const previousUrl = editor.value.getAttributes('link').href
      const url = window.prompt('URL', previousUrl)

      // cancelled
      if (url === null) {return}

      // empty
      if (url === '') {
        editor.value.chain().focus().extendMarkRange('link').unsetLink().run()
        return
      }
      // update link
      editor.value.chain().focus().extendMarkRange('link').setLink({ href: url }).run()
    }

</script>
  
  <style lang="scss">
  /* Basic editor styles */
  .tiptap {
    > * + * {
      margin-top: 0.75em;
    }

    a:hover{
        cursor: pointer;
    }
  
    ul,
    ol {
      padding: 0 1rem;
    }
  
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
      line-height: 1.1;
    }
  
    code {
      background-color: rgba(#616161, 0.1);
      color: #616161;
    }
  
    pre {
      background: #0D0D0D;
      color: #FFF;
      font-family: 'JetBrainsMono', monospace;
      padding: 0.75rem 1rem;
      border-radius: 0.5rem;
  
      code {
        color: inherit;
        padding: 0;
        background: none;
        font-size: 0.8rem;
      }
    }
  
    img {
      max-width: 100%;
      height: auto;
    }
  
    blockquote {
      padding-left: 1rem;
      border-left: 2px solid rgba(#0D0D0D, 0.1);
    }
  
    hr {
      border: none;
      border-top: 2px solid rgba(#0D0D0D, 0.1);
      margin: 2rem 0;
    }
  }
  </style>