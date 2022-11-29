<template>
    <long-press-btn class='btn_container'
        @LongPressEvent="this.onLongPress"
        @click="this.react"
        :title="':'+this.reaction_data.id">

        <img class='emote_img' :src="this.reaction_data.url" :alt="this.reaction_data.id">

        <div class="favorites_btn" 
            :class="{pressed: this.$store.getters.getStatus}"
            @click="this.$store.commit('changeStatus')">

            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
        </div>
    </long-press-btn>
</template>

<script>
import LongPressBtn from '@/components/Templates_components/LongPressBtn.vue'
export default {
    components: { LongPressBtn },
    props:['post_id', 'reaction_data', 'section_type'],
    data(){return{}},
    methods:{
        onLongPress(btn_element){
                const favorites_btn_el = btn_element.querySelector('.favorites_btn');
                this.$store.dispatch("changeStatusReactionInFavorites", [this.reaction_data.id, this.reaction_data.url]);
        },

        react(){
            debugger
            const reaction_id = this.reaction_data.id;
            const post_id = this.post_id;

            this.$store.dispatch("changeReactionStatus", {post_id, reaction_id});
        },


        // react(btn_element_target){
        //     if (btn_element_target.tagName == 'LABEL'){
        //         const element_id = btn_element_target.getAttribute('for');
        //         const post_id = this.post_id;
        //         const reaction_id = element_id.split('_p_')[0]; 

        //         this.$store.dispatch("changeReactionStatus", {post_id, reaction_id}); 
        //     }         
        
        // onLongPress(btn_element){
        //     if(this.$store.getters.getIsMobileState == true){
        //         const mobile_favorite_icon = btn_element.querySelector('.favorites_btn_mobile');
        //         console.log(mobile_favorite_icon)

        //         if(this.$store.getters.getStatus == false){
        //             //Start the animation 
        //             mobile_favorite_icon.classList.add('show');
        //             btn_element.classList.add('show_svg');

        //             //At the end of the animation we put the icon in the active state, so that the animation will not play next time
        //             setTimeout(() => {
        //                 mobile_favorite_icon.classList.remove('show');
        //                 mobile_favorite_icon.classList.add('show_1');
        //                 btn_element.classList.remove('show_svg');
        //                 this.$store.commit('changeStatus');
        //             }, 3000);
        //         }
        //         else{
        //            this.$store.commit('changeStatus'); 
        //         }
        //     }
            
        // },

        // // getUserData(){
        // //     // запрашиваем эти данные их localstorage или coockie
        // //     const user_info = {'username': 'usert2.804357', 'profile_img': '', 'date': '1995-12-17T09:24:00'}; 
        // //     return user_info;
        // // },

        // react(btn_element_target){
        //     if (btn_element_target.tagName == 'LABEL'){
        //         const element_id = btn_element_target.getAttribute('for');
        //         const post_id = this.post_id;
        //         const reaction_id = element_id.split('_p_')[0] + '.gif';

        //         const user_info = this.getUserData();

        //         this.$store.dispatch("changeReactionStatus", {post_id, reaction_id, user_info}); 
        //     }          
        // },
    },

}
</script>

<style lang="scss" scoped>

.btn_container{
    border: 2px solid var(--bg_button_active_color);;
    border-radius: 50%;
    padding: 5px;
}

.favorites_btn{
    display: none;
    position: absolute;
    height: 20px;
    width: 20px;
    border-radius: 50%;
    top: -2%;
    right: -25%;
    background-color: var(--bg_button_active_color);

    svg{
        width: 17px;
        height: 17px;
        stroke: var(--bg_button_color);;
        fill: var(--bg_button_color);
    }

}

.favorites_btn.pressed{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}

// .btn_container.pressed{
//     border: 2px solid var(--bg_button_active_color);
// }

// .btn_container:hover > .favorites_btn svg{display: block;}

// .favorites_btn_mobile{
//     position: absolute;
//     z-index: 1;
//     opacity: 0;
//     top: -20%;
//     left: 55%;
//     stroke: var(--bg_button_active_color);
//     animation-fill-mode: forwards;
//     pointer-events: none;
// }

/*.......Animation...........*/
.favorites_btn_mobile.show{
        animation-name: favorite_svg_animation_show;
        animation-duration: 3s;
}

.favorites_btn_mobile.show_1{
        opacity: 1;
        top: -20%;
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
        top: 18%;
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
        top: -20%;
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
