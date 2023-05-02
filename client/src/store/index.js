
import { createStore } from 'vuex'


export default createStore({
  state(){
    return{
      isMobile: null,
      modals_info: {id: 0, state: false, modal_type: '', action_pressed: false},
      postData: null,
      TagsData: null,
    }
    
  },
  getters: {

    getModalActionStatus(state){
      return state.modals_info.action_pressed;
    },

    //returns true/false
    getIsMobileState (state) {
        return state.isMobile;
    },

    //returns string 'light'/'dark' 
    getTheme (state){
        return state.theme;
    },

    getPostData(state){
      return state.postData;
    },

    getPostsList(state){
      return state.postData.results;
    },

    getTagsData(state){
      return state.TagsData;
    }
},

  mutations: {
    // Set posts_data /////////////////////////////////////////////////////////// there are we are use this code with a API
    
    setPostData(state, fetching_data){
      state.postData = fetching_data;
    },

    setPostsList(state, fetching_data){
      state.postData.results = fetching_data;
    },

    setTagsList(state, fetching_data){
      state.TagsData = fetching_data;
    },


    ////////////////////////////////////////////////////////////

    //Change the state of page size (true - mobile, false - desktop)
    changeIsMobileFlag(state, flag_pos) {
        state.isMobile = flag_pos;
    },

    //Change the website theme and add a value 'theme' to the local storage
    changeTheme(state, chose_theme){
      if(chose_theme == 'dark' || chose_theme == 'light'){
        state.theme = chose_theme;
        localStorage.theme = chose_theme;
      }
    },

},
  actions: {},
  modules: {}
})
