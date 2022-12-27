<template>
    <modal @close_modal='this.$emit("close_modal")'>
        <template #modal_header>
            <div class="reactions_more_container">
                <reaction-more 
                    :reactions_obj_by_post_id="this.reactions_obj_by_post_id"
                    @renderReactorsList="renderReactorsList">
                </reaction-more>
            </div>

            <!-- <search-bar 
                v-if='all_emoticon_checked == true'
                :post_id='this.post_id'
                @searchStart='(bool_trigger) => this.searchStart = bool_trigger'>
            </search-bar> -->
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

            <!-- <scroll-spy 
                v-if='this.all_emoticon_checked && this.searchStart'
                :isMobile='this.$store.getters.getIsMobileState'
                :post_id="this.post_id">
            </scroll-spy> -->

        </template>
    </modal>

</template>

<script>
import Modal from '@/components/Templates_components/Modal.vue';
import ReactionMore from './InModal/ReactionMore.vue';
import ReactorsList from './InModal/ReactorsList.vue';
import SearchBar from './InModal/SearchBar.vue';
import ScrollSpy from './InModal/ReactionScrollSpy.vue';

export default {
    components:{Modal, ReactionMore, ReactorsList, SearchBar, ScrollSpy},
    props:['post_id'],
    data(){
        return{
            reactions_obj_by_post_id: null,
            reactors_list: null,
            all_emoticon_checked: false,
            searchStart: null,
        }
    },

    beforeMount() {
        // Create a request to the server to get reaction data for a specific post, using post_id
        // Modelling a request by retrieving data from VueX

        this.reactions_obj_by_post_id = this.$store.state.reactions[this.post_id];
    },

    methods:{
        renderReactorsList(element_id){
            // The method takes event.target.tagName (id) and generates a list of users who reacted with the selected emoticon 
            // or a list of all reacted users (class='total_reactions_count_btn').

            switch(element_id){
                case 'total_reactions_count':
                    let reactors_info = [];

                    this.reactions_obj_by_post_id.forEach(element => {
                        reactors_info.push(...element.users_data);
                    });

                    this.reactors_list = reactors_info.sort((a, b) => new Date(b.reaction_date) - new Date(a.reaction_date));

                    return this.reactors_list;


                
                case 'all_emoticons':
                    this.all_emoticon_checked = true;
                    break
                
                default:
                    console.log(element_id)
                    this.reactors_list = this.reactions_obj_by_post_id.filter(element => element.emoticon_id == element_id);
                    return this.reactors_list;
            }
        }
    }
    //     renderReactorsList(emoticon_info){
    //         if(emoticon_info.includes('totalReaction') || emoticon_info.includes('all_emoticons')){
    //             this.btn_type = emoticon_info.split('_p_')[0];

    //             switch(this.btn_type){
    //                 case 'totalReaction':
    //                     const reactors = [];

    //                     for(const reaction of this.sortedReactions){
    //                         for(const reaction_data of reaction.data){
    //                             const data = {...reaction_data,...{'emot_id': reaction.reaction_id, 'emot_url': reaction.img_url}}
    //                             reactors.push(data);
    //                         }
    //                     }

    //                     this.reactors_list = this.sortReactorsbyDate(reactors);
    //                     this.all_emoticon_checked = false;
    //                     break;

    //                 case 'all_emoticons':
    //                     this.all_emoticon_checked = true;
    //                     break;
    //             }
    //         }

    //         else{
    //             this.btn_type = 'emot';
    //             const emoticon_id = emoticon_info.split('_p_')[0];
    //             const reactors = [];

    //             for(const reaction of this.sortedReactions){
    //                 if(reaction.reaction_id == emoticon_id){
    //                     for(const reaction_data of reaction.data){
    //                         const emot_data_obj = {'emot_id': reaction.reaction_id, 'emot_url': reaction.img_url, 
    //                                                 'username': reaction_data.username,'profile_img_url': reaction_data.profile_img_url, 
    //                                                 'date': reaction_data.date};
    //                         reactors.push(emot_data_obj);
    //                     }

    //                     this.reactors_list = this.sortReactorsbyDate(reactors);
    //                     this.all_emoticon_checked = false;
    //                     break;
    //                 }
    //             }
    //         }
    //     },

    //     // Can be deleted cuse users can not leave the reaction from past and object

    //     sortReactorsbyDate(reactors_list){
    //         reactors_list.sort((a,b) => {return new Date(b.date) - new Date(a.date);});
    //         return reactors_list;
    //     },
    // }
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
}

</style>