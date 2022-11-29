
<!-- Компонент для кнопки с длительным нажатием -->

<template>
    <div class="long_press__btn_container" ref='btn_container'>
        <slot></slot>
    </div>
</template>

<script>
import { onLongPress } from '@vueuse/core'
export default {
    data(){return{}},
    mounted(){
        // Longpress config
        const htmlEl = this.$refs.btn_container;
        onLongPress(
            htmlEl,
            this.onLongPress,
            { modifiers: { prevent: true } }
        )
    },
    methods:{
        onLongPress(event){
            this.$emit('LongPressEvent', event);
        },
    }
}
</script>

<style lang="scss" scoped>
    .long_press__btn_container{
        position: relative;
        cursor: pointer;
        width: max-content;
        height: max-content;
        z-index: 2;

        :slotted(img){
            height: 30px;
            width: 30px;
            border-radius: 50%;
            object-fit: contain;
            pointer-events: none;
        }
    }
</style>


