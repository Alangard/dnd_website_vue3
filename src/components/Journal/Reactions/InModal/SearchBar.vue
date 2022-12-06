<template>
    <div class="main_container">

        <div class="searchbar">

            <input type="text" v-model="search_query" placeholder="Search by emots..." />

            <div class="clear_btn" @click='this.search_query=""'>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>

            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>

        </div>

        <div class="search_results_container" 
            v-if='search_query.length > 0' 
            :class="{mobile: this.$store.getters.getIsMobileState == true, empty: this.FilterReactionsById.length == 0}">

            <in-favorites-btn
                v-for="reaction in FilterReactionsById" :key='reaction'
                :post_id="this.post_id"
                :isMobile="this.$store.getters.getIsMobileState">
            </in-favorites-btn>
        
        
            <span v-if='this.FilterReactionsById.length == 0'>Nothing was found</span>
        </div>
        

    </div>
</template>

<script>
import InFavoritesBtn from './InFavoritesBtn.vue';

export default {
  components: { InFavoritesBtn },
    props:['post_id'],
    data(){
        return{
           search_query: '',
           emoticons_list: this.$store.getters.getAllEmoticons,
        }
    },

    watch:{
        search_query(newValue, oldValue){
            if(newValue != ''){
                this.$emit('searchStart', false);
            }
            else{
                this.$emit('searchStart', true)
            }
        }
    },

    beforeMount(){
    //    this.getEmotsFromServer();
       this.$emit('searchStart', true);
    },

    methods:{
        // async getEmotsFromServer(){
        //     await fetch('https://jsonplaceholder.typicode.com/photos')
        //         .then(response => response.json())
        //         .then(json => {this.emoticons_list = json;})
        // }
    },

    computed:{
        FilterReactionsById(){
            return this.emoticons_list.filter(reaction => reaction.reaction_id.indexOf(this.search_query) !== -1)
        }
    },

    
}
</script>

<style lang="scss" scoped>
.main_container{
    width: 100%;
    margin-top: 10px;

    .searchbar{
        display: flex;
        align-items: center;
        
        input{
            width: 100%;
            border: 2px solid var(--bg_button_color);
            border-radius: 5px;
            padding: 5px 25px;
            background-color: var(--bg_button_color);
            color: var(--text_color_secondary);
            font-weight: 300;
            outline: none;
            caret-color: var(--text_color_secondary);

            &:hover{
                border-color: var(--bg_button_active_color);
            }
        }

        .clear_btn{
            position: absolute;
            height: 15px;
            width: 15px;
            right:35px;
            cursor: pointer;

            svg{stroke:var(--text_color_secondary);}
            &:hover > svg {stroke: var(--bg_button_active_color);} 
        }

        svg:last-child{
            position: absolute;
            height: 15px;
            width: 15px;
            left:15px;
            stroke:var(--text_color_secondary);
        }            
    }
    
    .search_results_container{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        margin-top: 10px;
        padding: 10px 0 10px 10px;
        border-radius: 5px;
        max-height: 300px;
        background-color: var(--bg_button_color);
        color: var(--text_color_secondary);
        overflow-y: hidden;
        scroll-behavior: smooth;

        &:hover, &:focus{
            overflow-y: scroll;
        }
        
        &::-webkit-scrollbar{width: 0.7vw;}

        &::-webkit-scrollbar-track{
            background-color: var(--bg_button_color);
            border-radius: 5px;
        }

        &::-webkit-scrollbar-thumb{
            background-color: var(--text_color_secondary);
            border-radius: 5px;
        }

        &.mobile{
            overflow-y: scroll;
        }

        &.empty{
            height: max-content;
            overflow-y: hidden;
        }

        span{
            width: 100%;
            text-align: center;
        }
              
        .img_container{
            padding: 5px 5px;
            border-radius: 5px;

            img{
                height: 40px;
                width: 40px;
                border-radius: 50%;
                object-fit: contain;
                background-color: #ffff;
                cursor: pointer;
            }

            &:hover{
                background-color: var(--active_section_color);
                transform: scale(1.1);
            }
        }
    }

}




</style>