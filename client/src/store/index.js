import { createStore } from 'vuex'
import axios from 'axios';


export default createStore({
  state(){
    return{
      isMobile: null,
      modals_info: {id: 0, state: false, modal_type: '', action_pressed: false},

      postData: {},
      postList: [],
      usersList: [],
      TagsList: [],
      currUserData: {},


      postListStyle: 'list',

      page_size: 7,
      page: 1,
      baseUrl: `/api/v1/`
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

    getUsersList(state){
      return state.usersList
    },

    getTagsList(state){
      return state.TagsList;
    },

    getCurrUserData(state){
      return state.currUserData;
    },

    getCurrUserResponseStatus(state){
      return state.currUserData.status;
    },

    getCurrUserError(state){
      return state.currUserData.error_info;
    },

    getJWT(state){
      return {'access_token': state.currUserData.access_token, 
              'refresh_token': state.currUserData.refresh_token, 
            }
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

    setUsersData(state, fetching_data){
      state.usersList = fetching_data
    },

    spliceUserList(state, index){
      state.usersList.splice(index, 1)
    },

    pushUserList(state, element){
      state.usersList.push(element)
    },

    setTagsData(state, fetching_data){
      state.TagsList = fetching_data;
    },

    changePostListStyle(state, post_syle){
      state.postListStyle = post_syle;
    },

    setCurrUserData(state, user_data){
      state.currUserData = user_data
    },

    setJWT(state, jwt_data){
      state.currUserData['access_token']= jwt_data.access
      state.currUserData['refresh_token']= jwt_data.access
    },

    setCurrUserError(state, err){
      state.currUserData['error_info'] = err
      state.currUserData['status'] = err.response.status
    },

    setCurrUserResponseStatus(state, status){
      state.currUserData['status'] = status
    },

    setToDefaultCurrUserData(state){
      for(const [key, value] of Object.entries(state.currUserData)){
        state.currUserData[key] = ''
      }
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
    async fetchPostData({ commit, dispatch, getters }, payload={'url': '', 'setVariable': false}) {

      let url = getters.getBaseUrl

      if (payload.url){url += payload.url}

      try{
        await axios.get(url).then(response => {
          payload.setVariable && payload.setVariable == true ? commit('setPostsList', response.data.results) : commit('extendPostsList', response.data.results)
          commit('setPostData', {'countPosts': response.data.count, 'nextPageUrl': response.data.next, 'previousPageUrl': response.data.previous})
        })
      }
      catch(err){console.log(err)}

    },

    async fetchUsersData({ commit, dispatch, getters }, payload={'url': ''}) {

      let url = getters.getBaseUrl

      if (payload.url){url += payload.url}

      try{
        await axios.get(url).then(response => {
          commit('setUsersData', response.data)
        })
      }
      catch(err){console.log(err)}

    },

    async fetchTagsData({ commit, dispatch, getters }, payload={'url': ''}) {

      let url = getters.getBaseUrl

      if (payload.url){url += payload.url}

      try{
        await axios.get(url).then(response => {
          commit('setTagsData', response.data)
        })
      }
      catch(err){console.log(err)}


    },

    async auth_login({ commit, dispatch, getters, }, payload={'url': '', 'userdata': {}}) {

      let url = getters.getBaseUrl

      if (payload.url){url += payload.url}

      try{
        await axios.post(url, payload.userdata)
        .then(response => {
          commit('setCurrUserResponseStatus',  response.status)
          commit('setJWT', response.data);
          localStorage.setItem('access_token', response.data.access);
          localStorage.setItem('refresh_token', response.data.refresh);
        })
        .catch((err) => {
          commit('setCurrUserError',  err)
          commit('setJWT', {'access': '', 'refresh': ''});
        })
      }
      catch(err){}
    },

    async create_account({ commit, dispatch, getters }, payload={'url': '', 'userdata':{}}){
      let url = getters.getBaseUrl

      if (payload.url){url += payload.url}

      try{
        await axios.post(url, payload.userdata)
        .then(response => {
          commit('setCurrUserData', response.data)
          commit('setCurrUserResponseStatus',  response.status)
        })
        .catch((err)=>{
          commit('setCurrUserError',  err)
        })
      }
      catch(err){console.log(err)}
    }

  },

  modules: {}
})
