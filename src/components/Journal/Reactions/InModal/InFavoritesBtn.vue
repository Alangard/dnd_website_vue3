<template>
    <long-press-btn class='favorites_block_section'
        v-if="this.isMobile == true"
        :title="':'+this.emoticon.emoticon_id"
        @LongPressEvent="changeFavoritesStatus"
        @click="react">

        <div class="container" :class="{mobile: this.isMobile == true, inFovorites: inFavorites}">
            <img :src="this.emoticon.emoticon_url" :alt="`:${this.emoticon.emoticon_id}`">
            <div class="favorites_btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                </svg>
            </div>
        </div>
    </long-press-btn>

    <long-press-btn class='favorites_block_section'
        v-else 
        :title="':'+this.emoticon.emoticon_id">

        <div class="container" @click="react" :class="{inFovorites: inFavorites}" >
                <img :src="this.emoticon.emoticon_url" :alt="`:${this.emoticon.emoticon_id}`" >
                <div class="favorites_btn" @click="changeFavoritesStatus"> 
                    <!-- the click event's propagation will be stopped -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                    </svg>
                </div>
        </div>
    </long-press-btn>

</template>


<script>
import LongPressBtn from '@/components/Templates_components/LongPressBtn.vue'
export default {
    components: { LongPressBtn },
    props:['post_id', 'isMobile'],
    data(){return{
        emoticon: this.$.vnode.key,
    }},

    methods:{
        //A method that leaves a user reaction
        react(){

            this.$store.dispatch('changeReactionStatus', 
                {'post_id': this.post_id, 'pressed_emoticon_id': this.emoticon.emoticon_id, 'pressed_emoticon_url': this.emoticon.emoticon_url}
            );
      
        },

        changeFavoritesStatus(btn_element){
            this.$store.dispatch("changeStatusReactionInFavorites", 
                {'emoticon_id':this.emoticon.emoticon_id, 'emoticon_url':this.emoticon.emoticon_url}
            );
        },
    },

    computed:{
        // Returns the index of the emoticon in the Favorites section. If there is no emoticon, the getter will return -1
        inFavorites(){
            const IndexEmoticonInFavorites = this.$store.getters.getIndexEmotInFavorites(this.emoticon.emoticon_id);
            return IndexEmoticonInFavorites != -1 ? true : false;
        }
        
    }
}
</script>

<style lang="scss" scoped>
.favorites_block_section{
    margin: 0px 5px;
    cursor: pointer;

    svg{stroke: var(--text_color_secondary); pointer-events: none;}

    .container{
        display: flex;
        position: relative;
        align-items: center;
        color: var(--text_color_secondary);
        padding: 5px 5px;
        margin-top: 3px;
        height: 100%;
        border: 2px solid var(--bg_button_active_color);
        border-radius: 50%;
        white-space: nowrap;

        img{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            object-fit: contain;
            pointer-events: none;
        }

        &:hover > svg {stroke: var(--bg_button_active_color);}
        &:hover {
            color: var(--bg_button_active_color);
            background-color: var(--active_section_color);
        }
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
        //style for mobile devieces


        &.mobile{
            border: 2px solid var(--bg_button_active_color);
            border-radius: 50%;
            .favorites_btn{display: none;}
        }

        &.inFovorites{
            .favorites_btn{
                display: flex;
                flex-direction: row;
                justify-content: center;
                align-items: center;
            } 
        }
    }
}
</style>
