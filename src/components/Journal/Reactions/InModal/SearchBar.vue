<template>
    <div class="main_container">

        <div class="searchbar">

            <input type="text" v-model="search_query" placeholder="Search by emots..." />

            <div class="clear_btn" @click='search_query=""'>
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
            :class="{mobile: store.getters.getIsMobileState == true, empty: filterReactionsById.length == 0}">

            <in-favorites-btn
                v-for="reaction in filterReactionsById" :key='reaction'
                :post_id="props.post_id"
                :isMobile="store.getters.getIsMobileState">
            </in-favorites-btn>
        
        
            <span v-if='filterReactionsById.length == 0'>Nothing was found</span>
        </div>
        

    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch, computed, defineAsyncComponent } from 'vue';
import { useStore } from 'vuex';

const InFavoritesBtn = defineAsyncComponent(() => import('./InFavoritesBtn.vue'));

const props = defineProps(['post_id']);
const emit = defineEmits(['searchStart'])
const store = useStore();

let search_query = ref('');

const getAllEmoticons = computed(() => store.state.emoticons.all);
const filterReactionsById = computed(() => getAllEmoticons.value.filter(emoticon => emoticon.emoticon_id.indexOf(search_query.value) !== -1));
        
watch(search_query, (newValue) => {
    if(newValue != ''){emit('searchStart', false);}
    else{emit('searchStart', true);}
});

//this.getEmotsFromServer();
emit('searchStart', true);
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
        
        &::-webkit-scrollbar{
            width: 0.7vw;
            max-width: 5px;
        }

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