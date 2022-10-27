<template>

    <div class="modal fade" :id="this.modal_id">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">

                    <div class="decorate_container">
                        
                        <reaction-more 
                            :post_id='this.post_id' 
                            :sortedReaction="this.sortedReaction"
                            @reactIsClicked="getCheckedEmoticonData">
                        </reaction-more>
                        
                    </div>
                    
                    <svg data-bs-dismiss="modal" aria-label="Close" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>

                </div>

                <div class="modal-body">
                    <div class="reactors_container" :class="{mobile: this.$store.getters.getIsMobileState == true}">
                        <reactors-list 
                            v-if="all_emoticon_checked == false"
                            :reactors_list='this.reactors_list'>
                        </reactors-list>
                    </div>
                

                    <search-bar v-if='all_emoticon_checked == true'></search-bar>

                    <accordion-emoticon-sections v-if='all_emoticon_checked == true'></accordion-emoticon-sections>
                    
                </div>
            </div>
        </div>
    </div>

</template>

    Добавить возможность добавления эмотикона в избранное нажатием на значок или удержанием (для мобильного)
    Добавить значок информации о человеке, оставившем эмотикон

<script>
import AccordionEmoticonSections from './AccordionEmoticonSections.vue'
import ReactionMore from './ReactionMore.vue'
import ReactorsList from './ReactorsList.vue'
import SearchBar from './SearchBar.vue'
export default {
  components: {ReactionMore, ReactorsList, SearchBar, AccordionEmoticonSections},
    props:['post_id','sortedReaction'],
    data(){
        return{
            modal_id: 'ReactionsModal' + this.post_id,
            reactors_list: null,
            all_emoticon_checked: null,
        }
    },
    methods:{

        getCheckedEmoticonData(emoticon_info){
            if(emoticon_info.includes('totalReaction') || emoticon_info.includes('all_emoticons')){
                const btn_type = emoticon_info.split('_p_')[0];

                switch(btn_type){
                    case 'totalReaction':
                        const reactors_list = [];
                        for(const reaction of this.sortedReaction){
                            reactors_list.push(...reaction.data);
                        }
                        this.sortReactorsbyDate(reactors_list);
                        this.reactors_list = reactors_list;
                        this.all_emoticon_checked = false;
                        break;

                    case 'all_emoticons':
                        this.all_emoticon_checked = true;
                        break;
                }
            }

            else{
                const emoticon_id = emoticon_info.split('_p_')[0];
                for(const reaction of this.sortedReaction){
                    if(reaction.name.split('.')[0] == emoticon_id){
                        const reactors_list = reaction.data;
                        this.sortReactorsbyDate(reactors_list);
                        this.reactors_list = reactors_list;
                        this.all_emoticon_checked = false;
                        break;
                    }
                }
            }

        },

        sortReactorsbyDate(reactors_list){
            reactors_list.sort((a,b) => {return new Date(b.date) - new Date(a.date);});
            return reactors_list;
        },
    }
}
</script>

<style lang="scss" scoped>
    .modal-content{
        background-color:var(--bg_color);
        max-height: 80%;
        filter: drop-shadow(0 0 10px var(--drop_shadow_color));
    }
    .modal-header{
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        border-bottom:  none;
        padding: 0 5px 10px 10px;
        color: var(--text_color_primary);

        svg[data-bs-dismiss="modal"]{
            position: absolute;
            right: 10px;
        }

        .decorate_container{
            display: flex;
            flex-direction: row;
            align-items: center;
            max-height: 53px;
            width: 97%;
            margin-top: 30px;
        }

        svg{
            height: 25px;
            width: 25px;
            margin-top: 3px;
            cursor: pointer;
            stroke: var(--text_color_secondary);
            &:hover{
                stroke: var(--bg_button_active_color);
            }
        }
    }
    .modal-body{
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        padding: 0 16px 16px 10px;

        .reactors_container{
            height: auto;
            max-height: 350px;
            padding: 0 5px 0 0;
            overflow-y: hidden;

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
        }
    
        .all_emoticons_container{
            display: flex;
            flex-direction: row;
            justify-content: flex-start;
            flex-wrap: wrap;
            border-radius: 5px;
            width: 100%;
            background-color: var(--bg_button_color);
            font-weight: 400;
        }
        
    }
</style>