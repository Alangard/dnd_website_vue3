<template>
    <long-press-btn class='reaction_more_block_section' 
        v-if="this.reaction.data.length != 0"
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
</template>


<script>
import LongPressBtn from '@/components/Templates_components/LongPressBtn.vue'
export default {
    components: { LongPressBtn },
    props:['post_id', 'isMobile'],
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

            const post_id = this.post_id;
            const userInfo = this.$store.getters.getUserInfo;
            const dataOfUserReaction = this.$store.getters.getDataOfUserReaction([post_id, userInfo]);

            this.$store.dispatch("changeReactionStatus", [...dataOfUserReaction, post_id, {'reaction_id': this.reaction.reaction_id, 'img_url': this.reaction.img_url}]); 
            this.$store.dispatch("addReactionToRecent", [this.reaction.reaction_id, this.reaction.img_url]);
            this.$emit('renderReactorsList', element_id);   
        },
    }
}
</script>

<style lang="scss" scoped>
.reaction_more_block_section{
    cursor: pointer;

    svg{stroke: var(--text_color_secondary); pointer-events: none;}
    input{display: none;}

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

        &:hover > svg {stroke: var(--bg_button_active_color);}
        &:hover {color: var(--bg_button_active_color);}
    }

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
}
</style>
