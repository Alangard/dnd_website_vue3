<template>
    <div class="section" :id='this.item_id'>
        <div class='section_header'
            :class="{visible: isVisible}"
            @click="this.collapse">

            <slot name='scrollspy_section__header'></slot>

            <svg class="collapse_icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 18l6-6-6-6"/>
            </svg>
        </div>

        <transition 
            name="collapse"
            @enter="start"
            @after-enter="end"
            @before-leave="start"
            @after-leave="end">

            <div class='section_body' v-show="this.isVisible">
                <slot name='scrollspy_section__body'></slot>
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
            this.$emit('changeCollapseState', true);
        },
        start(el) {el.style.height = el.scrollHeight + "px";},
        end(el) {el.style.height = "";}
    },
}
</script>

<style lang="scss" scoped>

.section{
    position: relative;
    margin: 0 7px 5px 0;
    border-radius: 5px;
    font-weight: 300;
    padding-bottom: 5px;
    color: var(--text_color_secondary);
    background-color: var(--bg_button_color);
    cursor: pointer;

    .section_header{
        position: sticky;
        z-index: 9999;
        top: -2px;
        padding: 5px 5px 5px 15px;
        font-weight: 400;
        border-radius: 5px;
        background-color: var(--bg_button_color);
        border-bottom: 3px solid transparent;
        //border-bottom: 3px solid var(--text_color_secondary);

        .collapse_icon{
            height: 1rem;
            stroke: var(--text_color_secondary);
        }

        &.visible > .collapse_icon{transform: rotate(90deg);}

        &.active{
            border-bottom: 3px solid var(--bg_button_active_color);
            color: var(--bg_button_active_color);
            background-color: var(--active_section_color);
        }

        &.active > svg{stroke: var(--bg_button_active_color);}


        
    }

    .section_body{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        padding: 5px 10px 0 10px;
    }

    .collapse-enter-active,
    .collapse-leave-active {
        will-change: height, opacity;
        transition: height 0.3s ease, opacity 0.3s ease;
        overflow: hidden;
    }

    .collapse-enter,
    .collapse-leave-to {
        height: 0 !important;
        opacity: 0;
    }
}



</style>