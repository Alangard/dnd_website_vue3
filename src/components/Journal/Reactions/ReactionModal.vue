<template>
    <modal @close_modal='this.$emit("close_modal")'>
        <template #modal_header>
            <div class="reactions_more_container">
                <reaction-more 
                    :reactions_obj_by_post_id="this.reactions_obj_by_post_id"
                    :post_id="this.post_id"
                    @renderReactorsList="renderReactorsList">
                </reaction-more>
            </div>

            <search-bar 
                v-if='this.chosen_section == "all_emoticons"'
                :post_id='this.post_id'
                @searchStart='(bool_trigger) => this.searchStart = bool_trigger'>
            </search-bar>
            
        </template>

        <template #modal_body>
            <div class="reactors_container" :class="{mobile: this.$store.getters.getIsMobileState == true}">
                <reactors-list 
                    v-if="this.chosen_section != 'all_emoticons' && this.chosen_section != null"
                    :reactors_list_prop='this.reactors_list'
                    :chosen_section="this.chosen_section">
                </reactors-list>
            </div>

            <scroll-spy 
                v-if="this.chosen_section == 'all_emoticons' && this.searchStart"
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

export default {
    components:{Modal, ReactionMore, ReactorsList, SearchBar, ScrollSpy},
    props:['post_id'],

    data(){
        return{
            reactions_obj_by_post_id: null,
            reactors_list: null, //sorted list of reactors
            searchStart: null,
            chosen_section: null, // str variable for type of section for ReactionMore component 
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

            let reactors_info = [];

            switch(element_id){
                case 'total_reactions_count': 

                    this.reactions_obj_by_post_id.forEach(element => {reactors_info.push(...element.users_data);});
                    this.reactors_list = reactors_info.sort((a, b) => new Date(b.reaction_date) - new Date(a.reaction_date));
                    
                    this.chosen_section = 'total_reactions_count';
                    return this.reactors_list;

                case 'all_emoticons':
                    this.chosen_section = 'all_emoticons';
                    break;
                
                default:
                    this.reactors_list = this.reactions_obj_by_post_id.find(element => element.emoticon_id == element_id).users_data;
                    this.chosen_section = element_id;
                    return this.reactors_list;
            }
            
        }
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


</style>