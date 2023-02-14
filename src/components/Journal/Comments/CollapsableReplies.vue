<template>
    <collapsable :item_id="this.item_id" :visible=false @changeCollapseState="(state) => this.collapseOpen = state">
            <template #collapse_header>
                <div class="collapse_header_container" v-if="this.collapseOpen == false">
                    Show more replies
                    <svg class="collapse_icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                </div>

                <div class="collapse_header_container" v-else>
                    Hide replies
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#290000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                </div>
            </template>
                <template #collapse_body>
                    <slot name='collapse_body'></slot>
                </template>
    
    </collapsable>


            
</template>

<script>
import Collapsable from '@/components/Templates_components/Collapse/Collapsable.vue';
export default {
    props:['item_id', 'replies_count'],
    components: { Collapsable },
    data(){return{collapseOpen: false,}},
}
</script>

<style lang="scss" scoped>
    .collapse_header_container{
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-left: 38px;
        font:var(--font_header);
        font-size: 13px;
        color: var(--bg_button_active_color);
        cursor: pointer;

        svg{
            width: 15px;
            height: 15px;
            stroke-width: 3px;
            stroke: var(--bg_button_active_color);
        }
    }
</style>