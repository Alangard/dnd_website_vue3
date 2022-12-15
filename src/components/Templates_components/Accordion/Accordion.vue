<template>
    <div class="accordion">
      <slot></slot>
    </div>
  </template>
  
  <script>
  export default {
    props: {},
    data() {
      return {
        Accordion: {
          count: 0,
          active: null
        }
      };
    },
    provide() {
      return { Accordion: this.Accordion };
    }
  };
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
  