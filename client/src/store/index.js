import { createStore } from 'vuex'
import axios from 'axios';


export default createStore({
  state(){
    return{
      isMobile: null,
      modals_info: {id: 0, state: false, modal_type: '', action_pressed: false},

      postData: {},
      postList: [],


      postListStyle: 'list',

      page_size: 7,
      page: 1,
      baseUrl: `/api/v1/posts/`
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

    getPostListStyle(state){
      return state.postListStyle;
    },

    getBaseUrl(state){
      return state.baseUrl;
    },

    getPage(state){
      return state.page;
    },

    getPageSize(state){
      return state.page_size;
    },

    getPostData(state){
      return state.postData;
    },

    getNextPostPageUrl(state){
      return state.postData.nextPageUrl;
    },

    getPostsList(state){
      return state.postList;
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
      state.postList = fetching_data;
    },

    extendPostsList(state, array_data){
      state.postList.push(...array_data)
    },


    setTagsList(state, fetching_data){
      state.TagsData = fetching_data;
    },

    changePostListStyle(state, post_syle){
      state.postListStyle = post_syle;
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
  actions: {
    async fetchPostData({ commit, dispatch, getters }, payload={}) {

      let url = getters.getBaseUrl + `?page=${getters.getPage}&page_size=${getters.getPageSize}`

      if (payload.url){url = payload.url}
      else if(payload.parametrs){url += payload.parametrs;}

      await axios.get(url).then(response => {
        payload.parametrs ? commit('setPostsList', response.data.results) : commit('extendPostsList', response.data.results)
        commit('setPostData', {'countPosts': response.data.count, 'nextPageUrl': response.data.next, 'previousPageUrl': response.data.previous})
      })
    }
  },

  modules: {}
})
