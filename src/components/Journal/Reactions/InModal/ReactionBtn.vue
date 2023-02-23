<template>
    <long-press-btn class='btn_container'
        @LongPressEvent="onLongPress"
        @click="react"
        :title="':'+ props.reaction_data.id">

        <img class='emote_img' :src="props.reaction_data.url" :alt="props.reaction_data.id">

        <div class="favorites_btn" 
            :class="{pressed: store.getters.getStatus}"
            @click="store.commit('changeStatus')">

            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
        </div>
    </long-press-btn>
</template>

<script setup>
import LongPressBtn from '@/components/Templates_components/LongPressBtn.vue'

import { defineProps } from 'vue';
import { useStore } from 'vuex';

const props = defineProps(['post_id', 'reaction_data']);
const store = useStore();

function onLongPress(btn_element){store.dispatch("changeStatusReactionInFavorites", [props.reaction_data.id, props.reaction_data.url]);}

function react(){
    debugger
    const reaction_id = props.reaction_data.id;
    const post_id = props.post_id;
    store.dispatch("changeReactionStatus", {post_id, reaction_id});
}


</script>

<!-- <script>
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
    },

}
</script> -->

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
