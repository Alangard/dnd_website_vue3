<template>
    <div class="section" :id='props.item_id'>
        <div class='collapse_header'
            :class="{visible: isVisible}"
            @click="collapse()">

            <slot name='collapse_header'></slot>
        </div>

        <transition 
            name="collapse"
            @enter="start"
            @after-enter="end"
            @before-leave="start"
            @after-leave="end">

            <div class='collapse_body' v-if="isVisible">
                <slot name='collapse_body'></slot>
            </div>
        </transition>
    </div>
</template>


<script setup>
import { ref, defineEmits, defineProps } from 'vue';

const emit = defineEmits(['changeCollapseState']);
const props = defineProps(['item_id', 'visible']);

const isVisible = ref(props.visible);

function collapse(){
    isVisible.value = !isVisible.value;
    emit('changeCollapseState', isVisible);
}

function start(el){el.style.height = el.scrollHeight + "px";}

function end(el){el.style.height = "";}

</script>


