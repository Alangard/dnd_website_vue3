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
            :class="{mobile: this.$store.getters.getIsMobileState == true}">

            <img :src="emot.url" alt="" 
                v-for="emot in FilterEmotByName" :key="emot.id"
            
            >
            
            <span v-if='this.FilterEmotByName.length == 0'>Nothing was found</span>
        </div>

    </div>
</template>

<script>
export default {
    props:[],
    data(){
        return{
           search_query: '',
           emoticons_list: [],
        }
    },

    computed:{
         FilterEmotByName(){
            return this.emoticons_list.filter(emoticon => emoticon.title.indexOf(this.search_query) !== -1)
         }
    },

    beforeMount(){
        fetch('https://jsonplaceholder.typicode.com/photos')
        .then(response => response.json())
        .then(json => {this.emoticons_list = json;})
    },
}
</script>

<style lang="scss" scoped>
.main_container{
    .searchbar{
        display: flex;
        align-items: center;
        width: 100%;
        
        input{
            width: 100%;
            height: 100%;
            border: 2px solid var(--bg_button_color);
            border-radius: 5px;
            padding: 0 25px;
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
        padding: 10px 0;
        border-radius: 5px;
        height: 250px;
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

        span{
            width: 100%;
            text-align: center;
        }
              
        img{
            height: 45px;
            width: 45px;
            margin: 3px 5px;
            border-radius: 50%;
            object-fit: contain;
            background-color: #ffff;
            cursor: pointer;

            &:hover{
                transform: scale(1.2);
            }
        }
    }

}




</style>