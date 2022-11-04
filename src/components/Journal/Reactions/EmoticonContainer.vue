<template>
    <div class="main_emot_container" @mouseover="this.isHover = true" @mouseleave="this.isHover = false">
        <div class="img_container" v-for='reaction in sortedReactions.slice(0,3)' :key='reaction'>
            <img :src='getImg(reaction.name)' alt="">
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
    </div>
</template>

<script>

export default {
    data(){
        return{
            isHover: null,
        }
    },
    props:['post_id', 'sortedReactions'],

    methods:{
        getFirstFrame(path){
        },   
        
        getImg(img_name){
            const url = '../../../assets/emoticons' + '/' + img_name;
            var image = (require.context('../../../assets/emoticons', false, /\.gif$/));
        
            if(img_name && img_name.includes('.gif')){
                // взять первый фрейм
                this.getFirstFrame(url);
                return image('./' + img_name);
            }
            
        },
        
    
    }

}
</script>

<style lang="scss" scoped>

    .main_emot_container{
        display: flex;
        flex-direction: row;
        align-items: center;
        position: relative;
        border: 1px solid var(--bg_button_color);
        border-radius: 5px;
        padding: 2px 2px;
        margin-right: 10px;
        cursor: pointer;
        background-color: var(--bg_button_color);
        color: var(--text_color_secondary);

        &:hover, &.selected, &:hover > svg{
            background-color: var(--bg_button_active_color);
            color: #ffff;
            stroke: #ffff;
        }

        svg{
            stroke: var(--text_color_secondary);
            height: 20px;
            width: 20px;
            margin: 0 3px;
        }

        .img_container img{
            width: 25px;
            height: 25px;
            border-radius: 50%;
            object-fit: contain;
            margin-right: 4px;
        }

        span{
            margin: 0 4px;
            font-weight: 300;
            font-size: 12px;
        }  
        
    }
</style>