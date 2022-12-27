<template>
    <div class="main_emot_container"
        :class="{reacted: this.short_post_data_reactions.reacted}">
        <div class="img_container" v-for='reaction in this.short_post_data_reactions.top3_reactions__list' :key='reaction'>
            <img :src='reaction.emoticon_url' alt="">
        </div>
        
        <svg v-if='this.short_post_data_reactions.top3_reactions__list.length == 0' xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.508 13.941c-1.513 1.195-3.174 1.931-5.507 1.931-2.335 0-3.996-.736-5.509-1.931l-.492.493c1.127 1.72 3.2 3.566 6.001 3.566 2.8 0 4.872-1.846 5.999-3.566l-.492-.493zm.492-3.939l-.755.506s-.503-.948-1.746-.948c-1.207 0-1.745.948-1.745.948l-.754-.506c.281-.748 1.205-2.002 2.499-2.002 1.295 0 2.218 1.254 2.501 2.002zm-7 0l-.755.506s-.503-.948-1.746-.948c-1.207 0-1.745.948-1.745.948l-.754-.506c.281-.748 1.205-2.002 2.499-2.002 1.295 0 2.218 1.254 2.501 2.002z"/>
        </svg>

        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
    </div>
</template>

<script>

export default {
    props:['short_post_data_reactions'],
    data(){return{}},
    methods:{}
}
</script>

<style lang="scss" scoped>

    .main_emot_container{
        display: flex;
        flex-direction: row;
        align-items: center;
        position: relative;
        border: 1px solid var(--bg_button_color);
        border-radius: 5px;
        padding: 2px 2px;
        margin-right: 10px;
        cursor: pointer;
        background-color: var(--bg_button_color);
        color: var(--text_color_secondary);

        &:hover, &.selected, &:hover > svg{
            background-color: var(--bg_button_active_color);
            color: #ffff;
            stroke: #ffff;
            fill: #ffff;
        }

        &.reacted{
            border: 1px solid var(--bg_button_active_color);

            svg{
                stroke: var(--bg_button_active_color);
                fill: var(--bg_button_active_color);
            }

            &:hover > svg{
                stroke: #ffff;
                fill: #ffff;

            }  
        }

        svg{
            stroke: var(--text_color_secondary);
            fill: var(--text_color_secondary);
            height: 20px;
            width: 20px;
            margin: 0 3px;
        }

        .img_container img{
            width: 25px;
            height: 25px;
            border-radius: 50%;
            object-fit: contain;
            margin-right: 4px;
        }

        span{
            margin: 0 4px;
            font-weight: 300;
            font-size: 12px;
        }  
        
    }
</style>