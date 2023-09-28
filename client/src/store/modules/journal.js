// import JournalService from '@/api/JournalAPI/index'
// import AuthService from '@/api/AuthAPI/auth'
import axios from 'axios';
import interceptorsInstance, {authHeader} from '@/api/main'


// const user = JSON.parse(localStorage.getItem('user'));
const BASE_URL = axios.defaults.baseURL;

const initialState = { haveInitialPosts: false, PostsList: [], TagsList: [], postDetail: {}};

export const journal = {
  namespaced: true,
  state: initialState,
  actions: {

    async conusmerSettings({rootGetters, commit}, data){ 
        const socket = data.data.socket
        const access_token = rootGetters['auth/getAccessToken']
        const refresh_token = rootGetters['auth/getRefreshToken']
        const action = data.action
        const payload = data.data.payload

        if (access_token != null) {
            try{
                const response = await axios.post(BASE_URL + 'auth/jwt/verify/', {token: access_token})
    
                let message = {
                  request_id: Date.now(),
                  action: action,
                  token: access_token,
                  payload: payload
                }
                socket.send(JSON.stringify(message))
            }
            catch(error){
                try{
                    const response_new_access = await axios.post(BASE_URL + 'auth/jwt/refresh/', {refresh: refresh_token})
                    commit('auth/setAccessToken', response_new_access.data.access, { root: true })
                    let message = {
                    request_id: Date.now(),
                    action: action,
                    token: response_new_access.data.access,
                    payload: payload
                    }
                    socket.send(JSON.stringify(message))
                }
                catch(error){
                    console.log(error)
                }
            }
        }
        else{
          console.log('You are logout')
        }
    },

    async conusmerSettingsWithPerm({rootGetters, commit}, data){
      const socket = data.data.socket
      const access_token = rootGetters['auth/getAccessToken']
      const refresh_token = rootGetters['auth/getRefreshToken']
      const user_data = rootGetters['auth/getUserData']
      const action = data.action
      const payload = data.data.payload
      const only_for_owner = data.only_for_owner

      const isOwner = () => {
          if(only_for_owner){
              return user_data?.username == data.payload.author.username
          }
          return user_data?.username != data.payload.author.username      
      } 
      
      if (access_token != null) {
          if(isOwner){
              try{
                  const response = await axios.post(BASE_URL + 'auth/jwt/verify/', {token: access_token})
                  console.log(response)

                  let message = {
                      request_id: Date.now(),
                      action: action,
                      token: access_token,
                      payload: payload
                  }
                  socket.send(JSON.stringify(message))
              }
              catch(error){
                  try{
                      console.log('1')
                      const response_new_access = await axios.post(BASE_URL + 'auth/jwt/refresh/', {refresh: refresh_token})
                      commit('auth/setAccessToken', response_new_access.data.access, { root: true })
                      let message = {
                          request_id: Date.now(),
                          action: action,
                          token: response_new_access.data.access,
                          payload: payload
                      }
                      socket.send(JSON.stringify(message))
                  }
                  catch(error){console.log(error)}
              }
          }else{console.log('You are dont have a permission')}
      }else{console.log('You are logout')}
    },

    async createPost({commit},post_data){
      try{
        const response = await interceptorsInstance.post(BASE_URL + 'post/', post_data, { headers:  {'Authorization': authHeader()['Authorization'], 'Content-Type': 'multipart/form-data' } })
        // commit('addPostInStore', response.data)
        return response.data
      }  
      catch(error){console.log(error)}
    },
    
    async deletePost({commit}, post_id){
      try{
        const response = await interceptorsInstance.delete(BASE_URL + `post/${post_id}/`, { headers: authHeader() })
        commit('deletePostInStore', response.data)
        return response
      }
      catch(error){console.log(error)}
    },

    async partialUpdatePost({commit}, post_data){
      try{
        const post_id = post_data.get("id")
        post_data.delete("id");

        const response = await interceptorsInstance.patch(BASE_URL + `post/${post_id}/`, post_data, { headers:  {'Authorization': authHeader()['Authorization'], 'Content-Type': 'multipart/form-data' } })
        // commit('updatePostInStore', response.data)

        return response.data
      }
      catch(error){console.log(error)}
    },

    async getPostList({commit}, {paginate_url, request_type}){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `post/${paginate_url}`, { headers: authHeader() })
        if(request_type == 'initial'){commit('setPostListInStore', response.data)}
        else if(request_type == 'load_more'){commit('addPostInStore', response.data)}
        return response.data
      }
      catch(error){console.log(error)}
    },
  
    async getPostDetail({commit}, data){
      console.log('dispatch', data)
      try{
        const response = await interceptorsInstance.get(BASE_URL + `post/${data['post_id']}/?editable=${data['editable']}`, { headers: authHeader() })
        commit('setPostDetailInStore', response.data)
        return response.data
      }
      catch(error){console.log(error)}
    },

    async getTagsList({commit}){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `tag/`)
        commit('setTagsInStore', response.data)
        return response.data
      }
      catch(error){console.log(error)}
    },

    // get_posts({ commit }, url) {
    //   return JournalService.get_posts(url).then(
    //     posts_data => {
    //       commit('gettingPostSuccess', posts_data.data);
    //       return Promise.resolve(posts_data.data);
    //     },
    //     error => {
    //       commit('gettingPostFailure');
    //       return Promise.reject(error);
    //     }
    //   );
    // },

    // getReactions({ commit }, data){
    //   return JournalService.get_reactions(data.post_id).then(
    //     reactions_data => {
    //       commit('gettingReactionsSuccess', reactions_data.data);
    //       return Promise.resolve(reactions_data.data);
    //     },
    //     error => {
    //       return Promise.reject(error);
    //     }
    //   );
    // },

    async set_reaction({ commit, dispatch}, data){
      //Если пользователь оставлял реакцию
      if(data.user_reaction.reacted){

        //Если выбранная реакция соответствует оставленной
        if(data.reaction_type == data.user_reaction.reaction_type){
          try{     
            const response = await interceptorsInstance.delete(BASE_URL + `post_reactions/${data.id}/`, { headers: authHeader()})
            commit('removeReaction', {'post_id': data.post_id,'reaction_type': data.reaction_type, 'set_reaction_in': data.set_reaction_in})
            return response.data
          }
          catch(error){console.log(error)}
        }
        else{
          try{ 
            const response = await interceptorsInstance.patch(BASE_URL + `post_reactions/${data.id}/`,{'reaction_type': data.reaction_type},  { headers: authHeader()}) 
            commit('changeReaction', {'post_id': data.post_id,'reaction_type': data.reaction_type, 'id': response.data.post, 'set_reaction_in': data.set_reaction_in})
            return response.data
          }
          catch(error){console.log(error)}          
        }
      }

      else{
        try{
          const response = await interceptorsInstance.post(BASE_URL + `post_reactions/`, {'reaction_type': data.reaction_type, 'post_id': data.post_id}, {headers: authHeader()})
          commit('setReaction', {'post_id': data.post_id, 'reaction_type': data.reaction_type, 'id': response.data.id, 'set_reaction_in': data.set_reaction_in})
          return response.data

        }
        catch(error){console.log(error)}
      }
    },

    async get_reaction({commit, }, filter_params_str){
      try{  
        const response = await interceptorsInstance.get(BASE_URL + `post_reactions/${filter_params_str}`,)
        return response.data
      }
      catch(error){console.log(error)}
    }
  },


  mutations: {

    setTagsInStore(state, data){
      state.TagsList = data
    },

    setPostListInStore(state, data){
      state.PostsList = data
    },

    addPostInStore(state, data){
      state.PostsList.count = data.count
      state.PostsList.results.unshift(...data.results)
    },

    deletePostInStore(state, data){
      const post_id = data.id
      const post_index = state.PostsList.results.findIndex(post => post.id == post_id)
      if (post_index > -1) {
        state.PostsList.results.splice(post_index, 1);
      }
      else{
        console.log('Post has not been found', post_index)
      }
    },

    updatePostInStore(state, data){
      const post_id = data.id
      const post_index = state.PostsList.results.findIndex(post => post.id == post_id)
      if (post_index > -1) {
        state.PostsList.results.splice(post_index, 1, data);
      }
      else{
        console.log('Post has not been found', post_index)
      }
    },

    setReaction(state, chosen_data){

      const post_obj = chosen_data.set_reaction_in == 'post_list' 
        ? state.PostsList.results.find(post => post.id == chosen_data.post_id) 
        : state.postDetail

      switch (chosen_data.reaction_type){
        case 'like':
          post_obj.post_reactions.num_likes += 1
          break
        case 'dislike':
          post_obj.post_reactions.num_dislikes += 1
          break
      }
      post_obj.post_reactions.total_reactions += 1
      
      post_obj.user_reaction = {'reacted': true, 'reaction_type': chosen_data.reaction_type, 'id': chosen_data.id}
    },

    removeReaction(state, chosen_data){
      const post_obj = chosen_data.set_reaction_in == 'post_list' 
        ? state.PostsList.results.find(post => post.id == chosen_data.post_id) 
        : state.postDetail

      switch (chosen_data.reaction_type){
        case 'like':
          post_obj.post_reactions.num_likes -= 1
          break
        case 'dislike':
          post_obj.post_reactions.num_dislikes -= 1
          break
      }
      post_obj.post_reactions.total_reactions -= 1
      post_obj.user_reaction = {'reacted': false, 'reaction_type': ''}


    },

    changeReaction(state, chosen_data){
      const post_obj = chosen_data.set_reaction_in == 'post_list' 
        ? state.PostsList.results.find(post => post.id == chosen_data.post_id) 
        : state.postDetail

      switch(chosen_data.reaction_type){
        case 'like':
          post_obj.post_reactions.num_likes += 1
          post_obj.post_reactions.num_dislikes -= 1
          break
        case 'dislike':
          post_obj.post_reactions.num_dislikes += 1
          post_obj.post_reactions.num_likes -= 1
          break  
      }
      post_obj.user_reaction.reaction_type = chosen_data.reaction_type
    },

    setPostDetailInStore(state, data){
      state.postDetail = data
    }
  },

  getters: {
    getPostsData(state){return state.PostsList},

    getPosts(state){return state.PostsList.results},

    getPostDetail(state){return state.postDetail},

    getTagsList(state){return state.TagsList},    
  }

};