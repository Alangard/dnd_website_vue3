<template>
    <long-press-btn @LongPressEvent="this.onLongPress" class='btn_container'>
        <img src="@/assets/test_blog_photo.png" alt="" >

        <div class="favorites_btn_desktop" 
            v-if='this.$store.getters.getIsMobileState == false'
            :class="{pressed: this.$store.getters.getStatus}"
            @click="this.$store.commit('changeStatus')">

            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
        </div>
  
        <div v-if="this.$store.getters.getIsMobileState == true"> 
            <svg ref='favorites_btn_mobile' class="favorites_btn_mobile" :class="{show_1: this.$store.getters.getStatus}" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
        </div>
    </long-press-btn>
</template>

<script>
import LongPressBtn from '@/components/Templates_components/LongPressBtn.vue'
export default {
  components: { LongPressBtn },
    data(){return{}},
    methods:{
        onLongPress(btn_element){
            if(this.$store.getters.getIsMobileState == true){
                const mobile_favorite_icon = btn_element.querySelector('.favorites_btn_mobile');

                if(this.$store.getters.getStatus == false){
                    //Start the animation 
                    mobile_favorite_icon.classList.add('show');
                    btn_element.classList.add('show_svg');

                    //At the end of the animation we put the icon in the active state, so that the animation will not play next time
                    setTimeout(() => {
                        mobile_favorite_icon.classList.remove('show');
                        mobile_favorite_icon.classList.add('show_1');
                        btn_element.classList.remove('show_svg');
                        this.$store.commit('changeStatus');
                    }, 3000);
                }
                else{
                   this.$store.commit('changeStatus'); 
                }
            }
            
        },
    },

}
</script>

<style lang="scss" scoped>
.favorites_btn_desktop svg{
    display: none;
    position: absolute;
    bottom: 3px;
    left: 12px;
    height: 15px;
    width: 15px;
    stroke: var(--bg_button_active_color);
}

.favorites_btn_desktop.pressed > svg{
    display: block;
    fill: var(--bg_button_active_color);
    stroke: var(--bg_button_active_color);
}

.btn_container:hover > .favorites_btn_desktop svg{display: block;}

.favorites_btn_mobile{
    position: absolute;
    z-index: 1;
    opacity: 0;
    top: 20%;
    left: 20%;
    stroke: var(--bg_button_active_color);
    animation-fill-mode: forwards;
    pointer-events: none;
}

/*.......Animation...........*/
.favorites_btn_mobile.show{
        animation-name: favorite_svg_animation_show;
        animation-duration: 3s;
}

.favorites_btn_mobile.show_1{
        opacity: 1;
        top: 50%;
        transform: scale(.7);
        fill: var(--bg_button_active_color);
}

.btn_container.show_svg{
        animation-name: favorite_btn_animation_show;
        animation-duration: 3s;
}

@keyframes favorite_svg_animation_show{
    0%{
        opacity: 0;  
    }
    1%{
        opacity: 0;
        top: 20%;
        left: 20%;
        fill: transparent;
    }
    30%{
        opacity: 1;
        top: 20%;
        left: 20%;
        fill: var(--bg_button_active_color);
        transform: rotate(0deg) scale(1.4);
    }
    70%{
        opacity: 0;
        fill: var(--bg_button_active_color);
        transform: rotate(360deg) scale(0);
    }

    100%{
        opacity: 1;
        top: 50%;
        transform: scale(.7);
        fill: var(--bg_button_active_color);
    }
}

@keyframes favorite_btn_animation_show{
    0%{filter: drop-shadow(0 0 0 transparent);}
    30%{filter: drop-shadow(0 0 0.75rem var(--drop_shadow_color));}
    100%{filter: drop-shadow(0 0 0.75rem transparent);}
}
</style>
