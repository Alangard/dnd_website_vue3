
<!-- Компонент для кнопки с длительным нажатием -->

<template>
    <div class="btn_container" ref='btn_container'>
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
            const btn_element = event.target;
            this.$emit('LongPressEvent', btn_element);
        },
    }
}
</script>

<style lang="scss" scoped>
    .btn_container{
        position: relative;
        cursor: pointer;
        width: max-content;
        height: max-content;
        z-index: 2;

        &:slotted(img){
            height: 40px;
            width: 40px;
            border-radius: 50%;
            object-fit: contain;
            pointer-events: none;
        }
    }
</style>


