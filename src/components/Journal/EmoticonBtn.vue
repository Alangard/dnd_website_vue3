<!-- Компонент для эмотикона с возможностью добавить в избранное-->

<template>
    <div class="emot_btn_container" :id='"emot_btn_container" + this.post_id'>
        <q-btn round v-touch-hold.mouse="this.test">
            <img src="../../assets/test_blog_photo.png" alt="" >
        </q-btn>

        <div class="favorites_btn_desktop" 
            v-if='this.$store.getters.getIsMobileState == false'
            :class="{pressed: this.$store.getters.getStatus}"
            @click="this.$store.commit('changeStatus')">

            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
        </div>

            
        <div v-if="this.$store.getters.getIsMobileState == true"> 
            <svg class="favorites_btn_mobile" :class="{show_1: this.$store.getters.getStatus}" :id='"favorites_btn_mobile" + this.post_id' xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
        </div>

  


    </div>
</template>

<script>
export default {
    data(){
        return{
            in_favorite: this.$store.getters.getStatus, 
            t: false,
            longpress: null  //long press for desktop
        }
    },
    props:['post_id'],
    methods:{
        run_animate(){
            if(this.$store.getters.getIsMobileState == true){
                if(this.$store.getters.getStatus == true){
                    this.$store.commit('changeStatus');
                }
                else{
                    this.$store.commit('changeStatus');
                    this.t = !this.t;
                }
                
               
                /*
                document.querySelector('.emot_btn_container').style.cssText = "animation-duration:3s";
                document.querySelector('.favorites_btn_mobile').style.cssText = "animation-duration:3s";
                */

                 
            }
        },

        test(){
            if(this.$store.getters.getIsMobileState == true){
                if(this.$store.getters.getStatus == false){
                    const btn_container_el = document.querySelector('#emot_btn_container'+this.post_id).classList;
                    const btn_mobile_el = document.querySelector('#favorites_btn_mobile'+this.post_id).classList;

                    btn_container_el.add('show_svg');
                    btn_mobile_el.remove('show_1');
                    btn_mobile_el.add('show');

                    setTimeout(()=>{
                        btn_container_el.toggle('show_svg');
                        btn_mobile_el.remove('show');
                        this.$store.commit('changeStatus');

                    }, 3000);
                }
                else{
                    this.$store.commit('changeStatus');
                }
            }
        }

        /* Long press for desktop 

        @mousedown="doSomething"
        @mouseup="clear_func"
        @mouseout="clear_func"

        doSomething(){
            this.longpress = setTimeout(
                () => {
                    
                    if(this.$store.getters.getIsMobileState == true){
                        this.in_favorite = !this.in_favorite;

                        document.querySelector('.favorites_btn_mobile.show svg').style.cssText = "animation-duration:3s";
                        document.querySelector('.btn_container.show_svg').style.cssText = "animation-duration:3s";
                    }

                },600)
        },

        clear_func(){
            clearTimeout(this.longpress)
        }
        */
    },    
    
}
</script>

<style lang="scss" scoped>

    .row>*{
        padding: 0;
        margin: 0;
    }
    .emot_btn_container{
        position: relative;
        cursor: pointer;
        width: max-content;
        height: max-content;
        z-index: 2;

        &:hover {transform: scale(1.2);}

        img{
            height: 40px;
            width: 40px;
            border-radius: 50%;
            background-color: #ffff;
            object-fit: contain;
        }

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

        &:hover > .favorites_btn_desktop svg{display: block; transform: scale(1.2);}

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
        30%{filter: drop-shadow(0 0 0.75rem var(--bg_button_active_color));}
        100%{filter: drop-shadow(0 0 0.75rem transparent);}
    }



</style>