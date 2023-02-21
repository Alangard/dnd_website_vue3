<template>
    <modal @close_modal='emit("close_modal")'>
        <template #modal_header>
            <div class="reactions_more_container">
                <reaction-more 
                    :reactions_obj_by_post_id="reactions_obj_by_post_id"
                    :post_id="props.post_id"
                    @renderReactorsList="renderReactorsList">
                </reaction-more>
            </div>

            <search-bar 
                v-if='chosen_section == "all_emoticons"'
                :post_id='props.post_id'
                @searchStart='(bool_trigger) => searchStart = bool_trigger'>
            </search-bar>
            
        </template>

        <template #modal_body>
            <div class="reactors_container" :class="{mobile: store.getters.getIsMobileState == true}">
                <reactors-list 
                    v-if="chosen_section != 'all_emoticons' && chosen_section != null"
                    :reactors_list_prop='reactors_list'
                    :chosen_section="chosen_section">
                </reactors-list>
            </div>

            <scroll-spy 
                v-if="chosen_section == 'all_emoticons' && searchStart"
                :isMobile='store.getters.getIsMobileState'
                :post_id="props.post_id">
            </scroll-spy>

        </template>
    </modal>

</template>

<script setup>
import { ref, defineProps, defineEmits,  defineAsyncComponent } from 'vue';
import { useStore } from 'vuex'

const Modal = defineAsyncComponent(() => import('@/components/Templates_components/Modal.vue'));
const ReactionMore = defineAsyncComponent(() => import('./InModal/ReactionMore.vue'));
const ReactorsList = defineAsyncComponent(() => import('./InModal/ReactorsList.vue'));
const SearchBar = defineAsyncComponent(() => import('./InModal/SearchBar.vue'));
const ScrollSpy = defineAsyncComponent(() => import('./InModal/ReactionScrollSpy.vue'));

const props = defineProps(['post_id']);
const emit = defineEmits(['close_modal']);
const store = useStore();

// Create a request to the server to get reaction data for a specific post, using post_id
// Modelling a request by retrieving data from VueX
let reactions_obj_by_post_id = ref(store.state.reactions[props.post_id]);
let reactors_list = ref(null); //sorted list of reactors
let searchStart = ref(null);
let chosen_section = ref(null); // str variable for type of section for ReactionMore component 

function renderReactorsList(element_id){
    // The method takes event.target.tagName (id) and generates a list of users who reacted with the selected emoticon 
    // or a list of all reacted users (class='total_reactions_count_btn').

    let reactors_info = [];
    switch(element_id){
        case 'total_reactions_count': 

            reactions_obj_by_post_id.value.forEach(element => {reactors_info.push(...element.users_data);});
            reactors_list.value = reactors_info.sort((a, b) => new Date(b.reaction_date) - new Date(a.reaction_date));
            
            chosen_section.value = 'total_reactions_count';
            return reactors_list;

        case 'all_emoticons':
            chosen_section.value = 'all_emoticons';
            break;
        
        default:
            reactors_list.value = reactions_obj_by_post_id.value.find(element => element.emoticon_id == element_id).users_data;
            chosen_section.value = element_id;
            return reactors_list;
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