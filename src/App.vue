<template>
  <TopNav v-if="!$route.meta.hideNavbar"/>
    
  <div 
    class="content"
    :class="{'navBarHide': $route.meta.hideNavbar}">
    <router-view></router-view>
  </div>

</template>

<script>
import TopNav from "./components/TopNav.vue";

export default {
    data() {
      return {}
    },

    mounted() {
        if (localStorage.theme) {
            this.$store.commit('changeTheme', localStorage.theme);
        }
        else{
            this.$store.commit('changeTheme', 'light'); 
            localStorage.theme = 'light';
        }
    },

    watch: {
      '$store.state.theme': function() {
        localStorage.theme = this.$store.state.theme;
      }
    },

    components: { TopNav },
}
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;500;600;700&display=swap');

.light-theme{
  --bg_color: #f2f2f3;
  --bg_block_color: #ffff;
  --bg_block_hover_color: #535C70;
  --bg_button_color:#dedee4;
  --bg_button_active_color:#5B58F7;
  --button_text_color: #a7b4cf;
  --text_color_primary: #162952;
  --text_color_secondary: #535C70;
  --text_color_hover: #ffff;
  --block_border_color: #535C70;
  --box_shadow: 1px 1px 5px #535C70;
  --font_header: 700 normal 17px/1.3em 'Oswald', sans-serif;
  --drop_shadow_color: #535C70;
  --gradien_to_transparent_color:#ababaf;



}

.dark-theme{
  --bg_color: #141414;
  --bg_block_color: #1c1c1e;
  --bg_block_hover_color: #535C70;
  --bg_button_color:#2b2c31;
  --bg_button_active_color:#5B58F7;
  --button_text_color: #a7b4cf;
  --text_color_primary: #ffff;
  --text_color_secondary: #8f8f91;
  --text_color_hover: #ffff;
  --block_border_color: #535C70;
  --box_shadow: 2px 2px 10px black;
  --font_header: 700 normal 17px/1.3em 'Oswald', sans-serif;
  --drop_shadow_color: #5B58F7;
  --gradien_to_transparent_color:#4c4b4b;


}

  .content{
    padding-top: 50px;

    &.navBarHide{
      padding: 0;
    }
  }
</style>
