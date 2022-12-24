<template>
    <long-press-btn class='reaction_more_block_section' 
        v-if="this.reaction.users_data.length != 0"
        :title="':'+this.reaction.emoticon_id"
        :class="{reacted: this.reaction_is_checked}"
        @LongPressEvent="react"
        @click="(event) => this.$emit('renderReactorsList', event.target.id)">
                
        <input type="radio" name="emoticonGroup" :value="`${this.reaction.emoticon_id}`" :id="`${this.reaction.emoticon_id}`">
        <label :for="`${this.reaction.emoticon_id}`">
            <img :src="this.reaction.emoticon_url" :alt="`:${this.reaction.emoticon_id}`">
            <span>{{Object.keys(this.reaction.users_data).length}}</span>
        </label>
    </long-press-btn>
</template>


<script>
import LongPressBtn from '@/components/Templates_components/LongPressBtn.vue'

export default {
    components: { LongPressBtn },

    props:['isMobile', 'user_info'],

    data(){
        return{
            reaction: this.$.vnode.key,
            user_index_in_reaction: null,
        }
    },

    computed:{

        //Get the object index of the user of the current session who left this response. Use to set the styles
        reaction_is_checked(){
            const user_index = this.reaction.users_data.findIndex(element => element.username == this.user_info.username);
            this.user_index_in_reaction = user_index;

            if(user_index != -1){

                //If the reaction has been selected, update the information in checked_emoticon_object inside the ReactionMore component
                this.$emit('FindReactedEmoticon', {'emoticon_id': this.reaction.emoticon_id, 'user_index': this.user_index_in_reaction});
                return true;
            }
            else{
                return false;
            }
        }
    },

    methods:{

        //A method that leaves a user reaction. Click handling proccessing in the ReactionMore component
        react(){
            this.$emit('react', this.reaction.emoticon_id);
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
