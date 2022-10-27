<template>
    <div class="wrapper">

        <div class="btn-left" @click="scroll_left">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 18l-6-6 6-6"/>
            </svg>
        </div>
        
        <div ref='emot_container' class="emot_container" @mousewheel="scrollX">

            <div class="emoticon_element all_emoticons_btn" @click="isClicked">
                <input type="radio" name="emoticonGroup" :value="`all_emoticons_p_${this.post_id}`" :id="`all_emoticons_p_${this.post_id}`">
                <label :for="`all_emoticons_p_${this.post_id}`">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                    </svg>
                </label>
            </div>

            <div class="emoticon_element" @click="isClicked">
                <input type="radio" name="emoticonGroup" :value="`totalReaction_p_${this.post_id}`" :id="`totalReaction_p_${this.post_id}`">
                <label :for="`totalReaction_p_${this.post_id}`">
                    <span>Reacted {{totalReactionsCount()}}</span>
                </label>
            </div>

            <div class="emoticon_element" 
                v-for='reaction in sortedReaction' :key='reaction' 
                @click="isClicked">

                    <input type="radio" name="emoticonGroup" :value="`${reaction.name.split(/[.]/)[0]}_p_${this.post_id}`" :id="`${reaction.name.split(/[.]/)[0]}_p_${this.post_id}`">
                    <label :for="`${reaction.name.split(/[.]/)[0]}_p_${this.post_id}`">
                        <img :src="getImg(reaction.name)" alt="">
                        <span>{{reaction.data.length}}</span>
                    </label>
            </div>
        </div>

        <div class="btn_right" @click="scroll_right">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 18l6-6-6-6"/>
            </svg>
        </div>
        
    </div>
</template>

<script>
export default {
    props:['post_id','sortedReaction'],
    data(){return{}},
    methods:{
        totalReactions(){
            var sum = 0;
            for(const element of this.sortedReaction){sum += element.data.length;}
            return sum;
        },

        getImg(img_name){
            const url = this.base_url + '/' + img_name;
            var image = (require.context('../../assets/emoticons', false, /\.gif$/));
        
            if(img_name && img_name.includes('.gif')){
                // взять первый фрейм
                return image('./' + img_name);
            }
        },

        isClicked(event){
            if (event.target.tagName == 'INPUT'){
                const element_id = event.target.id;
                this.$emit('reactIsClicked', element_id);
            }  
        },

        totalReactionsCount(){
            var sum = 0;
            for(const element of this.sortedReaction){sum += element.data.length;}
            return sum;
        },

        scrollX(e) {
            this.$refs['emot_container'].scrollLeft += e.deltaY;
        },

        scroll_left() {
            this.$refs['emot_container'].scrollLeft -= 100;
        },

        scroll_right() {
            this.$refs['emot_container'].scrollLeft += 100;
        }
    }
}
</script>

<style lang="scss" scoped>
    .wrapper{
        position: relative;
        display: flex;
        flex-direction: row;
        width: 100%;

        .btn-left{
            position: absolute;
            display: flex;
            z-index: 2;
            align-items: center;
            justify-self: flex-start;
            height: 100%;
            width: 30px;
            border-top-left-radius: 5px;
            border-bottom-left-radius: 5px;
            background-image: linear-gradient(to right, var(--bg_button_color), transparent);
            cursor: pointer;

            svg{stroke: var(--text_color_secondary);}

            &:hover{background-image: linear-gradient(to right, var(--gradien_to_transparent_color), transparent);}

        }

        .btn_right{
            position: absolute;
            right: 0px;
            display: flex;
            z-index: 2;
            align-items: center;
            justify-content: flex-end;
            height: 100%;
            width: 45px;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            background-image: linear-gradient(to left, var(--bg_button_color), transparent);
            cursor: pointer;

            svg{stroke: var(--text_color_secondary);}

            &:hover{background-image: linear-gradient(to left, var(--gradien_to_transparent_color), transparent);}
        }
    }


    .emot_container{
        display: flex;
        z-index: 1;
        flex-direction: row;
        justify-content: flex-start;
        padding: 0 30px;
        border-radius: 5px;
        width: 100%;
        background-color: var(--bg_button_color);
        font-weight: 400;
        scroll-behavior: smooth;

        overflow-x: scroll;
        -ms-overflow-style: none; /* for Internet Explorer, Edge */
        scrollbar-width: none; /* for Firefox */
        
        &::-webkit-scrollbar {
            display: none; /* for Chrome, Safari, and Opera */
        }

        .emoticon_element{

            svg{stroke: var(--text_color_secondary);}
            input{display: none;}

            input:checked + label{
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
                align-items: center;
                color: var(--text_color_secondary);
                padding: 8px 12px 5px 12px;
                height: 100%;
                border-bottom: 3px solid var(--bg_button_color);
                cursor: pointer;
                white-space: nowrap;

                img{
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    object-fit: contain;
                    margin-right: 10px;
                }

                &:hover > img {transform: scale(1.2);}
                &:hover > svg {stroke: var(--bg_button_active_color);}
                &:hover {color: var(--bg_button_active_color);}
            }
        }
    }
</style>