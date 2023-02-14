<template>
    <div class="wrapper">
        <div class="bottom_sheet_container" ref="bottomSheet_container">
            <div class="header">
                <div class="swipe_btn" ref="el"></div>
            </div>
        </div>

    
    </div>
</template>


<script>
import { useSwipe } from '@vueuse/core';
import { ref } from 'vue';
import { onClickOutside } from '@vueuse/core';

export default {
    mounted(){
        onClickOutside(this.$refs.bottomSheet_container, (event) => 
            this.$emit('close_bottomSheet')
        )
        
        // Disable scrolling background page when modal is open
        document.querySelector('body').style.overflow ='hidden';
    },

    beforeUnmount(){
        //Before the page is unmounted, toggle overflow back
        document.querySelector('body').style.overflow = 'visible'
    },
}
</script>

<style lang="scss" scoped>
.wrapper{
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1060;
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: flex-end;
    background-color: rgba(0,0,0, 0.3);
    overflow: hidden;

    .bottom_sheet_container{
        position: relative;
        width: 100%;
        height: 50%;
        background-color:var(--bg_color);

        .header{
            display: flex;
            flex-direction: row;
            justify-content: center;
            padding-top: 10px;
            .swipe_btn{ 
                content: '';
                width: 20%;
                height: 10px;
                border-radius: 5px;
                background-color: var(--text_color_primary);
            }
        }
    }
}
</style>

