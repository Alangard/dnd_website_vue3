import axios from 'axios';
import interceptorsInstance, {authHeader} from '@/api/main'


const BASE_URL = axios.defaults.baseURL;
const initialState = { Comments: [], replyIsPressed: ''}

export const comments = {
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

    async getCommentsList({commit}, {paginate_url, request_type}){
        try{
            const response = await interceptorsInstance.get(BASE_URL + `post_comments/${paginate_url}`, { headers: authHeader()})
            if(request_type == 'initial'){commit('setCommentsInStore', response.data)}
            
            return response.data
        }
        catch(error){console.log(error)}
    },

    async set_reaction({ commit, dispatch}, data){
        //Если пользователь оставлял реакцию
        if(data.user_reaction.reacted){
  
          //Если выбранная реакция соответствует оставленной
          if(data.reaction_type == data.user_reaction.reaction_type){
            try{     
              const response = await interceptorsInstance.delete(BASE_URL + `comment_reactions/${data.id}/`, { headers: authHeader()})
              commit('removeReaction', {'comment_id': data.comment_id, 'reaction_type': data.reaction_type})
              return response.data
            }
            catch(error){console.log(error)}
          }
          else{
            try{ 
              const response = await interceptorsInstance.patch(BASE_URL + `comment_reactions/${data.id}/`,{'reaction_type': data.reaction_type},  { headers: authHeader()}) 
              commit('changeReaction', {'comment_id': data.comment_id,'reaction_type': data.reaction_type, 'id': response.data.post})
              return response.data
            }
            catch(error){console.log(error)}          
          }
        }
  
        else{
          try{
            const response = await interceptorsInstance.post(BASE_URL + `comment_reactions/`, {'reaction_type': data.reaction_type, 'comment_id': data.comment_id}, {headers: authHeader()})
            commit('setReaction', {'comment_id': data.comment_id, 'reaction_type': data.reaction_type, 'id': response.data.id})
            return response.data
  
          }
          catch(error){console.log(error)}
        }
    },

    async createComment({commit}, comment_data){
      const response = await interceptorsInstance.post(BASE_URL + `post_comments/`, comment_data, { headers: authHeader()})
      commit('addCommentInStore', response.data)
      return response.data
    },

    async createReplyComment({commit}, comment_data){
      
      const response = await interceptorsInstance.post(BASE_URL + `post_comments/`, comment_data, { headers: authHeader()})
      commit('addCommentReplyInStore', response.data)
      return response.data
    },

    async deleteComment({commit}, comment_id){
      const response = await interceptorsInstance.delete(BASE_URL + `post_comments/${comment_id}/`, { headers: authHeader()})
      commit('deleteCommentInStore', {'response': response, 'comment_id': comment_id})
      return response.data
    },

    async partialUpdateComment({commit}, comment_data){
      const comment_id = comment_data.comment_id
      const response = await interceptorsInstance.patch(BASE_URL + `post_comments/${comment_id}/`, {'text': comment_data.new_comment_text}, { headers: authHeader()})
      commit('updateCommentInStore', {'response': response.data, 'comment_id': comment_id})
      return response.data
    }
  },

  
  mutations: {

    setCommentsInStore(state, data){
        state.Comments = data
    },

    setReaction(state, chosen_data){
        const comment_obj = state.Comments.results.comments.find(comment => comment.id == chosen_data.comment_id) 

        switch (chosen_data.reaction_type){
          case 'like':
            comment_obj.comment_reactions.num_likes += 1
            break
          case 'dislike':
            comment_obj.comment_reactions.num_dislikes += 1
            break
        }
        comment_obj.comment_reactions.total_reactions += 1
        
        comment_obj.user_reaction = {'reacted': true, 'reaction_type': chosen_data.reaction_type, 'id': chosen_data.id}
    },

    removeReaction(state, chosen_data){
    const comment_obj = state.Comments.results.comments.find(comment => comment.id == chosen_data.comment_id) 

    switch (chosen_data.reaction_type){
        case 'like':
        comment_obj.comment_reactions.num_likes -= 1
        break
        case 'dislike':
        comment_obj.comment_reactions.num_dislikes -= 1
        break
    }
    comment_obj.comment_reactions.total_reactions -= 1
    comment_obj.user_reaction = {'reacted': false, 'reaction_type': ''}


    },

    changeReaction(state, chosen_data){
    const comment_obj = state.Comments.results.comments.find(comment => comment.id == chosen_data.comment_id) 

    switch(chosen_data.reaction_type){
        case 'like':
        comment_obj.comment_reactions.num_likes += 1
        comment_obj.comment_reactions.num_dislikes -= 1
        break
        case 'dislike':
        comment_obj.comment_reactions.num_dislikes += 1
        comment_obj.comment_reactions.num_likes -= 1
        break  
    }
    comment_obj.user_reaction.reaction_type = chosen_data.reaction_type
    },
  
    addCommentInStore(state, data){
        state.Comments.results.comments.unshift(data)
        state.Comments.results.num_comments += 1
        state.Comments.count += 1
    },
  
    addCommentReplyInStore(state, newReply) {
      state.Comments.results.num_comments += 1
      // Обходим список комментариев с помощью массива методов
      function traverseComments(comments) {
        for (let comment of comments) {
          if (comment.id === newReply.parent.id) {
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
  
      traverseComments(state.Comments.results.comments);
    },
   
    deleteCommentInStore(state, comment_data){
        const commentId = comment_data.comment_id;
        const response_status_code = comment_data.response.status

        // Обходим список комментариев с помощью массива методов
        function traverseComments(comments) {
            for (let i = 0; i < comments.length; i++) {
                if (comments[i].id === commentId) {
                    if(response_status_code == 200){
                      // Найденный комментарий с ответами, изменяем его статус
                      state.Comments.results.num_comments -= 1
                      state.Comments.count -= 1
                      comments[i].status = comment_data.response.data.changed_fields.status
                      comments[i].text = comment_data.response.data.changed_fields.text
                    }
                    else if(response_status_code == 204){
                      // Найденный комментарий без ответов, удаляем его из списка
                      comments.splice(i, 1);
                      state.Comments.results.num_comments -= 1
                    }
                    return;
                } 
                else if (comments[i].replies) {
                    // Рекурсивно ищем комментарий с нужным id в ответах
                    traverseComments(comments[i].replies);
                }
            }
        }
        
        traverseComments(state.Comments.results.comments);
    },
  
    updateCommentInStore(state, comment_data){
      const commentId = comment_data.comment_id;
      const response = comment_data.response

      // Обходим список комментариев с помощью массива методов
      function traverseComments(comments) {
        for (let comment of comments) {
          if (comment.id === commentId) {
            // Найден комментарий, который обновляем
            comment.text = response.text;
            comment.updated_datetime = response.updated_datetime;
            return;
          } 
          else if (comment.replies) {
            // Рекурсивно ищем комментарий с нужным id в ответах
            traverseComments(comment.replies);
          }
        }
      }
        
      traverseComments(state.Comments.results.comments);
    },

    openReply(state, comment_id){
        if(state.replyIsPressed == comment_id){
          console.log('Same reply', comment_id)
          state.replyIsPressed = ''
        }
        else if(comment_id == ''){
          console.log('Blank')
          state.replyIsPressed = ''
        }
        else{
          console.log('New reply', comment_id)
          state.replyIsPressed = comment_id
        }
        
    }
  },

  getters: {
    getComments(state){
        return state.Comments.results
    },
  
    getReplyIsPressed(state){
        return state.replyIsPressed
    }
  }

}