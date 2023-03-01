<template>
  <TopNav/>
    
  <div class="main_content_wrapper"
    :class="{'navBarHide': $route.meta.hideNavbar,
             'light-theme': store.state.theme =='light', 
             'dark-theme': store.state.theme =='dark'
            }">

    <div class="content">
      <router-view></router-view>
    </div>

    <Alert class="delete_alert_modal"
        v-if="store.state.modals_info.modal_type == 'delete_alert'"
        :alert_object="{'header': 'Delete comment', 'message': 'Are you sure you want to delete this comment?', 
                        'action':'Delete', 'crtiticality': 'error'}"
        @close_alert='closeModal()'
        @doAction='doActionModal()'>
    </Alert>

    <swipe-bottom-sheet class="swipe_bottom_sheet"
        v-if="store.state.modals_info.modal_type == 'bottom_sheet'"
        @close_bottomSheet="closeModal()">
    </swipe-bottom-sheet>

  </div>



</template>

<script setup>
import TopNav from "./components/TopNav.vue"
import Alert from '@/components/Templates_components/Alert.vue';
import SwipeBottomSheet from '@/components/Templates_components/BottomSheet/SwipeBottomSheet.vue';
import { useStore } from 'vuex'
import { onMounted, onUnmounted, ref} from 'vue'

const store = useStore();
let windowWidth = ref(null);
const mobile_limit = 750; // 750px is the limit value. If the width is larger, it means that you are viewing from desktop


///////////////////////////////////
function closeModal(){
  store.state.modals_info.id = 0;
  store.state.modals_info.state = false;
  store.state.modals_info.modal_type = '';
}

function doActionModal(){
  store.state.modals_info.action_pressed = true;
  store.state.modals_info.state = false;
}

//////////////////////////////////

window.addEventListener('resize', checkScreen);
checkScreen();
// Making a request to retrieve user data and save it into vuex store

// Func to get the screen width and change the global store variable 'isMobile'
function checkScreen(){
  windowWidth = window.innerWidth;
  // console.log(windowWidth)
  if (windowWidth <= mobile_limit){
      store.commit('changeIsMobileFlag', true);
      return;
  }
  else{
    store.commit('changeIsMobileFlag', false);
    return; 
  }

}

onMounted(() => {
  if (localStorage.theme) {
    store.commit('changeTheme', localStorage.theme);
  }
  else{
    storecommit('changeTheme', 'light'); 
    localStorage.theme = 'light';
  }
})

onUnmounted(() => window.removeEventListener('resize',  checkScreen));
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
  --font_header: 700 normal 14px/1.3em 'Lato', sans-serif;
  --font_basic: 300 normal 14px 'Lato', sans-serif;
  --drop_shadow_color: #535C70;
  --gradien_to_transparent_color:#ababaf;
  --active_section_color: #bbbbc1;
  --error_color: #d42c2f;




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
  --font_header: 700 normal 14px/1.3em 'Lato', sans-serif;
  --font_basic: 300 normal 14px 'Lato', sans-serif;
  --drop_shadow_color: #5B58F7;
  --gradien_to_transparent_color:#4c4b4b;
  --active_section_color: #222121;
  --error_color: #d42c2f;

}

  .main_content_wrapper{
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 70px;
    height: auto;
    background-color: var(--bg_block_color);

    .content{
      width: 90%;
      max-width: 640px;
      height: 100vh;
    }

    &.navBarHide{
      padding: 0;
    }
  }
</style>
