<template>
    <long-press-btn class='emoticon_element'
        v-if="this.section_type == 'reacted_emots'"
        :title="':'+this.reaction.reaction_id"
        :class="{reacted: this.reaction.data.find(data => data.username == this.getUserInfo().username)}"
        @LongPressEvent="react"
        @click="(event) => this.$emit('renderReactorsList', event.target.id)">
                
        <input type="radio" name="emoticonGroup" :value="`${this.reaction.reaction_id}_p_${this.post_id}`" :id="`${this.reaction.reaction_id}_p_${this.post_id}`">
        <label :for="`${this.reaction.reaction_id}_p_${this.post_id}`">
            <img :src="this.reaction.img_url" :alt="`:${this.reaction.reaction_id}`">
            <span>{{this.reaction.data.length}}</span>
        </label>
    </long-press-btn>

    <long-press-btn class='emoticon_element'
        v-else-if="this.section_type == 'all_emots'"
        :title="':'+this.reaction.reaction_id"
        @LongPressEvent="changeInFavoritesStatus"
        @click="react">


        <input type="radio" :value="`${this.reaction.reaction_id}_p_${this.post_id}`" :id="`${this.reaction.reaction_id}_p_${this.post_id}`">
        <label class="all_emots_section" :class="{mobile: this.isMobile == true, inFovorites: this.$store.getters.getIndexEmotInFavorites(this.reaction.reaction_id) >= 0}" :for="`${this.reaction.reaction_id}_p_${this.post_id}`">
                <img :src="this.reaction.img_url" :alt="`:${this.reaction.reaction_id}`">
                <div class="favorites_btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                    </svg>
                </div>
        </label>
    </long-press-btn>

</template>


<script>
import LongPressBtn from '@/components/Templates_components/LongPressBtn.vue'
export default {
    components: { LongPressBtn },
    props:['post_id', 'section_type', 'isMobile'],
    data(){return{
        reaction: this.$.vnode.key,
    }},

    methods:{

        getUserInfo(){
            return this.$store.getters.getUserInfo;
        },

        //A method that leaves a user reaction
        react(btn_element){
            const element_id = btn_element.target.getAttribute('for');
            const reaction_id = this.reaction.reaction_id;

            const post_id = this.post_id;
            const userInfo = this.$store.getters.getUserInfo;
            const dataOfUserReaction = this.$store.getters.getDataOfUserReaction([post_id, userInfo]);

            this.$store.dispatch("changeReactionStatus", [...dataOfUserReaction, userInfo, post_id, reaction_id]); 

            if(this.section_type == 'reacted_emots'){
                this.$emit('renderReactorsList', element_id);   
            }       
        },

        changeInFavoritesStatus(btn_element){
            //const favorites_btn_el = btn_element.querySelector('.favorites_btn');
            this.$store.dispatch("changeStatusReactionInFavorites", [this.reaction.reaction_id, this.reaction.img_url]);
        },
    }
}
</script>

<style lang="scss" scoped>
.emoticon_element{
    cursor: pointer;

    svg{stroke: var(--text_color_secondary); pointer-events: none;}
    input{display: none;}

    &.reacted input + label img{
        filter: drop-shadow(0 0 5px var(--bg_button_active_color));
    }

    &.reacted input + label{
        color:var(--bg_button_active_color);
    }

    input:checked + label{
        background-color: var(--active_section_color);
        border-bottom: 3px solid var(--bg_button_active_color);
        color: var(--bg_button_active_color);
    }
    
    input:checked + label > img{
        transform: scale(1.2);
        filter: drop-shadow(0 0 5px var(--bg_button_active_color));
    }

    input:checked + label > svg{
        stroke: var(--bg_button_active_color);
    }

    label{
        display: flex;
        position: relative;
        align-items: center;
        color: var(--text_color_secondary);
        padding: 8px 12px 5px 12px;
        height: 100%;
        border: 2px solid transparent;
        border-bottom: 3px solid var(--bg_button_color);
        cursor: pointer;
        white-space: nowrap;

        img{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            object-fit: contain;
            margin-right: 10px;
            pointer-events: none;
        }

        // style for all_emots section
        &.all_emots_section{
            padding: 5px 5px;
            margin: 0px 5px;
            border-bottom: 0;
            border-radius: 50%;

            &.inFovorites{
                border: 2px solid var(--bg_button_active_color);
                .favorites_btn{
                    display: flex;
                    flex-direction: row;
                    justify-content: center;
                    align-items: center;

                    svg{
                        stroke: #ffff;
                        fill: #ffff;
                    }
                }
            }

            img{margin-right: 0;}

            &:hover{border: 2px solid var(--bg_button_active_color);}

            &:hover > .favorites_btn{
                display: flex;
                flex-direction: row;
                justify-content: center;
                align-items: center;
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
                    stroke: var(--bg_button_color);
                    fill: var(--bg_button_color);
                }
            }

            //style for mobile devieces
            &.mobile{
                border: 2px solid var(--bg_button_active_color);
                border-radius: 50%;
                .favorites_btn{
                    display: flex;
                    flex-direction: row;
                    justify-content: center;
                    align-items: center;
                } 
            }
        }
  
        &:hover > svg {stroke: var(--bg_button_active_color);}
        &:hover {color: var(--bg_button_active_color);}
    }
}
</style>
