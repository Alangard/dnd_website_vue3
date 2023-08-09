import JournalService from '@/api/JournalAPI/index'
import AuthService from '@/api/AuthAPI/auth'
import axios from 'axios';


const user = JSON.parse(localStorage.getItem('user'));

const initialState = user
  ? { status: { loggedIn: true }, user, haveInitialPosts: false, PostsList: [], Reactions: [], Comments: [], Comment: {}}
  : { status: { loggedIn: false }, user: null, haveInitialPosts: false, PostsList: [], Reactions: [], Comments: [], Comment: {} };

export const journal = {
  namespaced: true,
  state: initialState,
  actions: {

    async conusmerSettings({dispatch, rootGetters}, data){
      const socket = data.data.socket
      const access_token = rootGetters['auth/getAccessToken']
      const action = data.action
      const payload = data.data.payload

      if (access_token != null) {
        dispatch('auth/verifyToken', '', {root:true}).then(response => {
            
            let message = {
              request_id: Date.now(),
              action: action,
              token: access_token,
              payload: payload
            }
            socket.send(JSON.stringify(message))
        }).catch(error => {
            dispatch('auth/refreshToken','', {root:true}).then(response => {

              let message = {
                request_id: Date.now(),
                action: action,
                token: access_token,
                payload: payload
              }
              socket.send(JSON.stringify(message))
            })
          })
      }
      else{
        console.log('You are logout')
      }
    },

    async conusmerSettingsWithPerm({dispatch, rootGetters}, data){
      const socket = data.data.socket
      const access_token = rootGetters['auth/getAccessToken']
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
          dispatch('auth/verifyToken', '', {root:true}).then(response => {
            let message = {
              request_id: Date.now(),
              action: action,
              token: access_token,
              payload: payload
            }

            socket.send(JSON.stringify(message))

          }).catch(error => {
            dispatch('auth/refreshToken','', {root:true}).then(response => {
              let message = {
                request_id: Date.now(),
                action: action,
                token: access_token,
                payload: payload
              }
    
              socket.send(JSON.stringify(message))
            })
          })
        }
        else{
          console.log('You are dont have permission')
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

    getPostsComments({commit}, post_id){
      JournalService.get_posts_comments(post_id).then(
        response => {
          commit('gettingCommentsSuccess', response.data);
          return Promise.resolve(response.data);},
        error => {return Promise.reject(error);}
      )
    },

    async createComment({dispatch}, data){
      dispatch('conusmerSettings', {action: 'create_comment', data: data})
    },
    
    async createCommentReply({dispatch}, data){
      dispatch('conusmerSettings', {action: 'create_reply_comment', data: data})
    },
    
    async deleteComment({dispatch}, data){
      dispatch('conusmerSettingsWithPerm', {action: 'delete_comment', data: data, only_for_owner: true})
    },
    
    async partialUpdateComment({dispatch}, data){
      dispatch('conusmerSettingsWithPerm', {action: 'partial_update_comment', data: data, only_for_owner: true})
    },
    
    async banComment({dispatch}, data){
      dispatch('conusmerSettingsWithPerm', {action: 'ban_comment', data: data, only_for_owner: false})
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

    gettingCommentsSuccess(state, comments_data){
      state.Comments = comments_data;
    },

    gettingCommentSuccess(state, comment_data){
      state.Comment = comment_data;
    },

    addCommentInStore(state, data){
      state.Comments.comments.unshift(data)
    },

    addCommentReplyInStore(state, newReply) {
      // Обходим список комментариев с помощью массива методов
      function traverseComments(comments) {
        for (let comment of comments) {
          if (comment.id === newReply.parent) {
            // Найден комментарий, к которому добавляем новый ответ
            if (!comment.replies) {
              // Если у комментария еще нет списка ответов, создаем его
              comment.replies = [];
            }
            comment.replies.unshift(newReply);
            return;
          } 
          else if (comment.replies) {
            // Рекурсивно ищем комментарий с нужным id в ответах
            traverseComments(comment.replies);
          }
        }
      }
    
      traverseComments(state.Comments.comments);
    },

    // deleteCommentWithRepliesInStore(state, comment_obj){
    //   const commentId = comment_obj.id;

    //   // Обходим список комментариев с помощью массива методов
    //   function traverseComments(comments) {
    //     for (let i = 0; i < comments.length; i++) {
    //       if (comments[i].id === commentId) {
    //         // Найден комментарий, удаляем его из списка
    //         comments.splice(i, 1);
    //         return;
    //       } 
    //       else if (comments[i].replies) {
    //         // Рекурсивно ищем комментарий с нужным id в ответах
    //         traverseComments(comments[i].replies);
    //       }
    //     }
    //   }
    
    //   traverseComments(state.Comments.comments);
    // },
    

    deleteCommentInStore(state, comment_data){
      const commentId = comment_data.id;

      // Обходим список комментариев с помощью массива методов
      function traverseComments(comments) {
        for (let i = 0; i < comments.length; i++) {
          if (comments[i].id === commentId) {
            if(comments[i]?.replies?.length > 0){
              // Найденный комментарий с ответами, изменяем его статус
              comments[i].status = comment_data.status
              comments[i].text = comment_data.text
            }
            else{
              // Найденный комментарий без ответов, удаляем его из списка
              comments.splice(i, 1);
              state.Comments.num_comments -= 1
            }
            return;
          } 
          else if (comments[i].replies) {
            // Рекурсивно ищем комментарий с нужным id в ответах
            traverseComments(comments[i].replies);
          }
        }
      }
    
      traverseComments(state.Comments.comments);
    },

    updateCommentInStore(state, comment_data){
      // Обходим список комментариев с помощью массива методов
      function traverseComments(comments) {
        for (let comment of comments) {
          if (comment.id === comment_data.id) {
            // Найден комментарий, который обновляем
            comment.text = comment_data.text;
            comment.updated_datetime = comment_data.updated_datetime;
            comment.status = comment_data.status;
            return;
          } 
          else if (comment.replies) {
            // Рекурсивно ищем комментарий с нужным id в ответах
            traverseComments(comment.replies);
          }
        }
      }
    
      traverseComments(state.Comments.comments);
    },

    addPostInStore(state, data){
      state.PostsList.results.unshift(data);
    }
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

    getComments(state){
      return state.Comments
    },


    
  }

};