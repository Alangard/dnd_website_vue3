import axios from 'axios';


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

    async getInitialComments({state}, post_id){
        try{
            const response = await axios.get(BASE_URL + `post/${post_id}/comments/`)
            state.Comments = response.data
        }
        catch(error){
            console.log(error)
        }
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
        return state.Comments
    },
  
    getReplyIsPressed(state){
        return state.replyIsPressed
    }
  }

}