import interceptorsInstance, {authHeader, accessToken} from '@/api/main'
import axios from 'axios'

const user = JSON.parse(localStorage.getItem('user'));
const BASE_URL = axios.defaults.baseURL

const initialState = user
  ? { status: { loggedIn: true }, user, usersList: null, subscriptions: null, notifications: null, searched_user_info: null,
  showcase_info: {'stats': {
    'selected':[
      {'data': {'name': 'Likes','count': 12000},'order': 1},
      {'data': {'name': 'Comments','count': 360},'order': 2},
      {'data': {'name': 'Post','count': 15},'order': 3}],
    'all':[
      {'data': {'name': 'Likes','count': 12000}},
      {'data': {'name': 'Comments','count': 360}},
      {'data': {'name': 'Post','count': 15}},
      {'data': {'name': 'Dislikes','count': 3}}
    ]
  }
}}
  : { status: { loggedIn: false }, user: null, usersList: null, subscriptions:null, notifications: null, searched_user_info: null,
  showcase_info: {'stats': {
    'selected':[
      {'data': {'name': 'Likes','count': 12000},'order': 1},
      {'data': {'name': 'Comments','count': 360},'order': 2},
      {'data': {'name': 'Post','count': 15},'order': 3}],
    'all':[
      {'data': {'name': 'Likes','count': 12000}},
      {'data': {'name': 'Comments','count': 360}},
      {'data': {'name': 'Post','count': 15}},
      {'data': {'name': 'Dislikes','count': 3}}
    ]
  }
}}

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

    async getUserInfo({commit, state}, username){
      try{
        const response = await interceptorsInstance.get(BASE_URL + `auth/user/?username=${username}`)
        state.searched_user_info = response.data.results[0]
        return response.data.results[0]
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
      const length = state.showcase_info.stats.selected.length
      state.showcase_info.stats.selected.push({'data': {'name': '','count': 0},'order': length + 1, 'type': 'creating'})
    },

    removeStatBlock(state, order){
      const idx = state.showcase_info.stats.selected.findIndex((item) => item.order === order);
      state.showcase_info.stats.selected.splice(idx, 1)
    },

    updateCountStats(state, stats_name){
      const count = state.showcase_info.stats.all.filter((element)=> element.data.name == stats_name)[0].data.count
      const length = state.showcase_info.stats.selected.length
      const data = {'data': {'name': stats_name,'count': count},'order': length, 'type': 'creating'}
      state.showcase_info.stats.selected.splice(-1, 1, data)
    },

    saveLastStatBlock(state, stats_name){
      const count = state.showcase_info.stats.all.filter((element)=> element.data.name == stats_name)[0].data.count
      const length = state.showcase_info.stats.selected.length
      const data = {'data': {'name': stats_name,'count': count},'order': length}
      state.showcase_info.stats.selected.splice(-1, 1, data)
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
      return state.showcase_info.stats
    },

    getUserInfo(state){
      return state.searched_user_info
    }
  }
}