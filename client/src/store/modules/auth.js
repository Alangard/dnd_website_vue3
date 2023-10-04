
import interceptorsInstance, {authHeader, accessToken} from '@/api/main'
import axios from 'axios'

const user = JSON.parse(localStorage.getItem('user'));
const BASE_URL = axios.defaults.baseURL + 'auth/'

const initialState = user
  ? { status: { loggedIn: true }, user, usersList: null}
  : { status: { loggedIn: false }, user: null, usersList: null};

export const auth = {
  namespaced: true,
  state: initialState,
  actions: {
    async login({ commit }, user_data){
      try{
        const response = await interceptorsInstance.post(BASE_URL + `jwt/create/`, user_data)
       
        if(response.data.access){
          localStorage.setItem('user', JSON.stringify(response.data))
        }
        return  response.data
      }
      catch(error){console.log(error)}
    },

    async logout({ commit }) {
      try{
        localStorage.removeItem('user');
        commit('logout');
      }
      catch(error){console.log(error)}

    },

    async register({ commit }, user_data) {
      try{
        const response = interceptorsInstance.post(BASE_URL + 'user/register/', user_data)
        return response.data
      }
      catch(error){console.log(error)}

    },

    async user_activate({commit}, confirmation_code){
      try{
        const response = interceptorsInstance.post(BASE_URL + 'user/activation/', {confirmation_code: confirmation_code })
        return response.data
      }
      catch(error){console.log(error)}
    },

    async send_confirmation_code({commit}, email){
      try{
        const response = interceptorsInstance.post(BASE_URL + 'user/send_confirmation_code/', {email: email})
        return response.data
      }
      catch(error){console.log(error)}
    },

    async reset_password_confirm({commit}, user_data){
      try{
        const response = interceptorsInstance.post(BASE_URL + 'user/reset_password_confirm/', user_data)
        return response.data
      }
      catch(error){console.log(error)}
    },

    async dontRemember({commit}, ){
      localStorage.removeItem('user');
    },

    async refreshToken({commit}, ){
      try{
        const refresh = JSON.parse(localStorage.getItem('user')).refresh
        const user_data = JSON.parse(localStorage.getItem('user')).user_data

        const response = await interceptorsInstance.post(BASE_URL + 'jwt/refresh/', {refresh: refresh})

        localStorage.setItem('user', JSON.stringify({'user_data': user_data, 'access': response.data.access, 'refresh': refresh}))
        return response.data;
      }
      catch(error){console.log(error)}
    },

    async verifyToken({commit}, ){
      try{
        const response = await interceptorsInstance.post('auth/jwt/verify/', accessToken())
        return response.data
      }
      catch(error){console.log(error)}
    },

    async getMyData({commit}, user_id){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `user/${user_id}/`)
        console.log(response.data)
        commit('setUserData', response.data)
        return response.data
      } 
      catch(error){console.log(error)}
    }
  },
  mutations: {
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },

    setUser(state, user){
      state.user = user
    },
    
    setAccessToken(state, access_token){
      state.user.access = access_token
      const user = state?.user
      localStorage.setItem('user', JSON.stringify(user))
    },

    setUserData(state, user_data){
      state.user.user_data = user_data
      let user = JSON.parse(localStorage.getItem('user'))
      user['user_data'] = user_data

      localStorage.setItem('user', JSON.stringify(user))
    }
  },
  getters: {
    loginState(state){
      return state.status.loggedIn;
    },
    
    getAccessToken(state){
      if(state.user && state.user.access){
        return state.user.access
      }
      return null 
    },

    getRefreshToken(state){
      if(state?.user?.refresh){
        return state.user.refresh
      }
      return null 
    },

    getUser(state){
      if(state?.user){
        return state.user
      }
      return null 
    },

    getUserData(state){
      if(state.user && state.user.user_data){
        return state.user.user_data
      }
      return null 
    },
  }
};