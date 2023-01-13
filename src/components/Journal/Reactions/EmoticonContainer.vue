<template>
    <div class="main_emot_container"
        :class="{reacted: this.short_post_data_reactions.reacted}">
        <div class="img_container" v-for='reaction in this.short_post_data_reactions.top3_reactions__list' :key='reaction'>
            <img :src='reaction.emoticon_url' alt="">
        </div>

        <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" viewBox="0 0 1000 1000" enable-background="new 0 0 1000 1000" xml:space="preserve">
            <path d="M576.3,877.3c-30.5,7.2-62.1,10.9-93.7,10.9c-223.3,0-405-181.7-405-405s181.7-405,405-405c223.3,0,405,181.7,405,405c0,32.8-3.9,65.5-11.7,97.1c-4.5,18.1,6.6,36.4,24.7,40.8c18.1,4.7,36.4-6.5,40.8-24.7c9.1-36.9,13.7-75,13.7-113.3c0-260.6-212-472.5-472.5-472.5C222,10.6,10,222.6,10,483.1c0,260.6,212,472.6,472.5,472.6c36.9,0,73.7-4.3,109.3-12.7c18.1-4.3,29.4-22.4,25-40.6C612.6,884.2,594.4,872.9,576.3,877.3z"/>
            <path d="M250.2,594.7c-14.7,11.5-17.3,32.7-5.8,47.4c58,74.2,145.2,116.7,239.3,116.7c95.1,0,182.9-43.3,240.9-118.7c11.4-14.8,8.6-35.9-6.2-47.3s-35.9-8.6-47.3,6.2c-45.1,58.7-113.4,92.3-187.4,92.3c-73.2,0-141-33.1-186.2-90.8C286.1,585.8,264.8,583.3,250.2,594.7z"/>
            <path d="M382.4,435.9v-67.5c0-28-22.6-50.6-50.6-50.6s-50.6,22.6-50.6,50.6v67.5c0,28,22.6,50.6,50.6,50.6S382.4,463.8,382.4,435.9z"/><path d="M686.2,435.9v-67.5c0-28-22.7-50.6-50.6-50.6S585,340.4,585,368.3v67.5c0,28,22.7,50.6,50.6,50.6S686.2,463.8,686.2,435.9z"/>
            <path d="M956.2,786.9H855V685.6c0-18.7-15.1-33.8-33.8-33.8s-33.8,15.1-33.8,33.8v101.3H686.2c-18.7,0-33.8,15.1-33.8,33.8s15.1,33.8,33.8,33.8h101.3v101.3c0,18.7,15.1,33.8,33.8,33.8s33.8-15.1,33.8-33.8V854.4h101.3c18.7,0,33.8-15.1,33.8-33.8S974.9,786.9,956.2,786.9z"/>
        </svg>
        
        <!-- <svg v-if='this.short_post_data_reactions.top3_reactions__list.length == 0' xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.508 13.941c-1.513 1.195-3.174 1.931-5.507 1.931-2.335 0-3.996-.736-5.509-1.931l-.492.493c1.127 1.72 3.2 3.566 6.001 3.566 2.8 0 4.872-1.846 5.999-3.566l-.492-.493zm.492-3.939l-.755.506s-.503-.948-1.746-.948c-1.207 0-1.745.948-1.745.948l-.754-.506c.281-.748 1.205-2.002 2.499-2.002 1.295 0 2.218 1.254 2.501 2.002zm-7 0l-.755.506s-.503-.948-1.746-.948c-1.207 0-1.745.948-1.745.948l-.754-.506c.281-.748 1.205-2.002 2.499-2.002 1.295 0 2.218 1.254 2.501 2.002z"/>
        </svg>

        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg> -->
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