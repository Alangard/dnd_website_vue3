import interceptorsInstance, {authHeader, accessToken} from '@/api/main'
import axios from 'axios'

const user = JSON.parse(localStorage.getItem('user'));
const BASE_URL = axios.defaults.baseURL

const initialState = user
  ? { status: { loggedIn: true }, user, usersList: null, subscriptions: null}
  : { status: { loggedIn: false }, user: null, usersList: null, subscriptions:null};

export const accounts = {
  namespaced: true,
  state: initialState,
  actions: {
    async changeSubscription({commit}, user_id){
      try{
        const response = await interceptorsInstance.post(BASE_URL + `subs/change_subscription/`, {'user_id': user_id}, { headers: authHeader()})
        return response.data
      }
      catch(error){console.log(error)}

    },

    async getSubscriptions({commit}){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `subs/`, { headers: authHeader()})
        commit('setSubscriptionsInStore', response.data)
        return response.data
      }
      catch(error){console.log(error)}

    },

    async getUsersList({commit},){
      try{
        const response = await interceptorsInstance.get(BASE_URL + 'auth/user/')
        commit('setUsersListInStore', response.data)
        return response.data
      }  
      catch(error){console.log(error)}
    },
  },
  mutations: {
    setSubscriptionsInStore(state, data){
      state.subscriptions = data;
    },

    setUsersListInStore(state, data){
      state.usersList = data;
    },
  },
  getters: {
    getUsersList(state){
      return state.usersList
    },

    getSubscriptions(state){
      return state.subscriptions
    }
  }
}