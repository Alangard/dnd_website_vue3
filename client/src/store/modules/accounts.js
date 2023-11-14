import interceptorsInstance, {authHeader, accessToken} from '@/api/main'
import axios from 'axios'

const user = JSON.parse(localStorage.getItem('user'));
const BASE_URL = axios.defaults.baseURL

const initialState = user
  ? { status: { loggedIn: true }, user, usersList: null, subscriptions: null, notifications: null, all_notifications: null} 
  : { status: { loggedIn: false }, user: null, usersList: null, subscriptions:null, notifications: null, all_notifications: null};

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
        commit('setUsersListInStore', response.data)
        return response.data
      }  
      catch(error){console.log(error)}
    },

    async getNotificationsList({commit},{paginate_url, request_type}){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `notifications/${paginate_url}`, { headers: authHeader() })
        if(request_type == 'initial'){commit('setNotificationsListInStore', response.data)}
        else if(request_type == 'all_notifications'){commit('setAllNotificationsListInStore', response.data)}
        return response.data
      }
      catch(error){console.log(error)}
    },

    async submitNotificationsAction({commit}, action_data){
      try{
        switch(action_data.action.value){
          case 'seen':
            await interceptorsInstance.patch(BASE_URL + `notifications/`, { headers: authHeader() })
            break
          case 'unseen':
            await interceptorsInstance.patch(BASE_URL + `notifications/`, { headers: authHeader() })
            break
          case 'delete':
            await interceptorsInstance.delete(BASE_URL + `notifications/`, { headers: authHeader() })
            break
        }
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

    setAllNotificationsListInStore(state, data){
      state.all_notifications = data
    },


    addNotificationInStore(state, data){
      state.notifications.results.unshift(data)
      state.notifications.count += 1
    },

    removeNotificationInStore(state, notifications_id__list){
      for(notification_id of notifications_id__list){
        splice(notification_id, 1)
      }

    },

    removeAllNotificationsListInStore(state, data){}
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

    getAllNotificationsList(state){
      return state.all_notifications.results
    }
  }
}