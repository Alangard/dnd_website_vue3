<template>

    <div class="main-container" 
        :class="{'light-theme': this.$store.getters.getTheme =='light', 'dark-theme': this.$store.getters.getTheme =='dark'}">

        <button 
            class="router-link"
            @click="$router.push({ name: 'shop' })"
            >К магазину
        </button>



        <select v-model="theme"
            name="theme_selector" 
            id="theme_selector">
                <option value="dark">Dark</option>
                <option value="light">Light</option>
        </select>

    </div>
</template>


<script>
export default {
    data(){
        return{
            theme: '',
        }
    },

    mounted(){
        this.theme = localStorage.theme;
    },
    
    watch: {
        theme(newTheme) {
            this.$store.commit('changeTheme', newTheme); 
        }
    },

}
</script>

<style lang="scss" scoped>

    *{
        font-family: 'lato', sans-serif;
        font-size: 17px;
        font-weight: 300;
        color: #290000;
    }

    .main-container{
        position: fixed;
        display: flex;
        flex-direction: row;
        z-index: 99999;
        align-items: center;
        width: 100%;
        height: 50px;
        background-color: var(--bg_block_color);
        box-shadow: var(--box_shadow);

        .router-link{
            text-decoration: none;
            &:visited{color: #290000;}
            &:hover{color: #dd2727}
        }
    }



</style>




