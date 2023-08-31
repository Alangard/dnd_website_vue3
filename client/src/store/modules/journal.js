import JournalService from '@/api/JournalAPI/index'
import AuthService from '@/api/AuthAPI/auth'
import axios from 'axios';

import interceptorsInstance, {authHeader} from '@/api/main'


const user = JSON.parse(localStorage.getItem('user'));
const BASE_URL = axios.defaults.baseURL;

const initialState = { haveInitialPosts: false, PostsList: [], TagsList: []};

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
        return response
      }  
      catch(error){console.log(error)}
    },
    
    async deletePost({commit}, post_id){
      try{
        const response = await interceptorsInstance.delete(BASE_URL + `post/${post_id}/`, { headers: authHeader() })
        commit('deletePostInStore', response.data)
        return response
      }
      catch(error){}
    },

    async partialUpdatePost({commit}, post_data){
      try{
        const post_id = post_data['id']
        delete post_data['id']
        const response = await interceptorsInstance.patch(BASE_URL + `post/${post_id}/`, post_data, { headers: authHeader() })
        commit('updatePostInStore', response.data)
        return response
      }
      catch(error){console.log(error)}
    },

    async getPostList({commit}, paginate_url){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `post/${paginate_url}`, { headers: authHeader() })
        commit('setPostListInStore', response.data)
        return response
      }
      catch(error){console.log(error)}
    },
  
    async getPostDetail({}, post_id){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `post/${post_id}`, { headers: authHeader() })
        return response.data
      }
      catch(error){console.log(error)}
    },

    async getTagsList({commit}){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `tag/`)
        console.log(response)
        commit('setTagsInStore', response.data)

        return response
      }
      catch(error){console.log(error)}
    },

    get_posts({ commit }, url) {
      return JournalService.get_posts(url).then(
        posts_data => {
          commit('gettingPostSuccess', posts_data.data);
          return Promise.resolve(posts_data.data);
        },
        error => {
          commit('gettingPostFailure');
          return Promise.reject(error);
        }
      );
    },

    getReactions({ commit }, data){
      return JournalService.get_reactions(data.post_id).then(
        reactions_data => {
          commit('gettingReactionsSuccess', reactions_data.data);
          return Promise.resolve(reactions_data.data);
        },
        error => {
          return Promise.reject(error);
        }
      );
    },

    set_reaction({ commit, dispatch}, data){
      //Если пользователь оставлял реакцию
      if(data.user_reaction.reacted){

        //Если выбранная реакция соответствует оставленной
        if(data.reaction_type == data.user_reaction.reaction_type){
          
          commit('removeReaction', {'post_id': data.post_id,'reaction_type': data.reaction_type})

          JournalService.remove_reaction(data.post_id).then(
            response => {return Promise.resolve(response.data);},
            error => {return Promise.reject(error);}
          );
        }
        else{
          commit('changeReaction', {'post_id': data.post_id,'reaction_type': data.reaction_type})

          JournalService.change_reaction({'post_id': data.post_id,'reaction_type': data.reaction_type}).then(
            response => {return Promise.resolve(response.data);},
            error => {return Promise.reject(error);}
          );            
        }
      }

      else{
        commit('setReaction', {'post_id': data.post_id,'reaction_type': data.reaction_type})

        JournalService.add_reaction({'post_id': data.post_id,'reaction_type': data.reaction_type}).then(
          response => {return Promise.resolve(response.data);},
          error => {return Promise.reject(error);}
        );
      }
    },
  },


  mutations: {

    setPostListInStore(state, data){
      state.PostsList = data
    },

    addPostInStore(state, data){
      state.PostsList.results.unshift(data)
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

    setTagsInStore(state, data){
      state.TagsList = data
    },

    gettingReactionsSuccess(state, reactions_data){
      state.Reactions = reactions_data;
    },

    setReaction(state, chosen_data){
      const post_obj =  state.PostsList.results.find(post => post.id == chosen_data.post_id)
      switch (chosen_data.reaction_type){
        case 'like':
          post_obj.post_reactions.num_likes += 1
          break
        case 'dislike':
          post_obj.post_reactions.num_dislikes += 1
          break
      }
      post_obj.post_reactions.total_reactions += 1
      
      post_obj.user_reaction = {'reacted': true, 'reaction_type': chosen_data.reaction_type}
    },

    removeReaction(state, chosen_data){
      const post_obj =  state.PostsList.results.find(post => post.id == chosen_data.post_id)
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
      const post_obj =  state.PostsList.results.find(post => post.id == chosen_data.post_id)
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
  },

  getters: {

    getPostsData(state){
      return state.PostsList
    },

    getPosts(state){
      return state.PostsList.results
    },

    getPostById(state, post_id){
      return state.PostsList.results.filter(post => post.id == 2)
    },

    getTagsList(state){
      return state.TagsList
    },



    
  }

};