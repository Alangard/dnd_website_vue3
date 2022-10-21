<template>

<div class="main_emot_container" @mouseover="this.isHover = true" @mouseleave="this.isHover = false">
    <div class="emoticon_container" @click="emoticonIsClicked()" :class="{selected: this.isHover}">
        <img :src='getImg()' alt="">
        <span>{{this.counter}}</span>
    </div> 

    <Dropdown_info 
        :isHover="this.isHover"
        :reactors_list="this.$.vnode.key.data">
    </Dropdown_info>

</div>

<Modal :reactors_list="this.$.vnode.key.data"></Modal>
    
</template>

<script>
import Dropdown_info from './Dropdown_info.vue';
import Modal from './Modal.vue';
export default {
    components: { Dropdown_info, Modal },
    data(){
        return{
            base_url:'../../assets/emoticons', 
            img_name: this.$.vnode.key.name,
            counter: this.$.vnode.key.data.length,
            isHover: null,
        }
    },
    props:['post_id'],

    methods:{
        changeGlobalEmotCounter(){
            const emoticon_obj = this.$store.getters.getPostData[this.post_id].reactions;
            for(const emoticon of emoticon_obj){
                if(emoticon[0] == this.img_name){
                    emoticon[1] = this.counter;
                    this.$store.commit('printData', this.post_id)
                    break;
                }
            }
        },

        emoticonIsClicked(){   
            this.counter ++;
            this.changeGlobalEmotCounter();
        },

        getFirstFrame(path){
        },   
        
        getImg(){
            const url = this.base_url + '/' + this.img_name;
            var image = (require.context('../../assets/emoticons', false, /\.gif$/));
        
            if(this.img_name && this.img_name.includes('.gif')){
                // взять первый фрейм
                this.getFirstFrame(url);
                return image('./' + this.img_name);
            }
            
        },
        
    
    }

}
</script>

<style lang="scss" scoped>

    .main_emot_container{
        display: flex;
        justify-content: center;
        position: relative;
    }

    .emoticon_container{
        display: flex;
        flex-direction: row;
        align-items: center;
        border: 1px solid var(--bg_button_color);
        border-radius: 5px;
        padding: 2px 2px;
        margin-right: 10px;
        cursor: pointer;
        background-color: var(--bg_button_color);
        color: var(--text_color_secondary);

        &:hover, &.selected{
            background-color: var(--bg_button_active_color);
            color: #ffff;
        }

        img{
            width: 25px;
            height: 25px;
        }

        span{
            margin: 0 4px;
            font-weight: 300;
            font-size: 12px;
        }
    }

    .reactors_container {
        position: absolute; 
        bottom: 20px;
    }

</style>