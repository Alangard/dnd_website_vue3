<template>
  <div class="accordion__item">
    <div 
      class="accordion__trigger"
      :class="{'accordion__trigger_active': visible}"
      @click="open()">

      <!-- This slot will handle the title/header of the accordion and is the part you click on -->
      <slot name="accordion-trigger"></slot>
    </div>

    <transition 
      name="accordion"
      @enter="start()"
      @after-enter="end()"
      @before-leave="start()"
      @after-leave="end()">

      <div class="accordion__content"
        v-show="visible">
        <div>
          <!-- This slot will handle all the content that is passed to the accordion -->
          <slot name="accordion-content"></slot>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'

const Accordion = inject('Accordion');
let index = ref(Accordion.count.value++);

const visible = computed(() => {return index == Accordion.active});

function open() {
  if (visible) {Accordion.active.value = null;} 
  else {Accordion.active.value = index;}
};

function start(el) {el.style.height = el.scrollHeight + "px";};

function end(el) {el.style.height = "";};
</script>

<style lang="scss" scoped>
.accordion__item {
  cursor: pointer;
  padding: 10px 20px 10px 40px;
  border-bottom: 1px solid #ebebeb;
  position: relative;
}

.accordion__trigger {
  display: flex;
  justify-content: space-between;
}

.accordion__content{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
}

.accordion-enter-active,
.accordion-leave-active {
  will-change: height, opacity;
  transition: height 0.3s ease, opacity 0.3s ease;
  overflow: hidden;
}

.accordion-enter,
.accordion-leave-to {
  height: 0 !important;
  opacity: 0;
}
</style>
