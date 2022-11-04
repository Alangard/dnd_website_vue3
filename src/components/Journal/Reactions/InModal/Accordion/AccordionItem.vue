<template>
  <div class="accordion_item" :class="{active: visible}">
    <div class="accordion_trigger" :class="{active: visible}"
      @click="open">

      <!-- This slot will handle the title/header of the accordion and is the part you click on -->
      <slot name="accordion-trigger"></slot>
    </div>

    <transition 
      name="accordion"
      @enter="start"
      @after-enter="end"
      @before-leave="start"
      @after-leave="end">

      <div class="accordion_content"
        v-show="visible">
          <!-- This slot will handle all the content that is passed to the accordion -->
          <slot name="accordion-content"></slot>
      </div>
    </transition>
  </div>
</template>


<script>
export default {
  props: {},
  inject: ["Accordion"],
  data() {
    return {
      index: null
    };
  },
  computed: {
    visible() {
      return this.index == this.Accordion.active;
    }
  },
  methods: {
    open() {
      if (this.visible) {
        this.Accordion.active = null;
      } else {
        this.Accordion.active = this.index;
      }
    },
    start(el) {
      el.style.height = el.scrollHeight + "px";
    },
    end(el) {
      el.style.height = "";
    }
  },
  created() {
    this.index = this.Accordion.count++;
  }
};
</script>

<style lang="scss" scoped>
.accordion_item {
    position: relative;
    width: 100%;
    border-left: 4px solid var(--bg_button_color);
    margin: 10px 0;
    border-radius: 5px;
    background-color: var(--bg_button_color);
    font-weight: 400;
    font-size: 18px;
    color: var(--text_color_secondary);
    cursor: pointer; 

    &:hover, &.active{
        border-left: 4px solid var(--bg_button_active_color);
    }

    .accordion_trigger {
        display: flex;
        justify-content: space-between;
        width: 100%;
        padding: 5px 5px;

        &.active{
            border-bottom: 2px solid var(--bg_button_active_color);
        }
    }
}

.accordion_content{
    padding: 10px 5px;
    border-radius: 5px;
    background-color: var(--bg_button_color);
    font-weight: 300;
}


.accordion-enter-active,
.accordion-leave-active {
    will-change: height, opacity;
    transition: height 0.3s ease, opacity 0.3s ease;
    overflow: hidden;
}

// .accordion-enter,
// .accordion-leave-to {
//     height: 0 !important;
//     opacity: 0;
// }
</style>
