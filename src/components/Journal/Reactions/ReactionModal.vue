<template>
    <modal @close_modal='this.$emit("close_modal")'>
        <template #modal_header>
            <div class="reactions_more_container">
                <reaction-more 
                    :post_id='this.post_id' 
                    :sortedReaction="this.sortedReactions"
                    @renderReactorsList="renderReactorsList">
                </reaction-more>
            </div>

            <search-bar 
                v-if='all_emoticon_checked == true'
                :post_id='this.post_id'
                @searchStart='(bool_trigger) => this.searchStart = bool_trigger'>
            </search-bar>
        </template>

        <template #modal_body>
            <div class="reactors_container" :class="{mobile: this.$store.getters.getIsMobileState == true}">
                <reactors-list 
                    v-if="all_emoticon_checked == false"
                    :reactors_list='this.reactors_list'
                    :post_id='this.post_id'
                    :btn_type="this.btn_type">
                </reactors-list>
            </div>


            <!-- <reaction-accordion v-if='all_emoticon_checked && this.searchStart'></reaction-accordion> -->
            <scroll-spy 
                v-if='this.all_emoticon_checked && this.searchStart'
                :isMobile='this.$store.getters.getIsMobileState'
                :post_id="this.post_id">
            </scroll-spy>

        </template>
    </modal>

</template>

<script>
import Modal from '@/components/Templates_components/Modal.vue';
import ReactionMore from './InModal/ReactionMore.vue';
import ReactorsList from './InModal/ReactorsList.vue';
import SearchBar from './InModal/SearchBar.vue';
import ScrollSpy from './InModal/ReactionScrollSpy.vue';
import ReactionAccordion from './InModal/ReactionAccordion.vue'

export default {
    components:{Modal, ReactionMore, ReactorsList, SearchBar, ReactionAccordion, ScrollSpy},
    props:['post_id','sortedReactions'],
    data(){
        return{
            reactors_list: null,
            all_emoticon_checked: null,
            searchStart: null,
            btn_type: null,
        }
    },
    methods:{
        renderReactorsList(emoticon_info){
            if(emoticon_info.includes('totalReaction') || emoticon_info.includes('all_emoticons')){
                this.btn_type = emoticon_info.split('_p_')[0];

                switch(this.btn_type){
                    case 'totalReaction':
                        const reactors = [];

                        for(const reaction of this.sortedReactions){
                            for(const reaction_data of reaction.data){
                                const data = {...reaction_data,...{'emot_id': reaction.reaction_id, 'emot_url': reaction.img_url}}
                                reactors.push(data);
                            }
                        }

                        this.reactors_list = this.sortReactorsbyDate(reactors);
                        this.all_emoticon_checked = false;
                        break;

                    case 'all_emoticons':
                        this.all_emoticon_checked = true;
                        break;
                }
            }

            else{
                this.btn_type = 'emot';
                const emoticon_id = emoticon_info.split('_p_')[0];
                const reactors = [];

                for(const reaction of this.sortedReactions){
                    if(reaction.reaction_id == emoticon_id){
                        for(const reaction_data of reaction.data){
                            const emot_data_obj = {'emot_id': reaction.reaction_id, 'emot_url': reaction.img_url, 
                                                    'username': reaction_data.username,'profile_img_url': reaction_data.profile_img_url, 
                                                    'date': reaction_data.date};
                            reactors.push(emot_data_obj);
                        }

                        this.reactors_list = this.sortReactorsbyDate(reactors);
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


.reactions_more_container{
    display: flex;
    flex-direction: row;
    align-items: center;
    max-height: 53px;
    width: 100%;
}

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

</style>