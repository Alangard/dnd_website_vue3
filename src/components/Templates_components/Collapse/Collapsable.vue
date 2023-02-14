<template>
    <div class="section" :id='this.item_id'>
        <div class='collapse_header'
            :class="{visible: isVisible}"
            @click="this.collapse">

            <slot name='collapse_header'></slot>
        </div>

        <transition 
            name="collapse"
            @enter="start"
            @after-enter="end"
            @before-leave="start"
            @after-leave="end">

            <div class='collapse_body' v-if="this.isVisible">
                <slot name='collapse_body'></slot>
            </div>
        </transition>
    </div>
</template>


<script>
export default {
    props:['item_id', 'visible'],

    data() {
        return {isVisible: false,}
    },

    mounted(){
        this.isVisible = this.visible;
    },

    methods: {
        collapse(){
            this.isVisible = !this.isVisible;
            this.$emit('changeCollapseState', this.isVisible);
        },
        start(el) {el.style.height = el.scrollHeight + "px";},
        end(el) {el.style.height = "";}
    },
}
</script>


