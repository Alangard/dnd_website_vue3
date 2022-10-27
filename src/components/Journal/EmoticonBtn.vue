<template>
    <div class="btn_container">
        <img src="../../assets/test_blog_photo.png" alt="">
        
        <div class="favorites_btn_desktop" 
            v-if='this.$store.getters.getIsMobileState == false'
            :class="{pressed: this.pressed}"
            @click="this.pressed = !this.pressed">

            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
        </div>

        <div class="favorites_btn_mobile" v-else>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
        </div>

    </div>
</template>

<script>
export default {
    data(){return{pressed: false}},

    methods:{

    }

}
</script>

<style lang="scss" scoped>
    .btn_container{
        position: relative;
        cursor: pointer;
        width: max-content;
        height: max-content;

        img{
            height: 40px;
            width: 40px;
            border-radius: 50%;
            background-color: #ffff;
        }

        &:hover > img{transform: scale(1.2);}

        .favorites_btn_desktop svg{
            display: none;
            position: absolute;
            bottom: 2px;
            right: 12px;
            height: 15px;
            width: 15px;
            stroke: var(--bg_button_active_color);
        }

        .favorites_btn_desktop.pressed > svg{
            display: block;
            fill: var(--bg_button_active_color);
            stroke: var(--bg_button_active_color);
        }

        &:hover > .favorites_btn_desktop svg{display: block; transform: scale(1.2);}


        .favorites_btn_mobile svg{
            display: none;
            position: absolute;
            top: 20%;
            left: 20%;
            stroke: var(--bg_button_active_color);

        }
    }
</style>