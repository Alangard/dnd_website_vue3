import AuthService from '@/api/AuthAPI/auth';
import interceptorsInstance from '@/api/main'
import axios from 'axios';

const user = JSON.parse(localStorage.getItem('user'));
const BASE_URL = axios.defaults.baseURL;

const initialState = user
  ? { status: { loggedIn: true }, user}
  : { status: { loggedIn: false }, user: null};

export const auth = {
  namespaced: true,
  state: initialState,
  actions: {
    login({ commit }, user_data) {
      return AuthService.login(user_data).then(
        user_data => {
          commit('loginSuccess', user_data);
          return Promise.resolve(user_data);
        },
        error => {
          commit('loginFailure');
          return Promise.reject(error);
        }
      );
    },

    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },

    register({ commit }, user_data) {
      return AuthService.user_create(user_data).then(
        response => {
          commit('registerSuccess');
          return Promise.resolve(response.data);
        },
        error => {
          commit('registerFailure');
          return Promise.reject(error);
        }
      );
    },

    user_activate({commit}, confirmation_code){
      return AuthService.user_activate(confirmation_code).then(
        response => {return Promise.resolve(response.data)},
        error => {return Promise.reject(error)}
      )
    },

    send_confirmation_code({commit}, email){
      return AuthService.send_confirmation_code(email).then(
        response => {return Promise.resolve(response.data)},
        error => {return Promise.reject(error)}
      )
    },

    reset_password({commit}, user_email){
      return AuthService.reset_password(user_email).then(
        response => { return Promise.resolve(response.data)},
        error => { return Promise.reject(error) }
      )
    },

    reset_password_confirm({commit}, user_data){
      return AuthService.reset_password_confirmation(user_data).then(
        response => { return Promise.resolve(response.data)},
        error => { return Promise.reject(error) }
      )
    },

    dontRemember(){
      AuthService.logout();
    },

    checkExpirationToken({commit}, token){
      return AuthService.expired_token(token);
    },


    async refreshToken({commit,getters, dispatch}){
      const response = await AuthService.refresh_access_token()
      console.log(response)
      // response.then(resp => {
      //   commit('setUser', JSON.parse(localStorage.getItem('user')))
      // }).catch(error => {
      //   if(getters.loginState){
      //     dispatch('logout')
      //   }
        
      // })
      return response
    },

    async verifyToken({commit}){
      return await AuthService.verify_access_token()
    },

    async getUsersList({}){
      try{
        const response = await axios.get(BASE_URL + 'auth/users/')
        return response.data
      }  
      catch(error){console.log(error)}
    }




  },
  mutations: {
    loginSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    registerSuccess(state) {
      state.status.loggedIn = false;
    },
    registerFailure(state) {
      state.status.loggedIn = false;
    },

    setUser(state, user){
      state.user = user
    },
    
    setAccessToken(state, access_token){
      console.log(access_token)
      state.user.access = access_token
      const user = state?.user
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