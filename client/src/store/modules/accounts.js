import interceptorsInstance, {authHeader, accessToken} from '@/api/main'
import axios from 'axios'

const user = JSON.parse(localStorage.getItem('user'));
const BASE_URL = axios.defaults.baseURL

const initialState = user
  ? { status: { loggedIn: true }, user, usersList: null, subscriptions: null, notifications: null, searched_user_info: null, userSettings: null,}
  : { status: { loggedIn: false }, user: null, usersList: null, subscriptions:null, notifications: null, searched_user_info: null, userSettings: null,}

export const accounts = {
  namespaced: true,
  state: initialState,
  actions: {
    async changeSubscription({commit}, user_id){
      try{
        const response = await interceptorsInstance.post(BASE_URL + `subs/change_subscription/`, {'user_id': user_id}, { headers: authHeader()})
        if(Object.keys(response.data.data).length != 0){commit('addSubscribeToInStore', response.data.data)}
        else{commit('removeSubscribeToInStore', user_id)}
        return response.data
      }
      catch(error){console.log(error)}

    },

    async getSubscriptions({commit}, user_id){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `subs/${user_id}/`, { headers: authHeader()})
        commit('setSubscriptionsInStore', response.data)
        return response.data
      }
      catch(error){console.log(error)}

    },

    async getUsersList({commit},){
      try{
        const response = await interceptorsInstance.get(BASE_URL + 'auth/user/')
        commit('setUsersListInStore', response.data.results)
        return response.data.results
      }  
      catch(error){console.log(error)}
    },

    async getUserInfo({commit, state}, profile_name){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `auth/user/?profile_name=${profile_name}`)
        if(response.data.data !== null){
          state.searched_user_info = response.data?.results
          return response.data?.results[0]
        }
        else{return null}

      }
      catch(error){console.log(error)}
    },

    async getNotificationsList({commit},{paginate_url, request_type}){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `notifications/${paginate_url}`, { headers: authHeader() })
        if(!request_type){commit('setNotificationsListInStore', response.data)}
        return response.data
      }
      catch(error){console.log(error)}
    },


    async submitNotificationsAction({commit}, action_data){
      try{
        if(action_data.action.value == 'seen' || action_data.action.value == 'unseen'){
          await interceptorsInstance.post(BASE_URL + `notifications/update_notifications/`, action_data,  { headers: authHeader() })
        }
        else if(action_data.action.value == 'delete'){
          await interceptorsInstance.post(BASE_URL + `notifications/delete_notifications/?page_size=${action_data.page_size}`, action_data, { headers: authHeader() })
        }
      }
      catch(error){console.log(error)}
    },

    // async getStatsWhileCreating({commit}, stats_type){
    //   try{
    //     await interceptorsInstance.get(BASE_URL + `profile/createing_stats_block/?stats_type=${stats_type}`, { headers: authHeader() })
    //   }
    //   catch(error){console.log(error)}
    // }

    async getUserSettings({state, commit}){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `auth/user/${state.user.user_data.id}/settings/`, { headers: authHeader() })
        console.log(response.data)
        state.userSettings = response.data
        return response.data
      }
      catch(error){console.log(error)}
    },

    async updateUserSettings({state, commit}, data){
      try{
        const response = await interceptorsInstance.post(BASE_URL + `auth/user/${state.user.user_data.id}/settings/change/`, data, { headers: authHeader() })
        return response
      }
      catch(error){console.log(error)}
    },

    async changeAccountData({state, commit}, data){
      try{
        const response = await interceptorsInstance.patch(BASE_URL + `auth/user/${state.user.user_data.id}/`, data,  { headers: authHeader() })
        commit('auth/changeUserData', response.data, { root: true })
        commit('changeUserData', response.data)
        return response.data
      }
      catch(error){console.log(error)}
    }

  },
  mutations: {
    setSubscriptionsInStore(state, data){
      state.subscriptions = data;
    },

    addSubscribeToInStore(state, data){
      state.subscriptions.subscribed_to.unshift(data)
    },

    removeSubscribeToInStore(state, user_id){
      const index = state.subscriptions.subscribed_to.findIndex(user => user.id === user_id);
      if(index != -1){state.subscriptions.subscribed_to.splice(index, 1)}
    },

    setUsersListInStore(state, data){
      state.usersList = data;
    },

    setNotificationsListInStore(state, data){
      state.notifications = data;
    },

    addNotificationInStore(state, data){
      state.notifications.results.unshift(data)
      state.notifications.count += 1
    },

    removeNotificationInStore(state, notifications_id__list){
      notifications_id__list.forEach(element => {
          state.notifications.results = state.notifications.results.filter(obj => obj.notification_id !== element);
      });

      state.notifications.count = state.notifications.results.length
    },


    addStatBlock(state){
      const length = state.userSettings.statistics.selected.length
      state.userSettings.statistics.selected.push({'data': {'name': '','count': 0},'order': length + 1, 'type': 'creating'})
    },

    removeStatBlock(state, order){
      const idx = state.userSettings.statistics.selected.findIndex((item) => item.order === order);
      state.userSettings.statistics.selected.splice(idx, 1)
    },

    updateCountStats(state, stats_name){
      console.log(stats_name)
      const count = state.userSettings.statistics.all.filter((element)=> element.data.name == stats_name)[0].data.count
      const length = state.userSettings.statistics.selected.length
      const data = {'data': {'name': stats_name,'count': count},'order': length}
      state.userSettings.statistics.selected.splice(-1, 1, data)
    },

    saveLastStatBlock(state, stats_name){
      const count = state.userSettings.statistics.all.filter((element)=> element.data.name == stats_name)[0].data.count
      const length = state.userSettings.statistics.selected.length
      const data = {'data': {'name': stats_name,'count': count},'order': length}
      state.userSettings.statistics.selected.splice(-1, 1, data)
    },
    
    changeUserData(state, user_data){
      state.user.user_data = user_data
      state.searched_user_info = user_data
      const user = JSON.parse(localStorage.getItem('user'))
      user['user_data'] = user_data

      localStorage.setItem('user', JSON.stringify(user))
    },


  },
  getters: {
    getUsersList(state){
      return state.usersList
    },

    getSubscriptions(state){
      return state.subscriptions
    },

    getNotificationsList(state){
      return state.notifications.results
    },

    getShowcaseStats(state){
      return state.userSettings.statistics
    },

    getUserInfo(state){
      return state.searched_user_info
    }
  }
}