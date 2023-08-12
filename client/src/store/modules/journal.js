import JournalService from '@/api/JournalAPI/index'
import AuthService from '@/api/AuthAPI/auth'
import axios from 'axios';


const user = JSON.parse(localStorage.getItem('user'));

const initialState = user
  ? { status: { loggedIn: true }, user, haveInitialPosts: false, PostsList: [], Reactions: [], Comments: [], Comment: {}, replyIsPressed: ''}
  : { status: { loggedIn: false }, user: null, haveInitialPosts: false, PostsList: [], Reactions: [], Comments: [], Comment: {}, replyIsPressed: ''};

export const journal = {
  namespaced: true,
  state: initialState,
  actions: {

    async conusmerSettings({state}, data){
      const socket = data.data.socket
      const access_token = state?.user?.access
      const refresh_token = state?.user?.refresh
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
                  const response = await axios.post(BASE_URL + 'auth/jwt/refresh/', {refresh: refresh_token})

                  let message = {
                  request_id: Date.now(),
                  action: action,
                  token: response.data.access,
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

    async conusmerSettingsWithPerm({dispatch, rootGetters}, data){
      const socket = data.data.socket
      const access_token = state?.user?.access
      const refresh_token = state?.user?.refresh
      const user_data = state?.user?.user_data
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
              const response = await axios.post(BASE_URL + 'auth/jwt/refresh/', {refresh: refresh_token})

              let message = {
                  request_id: Date.now(),
                  action: action,
                  token: response.data.access,
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
          console.log('You are dont have a permission')
        }
      }  
      else{
          console.log('You are logout')    
      }
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

    gettingPostSuccess(state, posts_data){
      state.haveInitialPosts = true;
      state.PostsList = posts_data
    },

    gettingPostFailure(state){
      state.haveInitialPosts = false;
    },

    setPostsList(state, posts_list){
      state.PostsList = posts_list
    },

    setAccessToken(state, token){
      state.user.access = token
    },

    updatePostsList(state, post_data){
      state.PostsList.unshift(post_data)
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

    addPostInStore(state, data){
      state.PostsList.results.unshift(data);
    },
  },

  getters: {
    loginState(state){
      return state.status.loggedIn
    },

    getAccessToken(state){
      if(state.user && state.user.access){
        return state.user.access
      } 
    },

    getPostsData(state){
      return state.PostsList
    },

    getPosts(state){
      return state.PostsList.results
    },

    getReactions(state){
      return state.Reactions.results
    },

    getPostById(state, post_id){
      return state.PostsList.results.filter(post => post.id == 2)
    },



    
  }

};