<template>
   <div class="share_container">

       <div class="test" v-if="this.$store.getters.getIsMobileState == false"></div>

        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="18" cy="5" r="3"></circle>
            <circle cx="6" cy="12" r="3"></circle>
            <circle cx="18" cy="19" r="3"></circle>
            <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
            <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
        </svg>

    </div> 
</template>

<script>
export default {
}
</script>

<style lang="scss" scoped>
.share_container{
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    height: 31px;
    width: 45px;
    padding: 0 2px 0 0;
    border: 1px solid var(--bg_button_color);
    border-radius: 5px;
    cursor: pointer;
    background-color: var(--bg_button_color);

    & svg{
        stroke: var(--text_color_secondary);
        width: 20px;
        height: 20px; 
    }

    &:hover{
        background-color: var(--bg_button_active_color);
        color: #ffff;
    }

    &:hover > svg{
        stroke: #ffff;;
    }
}
</style>