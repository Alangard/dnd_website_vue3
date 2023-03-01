<template>
    <div class="accordion">
      <slot></slot>
    </div>
</template>

<script setup>
import { ref, provide } from 'vue'

const Accordion = ref({count: 0, active: null});
provide('Accordion', Accordion)
</script>

<style lang="scss" scoped>
  .accordion {
      margin: 0;
      padding: 0;
      width: 100%;
  
      &:last-child {
      border-bottom: none;
      }
  }
</style>
  